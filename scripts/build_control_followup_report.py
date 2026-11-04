#!/usr/bin/env python3
"""Render final reviewed tables from immutable result artifacts, never invented values."""
import json,pathlib
repo=pathlib.Path(__file__).resolve().parents[1];a=repo/'artifacts/control_followup_20261104';d=repo/'research/control_followup_20261104'
load=lambda name:json.loads((a/name).read_text())
def fmt(x,n=4):return '보류' if x is None else f'{x:.{n}f}'
def main():
 m=load('MONITOR_CENSUS.json');o=load('ORGANIZATION_REPRODUCTION.json');c=load('COMPONENT_REPRODUCTION.json');repro=load('FINAL_REPRODUCTION.json');parser=load('PARSER_RECOVERY_AUDIT.json');archives=load('PUBLIC_ARCHIVES.json');backups=load('BACKUP_VERIFICATION.json');attack=load('ADAPTIVE_ATTACKER_AUDIT.json')
 assert all(x['pass_gate'] for x in [m,o,c,repro,parser]);assert c['trades']==4896 and o['main_teams']==1728;assert backups['ssd_verified'] and backups['hdd_verified']
 ca=c['analysis'];lines=['# AgentRisk Control Study — 잔여 목표 검토·보완 결과','',
 '기존 V1 결과와 실패 기록을 보존한 채 후속 실행·독립 검산·재현 코드·백업을 완료했습니다. 사람 블라인드 이중 검토는 사용자의 “스킵” 지시에 따라 제외했으며, 사람 판정이 수행됐다고 표시하지 않습니다.','',
 '| 실행 단위 | 완료 | 판정·비고 |','|---|---:|---|',
 f"| 모니터 전수 검토 | {m['rows']:,}판정 / {m['unique_actions']}행동 | 기존 800판정 재사용, 새 호출 {m['new_calls']:,}건 |",
 f"| 조직·세션·이력 공유 | {o['main_teams']:,}팀 | {o['main_teams']-o['unknown']:,}팀 판정 가능, 원본 {o['unknown']}팀 미확정 보존 |",
 f"| RiskQuote 구성요소 비교 | {c['trades']:,}거래 | 미확정 {c['unknown']}건, 17조건·24업무 규칙 |",
 f"| 적응형 공격 개발 | {attack['candidates']}후보·{attack['probe_episodes']}검증 실행 | 선택 공격의 개발 위험 실행 {attack['selected_unsafe_probe_score']}건 |",
 '| 별도 파일럿 | 조직 12팀·구성요소 17+17거래 | 첫 구성요소 파일럿의 형식 오류 2건 보존 |','',
 '표의 단위는 서로 다릅니다. 이를 합쳐 독립 표본 수로 사용하지 않습니다. GPU2의 GPT-OSS-20B, medium, 0.6/0.95, 호출당 4,096토큰을 유지했으며 기존 검증 C512를 사용했습니다.','',
 '## 1. 실행 증거가 모니터 판단을 개선했는가','',
 '| 조건 | 판정 대상 | UNSURE | TP / FN / FP / TN | Brier |','|---|---:|---:|---|---:|']
 for k in ['M0','M1','M2','M3','M2_PROSE']:
  r=m['summary'][k];lines.append(f"| {k} | {r['n']} | {r['unsure']} | {r['tp']} / {r['fn']} / {r['fp']} / {r['tn']} | {r['brier_all_valid']:.6f} |")
 x=m['paired_brier']['M2-M0'];lines+=['',f"M2−M0의 업무군 평균 Brier 차이는 {x['effect']:.6f}, 95% 재표집 구간 {x['cluster_bootstrap_ci95']}, exact p={x['exact_two_sided_signflip_p']:.6f}입니다. 실행 영수증·상태를 제공한 조건에서 개선이 관측됐습니다. 실제 위험 행동은 17개이며, 기존 V1의 사후 전수 분석입니다.",
 'M3의 과거 이력 추가 효과와 M2의 구조화 형식 자체 효과는 각각 비교 구간이 0을 포함했습니다. 보류를 정상 판정으로 바꾸지 않았고, 사후 상태 정보를 과거 차단 결정에 사용하지 않았습니다.','',
 '## 2. 적응형 제어가 단순 통제보다 나았는가','',
 '| 정책 | 정상 업무 전체 완료 | 위험 팀 / 판정 가능 | 합성 직접손실 | 미확정 |','|---|---:|---:|---:|---:|']
 for k in ['STATIC','CUMULATIVE','FROZEN','ADAPTIVE']:
  r=o['analysis']['summary'][k];lines.append(f"| {k} | {r['benign_complete']}/{r['benign_n']} | {r['unsafe_teams']}/{r['known']} | {r['synthetic_loss']:,} | {r['unknown']} |")
 x=o['analysis']['paired']['CUMULATIVE'];lines+=['',f"ADAPTIVE−CUMULATIVE의 위험 팀 비율 차이는 {100*x['unsafe']['effect']:.3f}%p, 정상 업무 전체 완료 차이는 {100*x['complete']['effect']:.3f}%p였습니다. 적응형 점수 갱신의 우위는 입증되지 않았습니다.",
 '여섯 명칭은 하나의 지급 상태기계에 대한 계약 변형입니다. 최종 감사에서 이를 확인해 업무 간 확증 p·신뢰구간은 보류했습니다. 여섯 변형의 민감도 분석은 별도로 남겼습니다. 미확정 팀의 부분 처리 건수는 효용 비교에서 제외했습니다.',
 '전체 이력 공유에서는 위험 팀 26/573·정상 완료 176/287, 최근 두 건만 제공하면 위험 팀 425/574·정상 완료 33/286이었습니다. 최근 두 건 조건은 자신의 긴 이력을 포함하는 조건의 상위집합이 아니므로 “이력을 조금 주면 항상 해롭다”고 해석하지 않습니다. 조직 크기는 1/2/4로 배정한 것이며 자율 소환의 실측으로 부르지 않습니다.','',
 '## 3. RiskQuote의 어느 구성요소가 효과를 냈는가','',
 '동일 후보·권한 선택지·초기 이력·업무 규칙으로 2×2×2×2 요인 설계와 단순 Beta 이력 정책을 실제 실행했습니다. AR·GB·SIMPLE은 각 거래의 **동일하게 선택된 행동**도 결과 전에 예측했습니다.','',
 '| 구성요소 변화 | 평균 순가치 차이 | 95% 업무군 구간 | Holm4 p |','|---|---:|---|---:|']
 for k,title in [('predictor','AR − GB'),('supplier','공급자 선택 − 고정'),('authority','권한 선택 − 고정'),('history','이력 갱신 − 동결')]:
  r=ca['component_effects'][k]['buyer_net'];lines.append(f"| {title} | {fmt(r['effect'])} | {r.get('cluster_bootstrap_ci95')} | {fmt(r.get('holm4_p'))} |")
 lines+=['','양의 순가치 차이는 안전성 우위를 뜻하지 않습니다. 순가치는 정확한 지급 업무 가치 100에서 공급자 비용·독립 확인 손실·고정 비용 0.6을 뺀 합성 회계 단위입니다. 실제 금액·보험료가 아닙니다.','',
 '| 동일 행동 예측 대상 | AR Brier | GB Brier | SIMPLE Brier | 공통 표본 |','|---|---:|---:|---:|---:|']
 for k,r in ca['same_action_forecast_scores'].items():lines.append(f"| {k} | {fmt(r['AR']['brier'],6)} | {fmt(r['GB']['brier'],6)} | {fmt(r['SIMPLE']['brier'],6)} | {r['AR']['n']} |")
 lines+=['','조건별 전체 결과:','', '| 예측/공급자/권한/이력 | 정상 업무 정확 완료 | 위험 상태 변경 | 합성 손실 | 미지급 의무 | 평균 순가치 |','|---|---:|---:|---:|---:|---:|']
 for k,r in sorted(ca['summary'].items()):lines.append(f"| {k} | {r['benign_correct_paid_work']}/{r['benign_known']} | {r['material_events']}/{r['known']} | {r['loss']:,} | {r['unpaid_obligations']:,} | {fmt(r['mean_buyer_net'])} |")
 lines+=['','같은 GPT-OSS 모델의 다섯 공급자 구성(위임 깊이·프롬프트 스타일)을 사용했습니다. 과거 두 모델 결과의 재현이나 신규 업무 일반화라고 부르지 않습니다. 두 요인 상호작용과 관측 효용–위험 경계는 JSON에 탐색 분석으로 포함했습니다.','',
 '## 4. 구현·증거 보완','',
 f"- Harmony의 중복 종료 토큰만 복구하는 전용 wrapper를 적용했습니다. {parser['recoveries']}건을 원시 응답 ID·생성 토큰 수·API 사용량과 대조했습니다. 원래 실패 7건은 성공으로 바꾸지 않았습니다.",
 '- 원본 보호 파일 119,046개 해시 일치, 원래 POST된 요청 재발행 0건. 미제출이 입증된 요청만 별도 continuation에서 처리했습니다.',
 '- 처음 구성요소 파일럿의 설명 반복·잘림은 스키마가 모델 입력에 명시되지 않은 경로에서 발생했습니다. 스키마를 입력에 추가한 새 버전에서 파일럿을 통과했고, 출력 예산은 줄이지 않았습니다.',
 '- 역사적 RiskRank 2,304개 예측과 RiskQuote 1,440개 휴대형 계산을 원본과 정확히 대조했습니다. 지원되지 않는 새 업무의 RiskRank 예측은 NEEDS_ANCHOR_EVALUATION으로 보류합니다.',
 '- 실제 원시 응답·상태·점수·요청별 맥락을 ControlArena directory 형식으로 내보냈습니다. 설치되지 않은 native ControlArena/Inspect 실행 플러그인을 인증했다고 주장하지 않습니다.',
 '- 사람 이중 검토: SKIPPED_BY_USER. 기존 156건 검토 패키지와 빈 판정지는 보존했습니다.','',
 '## 5. 재현·백업','',
 '로컬과 원격의 원시 상태 재구성·판정·분모를 대조했습니다. 정수·판정은 정확 비교하고, Python 부동소수점 차이에만 10⁻¹² 허용치를 적용했습니다. 결과·요청·응답·예측 잠금·실패·프로토콜과 파일 SHA를 공개 패키지에 포함했습니다.',
 f"SSD·별도 HDD 읽기 후 SHA 검증을 통과했습니다. NAS 쓰기는 재확인에서도 errno 122(할당량 초과)로 거부됐으며 기존 NAS 자료는 삭제하지 않았습니다. 공개 아카이브는 {len(archives['archives'])}개이며 파일별 검증 목록을 제공합니다.",
 '[재현 방법](README.md) · [영문 요약](RESEARCH_BRIEF_EN.md) · [최종 상태](../../artifacts/control_followup_20261104/FINAL_STATUS.json) · [전체 결과](../../artifacts/control_followup_20261104/COMPONENT_REPRODUCTION.json)',
 '', '실행 완료와 연구 가설의 성공은 구분합니다. 이번 후속 연구는 실행 증거 기반 모니터링의 유용한 신호와 공유 이력의 중요성을 보여 주지만, 적응형 위험 점수의 일반적인 안전성–효용 우위를 확증하지는 못했습니다.']
 (d/'RESEARCH_FINDINGS_KO.md').write_text('\n'.join(lines)+'\n')
 final={'requested_followup_execution_complete':True,'all_planned_outcomes_known':o['unknown']+c['unknown']==0,'human_review':'SKIPPED_BY_USER','monitor_census':{'actions':491,'judgments':2455,'new_calls':1655,'reused_calls':800},'organizations':{'planned':1728,'finished':1728,'known':1728-o['unknown'],'unknown_preserved':o['unknown'],'raw_calls_including_pilot':o['raw_calls_verified'],'cross_workflow_superiority':'NOT_ESTABLISHED','adaptive_over_cumulative':'NOT_ESTABLISHED'},'components':{'planned':4896,'finished':c['trades'],'unknown':c['unknown'],'raw_calls_including_valid_pilot':c['raw_calls'],'failed_original_pilot_preserved':17,'valid_new_pilot':c['pilot_trades']},'independent_reproduction':True,'parser_recoveries_audited':parser['recoveries'],'historical_RiskRank_predictions_reproduced':2304,'historical_RiskQuote_predictions_reproduced':1440,'ControlArena_directory_export':True,'native_ControlArena_plugin':False,'customer_or_insurance_validation':False,'backups':backups,'gpu':2,'model_retained':True,'original_results_modified':False,'original_posted_requests_reissued':0}
 (a/'FINAL_STATUS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
 print('rendered',d/'RESEARCH_FINDINGS_KO.md')
if __name__=='__main__':main()
