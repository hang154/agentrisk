import copy
from decimal import Decimal
import json
from pathlib import Path
import unittest
import evaluation as e

class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.spec=json.loads((e.BASE/"fixtures/scenarios.json").read_text())
    def test_end_to_end(self):
        result=e.demo()
        self.assertEqual(len(result["events"]),len(self.spec["cases"])*2)
        self.assertEqual(result["origin"],"OFFLINE_SCRIPTED_DEMO")
    def test_research_linkage(self):
        self.assertEqual(e.research()["status"],"PASS")
    def test_publication_scan(self):
        self.assertEqual(e.audit()["status"],"PASS")
    def test_repeatable(self):
        self.assertEqual(e.canonical(e.demo()),e.canonical(e.demo()))
    def test_duplicate_roots(self):
        c=self.spec["cases"][0]
        with self.assertRaises(ValueError): e.evaluate(self.spec["kind"],[c,c])
    def test_unknown_not_pass_or_zero(self):
        row=next(r for r in e.demo()["events"] if r["status"]=="UNKNOWN")
        self.assertIsNone(row["success"])
        self.assertIsNone(row["synthetic_loss"])
    def test_missing_outcome_reported(self):
        for row in e.demo()["summary"]:
            self.assertGreater(row["unknown"],0)
    def test_guarded_reduces_scripted_errors(self):
        baseline,guarded=e.demo()["summary"]
        self.assertGreater(baseline["material_errors"],guarded["material_errors"])
    def test_normal_utility_is_retained(self):
        baseline,guarded=e.demo()["summary"]
        self.assertEqual(baseline["normal_success"],guarded["normal_success"])
        self.assertGreater(guarded["normal_success"],0)
    def test_oracle_does_not_drive_gate(self):
        c=copy.deepcopy(self.spec["cases"][0])
        before=e.gate(self.spec["kind"],c["action"],"guarded",c)
        c["oracle_good"]=not c["oracle_good"]
        self.assertEqual(before,e.gate(self.spec["kind"],c["action"],"guarded",c))
    def test_unknown_policy(self):
        c=self.spec["cases"][0]
        with self.assertRaises(ValueError):e.gate(self.spec["kind"],c["action"],"typo",c)
    def test_negative_invalid_money(self):
        for x in [-1,"NaN","Infinity",True]:
            with self.assertRaises(ValueError):e.money(x)
    def test_seven_axes(self):
        with self.assertRaises(ValueError):e.public_cell_id({"workflow":"refund"})
    def test_authority_changes_identity(self):
        axes=json.loads((e.BASE/"data/risk_cells.json").read_text())[0]["dimensions"]
        other=copy.deepcopy(axes);other["authority"]={"scope":"changed"}
        self.assertNotEqual(e.public_cell_id(axes),e.public_cell_id(other))
    def test_malformed_action_rejected(self):
        c=copy.deepcopy(self.spec["cases"][0])
        with self.assertRaises(KeyError):e.gate(self.spec["kind"],{},"guarded",c)
    def test_state_change_is_not_proposal(self):
        rows=e.demo()["events"]
        denied=next(r for r in rows if r["verdict"].startswith("DENIED"))
        self.assertFalse(denied["state_changed"])
        self.assertFalse(denied["material_error"])

    def test_duplicate_research_cell_rejected(self):
        cell=json.loads((e.BASE/"data/risk_cells.json").read_text())[0]
        with self.assertRaises(ValueError): e.validate_cells([cell,cell])
    def test_negative_exposure_rejected(self):
        cell=json.loads((e.BASE/"data/risk_cells.json").read_text())[0]
        cell["exposure"]={"known":-1}
        with self.assertRaises(ValueError):e.validate_cells([cell])
    def test_boolean_exposure_rejected(self):
        cell=json.loads((e.BASE/"data/risk_cells.json").read_text())[0]
        cell["exposure"]={"known":True}
        with self.assertRaises(ValueError):e.validate_cells([cell])
    def test_invalid_probability_rejected(self):
        cell=json.loads((e.BASE/"data/risk_cells.json").read_text())[0]
        cell["metrics"]["success_rate"]=1.5
        with self.assertRaises(ValueError):e.validate_cells([cell])
    def test_deny_unlisted_tool(self):
        c=copy.deepcopy(self.spec["cases"][0])
        self.assertEqual(e.gate(self.spec["kind"],{"tool":"not_permitted"},"guarded",c),"DENIED_TOOL")
    def test_zero_loss_on_blocked_action(self):
        rows=e.demo()["events"]
        denied=next(r for r in rows if r["verdict"].startswith("DENIED"))
        self.assertEqual(denied["synthetic_loss"],"0")

if __name__=="__main__":
    unittest.main()
