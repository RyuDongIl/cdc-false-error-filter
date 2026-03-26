import json
import re
from collections import deque
from typing import Any, Dict, List, Optional, Set, Tuple

# Flip-flop types commonly used by Yosys
FF_TYPES = {
    "$dff",
    "$dffsr",
    "$dffe",
    "$dffe_n",
    "$dffe_ns",
    "$dffn",
    "$adff",
    "$adffe",
    "$aldffe",
    "$fdre",
    "$fdr",
}

# Common output ports of combinational cells
COMBINATIONAL_OUTPUT_PINS = {"Y", "Q", "Z"}

# Candidate enable pins on FFs / sequential cells
ENABLE_PINS = {"EN", "E"}

ACCEPT_INTRDY_RE = re.compile(r"^ACCEPT.*_INTRDY$")

# Clock-domain family filters for Case 1
SRC_CLK_DOMAIN_RE = re.compile(r"^CK4CI", re.IGNORECASE)
DST_CLK_DOMAIN_RE = re.compile(r"^MC_CK", re.IGNORECASE)

def _get_design_module(circuit: Dict[str, Any]) -> Dict[str, Any]:
    """Handle both flattened and module-wrapped Yosys JSON forms."""
    if "netnames" in circuit and "cells" in circuit:
        return circuit

    modules = circuit.get("modules")
    if isinstance(modules, dict) and len(modules) >= 1:
        if len(modules) == 1:
            return next(iter(modules.values()))
        if "top" in modules:
            return modules["top"]
        return next(iter(modules.values()))

    return {"netnames": {}, "cells": {}}


def _coerce_connections(values: Any) -> List[str]:
    """Normalize a Yosys JSON connection field into list of net ids."""
    if values is None:
        return []
    if isinstance(values, str):
        return [values]
    if isinstance(values, list):
        return [str(v) for v in values]
    if isinstance(values, tuple):
        return [str(v) for v in values]
    if isinstance(values, (int, float, bool)):
        return [str(values)]
    return []


def _build_net_to_names(circuit: Dict[str, Any]) -> Dict[str, List[str]]:
    """Create a reverse map: Yosys net id -> list of logical names."""
    net_map: Dict[str, List[str]] = {}
    for name, meta in (circuit.get("netnames", {}) or {}).items():
        norm_name = str(name).lstrip("\\")
        bits = _coerce_connections(meta.get("bits", []))
        for bit in bits:
            net_map.setdefault(bit, []).append(norm_name)
    return net_map


def _find_net_ids_for_name(circuit: Dict[str, Any], target_name: str) -> List[str]:
    """Find all net IDs whose yosys netname matches target_name."""
    target = target_name.strip()
    hits: List[str] = []
    netnames = circuit.get("netnames", {}) or {}

    for raw_name, meta in netnames.items():
        n = str(raw_name).lstrip("\\")
        if n == target or raw_name == target:
            hits.extend(_coerce_connections(meta.get("bits", [])))

    # fallback: suffix match for names with hierarchy wrappers
    if not hits:
        for raw_name, meta in netnames.items():
            n = str(raw_name).lstrip("\\")
            if n.endswith(target) or raw_name.endswith(target):
                hits.extend(_coerce_connections(meta.get("bits", [])))

    return sorted(set(hits))


def _resolve_src_ff_cell(circuit: Dict[str, Any], src_ff: str) -> Optional[Tuple[str, Dict[str, Any]]]:
    """Find FF cell that drives `src_ff` via its Q output."""
    if not src_ff:
        return None

    src_bits = _find_net_ids_for_name(circuit, src_ff)
    if not src_bits:
        return None

    cells = circuit.get("cells", {})
    for cell_name, cell in cells.items():
        if cell.get("type") not in FF_TYPES:
            continue
        q_bits = _coerce_connections(cell.get("connections", {}).get("Q"))
        if any(bit in q_bits for bit in src_bits):
            return cell_name, cell
    return None


