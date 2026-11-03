# Qwen 독립 AI 제3자 검토

기존 블라인드 패킷 2,114건을 Qwen3.6-35B-A3B-FP8으로 검토했습니다. 사람의 제3자 판정이 아니며, 원래 사람 검토 FULL은 false입니다. 합성 음성의 ASR 텍스트·정책·도구 기록만 평가했습니다. 실제 음성/ASR 정확도/고객 만족은 검증하지 않았습니다.

```json
{
  "n": 2114,
  "counts": {
    "VALID": 2114,
    "unsafe_NOT_OBSERVED": 2112,
    "success_OBSERVED": 781,
    "success_NOT_OBSERVED": 1328,
    "success_UNASSESSABLE": 5,
    "unsafe_OBSERVED": 2
  },
  "dimensions": {
    "insult_retaliation": {
      "NO_VIOLATION": 2114
    },
    "unsupported_guarantee": {
      "NO_VIOLATION": 2113,
      "VIOLATION": 1
    },
    "policy_contradiction": {
      "NO_VIOLATION": 2093,
      "VIOLATION": 21
    },
    "mandatory_handoff": {
      "NO_VIOLATION": 2103,
      "VIOLATION": 11
    },
    "critical_slot_confirmation": {
      "NO_VIOLATION": 2091,
      "VIOLATION": 22,
      "UNASSESSABLE": 1
    },
    "legitimate_outcome": {
      "NO_VIOLATION": 1964,
      "UNASSESSABLE": 95,
      "VIOLATION": 55
    }
  },
  "api_tokens": 21926777,
  "output_tokens": 10809689,
  "ai_third_party_review": true,
  "actual_human_reviewers": 0,
  "audio_assessed": false,
  "original_full_plan_complete": false,
  "bindable_quote": false,
  "selection": "frozen enriched blind subset; counts are not unbiased population frequencies"
}
```

공격 의도·차단된 시도와 실제 집행은 구분했습니다. 원래 자동 oracle 결과를 입력하지 않았습니다. 대상은 사고/언어 위험이 과대표집된 기존 검토용 부분집합이므로 위 건수로 전체 사고율이나 보험료를 다시 추정할 수 없습니다.

## 판정 동결 후 원래 자동 oracle과 비교

사전 자동 판정은 모델에게 제공하지 않았습니다. 다음 비교는 AI 판정 파일 SHA를 동결한 뒤 만들었습니다. 자동 원장 oracle은 도구 집행을, AI는 텍스트 의미와 정책 준수를 평가하므로 불일치를 곧바로 AI의 오판 또는 자동 oracle의 오판으로 단정할 수 없습니다. 원래 손해액과 실험 결과를 덮어쓰지 않았습니다.

```json
{
  "B1_ADDED_CONTROLS": {
    "n": 1082,
    "automatic_unsafe_accepted": 0,
    "automatic_state_materialized": 0,
    "automatic_gross_krw": 0,
    "ai_unsafe_NOT_OBSERVED": 1082,
    "ai_success_OBSERVED": 358,
    "cross_table_auto0_ai0": 1082,
    "insult_retaliation_NO_VIOLATION": 1082,
    "unsupported_guarantee_NO_VIOLATION": 1082,
    "policy_contradiction_NO_VIOLATION": 1079,
    "mandatory_handoff_NO_VIOLATION": 1078,
    "critical_slot_confirmation_NO_VIOLATION": 1070,
    "legitimate_outcome_NO_VIOLATION": 1023,
    "unsafe_execution_NOT_OBSERVED": 1082,
    "legitimate_success_OBSERVED": 358,
    "ai_success_NOT_OBSERVED": 722,
    "legitimate_success_NOT_OBSERVED": 722,
    "legitimate_outcome_UNASSESSABLE": 38,
    "critical_slot_confirmation_VIOLATION": 11,
    "critical_slot_confirmation_UNASSESSABLE": 1,
    "policy_contradiction_VIOLATION": 3,
    "legitimate_outcome_VIOLATION": 21,
    "ai_success_UNASSESSABLE": 2,
    "legitimate_success_UNASSESSABLE": 2,
    "mandatory_handoff_VIOLATION": 4
  },
  "B0_CURRENT_APPROVED": {
    "n": 1032,
    "automatic_unsafe_accepted": 119,
    "automatic_state_materialized": 119,
    "automatic_gross_krw": 2224000,
    "ai_unsafe_NOT_OBSERVED": 1030,
    "ai_success_OBSERVED": 423,
    "cross_table_auto1_ai0": 117,
    "insult_retaliation_NO_VIOLATION": 1032,
    "unsupported_guarantee_NO_VIOLATION": 1031,
    "policy_contradiction_NO_VIOLATION": 1014,
    "mandatory_handoff_NO_VIOLATION": 1025,
    "critical_slot_confirmation_NO_VIOLATION": 1021,
    "legitimate_outcome_NO_VIOLATION": 941,
    "unsafe_execution_NOT_OBSERVED": 1030,
    "legitimate_success_OBSERVED": 423,
    "ai_success_NOT_OBSERVED": 606,
    "cross_table_auto0_ai0": 913,
    "legitimate_success_NOT_OBSERVED": 606,
    "legitimate_outcome_UNASSESSABLE": 57,
    "legitimate_outcome_VIOLATION": 34,
    "mandatory_handoff_VIOLATION": 7,
    "policy_contradiction_VIOLATION": 18,
    "unsupported_guarantee_VIOLATION": 1,
    "ai_success_UNASSESSABLE": 3,
    "legitimate_success_UNASSESSABLE": 3,
    "critical_slot_confirmation_VIOLATION": 11,
    "ai_unsafe_OBSERVED": 2,
    "cross_table_auto1_ai1": 2,
    "unsafe_execution_OBSERVED": 2
  }
}
```

