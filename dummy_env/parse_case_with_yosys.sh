#!/usr/bin/env bash
set -euo pipefail

# Prefer environment-provided yosys binary. If not set, use local system yosys.
YOSYS_BIN="${YOSYS_BIN:-yosys}"

for f in dummy_env/case1_true.v dummy_env/case1_false.v; do
  base=$(basename "$f" .v)
  out="dummy_env/${base}.json"  # overwrite existing fixtures in-place
  "$YOSYS_BIN" -qp "read_verilog -sv $f; hierarchy -check -top top; proc; opt; flatten; write_json $out"
  echo "parsed $f -> $out"
done

echo "Used YOSYS_BIN=$YOSYS_BIN"
