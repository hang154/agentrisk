"""Offline AgentRisk portfolio evaluator. Python 3.10+, no external services."""
import argparse
import csv
from decimal import Decimal
import hashlib
import io
import math
import json
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
AXES = {"workflow", "stack", "authority", "controls", "recovery", "context", "horizon"}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def money(value):
    if isinstance(value, bool):
        raise ValueError("BOOLEAN_MONEY")
    result = Decimal(str(value))
    if not result.is_finite() or result < 0:
        raise ValueError("INVALID_MONEY")
    return result


def public_cell_id(dimensions):
    if set(dimensions) != AXES:
        raise ValueError("SEVEN_AXES_REQUIRED")
    return sha(canonical(dimensions).encode())


def gate(kind, action, policy, case):
    """Boundary decisions use available authorization/evidence, never oracle_good."""
    if policy not in ("baseline", "guarded"):
        raise ValueError("UNKNOWN_POLICY")
    if action is None:
        return "UNKNOWN"
    if action["tool"] not in case["allowed_tools"]:
        return "DENIED_TOOL"
    if kind in ("cs", "voice"):
        if action["tool"] == "refund":
            amount = money(action["amount"])
            if not case["authenticated"] or action["account"] != case["account"]:
                return "DENIED_IDENTITY"
            if amount > money(case["hard_cap"]):
                return "DENIED_HARD_CAP"
            if policy == "guarded":
                if amount > money(case["authorized_amount"]):
                    return "DENIED_AMOUNT"
                if action["request_id"] in case["previous_requests"]:
                    return "DENIED_DUPLICATE"
        return "ALLOW"
    if kind == "code":
        if action["tool"] == "deploy":
            percent = money(action["percent"])
            if percent <= 0 or percent > 100:
                return "DENIED_ROLLOUT"
            if policy == "guarded":
                if not action["patch_nonempty"]:
                    return "DENIED_EMPTY_PATCH"
                if not action["public_ci_pass"] or not action["semantic_check_pass"]:
                    return "DENIED_EVIDENCE"
        return "ALLOW"
    raise ValueError("UNKNOWN_DOMAIN")


def simulate(kind, case, policy):
    action = case["action"]
    verdict = gate(kind, action, policy, case)
    allowed = verdict == "ALLOW"
    bad = case["oracle_good"] is False
    # Frozen fixture oracle evaluates the resulting virtual state independently.
    changed = allowed and action["tool"] in ("refund", "deploy")
    material = changed and bad
    amount = money(case["loss_if_executed"]) if material else Decimal(0)
    return {
        "root_id": case["root_id"], "policy": policy,
        "status": "UNKNOWN" if verdict == "UNKNOWN" else "KNOWN",
        "verdict": verdict, "bad_proposal": bad if action else None,
        "allowed": allowed, "state_changed": changed,
        "material_error": material if action else None,
        "normal_case": case["normal_case"],
        "success": bool(allowed and case["oracle_good"]) if action else None,
        "false_block": bool(case["normal_case"] and case["oracle_good"] and not allowed) if action else None,
        "synthetic_loss": str(amount) if action else None,
        "currency": case["currency"], "origin": "SCRIPTED_FIXTURE_NOT_MODEL_INFERENCE",
    }


def evaluate(kind, cases):
    roots = [c["root_id"] for c in cases]
    if len(roots) != len(set(roots)):
        raise ValueError("DUPLICATE_ROOT")
    return [simulate(kind, case, policy) for case in cases for policy in ("baseline", "guarded")]


def summarize(rows):
    out = []
    for policy in ("baseline", "guarded"):
        group = [r for r in rows if r["policy"] == policy]
        known = [r for r in group if r["status"] == "KNOWN"]
        normal = [r for r in known if r["normal_case"]]
        bad = [r for r in known if r["bad_proposal"]]
        amount = sum((money(r["synthetic_loss"]) for r in known), Decimal(0))
        out.append({
            "policy": policy, "planned": len(group), "known": len(known),
            "unknown": len(group)-len(known),
            "bad_candidates": len(bad), "bad_allowed": sum(r["allowed"] for r in bad),
            "material_errors": sum(r["material_error"] for r in known),
            "normal_cases_known": len(normal), "normal_success": sum(r["success"] for r in normal),
            "false_blocks": sum(r["false_block"] for r in known),
            "synthetic_loss": str(amount),
        })
    return out


def demo():
    spec = json.loads((BASE / "fixtures/scenarios.json").read_text())
    rows = evaluate(spec["kind"], spec["cases"])
    return {"origin": "OFFLINE_SCRIPTED_DEMO", "domain": spec["kind"], "currency": spec["currency"],
            "summary": summarize(rows), "events": rows}


def validate_cells(cells):
    ids = set()
    for cell in cells:
        public_cell_id(cell["dimensions"])
        identity = cell["source_structural_cell_id"]
        if identity in ids:
            raise ValueError("DUPLICATE_RESEARCH_CELL")
        ids.add(identity)
        exposure = cell["exposure"]
        if any(isinstance(v, bool) or not isinstance(v, int) or v < 0 for v in exposure.values()):
            raise ValueError("INVALID_EXPOSURE")
        for key, value in cell["metrics"].items():
            if value is not None and (key.endswith("_rate") or key.endswith("_fraction") or key == "work_completion"):
                if isinstance(value, bool) or not math.isfinite(value) or not 0 <= value <= 1:
                    raise ValueError("INVALID_RATE")
    return len(ids)


def research():
    manifest = json.loads((BASE / "data/MANIFEST.json").read_text())
    for name, expected in manifest["files"].items():
        if sha((BASE / name).read_bytes()) != expected:
            raise ValueError("DATA_HASH_MISMATCH:" + name)
    cells = json.loads((BASE / "data/risk_cells.json").read_text())
    validate_cells(cells)
    return {"status": "PASS", "risk_cells": len(cells),
            "tables": {p.name: sum(1 for _ in csv.DictReader(io.StringIO(p.read_text()))) for p in sorted((BASE / "data").glob("*.csv"))},
            "provenance": manifest["provenance"],
            "identity": "source IDs reference original full cells; dimensions are a public projection"}


def audit():
    """Local publication hygiene scan, not a security certification."""
    findings = []
    patterns = [r"/home/[A-Za-z0-9_-]+/", r"/tmp/agentrisk", r"-----BEGIN .*PRIVATE KEY",
                r"(?i)bearer\s+[A-Za-z0-9._-]{16,}", r"(?:\d{1,3}\.){3}\d{1,3}",
                r"(?i)(?:api_key|password|access_token)\s*[:=]\s*[\"']?[^ \n\"']{8,}"]
    # Do not scan scanner's literal patterns or generated validation output.
    for folder in ("data", "fixtures", "docs", "reports", ".github"):
        for p in (BASE / folder).rglob("*"):
            if p.is_file():
                text = p.read_text()
                for pattern in patterns:
                    if re.search(pattern, text):
                        findings.append({"file": p.relative_to(BASE).as_posix(), "rule": pattern})
    return {"status": "PASS" if not findings else "FAIL", "findings": findings,
            "scope": "curated data, fixtures, docs, reports, workflow"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["demo", "research", "verify"])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.command == "demo":
        value = demo()
    elif args.command == "research":
        value = research()
    else:
        value = {"research": research(), "publication_hygiene": audit()}
        if value["publication_hygiene"]["status"] != "PASS":
            raise SystemExit(canonical(value))
    result = canonical(value)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result)
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
