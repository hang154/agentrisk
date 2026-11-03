# AgentRisk 연구 결과 색인

서로 다른 연구의 모델 실행, 정책 재생, 시나리오 셀은 각각 다른 단위다. 금액은 가상 원장 또는 가정에 따른 결과다.

| 연구 | 관측 및 결과 | 해석 |
|---|---|---|
| Native CodeOps | 100개 파생 과제 × 두 모델 × Single/Swarm × 두 시드 = 800회. Qwen 해결 238/400, GPT-OSS 195/400; 판정 불능 각각 44, 6 | 공식 SWE-bench 성적이 아니다. reviewer·repair 등 전체 후속 패널은 미완료 |
| 음성 인젝션 | 합성 음성 5,000회 중 평가 가능 4,768회, 판정 유보 232회. 공격 시험 위험 행동 통과 B0 66/1,664, B1 0/1,679 | B1은 복합 통제이며 reviewer 단독 효과가 아니다. 실제 고객 통화가 아니다 |
| CS V3 | 실제 모델 실행 2,600회. 타임아웃 65건, 63개 Root·정책 셀 미확정. 계층모형 8개 수렴 실패 | 사전 예측 성공이나 권한 추천 효과를 입증하지 못했다 |
| RiskQuote 반복 실험 | 36,864개 정책별 실행 기회. COLD/WARM AgentRisk−GBDT 평균 순가치 차이 6.03/4.73; 두 비교 Holm 보정 p=0.02734 | 합성 업무 기준 정책 패키지 비교. STEP 대비 두 비교는 Holm 보정 기준 미통과 |
| 통합 Risk Cell V1 | 1,399 집계 셀, 10개 numeric adapter; Code와 AP 업무 평가 | 집계 수를 독립 실험 수로 해석하지 않는다. 동조건 Beta 갱신과 제한적 전이를 구분 |

## RiskQuote 설계와 추가 결과

24개 작성 업무 규칙, 12개 공유 출처 군집, 16개 새 시드, COLD/WARM, 4개 정책, 12개 순차 계약을 사용했다. 동일 초기 후보와 정보를 제공하고 이후 정책별 결과가 이력에 반영된다. 전체 36,864건은 기록·평가 가능했고 형식 오류 4건은 실패로 보존했다. 군집 단위 정확 검정과 재시도까지 포함한 8개 비교의 Holm 보정을 적용했다.

| 비교 | 평균 차이 | 95% bootstrap 구간 | Holm8 p | 판정 |
|---|---:|---:|---:|---|
| COLD AR−GB | 6.03 | 2.47 ~ 10.32 | 0.02734 | 통과 |
| WARM AR−GB | 4.73 | 2.29 ~ 7.58 | 0.02734 | 통과 |
| COLD AR−STEP | 7.51 | 1.92 ~ 14.09 | 0.11719 | 미통과 |
| WARM AR−STEP | 6.30 | 1.63 ~ 11.91 | 0.09570 | 미통과 |

순가치는 정상 업무 가치에서 수수료, 지연, 평가비용, 직접손실을 뺀 합성 지표다. 개별 95% 구간은 다중비교 동시구간이 아니다. 순가치 우위는 손실 감소와 같지 않다. WARM에서 AR의 가상 직접손실은 5,661, GB는 5,170이었다. 정책 선택과 이후 이력의 결합 효과이며 위험 예측 알고리즘 단독 효과로 해석하지 않는다.

## 공개 근거

- [CS 공개 평가 결과](../examples/cs-agent-safety-evaluation-portfolio/docs/RESULTS.md)
- [Voice 공개 평가 결과](../examples/voice-agent-injection-qa-portfolio/docs/RESULTS.md)
- [Coding 공개 평가 결과](../examples/coding-agent-release-evaluation-portfolio/docs/RESULTS.md)
- [RiskQuote 확정 수치](riskquote/PRIMARY_ANALYSIS.json)
- [RiskQuote 결과 보고서](riskquote/RESEARCH_FINDINGS_KO.md)

연구에서 사용한 보험 기술요율은 실험실의 빈도·심도·담보 가정에 의존한다. 기업별 보험 판매가격 또는 인수 승인이 아니다. 원본 기록, 개인정보와 내부 실행환경을 포함할 수 있는 자료는 별도 공개 검토 후 추가한다.
