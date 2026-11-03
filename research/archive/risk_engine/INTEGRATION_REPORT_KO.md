# 연구 통합·업무별 평가 V1 완료 기록

2026-10-11. 기존 실험 재실행 없이 공통 엔진·두 업무 심사 보고서·추가 증거 갱신 경로를 구현했다. 고객 또는 보험사의 실제 인수결정까지 완료했다는 뜻은 아니다.

## 요구별 검증

| 요청 | 구현·증빙 | 판정 |
|---|---|---|
| 기존 핵심 연구를 공통 Evidence Schema로 연결 | 1,399 집계 셀, 10 numeric adapters, 원본 SHA·행 위치·분모·조건 | PASS |
| 원본 의미와 서로 다른 증거 수준 보존 | 원본 행, Direct/Paired/Transported/Scenario/Unidentified, 화폐·손실 endpoint 분리 | PASS |
| Code 배포 업무 평가 | CODE_ASSESSMENT_KO.md: 독립 해결·missing·bad release + 별도 Monetary 권한/통제 시나리오 | PASS |
| AP 지급·회수 업무 평가 | PAY_ASSESSMENT_KO.md: normal completion·현금손실·총비용·미지급 의무·권한/통제 | PASS |
| Risk Cell 추가 데이터 Bayesian update | append-only SQLite, exact counts, Beta working posterior, 중복/겹침 거부 | PASS |
| 권한 변경 위험 차이 | 동일 조건 한 축 비교·효용/사건/손실 차이, 별도 변경 유효시각 원장 | PASS |
| 제한적인 외삽 | 명시적 가정·약한 prior·Transported 표시; 미측정 권한/업무/모델/고객 전이 거부 | PASS |
| 독립 재현과 recovery | 21 regression/E2E 검사 통과, 새 디렉터리 생성 결과 SHA 일치, idempotent resume | PASS |

[검증 receipt](VALIDATION.json), [실제 테스트 로그](TEST_LOG.txt), [데이터 SHA manifest](results/v1/MANIFEST.json)를 함께 확인한다. 첫 재현 검사는 실행 중 구현 파일이 바뀌어 lock 불일치를 잡았다. 최종 source 동결 후 21검사를 다시 통과했으며 그 실패를 receipt에 보존했다.

## 통합 범위

| 연구 | 집계 셀 | 원본 단위 |
|---|---:|---|
| Native CodeOps | 8 | 100 원본 ID, 800 model executions, 2 stratum |
| v6 OSS / 배포 / AP | 2 / 17 / 12 | OSS test / service observations / synthetic ledger |
| Dynamic Graph | 90 | 23,040 model episodes; known state 결과와 usage 불확실성 구분 |
| Pay Loss Distribution | 945 | 2,007,040 settlement replays |
| CS / Voice | 7 / 28 | 4,900 / 5,000 synthetic episodes |
| Code Monetary | 288 + 2 demo | 147,456 policy replays + 별도 demo |

29개 등록 연구의 출처는 색인으로 연결했다. 모든 29개 연구의 원시 micro-action을 한 줄씩 정규화한 것이 아니다. 위 요청된 핵심 연구군의 수치 adapter와 전체 연구의 증거 색인을 구별한다. 행 수를 새로운 독립 표본 수로 사용하지 않는다. 원래 100 task ID는 ontology에 보존하고 task별 2 seed만으로 안정된 사고확률을 주장하지 않는다.

권한별 손실 비교 1,980건, 권한별 가상 사건률 비교 1,980건, 통제별 잔여손실 비교 3,048건을 생성했다. 별도 Code Monetary는 권한 비교 432건·통제 비교 720건이다. 이는 동결된 집계 간 비교 건수이지 새로운 실험 실행 건수가 아니다. binomial metric에 대한 posterior 산출은 1,139개이며 실제로 eligible 관측이 없는 경우 Unidentified로 남는다.

## 두 업무 평가에서 드러나는 점

Code는 독립 해결률과 잘못된 후보의 release를 동시에 봐야 한다. Monetary의 work completion은 후보 작업 실행량 비율이지 패치의 정답률이 아니다. 서로 다른 연구의 해결률·배포 선택·금전손실을 곱해 기업 사고율로 만들지 않았다. 경제 시나리오에서 전체 차단은 손실을 줄여도 실제 업무를 멈출 수 있다.

AP의 frozen CONTROLLED / ENTERPRISE / FAST_FINAL / P0에서 draft-only는 cash loss 0이지만 normal completion도 0이다. A100은 normal completion 0.5와 mean residual cash loss 7,850,275.91 LAB_USD_CENTS를 함께 갖는다. 이 금액은 실제 기업 손해가 아니라 가상 원장의 가정 금액이다. 실제 model-intent lane a의 낮은 업무 효용도 보고서에 그대로 남겨 ‘사고가 없어 안전하고 유용하다’고 설명하지 않는다.

## Bayesian과 의사결정의 한계

추가 독립 배치는 같은 셀의 binomial posterior를 갱신한다. 설정 변경은 별도 셀로 생성하고, 누적 배치와 변경 원장은 새 snapshot으로 내보낸다. 원본 source 파일과 이전 frozen 보고서는 변경하지 않는다.

Beta cluster-power 모델은 검증된 hierarchical model이나 미래 사고 예측 모델이 아니다. 반복 task correlation은 선언된 discount로 민감도를 낮추지만 학습된 random effect가 아니다. 경제손실 심도·법적 책임·보험 담보는 이 Bayesian 빈도 likelihood에 넣지 않았다. source SHA는 무결성 증거이며 독립 oracle의 정확성이나 집계 배치의 독립성을 대신 증명하지 않는다.

미측정 권한의 새 위험경로는 자동 외삽하지 않는다. 실제 동일 조건 자료가 있는 권한끼리 비교하고 추가 관측을 요구한다. Frontier는 같은 조건·화폐의 point-estimate 비교이며 고객 위험허용 문턱과 꼬리위험 제약을 넣은 최적 인수결정은 아니다.

`enterprise_calibrated=false`, `bindable_quote=false`, `production_approval=NOT_ASSESSED`다. 실제 고객 telemetry·비용·사용권·보험사 피드백이 들어오기 전까지 현장 사고율, 보험료, 법적 책임이나 경쟁 우위를 입증했다고 주장하지 않는다.
