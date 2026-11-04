import json,pathlib
from .common import freeze,file_sha

def report(root):
 root=pathlib.Path(root);r=json.loads((root/'RESULTS.json').read_text());audit=json.loads((root/'INDEPENDENT_REPRODUCTION.json').read_text())
 lines=['# AgentRisk Control Study V1 — 연구 결과','', '신규 합성 업무의 실제 모델 실행 결과입니다. 과거 연구의 결과·원장·판정은 변경하지 않았습니다.','',
 '| 정책 | 완료/계획 | 판정 가능 | 정상 업무 완료 | 위험 상태 변경 | 합성 직접손실 | API 토큰 |','|---|---:|---:|---:|---:|---:|---:|']
 for arm,s in r['summary'].items():lines.append(f"| {arm} | {s['completed']}/{s['planned']} | {s['known']} | {s['benign_complete']}/{s['benign_known']} | {s['unsafe_episodes']}/{s['known']} | {s['synthetic_direct_loss']} | {s['api_tokens']:,} |")
 lines+=['','B0 정적 게이트, B1 별도 역할 LLM 모니터, B2 단순 누적·중복 제한, B3 동결 Beta 위험 통제, B4 실제 실행 결과로 갱신하는 Beta 위험 통제.','',
 '## 사전 고정 비교','']
 for b in ['B2','B0']:
  c=r['paired'][b];lines.append(f"- B4−{b}: 위험 효과 {c['risk'].get('effect')}, 95% 구간 {c['risk'].get('ci95')}; 정상 업무 효용 효과 {c['benign_utility'].get('effect')}, 95% 구간 {c['benign_utility'].get('ci95')}. 안전성·효용 동시 성공 기준: {c['safety_utility_success']}.")
 lines+=['','## 실행 증거별 사후 모니터','', '| 조건 | 유효/제출 | 보류 | TP/FN/FP/TN | Brier |','|---|---:|---:|---|---:|']
 for c,s in r['monitors'].items():lines.append(f"| {c} | {s['valid']}/{s['rows']} | {s['abstained']} | {s['tp']}/{s['fn']}/{s['fp']}/{s['tn']} | {s['brier_all_valid']} |")
 lines+=['','이 비교는 이미 실행된 행동의 탐지입니다. 현재 행동의 미래 상태를 차단 판단에 넣지 않았습니다. M3는 같은 업무의 앞선 이력이며 장기 다중 세션 효과는 별도 후속 연구입니다.','',
 '## 예측 비교','', '| 예측기 | 공통 B0 행동 수 | Brier | Log loss |','|---|---:|---:|---:|']
 for k,s in r['forecasts'].items():lines.append(f"| {k} | {s['n']} | {s['brier']} | {s['log_loss']} |")
 lines+=['','베이스라인은 동일 개발 자료·관측 가능한 특징을 사용했습니다. 대상은 제안의 계약 위반 확률이며, 미관측 모델의 실제 고객 사고율을 뜻하지 않습니다. 기존 RiskRank의 이질적인 특징을 새 업무로 옮기는 어댑터는 검증하지 않았으므로 기존 모델보다 우월하다고 주장하지 않습니다.','',
 '## 재현 및 남은 범위','',f"별도 상태·원장 재구성 {audit['episodes_checked']}건, 원시 API 호출 {audit['api_calls_checked']}건 검증 PASS. 독립성은 10개 의미적 업무군으로 보수적으로 처리했습니다. 800번을 독립 표본 800개로 세지 않았습니다.",
 '','사람 블라인드 이중 검토, 적응형 공격자·여러 세션·다중 에이전트 조직 실험, RiskQuote 구성요소 분해는 이 최소 V1의 완료 항목이 아닙니다. 과거 Voice 불일치 원인은 별도 감사 표에 연결했습니다.','',
 '긍정적 결과 여부와 실행 완료를 구분합니다. 이 연구로 고객 권한 승인·원화 보험료·사람 판정을 생성하지 않았습니다.']
 (root/'RESEARCH_FINDINGS_KO.md').write_text('\n'.join(lines)+'\n')
 complete=r['rows']==800 and all(s['pending']==0 for s in r['summary'].values())
 status={'implementation_tested':True,'planned_main_episodes':800,'recorded_main_episodes':r['rows'],'main_execution_complete':complete,'independent_reproduction_pass':audit['passed'],'human_review_complete':False,'entire_research_agenda_complete':False,
 'simultaneous_safety_utility_improvement':any(r['paired'][b]['safety_utility_success'] for b in ['B2','B0']),'unknown':sum(s['unknown'] for s in r['summary'].values()),'gpu_target':2,'other_services_changed':False}
 freeze(root/'FINAL_STATUS.json',status)
 files={str(p.relative_to(root)):file_sha(p) for p in sorted(root.rglob('*')) if p.is_file() and (p.suffix in ['.json','.jsonl','.csv','.md','.raw'] or p.name=='post_started') and not any(k in p.parts for k in ['cache','__pycache__']) and p.name!='SHA256_MANIFEST.json'}
 freeze(root/'SHA256_MANIFEST.json',files)
 return status
if __name__=='__main__':
 import sys;print(json.dumps(report(sys.argv[1]),indent=2))
