from fastapi.testclient import TestClient
from ea_assistant.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_morning_briefing_example():
    import json
    from pathlib import Path

    payload = json.loads(Path("prompts/morning_briefing/input_example.json").read_text())
    response = client.post("/api/v1/morning-briefing", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["audit"]["use_case"] == "EA_MorningBriefing"
    assert "briefing_summary" in body
