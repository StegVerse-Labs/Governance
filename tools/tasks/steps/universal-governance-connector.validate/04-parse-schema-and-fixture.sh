python - <<'PY'
import json
from pathlib import Path
for p in [
    Path("schemas/universal_governance_connector_profile.schema.json"),
    Path("fixtures/universal-governance-connector/profile.example.json"),
    Path("schemas/universal_governance_connector_request.schema.json"),
    Path("fixtures/universal-governance-connector/request.example.json"),
    Path("schemas/universal_governance_connector_registry.schema.json"),
    Path("specs/universal-governance-connector-profiles.v1.json"),
    Path("schemas/universal_governance_external_adapter.schema.json"),
    Path("fixtures/universal-governance-connector/external-adapter.example.json"),
]:
    json.loads(p.read_text())
    print("JSON_OK", p)
PY
