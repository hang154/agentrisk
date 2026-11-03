# AgentRisk — 에이전트 업무 위임과 위험 연구

AI 에이전트에 누구의 업무를 얼마나 맡길지 결정할 때, **정상 업무 효용과 위험을 함께 비교**합니다. 핵심 연구는 같은 공급자 후보와 업무를 제공한 뒤 거래 이력을 바탕으로 공급자·권한을 선택하는 정책을 비교합니다.

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

- [연구 시제품과 결과](https://hang154.github.io/agentrisk/)
- [교수님 검토용 문서](research/riskquote/PROFESSOR_NOTION_BRIEF_KO.md)
- [최종 보고서](research/riskquote/RESEARCH_FINDINGS_KO.md) · [주 분석](research/riskquote/PRIMARY_ANALYSIS.json) · [다중검정](research/riskquote/MULTI_ATTEMPT_FAMILY.json) · [실험 프로토콜](research/economy/agent_company_riskquote_repeat16_20261026/PROTOCOL.md)
- [전체 공개 연구 색인](research/RESULTS_KO.md) · [제품·연구 설계](research/DESIGN_KO.md) · [기존 보고서](research/archive/INDEX.md) · [경제 실험](research/economy/INDEX.md)
- 공개 평가 코드: [CS](examples/cs-agent-safety-evaluation-portfolio/) · [음성](examples/voice-agent-injection-qa-portfolio/) · [코딩](examples/coding-agent-release-evaluation-portfolio/)

연구는 가상 업무·합성 경제 가정에 기초합니다. 실제 기업 사고율, 보험료 또는 인수 승인이 아닙니다. 공개 저장소에는 원시 증거 전체가 포함되어 있지 않습니다. 예제별 라이선스와 출처는 각 폴더에 기재되어 있습니다.
