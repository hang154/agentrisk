"""Validate the complete public candidate; run without installing anything."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import evaluation as e

BASE = Path(__file__).resolve().parent


def run():
    tests = subprocess.run([sys.executable, "-W", "error::ResourceWarning", "-m", "unittest", "-v"],
                           cwd=BASE, text=True, capture_output=True)
    if tests.returncode:
        raise RuntimeError(tests.stdout + tests.stderr)
    count = int(re.search(r"Ran (\d+) tests", tests.stderr).group(1))
    checks = {"regression_tests": count, "test_pass": True, "research": e.research(),
              "hygiene": e.audit()}
    assert checks["hygiene"]["status"] == "PASS"
    frozen = (BASE / "reports/DEMO_OUTPUT.json").read_bytes()
    for _ in range(2):
        raw = subprocess.check_output([sys.executable, "evaluation.py", "demo"], cwd=BASE)
        assert raw == frozen, "DEMO_NOT_BYTE_IDENTICAL"
    checks["byte_identical_demo_rebuilds"] = 2
    broken = []
    for path in BASE.rglob("*.md"):
        if ".git" in path.parts:
            continue
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text()):
            if "://" not in target and not target.startswith("#"):
                if not (path.parent / target.split("#")[0]).is_file():
                    broken.append({"file": path.relative_to(BASE).as_posix(), "link": target})
    assert not broken, broken
    checks["relative_markdown_links"] = "PASS"
    checks["demo_sha256"] = hashlib.sha256(frozen).hexdigest()
    checks["videos_created"] = 0
    checks["remote_state_not_checked_by_offline_verifier"] = True
    checks["status"] = "PASS"
    return checks


if __name__ == "__main__":
    result = run()
    (BASE / "VALIDATION.json").write_text(e.canonical(result))
    print(e.canonical(result), end="")