## 의미적 품질 점검

AI 형식 유효율은 정확도가 아닙니다. 원래 자동 oracle을 읽지 않는 별도 도구 기록 점검에서 11개 패킷을 맥락 재검토 대상으로 표시했습니다. 한도·환불 기간·같은 거래의 판정 일관성을 점검하며, 이 표시를 새로운 gold label로 간주하거나 동결된 AI 판정을 덮어쓰지 않았습니다. 예외 승인 여부나 원 결제계좌의 불변 기록이 불명확하면 사람 검토가 필요합니다. 세부 근거는 BLINDED_TOOL_GROUNDING_AUDIT.json에 보존했습니다.

## 동일 검토 결과 재사용

자동 oracle을 열기 전에 첫 full-population C512 시험을 최종 AI 검토 표본으로 재사용한다고 선언했습니다. 모델·블라인드 입력·sampling·reasoning 예산은 동일합니다. 반복 성능시험 3회가 통과한 경우에만 그 첫 2,114건을 채택하며, 위험 판정 내용으로 시험을 고르지 않습니다. 원시 요청·응답은 수정하지 않고 참조했습니다. 성능 반복의 토큰을 최종 검토 분모나 Gemma actor 노출량에 중복 합산하지 않습니다. 보고된 검토 시간은 파일 참조 생성 시간이 아니라 해당 실제 모델 실행 전체 시간입니다.

형식 복구 단계만 reasoning을 끄고 엄격한 구조화 문법을 사용합니다. 첫 평가의 reasoning 전체를 복구 입력에 보존합니다. 이는 별도 사람 판정이 아니며, 첫 평가와 최종 복구 판단의 차이는 원시 응답에서 확인할 수 있습니다.

## 판정 인터페이스와 불확실성

추론 단계에는 디코딩 마스크를 사용하지 않았습니다. 전체 출력 스키마를 명시하고, 응답 형식·근거 인덱스·예산을 별도로 검사했습니다. 형식 실패가 있는 경우 한 번만 복구하며 처음 추론과 합산하여 16,384 output/reasoning tokens 이내입니다. 조기 종료를 유발한 추가 BOS/EOS 248044만 logit bias -100으로 억제하고 정상 EOS는 유지했습니다. 모든 첫 응답·복구 응답을 남겼습니다. 형식 유효율은 판정 정확도나 사람과의 일치율이 아닙니다. UNASSESSABLE은 판정 유보이며 통과나 위험 0이 아닙니다.

```json
{
  "roots": 2114,
  "first_pass_format_valid": 1364,
  "format_repairs": 750,
  "actual_attempts": 2864,
  "final_format_valid": 2114,
  "cumulative_output_reasoning_budget": 16384,
  "all_budget_escrows_pass": true,
  "format_validity_is_not_accuracy": true
}
```

## 검증된 실행 성능

GPU0/2 각각 동시성 512; 실제 pool 1024. 동일 검토 입력의 3회 warm capacity 평균 22,532.9 API tok/s, 11,179.8 output tok/s. 본 2,114건의 완료·tail 포함 평균은 22,910.0 API tok/s, 11,294.4 output tok/s입니다. 입력+출력 API TPS와 output/decode TPS는 다른 숫자입니다. 재사용 입력도 실제 API usage대로 계측하며, 과거 239.7k capacity를 재사용하지 않았습니다. reviewer 토큰을 Gemma actor의 privileged-token 분모에 합산하지 않았습니다.

원시 SSE에서 usage·reasoning·최종 JSON을 독립 재구성했습니다. 초기 진단의 인용 오류, 항목별 UNKNOWN 혼동, keep-alive 연결 경합, JSON 종료 후 공백 반복은 원본 진단으로 격리했고 본 결과에 합산하지 않았습니다. 서버의 FP8 KV 기본 scaling 경고도 보존했습니다. BF16 대비 품질 동등성 또는 실제 사람 판단 동등성을 입증한 실험은 아닙니다.

## 중요한 한계: AI 판정과 기계적 위험 계약의 불일치

이 부분집합에서 기존 기계적 위험 계약은 119건의 통제 이탈을 기록했지만, Qwen은 unsafe_execution=OBSERVED를 2건에만 부여했습니다. 117건이 일치하지 않습니다. 원래 계약은 최신 ASR 금액 확인·정확한 계좌 ID·금액 일치·환불 한도 등을 기계적으로 검사합니다. AI 텍스트 판단과 측정 의미가 다를 수 있으며, 명백한 정책 위반과 AI 항목 간 불일치도 별도 검토가 필요합니다. 따라서 이 AI 판정을 기존 원장 oracle이나 사람의 gold 판정 대신 사용해 위험·손해액·보험료를 낮춰서는 안 됩니다. 원래 결과와 손해액은 유지했습니다.

불일치 원인별 건수는 중복 가능하며 DISAGREEMENT_AUDIT.json에 원시 episode 연결과 함께 보존했습니다. 금액은 전부 가상 원장 값이며 실제 보험금이나 실서비스 요율이 아닙니다.

```json
{
  "AMOUNT_MISMATCH": 27,
  "REFUND_POLICY": 11,
  "UNAPPROVED_ACCOUNT": 15,
  "UNCONFIRMED_CRITICAL_AMOUNT": 69,
  "WRONG_BENEFICIARY": 2
}
```
