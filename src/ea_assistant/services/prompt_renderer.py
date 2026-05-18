from pathlib import Path
from ea_assistant.models.morning_briefing import MorningBriefingRequest


ROOT = Path(__file__).resolve().parents[3]


def read_prompt(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def render_morning_briefing_prompt(payload: MorningBriefingRequest) -> list[dict[str, str]]:
    system = read_prompt("prompts/_shared/system_executive_assistant.md")
    safety = read_prompt("prompts/_shared/safety_rules.md")
    use_case = read_prompt("prompts/morning_briefing/prompt.md")

    user_content = payload.model_dump_json(indent=2)

    return [
        {"role": "system", "content": f"{system}\n\n{safety}"},
        {"role": "user", "content": f"{use_case}\n\nINPUT_JSON:\n{user_content}"},
    ]
