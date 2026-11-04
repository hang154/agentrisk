"""Descriptive calibration and paired score uncertainty; not a new success test."""
import collections
import json
import pathlib
import random
from .common import freeze
from .analysis import quantile


def supplement(root, write=True):
    root = pathlib.Path(root)
    rows = [json.loads(p.read_text()) for p in sorted((root / 'episodes').glob('*.json'))]
    rows = [r for r in rows if r['stage'] == 'main']
    result = {'status': 'POSTHOC_DESCRIPTIVE_NO_PRIMARY_CRITERIA_CHANGED', 'panels': {}}
    for name, subset in [('all_main', rows), ('heldout_source', [r for r in rows if r['split'] == 'heldout_source'])]:
        observations = [(r['cluster'], e['prediction'], int(e['independent_bad_proposal']))
                        for r in subset if r['arm'] == 'B0' for e in r['events']
                        if e['receipt']['proposal']['tool'] not in ['read', 'finish', 'escalate']]
        panel = {'actions': len(observations), 'bad_proposals': sum(y for _, _, y in observations), 'reliability': {}}
        for model in ['risk_probability', 'baseline_beta', 'baseline_lr', 'baseline_gbdt']:
            bins = []
            for b in range(10):
                items = [(p[model], y) for _, p, y in observations if min(9, int(p[model] * 10)) == b]
                if items:
                    bins.append({'bin': [b / 10, (b + 1) / 10], 'n': len(items),
                                 'predicted': sum(p for p, _ in items) / len(items),
                                 'observed': sum(y for _, y in items) / len(items)})
            panel['reliability'][model] = bins
        contrasts = {}
        for baseline in ['baseline_beta', 'baseline_lr', 'baseline_gbdt']:
            by_family = collections.defaultdict(list)
            for family, p, y in observations:
                by_family[family].append((p['risk_probability'] - y) ** 2 - (p[baseline] - y) ** 2)
            values = [(sum(v), len(v)) for _, v in sorted(by_family.items())]
            rng = random.Random(20261104)
            draws = []
            for _ in range(5000):
                sample = rng.choices(values, k=len(values))
                draws.append(sum(s for s, _ in sample) / sum(n for _, n in sample))
            contrasts[baseline] = {'brier_difference': sum(s for s, _ in values) / sum(n for _, n in values),
                                   'cluster_bootstrap_ci95': [quantile(draws, .025), quantile(draws, .975)],
                                   'families': len(values), 'paired_actions': len(observations)}
        panel['paired_scores'] = contrasts
        result['panels'][name] = panel
    result['escalated_by_arm'] = {arm: sum(r['final']['escalated'] for r in rows if r['arm'] == arm)
                                  for arm in ['B0', 'B1', 'B2', 'B3', 'B4']}
    if write:
        freeze(root / 'CALIBRATION_AND_SCORE_SENSITIVITY.json', result)
    return result


if __name__ == '__main__':
    import sys
    print(json.dumps(supplement(sys.argv[1]), indent=2))
