import json
import subprocess
from pathlib import Path

import os

YOSYS_BIN = os.environ.get("YOSYS_BIN", "yosys")

ROOT = Path(__file__).resolve().parent.parent / "case_suite"

for case_dir in sorted((ROOT / "case1").glob("case1_*")):
    if not case_dir.is_dir():
        continue

    meta_path = case_dir / "meta.json"
    if not meta_path.exists():
        continue

    meta = json.loads(meta_path.read_text())
    src_dir = case_dir / "src"
    source_files = [src_dir / f for f in meta.get("source_files", [])]
    for p in source_files:
        if not p.exists():
            raise FileNotFoundError(f"Missing source file: {p}")

    out_path = case_dir / "case.json"

    read_cmd = " ".join(str(p) for p in source_files)
    script = (
        f"read_verilog -sv {read_cmd}; "
        "hierarchy -check -top top; proc; opt; flatten; "
        f"write_json {out_path}"
    )

    subprocess.run([YOSYS_BIN, "-qp", script], check=True)
    print(f"generated {out_path}")
