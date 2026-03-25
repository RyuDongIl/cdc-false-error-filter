from core.rule_engine import check_false_path_rules, load_json_file


def test_case1_true_with_valid_clk_domain():
    c = load_json_file("dummy_env/case1_true.json")
    ok, reason = check_false_path_rules(c, "q_out", "q_dst", "CK4CI_S0", "MC_CK_S0", max_depth=5)
    assert ok is True
    assert "ACCEPT" in reason


def test_case1_false_signal_path():
    c = load_json_file("dummy_env/case1_false.json")
    ok, reason = check_false_path_rules(c, "q_out", "q_dst", "CK4CI_S0", "MC_CK_S0", max_depth=5)
    assert ok is False
    assert "no ACCEPT" in reason


def test_case1_reject_invalid_src_clk_domain():
    c = load_json_file("dummy_env/case1_true.json")
    ok, reason = check_false_path_rules(c, "q_out", "q_dst", "SLOW_CLK", "MC_CK_S0", max_depth=5)
    assert ok is False
    assert "source clock domain" in reason


def test_case1_reject_invalid_dst_clk_domain():
    c = load_json_file("dummy_env/case1_true.json")
    ok, reason = check_false_path_rules(c, "q_out", "q_dst", "CK4CI_S0", "CLK_S0", max_depth=5)
    assert ok is False
    assert "destination clock domain" in reason
