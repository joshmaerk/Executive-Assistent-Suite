import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    schema = json.loads((ROOT / "schemas/responses/morning_briefing_response.schema.json").read_text())
    example = json.loads((ROOT / "prompts/morning_briefing/output_example.json").read_text())
    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(example))
    if errors:
        for error in errors:
            print(error.message)
        raise SystemExit(1)
    print("schema eval ok")


if __name__ == "__main__":
    main()
