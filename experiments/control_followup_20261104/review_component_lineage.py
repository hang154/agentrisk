"""Supplement the preserved 24-rule analysis with original 12-source clustering."""
import collections,json,pathlib
from experiments.control_study_202611.common import file_sha
from .audit_components import summarize
from .riskquote_ablation import TEST

def review(root):
 root=pathlib.Path(root)
 mapping_file=pathlib.Path(__file__).parent/'data/RISKQUOTE_SHARED_LINEAGE.json'
 mapping=json.loads(mapping_file.read_text())['groups']
 assert set(mapping)==set(TEST) and len(set(mapping.values()))==12
 assert set(collections.Counter(mapping.values()).values())=={2}
 rows=[json.loads(p.read_text()) for p in sorted((root/'trades').glob('*.json'))]
 rows=[r for r in rows if not r['pilot']]
 assert len(rows)==4896
 return {'analysis_revision':'component-analysis-v2-original-shared-lineage',
         'post_hoc':True,'new_model_calls':0,'raw_outcomes_changed':False,
         'preregistered_24rule_analysis_preserved':'COMPONENT_REPRODUCTION.json',
         'lineage_mapping_sha256':file_sha(mapping_file),'trades':len(rows),
         'analysis':summarize(rows,cluster_map=mapping)}
