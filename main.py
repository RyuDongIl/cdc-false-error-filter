import argparse
import json
from core.rule_engine import check_false_path_rules, load_json_file


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="CDC False Path Filter Rule Engine")
    p.add_argument("--json", required=True, help="Yosys JSON path")
    p.add_argument("--src_ff", required=True, help="Source FF instance/name")
    p.add_argument("--dst_ff", required=True, help="Destination FF instance/name")
    p.add_argument("--src_clk", required=True, help="Source clock")
    p.add_argument("--dst_clk", required=True, help="Destination clock")
    p.add_argument("--depth", type=int, default=5, help="Reverse traversal depth limit")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    circuit = load_json_file(args.json)
    is_false, reason = check_false_path_rules(
        circuit,
        args.src_ff,
        args.dst_ff,
        args.src_clk,
        args.dst_clk,
        max_depth=args.depth,
    )
    print(json.dumps({"is_false_path": is_false, "reason": reason}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
