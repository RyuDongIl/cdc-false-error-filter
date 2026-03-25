# Case Test Suite

`tests/case_suite/`는 엔진 규칙 검증용 케이스를 모듈별로 관리합니다.

현재는 `case1`(Source FF Enable 경로 기반 False-path 후보 판별) 10개 케이스를 구성했습니다.

## 구조

```text
tests/
  case_suite/
    case1/
      case1_01_unit_positive/
        meta.json      # 테스트 메타(입력 파라미터 + 기대 결과)
        src/           # Verilog 소스 파일들
          top.sv
        case.json      # Yosys로 생성한 gold JSON
      case1_02_unit_negative/
        ...
    scripts/
  ...
```

- `case_id`는 `case1_01_*` 형태로 개별 테스트 케이스를 식별합니다.
- `meta.json`의 `expected` 값이 테스트 기대 결과입니다.
- `source_files`는 `src/` 아래의 Verilog 소스 목록입니다.

## Case 파일 생성/갱신

Yosys 기반 JSON은 아래 스크립트로 재생성합니다.

```bash
YOSYS_BIN=/tmp/oss-cad-suite-arm64/oss-cad-suite/bin/yosys \
  python3 tests/scripts/build_case_suite_json.py
```

## 실행

```bash
python3 -m pytest tests/test_case_suite.py
```
(환경에 따라 pytest가 없으면 동일 로직으로 대체 실행 가능)

## Top module setting

Each case has `meta.json` with `top_module` so Yosys uses the real top design module.
This avoids dependency on file name (`top.sv`) and handles real project style names.
