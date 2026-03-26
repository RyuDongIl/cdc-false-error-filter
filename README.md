# cdc-false-error-filter

CDC false-path candidate filtering (Yosys + Python).

## 목적
- NAND/ASIC RTL에서 CDC 분석 시 발생하는 많은 경고 중 하드웨어 연결 상태 기반의 'False Path' 후보를 자동으로 선별
- 민감 데이터(실제 RTL/넷리스트)는 외부망으로 노출하지 않고, 핵심 엔진 로직만 오프라인/온라인 분리 환경에서 개발

## 프로젝트 구조
- `core/rule_engine.py` : 핵심 DFS 룰 엔진
- `main.py` : CLI 진입점 (`argparse`)
- `dummy_env/` : 오프라인 검증용 더미 설계/테스트 케이스

## 현재 구현 상태
- Case 1 (Source FF Enable Path) 룰 엔진 구현: `check_false_path_rules`
  - Src FF(`--src_ff`)의 **enable 신호(EN/E 핀만)** 로부터 역방향 탐색
  - 최대 깊이(default 5) 내에서 `ACCEPT.*_INTRDY` 패턴 매칭 시 false path 판정
  - Clk Domain 제약: `--src_clk`는 `CK4CI*` 계열, `--dst_clk`는 `MC_CK*` 계열만 통과

## 실행
```bash
python main.py \
  --json dummy_env/case1_true.json \
  --src_ff q_out \
  --dst_ff q_dst \
  --src_clk CK4CI_S0 \
  --dst_clk MC_CK_S0
```

출력 예시:
```json
{"is_false_path": true, "reason": "matched at ..."}
```

## 보안 주의
- 실 설계 RTL과 실제 생성 JSON은 **로컬 사내망**에서만 사용
- 이 레포의 핵심은 알고리즘 구조와 예외처리

## Yosys 버전 정렬(사내-외부 호환)

사내 기준(예: 2025-03-24 Release, `0.63+173`)에 맞추려면, 아래 방식으로 `0.63+173` 바이너리를 사용하세요.

- OSS CAD Suite(arm64) 다운로드: `oss-cad-suite-linux-arm64-20260324.tgz`
- 실행 예:
  - `YOSYS_BIN=/tmp/oss-cad-suite-arm64/oss-cad-suite/bin/yosys bash dummy_env/parse_case_with_yosys.sh`  # 단일 엔트리: case1_true/false를 같이 갱신

기본적으로 스크립트는 `YOSYS_BIN` 환경변수가 있으면 그걸 쓰고, 없으면 시스템 `yosys`를 사용합니다.

## Case1 테스트 스위트

- 다중 파일/계층/예외 케이스를 포함한 `case1` 테스트 케이스를 `tests/case_suite/case1/`에 추가했습니다.
- 각 케이스 구조
  - `meta.json`: 입력/기대결과/소스 파일 목록
  - `src/*.sv`: Verilog 소스
  - `case.json`: Yosys(`.yosys` 파서)로 만든 참조 JSON

테스트 실행:
```bash
YOSYS_BIN=/tmp/oss-cad-suite-arm64/oss-cad-suite/bin/yosys python3 tests/scripts/build_case_suite_json.py
pytest tests/test_case_suite.py
```

## 테스트 스위트 개선 반영

`tests/case_suite`의 `meta.json`에 `top_module`이 추가되었습니다.
실제 현업 설계에서 top module명이 `top`이 아닐 수 있으므로, Case 검증 시 메타의 `top_module`을 기준으로 Yosys를 실행합니다.
