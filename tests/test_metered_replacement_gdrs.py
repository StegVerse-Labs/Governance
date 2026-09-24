"""Negative contract tests for synthetic metered replacement GDRs."""
import copy
import json
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_metered_replacement_gdrs as contract

class MeteredGDRContractTests(unittest.TestCase):
    def setUp(self):
        self.records={path:json.loads((ROOT/path).read_text()) for path in contract.FIXTURES}
    def check(self,record,expected):
        with tempfile.TemporaryDirectory() as d:
            path=pathlib.Path(d)/"fixture.json"
            path.write_text(json.dumps(record))
            return contract.validate_fixture(str(path),expected)
    def test_original_fixtures(self):
        for path,expected in contract.FIXTURES.items():
            self.assertEqual([],self.check(self.records[path],expected))
    def test_selection_cannot_authorize_cancellation(self):
        path=next(k for k,v in contract.FIXTURES.items() if v["scope"]=="REPLACEMENT_DESIGN_ONLY")
        record=copy.deepcopy(self.records[path])
        record["execution_boundary"]["cancellation_authority"]=True
        self.assertTrue(self.check(record,contract.FIXTURES[path]))
    def test_selection_prohibitions_immutable(self):
        path=next(k for k,v in contract.FIXTURES.items() if v["scope"]=="REPLACEMENT_DESIGN_ONLY")
        record=copy.deepcopy(self.records[path])
        record["replacement_boundary"]["prohibited_actions"].remove("retire_provider")
        self.assertTrue(self.check(record,contract.FIXTURES[path]))
    def test_retirement_missing_gate_denied(self):
        path=next(k for k,v in contract.FIXTURES.items() if v["scope"]=="PROVIDER_RETIREMENT")
        record=copy.deepcopy(self.records[path])
        record["retirement_boundary"]["missing_evidence"]=[]
        self.assertTrue(self.check(record,contract.FIXTURES[path]))
    def test_retirement_receipt_not_minted(self):
        path=next(k for k,v in contract.FIXTURES.items() if v["scope"]=="PROVIDER_RETIREMENT")
        record=copy.deepcopy(self.records[path])
        record["runtime_expectation"]["continuity_receipt_minted"]=True
        self.assertTrue(self.check(record,contract.FIXTURES[path]))
    def test_synthetic_fixture_classification(self):
        for path,record in self.records.items():
            self.assertEqual("SYNTHETIC_NON_AUTHORITATIVE",record["fixture_classification"])
            self.assertEqual("SYNTHETIC_TEST_FIXTURE",record["evaluated_inputs"]["source"])
if __name__=="__main__":
    unittest.main()
