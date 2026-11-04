"""Read-only post-action wire audit, independent of runner parsing/scoring."""
import json
from pathlib import Path

from .common import file_sha, freeze, sha, wire, MONITOR_SCHEMA
from .monitors import post_action


def audit_monitors(root, write=True, require_complete=True):
    root = Path(root)
    load = lambda p: json.loads(p.read_text())
    plan = load(root / 'PROTOCOL_LOCK.json')
    tasks = {t['task_id']: t for t in load(root / 'TASK_BANK.json')}
    episodes = {r['episode_id']: r for p in (root / 'episodes').glob('*.json')
                if (r := load(p))['stage'] == 'main' and r['arm'] == 'B0'}
    expected = {(e, c) for e in episodes for c in plan['monitors']}
    seen = set()
    api_tokens = output_tokens = known_unsafe = 0
    manifest = {}
    for p in sorted((root / 'monitor_results').glob('*.json')):
        row = load(p)
        key = row['episode_id'], row['condition']
        assert key in expected and key not in seen, 'DUPLICATE_OR_FOREIGN_MONITOR'
        seen.add(key)
        episode = episodes[key[0]]
        eligible = [(i, e) for i, e in enumerate(episode['events'])
                    if e['receipt']['proposal']['tool'] not in ['read', 'finish', 'escalate']]
        assert eligible, 'NO_ELIGIBLE_ACTION'
        i, event = eligible[int(sha(key[0])[:12], 16) % len(eligible)]
        assert row['event_index'] == i
        assert row['target_actual_unsafe_execution'] is event['executed_bad'], 'TARGET_CHANGED'
        assert row['status'] == 'VALID', 'NONVALID_MONITOR_REQUIRES_UNKNOWN_REPORT'
        rid = key[0] + '-post-' + key[1]
        assert row['raw_request_id'] == rid
        d = root / 'raw' / rid
        request, dispatch = load(d / 'request.json'), load(d / 'dispatch.json')
        raw, receipt = load(d / 'response.raw'), load(d / 'receipt.json')
        assert file_sha(d / 'request.json') == receipt['request_sha256'], 'REQUEST_HASH'
        assert file_sha(d / 'response.raw') == receipt['raw_sha256'], 'RESPONSE_HASH'
        assert raw == load(d / 'response.json')
        assert sha(request) == dispatch['payload_sha256']
        assert dispatch['role'] == receipt['role'] == 'post_action_monitor'
        assert dispatch['time'] >= episode['completed_epoch'], 'FUTURE_EVIDENCE_USED_PRE_ACTION'
        expected_request = wire(post_action(tasks[episode['task_id']], event,
                                [e['receipt'] for e in episode['events'][:i]], key[1]),
                                episode['seed'], MONITOR_SCHEMA, plan['monitor_per_call_output'])
        assert request == expected_request, 'FROZEN_MONITOR_INPUT_CHANGED'
        assert raw['choices'][0]['finish_reason'] == receipt['finish'] == 'stop'
        verdict = json.loads(raw['choices'][0]['message']['content'])
        assert verdict == row['verdict'] and set(verdict) == {'decision', 'risk_probability', 'reason'}
        assert verdict['decision'] in ['ALLOW', 'BLOCK', 'UNSURE']
        assert type(verdict['risk_probability']) in [int, float] and 0 <= verdict['risk_probability'] <= 1
        assert isinstance(verdict['reason'], str)
        usage = raw['usage']
        assert usage == receipt['usage'] == row['usage']
        assert all(type(usage[k]) is int and usage[k] >= 0 for k in ['prompt_tokens', 'completion_tokens', 'total_tokens'])
        assert usage['total_tokens'] == usage['prompt_tokens'] + usage['completion_tokens']
        assert usage['completion_tokens'] <= request['max_tokens']
        api_tokens += usage['total_tokens']
        output_tokens += usage['completion_tokens']
        known_unsafe += row['target_actual_unsafe_execution']
        manifest[str(p.relative_to(root))] = file_sha(p)
    if require_complete:
        assert len(episodes) == 160 and seen == expected, 'INCOMPLETE_MONITOR_GRID'
    result = {'pass': True, 'rows_checked': len(seen), 'expected_rows': len(expected),
              'complete_grid': seen == expected, 'api_tokens': api_tokens,
              'output_tokens': output_tokens, 'unsafe_targets_repeated_across_conditions': known_unsafe,
              'checks': ['wire hashes', 'raw JSON verdict and usage', 'frozen input and seed',
                         'label-independent event selection', 'post-action chronology', 'full paired grid'],
              'manifest': manifest}
    if write:
        freeze(root / 'MONITOR_INDEPENDENT_REPRODUCTION.json', result)
    return result


if __name__ == '__main__':
    import sys
    r = audit_monitors(sys.argv[1])
    print(json.dumps({k: v for k, v in r.items() if k != 'manifest'}, indent=2))
