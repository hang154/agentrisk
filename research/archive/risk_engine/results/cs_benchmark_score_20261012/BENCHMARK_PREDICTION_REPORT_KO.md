# 공개 벤치 점수 → CS 효용·위험 예측 실험

## 결론

공개 벤치 점수만으로 업무별 위험을 신뢰할 수준으로 외삽할 수 있다는 근거는 확보하지 못했다. 정상 완료와 bad proposal의 점 Brier는 pooled Beta보다 낮았지만 Root bootstrap 구간은 0을 포함했다. F0 escape는 Beta보다 크게 나빴다(0.33014 대 0.12405). F1 material도 Beta보다 나빴다(0.26401 대 0.24837). 추가 Anchor-only Beta 대비 보편적 개선도 확인하지 못했다. 실보험료·권한 승인 입력으로 승격하지 않는다.

개별 업무의 오차도 컸다. Blind 청구조회 정상 완료는 F0 9.6% 예측 대 5/8 관측(62.5%), 정보 안내 위험은 1.5% 예측 대 4/16 관측(25%)이었다. 이 사례들을 숨기거나 전체 평균 하나로 대체하지 않았다.

이번 시험은 공개 벤치 점수로 실제 CS 결과를 예측할 수 있는지 확인한다. 과거 Qwen 결과는 적합에 쓰지 않았다. 다만 Qwen 자체는 이전 연구에서 이미 관측한 모델이므로 세계 최초 미관측 모델 검증이라고 부르지 않는다.

## 실험

- 기존 모델 전체 제외 검증: R3 B0에서 3개 Actor를 하나씩 통째로 제외한 사후 검증. 점 Brier 개선은 18/24지만 알려진 자료의 탐색적 결과다.
- 신규 실행: 기존 Qwen GPU2 서비스 유지, 5개 CS 업무 × 20개 신규 Root × 2시드 = 200회. 최초 파일럿 10회는 모두 판정됐지만 위기 이관 0/2 완료로 scale gate가 닫혔다. 원본을 보존하고 새 정상 진단 Root 3개/업무 × 2시드의 30회 파일럿을 별도 V2에서 시행했다. 파일럿 전체는 본표본/적합에서 제외했고 primary 원본 생성 인덱스·수·seed·예산·oracle는 유지했다.
- F0: Gemma/GPT의 과거 적격 B0 증거와 공개 GPQA 점수로 예측, target 호출 전에 잠금.
- Anchor: 20개 신규 Root/40회. F1 잠금 후 나머지 80 Root/160회를 실제 실행.
- 총 출력/추론 32K, 호출당 8K, 131K 맥락, 기존 sampling·도구·오라클 유지. C64 pool와 HTTP semaphore는 실제 동일 검증 프로필에 결합. 다른 GPU/모델 서비스를 종료하지 않음.

## 같은 Blind Root에서 Beta와 비교

음수 ΔBrier는 벤치 기반 예측이 더 낫다는 뜻이다. Root bootstrap 구간은 이 Qwen/업무 모집단의 표본오차이며 모델 계보 일반화의 확신이 아니다.

| 단계 | 지표 | 공통 Root | 모델 Brier | Beta Brier | ΔBrier 95% 구간 |
|---|---|---:|---:|---:|---|
| F0 | utility | 40 | 0.26252 | 0.32084 | [-0.16498315877195044, 0.049980849346268355] |
| F1 | utility | 40 | 0.26777 | 0.30917 | [-0.15228478900188977, 0.07616866087946364] |
| F0 | material | 80 | 0.24478 | 0.24874 | [-0.06560313289362363, 0.06840354878065405] |
| F1 | material | 80 | 0.26401 | 0.24837 | [-0.03841417370617905, 0.07360358249286561] |
| F0 | bad | 80 | 0.24905 | 0.32451 | [-0.16709088501300837, 0.017142195666980175] |
| F1 | bad | 80 | 0.25659 | 0.31149 | [-0.1375143037428251, 0.03000507623451899] |
| F0 | escape | 30 | 0.33014 | 0.12405 | [0.08019100257647911, 0.32652941485889897] |
| F1 | escape | 30 | 0.12123 | 0.12058 | [-0.08284733942868024, 0.08055745164786056] |

## 판정 범위

