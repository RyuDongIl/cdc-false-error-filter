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

## 실행
```bash
python main.py \
  --json dummy_env/case1_yosys.json \
  --src_ff top.u_reg \
  --dst_ff top.v_reg \
  --src_clk clk_a \
  --dst_clk clk_b
```

출력 예시:
```json
{"is_false_path": true, "reason": "matched at ..."}
```

## 보안 주의
- 실 설계 RTL과 실제 생성 JSON은 **로컬 사내망**에서만 사용
- 이 레포의 핵심은 알고리즘 구조와 예외처리
