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
  - Src FF(`--src_ff`)의 enable/제어 신호로부터 역방향 탐색
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