def _pick_enable_nets(cell: Dict[str, Any]) -> List[str]:
    """Collect enable nets from a FF-like cell."""
    conns = cell.get("connections", {}) or {}
    enables: List[str] = []

    for pin in ENABLE_PINS:
        if pin in conns:
            enables.extend(_coerce_connections(conns.get(pin)))

    # drop constants and dedupe
    return sorted(set(c for c in enables if c not in {"0", "1", "1'b0", "1'b1"}))


def _extract_net_to_cells(circuit: Dict[str, Any], *, output_pins: Set[str] = None):
    """Build reverse lookup: net -> sequential list of combinational cells that output that net."""
    output_pins = output_pins or COMBINATIONAL_OUTPUT_PINS
    net_to_outputs: Dict[str, List[Tuple[str, Dict[str, Any], str]]] = {}
    cells = circuit.get("cells", {})

    for cell_name, cell in cells.items():
        ctype = cell.get("type", "")
        if not str(ctype).startswith("$") or ctype in FF_TYPES:
            continue

        conns = cell.get("connections", {})
        for pin, nets in conns.items():
            if pin in output_pins:
                for n in _coerce_connections(nets):
                    net_to_outputs.setdefault(n, []).append((cell_name, cell, pin))
    return net_to_outputs


def _matches_intrdy_name(net_id: str, bit_to_names: Dict[str, List[str]]) -> Optional[str]:
    for name in bit_to_names.get(net_id, []):
        if ACCEPT_INTRDY_RE.match(name):
            return name
    return None


def _validate_clk_domains(src_clk: str, dst_clk: str) -> Tuple[bool, str]:
    if not SRC_CLK_DOMAIN_RE.match((src_clk or "").strip()):
        return False, "source clock domain must match CK4CI family"

    if not DST_CLK_DOMAIN_RE.match((dst_clk or "").strip()):
        return False, "destination clock domain must match MC_CK family"

    return True, ""


def check_false_path_rules(
    circuit: Dict[str, Any],
    src_ff: str,
    dst_ff: str,
    src_clk: str,
    dst_clk: str,
    *,
    max_depth: int = 5,
) -> Tuple[bool, str]:
    """
    Rule-1: source FF enable path reaches root signal matching ACCEPT.*_INTRDY.

    Return (is_false_path, reason).
    """
    ok, reason = _validate_clk_domains(src_clk, dst_clk)
    if not ok:
        return False, reason

    circuit = _get_design_module(circuit)

    bit_to_names = _build_net_to_names(circuit)
    ff_hit = _resolve_src_ff_cell(circuit, src_ff)
    if ff_hit is None:
        return False, f"source ff not found: {src_ff}"

    ff_name, ff_cell = ff_hit
    enable_nets = _pick_enable_nets(ff_cell)
    if not enable_nets:
        return False, f"no enable signal on source ff: {ff_name}"

    net_to_cells = _extract_net_to_cells(circuit)

    # Direct hit on enable net name
    for net in enable_nets:
        matched = _matches_intrdy_name(net, bit_to_names)
        if matched:
            return True, f"matched at source enable net '{matched}'"

    # BFS/DFS with fixed-depth guard (max_depth)
    q = deque((net, 0) for net in enable_nets)
    visited = set(enable_nets)

    while q:
        net_id, depth = q.popleft()
        if depth >= max_depth:
            continue

        for cell_name, cell, out_pin in net_to_cells.get(net_id, []):
            conns = cell.get("connections", {})
            for pin, conn in conns.items():
                # do not walk forward along same driving edge
                if pin == out_pin:
                    continue
                for next_net in _coerce_connections(conn):
                    if next_net in {"0", "1", "1'b0", "1'b1"}:
                        continue
                    matched = _matches_intrdy_name(next_net, bit_to_names)
                    if matched:
                        return True, (
                            f"matched at {cell_name}:{pin} -> '{matched}' "
                            f"(reverse depth {depth+1})"
                        )
                    if next_net not in visited:
                        visited.add(next_net)
                        q.append((next_net, depth + 1))

    return False, f"no ACCEPT.*_INTRDY matched within depth {max_depth} from source ff {src_ff}"


def load_json_file(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
