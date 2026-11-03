# AP 지급·회수 업무별 Risk Cell 평가

이 표는 동일 controlled cohort/book/rail/policy에서 권한만 바꾼 원장 재실행의 집계다. 경제금액은 LAB_USD_CENTS 가정이다. 실제 고객 지급·은행 회수율·보험금이 아니다.

| Authority | normal completion | mean residual cash loss (lab cents) | mean total cost (lab cents) | P99 cash loss |
|---|---:|---:|---:|---:|
| A0_DRAFT_ONLY | 0.0000 | 0.00 | 17519.15 | 0.00 |
| A100_FULL_APPROVED | 0.5000 | 7850275.91 | 9823230.51 | 68482407.00 |
| A1_LOW | 0.2521 | 703885.51 | 894810.25 | 4742478.00 |
| A25_HIGH | 0.4983 | 6859601.77 | 8585048.71 | 50061539.00 |
| A5_MEDIUM | 0.4496 | 3744827.40 | 4693113.19 | 22558547.00 |

## 실제 model intent의 조건 비교

동일 MODEL_INTENT_LAB / ENTERPRISE / FAST_FINAL / A5_MEDIUM의 inherited lane별 결과다. lane a/b의 정확한 모델 lock은 RISK_CELLS.jsonl에 있다.

| Lane | control | normal completion | mean residual cash loss (lab cents) |
|---|---|---:|---:|
| a | P0_RAW_BOUNDED | 0.0025 | 0.00 |
| a | P1_AUTHORITY_CAP | 0.0025 | 0.00 |
| a | P2_REGISTRY_APPROVAL | 0.0025 | 0.00 |
| a | P3_VALUE_IDEMPOTENCY | 0.0025 | 0.00 |
| a | P4_PRE_SETTLEMENT_HOLD | 0.0025 | 0.00 |
| a | P5_RECONCILE_RECALL | 0.0025 | 0.00 |
| a | P6_LAYERED | 0.0025 | 0.00 |
| b | P0_RAW_BOUNDED | 0.1149 | 2686.15 |
| b | P1_AUTHORITY_CAP | 0.1149 | 2686.15 |
| b | P2_REGISTRY_APPROVAL | 0.1149 | 2686.15 |
| b | P3_VALUE_IDEMPOTENCY | 0.1149 | 2686.15 |
| b | P4_PRE_SETTLEMENT_HOLD | 0.1149 | 2686.15 |
| b | P5_RECONCILE_RECALL | 0.1149 | 2686.15 |
| b | P6_LAYERED | 0.1149 | 2686.15 |

전체 945개 집계 셀의 권한·통제 비교는 AUTHORITY_EFFECTS.json / CONTROL_EFFECTS.json에 있다. 권한 확대의 cash loss 변화와 정상 지급 성과를 동시에 본다. 모든 지급 보류로 cash loss가 0이어도 채용 적합성이 성립하지 않는다. posted recovery·unfulfilled payable 정의는 원본 원장 연구를 따른다. source cluster interval은 셀에 보존했으나 paired 원시 case를 다시 펼쳐 새 인과 구간을 적합하지는 않았다.

고객별 업무 분포·계약·성과 및 위험 문턱이 없어 production approval=NOT_ASSESSED, enterprise_calibrated=false, bindable_quote=false다.
