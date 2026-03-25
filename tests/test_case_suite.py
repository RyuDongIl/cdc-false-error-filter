import json
from pathlib import Path

from core.rule_engine import check_false_path_rules, load_json_file


CASES_ROOT = Path(__file__).resolve().parent / "case_suite" / "case1"


def _iter_cases():
    for meta_path in sorted(CASES_ROOT.glob("case1_*/meta.json")):
        meta = json.loads(meta_path.read_text())
        case_dir = meta_path.parent
        json_path = case_dir / "case.json"
        yield case_dir.name, meta, json_path


def test_case1_suite():
    for case_id, meta, json_path in _iter_cases():
        circuit = load_json_file(str(json_path))
        ok, reason = check_false_path_rules(
            circuit,
            meta["src_ff"],
            meta["dst_ff"],
            meta["src_clk"],
            meta["dst_clk"],
            max_depth=meta.get("max_depth", 5),
        )

        expected = meta["expected"]
        assert ok == expected["is_false_path"], (
            f"[{case_id}] expected {expected['is_false_path']} but got {ok}; reason: {reason}"
        )
        assert expected["contains"] in reason, f"[{case_id}] unexpected reason: {reason}"
