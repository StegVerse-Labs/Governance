"""bootstrap-stegtrace reads no credential and fails closed toward the TV/TVC broker."""
from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SIX = ("failure_code", "failed_predicate", "required_evidence_or_repair", "retry_entrypoint",
       "owning_existing_goal", "next_attempt")


class TestBootstrapStegTrace(unittest.TestCase):
    def run_script(self, extra_env):
        with tempfile.TemporaryDirectory() as home:
            env = {"PATH": os.environ.get("PATH", ""), **extra_env}
            proc = subprocess.run([sys.executable, str(ROOT / "scripts/bootstrap_stegtrace.py")], cwd=home,
                                  env=env, text=True, capture_output=True)
            receipt = json.loads((Path(home) / "evidence/stegtrace-bootstrap/latest.json").read_text())
        return proc, receipt

    def test_fails_closed_with_the_six_fields_and_a_broker_request(self):
        proc, receipt = self.run_script({})
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(receipt["disposition"], "FAIL_CLOSED")
        for field in SIX:
            self.assertTrue(receipt.get(field), field)
        self.assertEqual(receipt["failed_predicate"], "GITHUB_MUTATION_CREDENTIAL_IS_TV_TVC_WARRANTED")
        ops = [op["operation_class"] for op in receipt["broker_request"]["operations"]]
        self.assertEqual(ops, ["APPLY_BOUNDED_FILE_SET", "OPEN_PULL_REQUEST"])
        self.assertEqual(receipt["lowest_mode"], "E0")
        self.assertNotIn("observed_at", receipt)

    def test_a_present_token_changes_nothing(self):
        _, without = self.run_script({})
        _, with_token = self.run_script({"GH_TOKEN": "not-a-real-token-fixture"})
        self.assertEqual(without, with_token)

    def test_workflow_and_script_read_no_secret(self):
        workflow = (ROOT / ".github/workflows/bootstrap-stegtrace.yml").read_text(encoding="utf-8")
        self.assertNotIn("secrets.", workflow)
        self.assertNotIn("GH_STEGVERSE_BRIDGE_PAT", workflow)
        script = (ROOT / "scripts/bootstrap_stegtrace.py").read_text(encoding="utf-8")
        code = script[script.index("BROKER_ENTRYPOINT ="):]
        for banned in ("GH_TOKEN", "os.environ", "subprocess", "time.time"):
            self.assertNotIn(banned, code)


if __name__ == "__main__":
    unittest.main()
