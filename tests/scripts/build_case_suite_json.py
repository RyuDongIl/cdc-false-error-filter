import json
import os
import re
import subprocess
from pathlib import Path

YOSYS_BIN = os.environ.get("YOSYS_BIN", "yosys")

ROOT = Path(__file__).resolve().parent.parent / "case_suite"

_module_re = re.compile(r"^\s*module\s+([A-Za-z_][A-Za-z0-9_]*)", re.MULTILINE)


def _infer_top_module(src_files):
    modules = []
    for path in src_files:
        text = path.read_text()
        modules.extend(_module_re.findall(text))

    # uniq while preserving order
    seen = set()
    ordered = []
    for m in modules:
        if m not in seen:
            seen.add(m)
            ordered.append(m)

    if len(ordered) == 1:
        return ordered[0]

    # fallback for known style where top is often named 'top'
    if "top" in ordered:
        return "top"

    raise RuntimeError(f"Unable to infer unique top module from {', '.join(p.name for p in src_files)}")


for case_dir in sorted((ROOT / "case1").glob("case1_*")):
    if not case_dir.is_dir():
        continue

    meta_path = case_dir / "meta.json"
    if not meta_path.exists():
        continue

    meta = json.loads(meta_path.read_text())
    src_dir = case_dir / "src"
    source_files = [src_dir / f for f in meta.get("source_files", [])]

    if not source_files:
        # backward compatibility: take all sv files under src/
        source_files = sorted(src_dir.glob("*.sv"))
        meta["source_files"] = [p.name for p in source_files]
        meta_path.write_text(json.dumps(meta, indent=2))

    for p in source_files:
        if not p.exists():
            raise FileNotFoundError(f"Missing source file: {p}")

    top_module = meta.get("top_module") or _infer_top_module(source_files)

    out_path = case_dir / "case.json"

    read_cmd = " ".join(str(p) for p in source_files)
    script = (
        f"read_verilog -sv {read_cmd}; "
        f"hierarchy -check -top {top_module}; proc; opt; flatten; "
        f"write_json {out_path}"
    )

    subprocess.run([YOSYS_BIN, "-qp", script], check=True)
    print(f"generated {out_path} with top={top_module}")
