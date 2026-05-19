import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def validate_json_file(path: Path) -> None:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"Invalid JSON: {path}: {exc}") from exc


def main() -> None:
    for path in list((ROOT / "schemas").rglob("*.json")) + list((ROOT / "prompts").rglob("*.json")):
        validate_json_file(path)

    schema = json.loads(
        (ROOT / "schemas/responses/morning_briefing_response.schema.json").read_text()
    )
    example = json.loads((ROOT / "prompts/morning_briefing/output_example.json").read_text())
    errors = list(Draft202012Validator(schema).iter_errors(example))
    if errors:
        for error in errors:
            print(f"{list(error.path)}: {error.message}")
        raise SystemExit(1)

    print("All schemas and examples valid.")


if __name__ == "__main__":
    main()