지표별 결과를 따로 본다. 업무 성공을 예측했다고 위험·손실까지 예측한 것은 아니다. 추가 Anchor 후 개선은 공개 벤치 점수만의 성능이 아니다. F0/F1 비교에는 동일 Blind 집합만 사용했다.
더 강한 참고 기준인 Qwen Anchor-only Beta도 별도 비교했다. 첫 Blind dispatch 뒤 추가한 보조 분석이므로 사전 잠금 성과로 승격하지 않는다. 이 기준선은 Anchor 정답만 사용하며 Blind 정답으로 적합하지 않는다. 수치는 PAIRED_BENCHMARK_VALUE.json의 auxiliary_anchor_only_comparisons에 있다.
공개 점수는 Qwen GPQA 86.0, Gemma GPQA Diamond 58.6, GPT medium/no-tools GPQA Diamond 66.0이다. Qwen 카드의 GPQA subset 표기는 불명확하고 publisher 하네스·예산·quantization 조건도 같다고 확인되지 않았다. 따라서 통일 벤치의 정확한 수치가 아니라 외부 능력 proxy를 시험한 것이다.
출처: [Qwen FP8 공식 카드](https://huggingface.co/Qwen/Qwen3.6-35B-A3B-FP8), [Gemma QAT 공식 카드](https://huggingface.co/google/gemma-4-E4B-it-qat-w4a16-ct), [GPT-OSS 공식 카드](https://deploymentsafety.openai.com/gpt-oss).
학습 Actor가 2개, 새 실행 Actor가 1개뿐이다. 반복 Root 수가 많아도 모델 수가 늘어나지 않는다. 모델 효과·고객 정책/생성기 차이·publisher 측정 오차가 교란될 수 있다. 폭넓은 신규 모델 일반화나 고객 권한 추천으로 승격하지 않는다.
Root는 정상/적대 상황 50:50의 합성 스트레스 모집단이다. 실제 고객 사고빈도로 옮길 수 없다. 이번 예측은 업무별 확률이며 개별 고객 사례의 정확한 참/거짓 예언이 아니다. 권한은 B0로 고정했으므로 이 실험 자체로 권한 변경 효과를 추정하지 않는다.
기존 3개 Actor 점수의 6가지 순열 대조에서 실제 배치가 macro Brier 0.22075로 가장 낮았다. 그러나 가능한 배치가 6개뿐이라 최소 단측 비율도 1/6이다. 이는 탐색적 근거이지 95% 유의성이나 신규 모델 일반화의 증명은 아니다.
이번 모형은 업무별 독립 적합이다. 기존 평가기의 공통 draw-index 방식은 다른 업무의 marginal posterior 사이에 인위적 결합을 줄 수 있어, 그 joint predictive-count 구간은 승격하지 않는다. 잠근 marginal draws를 업무별로 독립 재표집한 FORECAST_NUMERICAL_AUDIT.json을 별도 제공한다. 원래 잠금·Brier/Log Loss는 변경하지 않았다.
과거 예약·반품의 등록 오라클 공백은 보존했으며 사후 재분석으로 숨기지 않았다. 신규 5개 업무에는 예약·반품을 포함하지 않는다. 정보 안내는 typed policy facts에 한정한다.
실기업 손실·법적 책임·실보험료는 이번 예측 대상이 아니며, 미확정 응답·Root는 0으로 바꾸지 않는다.

## 실행 상태

{"accepted_roots": 100, "benchmark_to_risk_product_validated": false, "bindable_quote": false, "execution_analysis_complete": true, "independent_test_models": 1, "independent_training_models": 2, "primary_episodes": 200, "unknown_roots": 0}

원시 사용량·모델 응답·Tool/원장 변화·Seed·예측 잠금과 출처 SHA를 보존했고, 새 SQLite admission으로 독립 재현했다.

## 업무별 사전 확률과 관측

| 업무 | 지표 | Blind 적격 Root | F0 벤치 기반 | F1 Anchor 추가 | 독립 관측 |
|---|---|---:|---:|---:|---:|
| refunds | utility | 8 | 78.2% | 88.2% | 4/8 |
| refunds | material | 16 | 12.3% | 16.7% | 7/16 |
| account_change | utility | 8 | 99.1% | 99.2% | 8/8 |
| account_change | material | 16 | 35.3% | 13.1% | 5/16 |
| billing | utility | 8 | 9.6% | 6.1% | 5/8 |
| billing | material | 16 | 16.1% | 49.7% | 3/16 |
| information | utility | 8 | 96.3% | 85.7% | 7/8 |
| information | material | 16 | 1.5% | 5.5% | 4/16 |
| crisis | utility | 8 | 82.0% | 67.5% | 4/8 |
| crisis | material | 16 | 29.4% | 25.5% | 7/16 |
