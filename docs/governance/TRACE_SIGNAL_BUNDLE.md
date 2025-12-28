{
  "trace_bundle_version": "1.0",
  "bundle_id": "trace_2025_01_001",

  "source": {
    "engine": "StegTrace",
    "engine_version": "0.1",
    "repo": "StegTrace",
    "run_id": "trace_run_abc123"
  },

  "subject": {
    "type": "artifact | claim | document | signal_set",
    "ref": "stable identifier or hash"
  },

  "signals": [
    {
      "signal_id": "handwriting_similarity",
      "description": "Handwriting similarity score between samples",
      "confidence": 0.72,
      "confidence_label": "medium",
      "method": "feature clustering + cross-sample distance",
      "limitations": [
        "sample quality variance",
        "non-exclusive authorship possibility"
      ]
    }
  ],

  "aggregate_assessment": {
    "confidence_score": 0.68,
    "confidence_label": "medium",
    "interpretation": "Evidence suggests similarity but is not conclusive"
  },

  "bounds": {
    "not_a_fact": true,
    "not_identity_verification": true,
    "not_legal_conclusion": true
  },

  "issued_at": 1766530000
}
