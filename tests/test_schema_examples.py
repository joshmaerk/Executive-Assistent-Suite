import json
from pathlib import Path

from ea_assistant.services.schema_validator import validate_json_schema

ROOT = Path(__file__).resolve().parents[1]


def test_output_example_matches_schema():
    instance = json.loads((ROOT / "prompts/morning_briefing/output_example.json").read_text())
    errors = validate_json_schema(
        instance, "schemas/responses/morning_briefing_response.schema.json"
    )
    assert errors == []
