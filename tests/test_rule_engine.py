from core.rule_engine import check_false_path_rules, load_json_file


def test_case1_true():
    c = load_json_file("dummy_env/case1_true.json")
    ok, reason = check_false_path_rules(c, "src_ff", "dst_ff", "clk_a", "clk_b", max_depth=5)
    assert ok is True
    assert "ACCEPT" in reason


def test_case1_false():
    c = load_json_file("dummy_env/case1_false.json")
    ok, reason = check_false_path_rules(c, "src_ff", "dst_ff", "clk_a", "clk_b", max_depth=5)
    assert ok is False
    assert "no ACCEPT" in reason
