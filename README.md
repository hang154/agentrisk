# AgentRisk — 에이전트 업무 위임과 위험 연구

**처음 보는 AI 에이전트에게 어떤 일을, 어느 권한까지 맡길 수 있을까요?** AgentRisk는 업무를 맡기기 전의 조건 설정과 실행 후의 독립 검증을 연결합니다. 모델의 정답률에 더해 실제 완료, 잘못된 상태 변경, 검토 비용과 손실을 함께 평가하는 연구입니다.

예를 들어 주문서·입고·송장을 대조하는 에이전트에게 읽기만 허용할지, 저액 지급까지 허용할지 결정합니다. 실행 후에는 계약상 정답과 원장 상태를 비교하고 검증된 결과를 다음 업무의 이력에 반영합니다. 이 설명은 가상 지급 실험의 목적이며 실제 고객 거래 사례가 아닙니다.

[사이트에서 연구 보기](https://hang154.github.io/agentrisk/) · [연구 목적과 전체 서사](research/RESEARCH_STORY_KO.md) · [교수님 검토용 문서](research/riskquote/PROFESSOR_NOTION_BRIEF_KO.md)

## 최근 핵심 실험: RiskQuote

실제 Gemma E4B·GPT-OSS-20B가 가상 지급 업무를 수행한 신규 **36,864개 정책별 실행 기회**에서 AgentRisk 정책의 평균 구매자 순가치는 GBDT 기반 정책보다 COLD **+6.03**, WARM **+4.73** 합성 단위 높았습니다. 이전 시도를 포함한 8개 검정의 Holm 보정 p는 각각 **0.0273**입니다.

단계적 승격 대비 두 비교는 같은 보정 기준을 통과하지 못했습니다. 순가치는 합성된 효용·비용 지표이며, WARM 직접손실은 AgentRisk가 GBDT보다 컸습니다. 따라서 결과는 손실 감소나 위험 예측기 단독 효과가 아니라 **정책 묶음의 순가치 비교**입니다.

| 비교 | 거래 기회당 순가치 차이 | Holm8 p | 판정 |
|---|---:|---:|---|
| COLD AgentRisk − GBDT | +6.03 | 0.0273 | 통과 |
| WARM AgentRisk − GBDT | +4.73 | 0.0273 | 통과 |
| COLD AgentRisk − 단계적 승격 | +7.51 | 0.1172 | 미통과 |
| WARM AgentRisk − 단계적 승격 | +6.30 | 0.0957 | 미통과 |

24개 규칙은 12개의 공유 출처 군집에 속합니다. 반복 36,864회를 독립 업무군 36,864개로 해석하지 않습니다.

## 숫자를 업무 결과로 읽으면

| 이력 | GBDT 정확 완료 | AgentRisk 정확 완료 | GBDT 직접손실 | AgentRisk 직접손실 |
|---|---:|---:|---:|---:|
| COLD | 1,685/4,608 (36.57%) | 1,963/4,608 (42.60%) | 5,385 | 5,279 |
| WARM | 1,754/4,608 (38.06%) | 1,976/4,608 (42.88%) | 5,170 | 5,661 |

추가 완료는 COLD 278건, WARM 222건이었습니다. WARM의 직접손실도 491 합성 단위 증가했습니다. 주 결과는 지정한 가치·비용 가정 아래의 평균 순가치 개선입니다. 완료율·손실 차이의 별도 통계적 우위를 이 표만으로 주장하지 않습니다.

## 이 비교가 필요했던 이유

초기 A–D 실험에서 매칭 정책의 순가치 개선을 관측했지만, 후보 공급자를 더 넓게 고르는 효과가 함께 포함돼 있었습니다. 이후 같은 후보와 증거를 제공하는 실험에서는 초기 선택기의 추가 가치가 입증되지 않았습니다. RiskQuote에서는 저액 고정·단계적 승격·GBDT·AgentRisk를 공통 초기 조건에서 비교하고, 지급·읽기 오류와 업무 완료를 구분했습니다.

첫 18,432건에서 당시 네 검정 보정 기준으로 COLD−STEP만 통과했습니다. 그 결과를 본 뒤 신규 36,864건의 규모와 종료 기준을 고정했고, 직전 시도의 네 검정을 포함한 Holm8을 적용했습니다. 과거와 신규 자료는 합산하지 않았습니다. [실험별 변화와 원문](research/RESEARCH_STORY_KO.md#연구-질문은-어떻게-구체화됐나)을 공개합니다.

## 동작 경로와 다음 목표

**계약 → 공급자·권한 선택 → 실제 모델 역할 수행 → 권한 게이트 → 가상 지급 원장 → 독립 판정 → 다음 거래의 이력**

이 경로를 업무·스택·권한·통제·복구·맥락·기간의 **Risk Cell**에 연결합니다. 목표는 검증된 실행 증거로 첫 업무의 조건을 정하고 이후 권한을 재평가하는 것입니다. 현재 실험은 정책 전체의 효용을 비교하며, 예측기 단독 기여·신규 업무 일반화·기업 간 신용 이전은 별도 연구 질문입니다.

## 공개 자료

- [연구 시제품과 결과](https://hang154.github.io/agentrisk/)
- [교수님 검토용 문서](research/riskquote/PROFESSOR_NOTION_BRIEF_KO.md)
- [최종 보고서](research/riskquote/RESEARCH_FINDINGS_KO.md) · [주 분석](research/riskquote/PRIMARY_ANALYSIS.json) · [다중검정](research/riskquote/MULTI_ATTEMPT_FAMILY.json) · [실험 프로토콜](research/economy/agent_company_riskquote_repeat16_20261026/PROTOCOL.md)
- [전체 공개 연구 색인](research/RESULTS_KO.md) · [제품·연구 설계](research/DESIGN_KO.md) · [기존 보고서](research/archive/INDEX.md) · [경제 실험](research/economy/INDEX.md)
- 공개 평가 코드: [CS](examples/cs-agent-safety-evaluation-portfolio/) · [음성](examples/voice-agent-injection-qa-portfolio/) · [코딩](examples/coding-agent-release-evaluation-portfolio/)

연구는 가상 업무·합성 경제 가정에 기초합니다. 실제 기업 사고율, 보험료 또는 인수 승인이 아닙니다. 공개 저장소에는 원시 증거 전체가 포함되어 있지 않습니다. 예제별 라이선스와 출처는 각 폴더에 기재되어 있습니다.
