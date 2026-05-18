from pathlib import Path
import json
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]


def load_schema(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def validate_json_schema(instance: dict, schema_path: str) -> list[str]:
    schema = load_schema(schema_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
    return [f"{'/'.join(map(str, error.path))}: {error.message}" for error in errors]
