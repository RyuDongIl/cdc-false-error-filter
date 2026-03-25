# Test Script Utilities

- `build_case_suite_json.py` : `tests/case_suite` 하위의 모든 case 메타(`meta.json`)를 읽어
  `case.json`(golden yosys JSON)을 재생성합니다.

환경변수:
- `YOSYS_BIN` (기본값: `yosys`)

The generator reads `meta.json` in each case and uses `top_module` as Yosys entry module.
If `top_module` is missing, it auto-fallback to unique module in the case sources.
