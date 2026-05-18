from fastapi import APIRouter, HTTPException

from ea_assistant.clients.azure_openai_client import call_morning_briefing_model
from ea_assistant.models.morning_briefing import MorningBriefingRequest, MorningBriefingResponse
from ea_assistant.services.policy_engine import enforce_action_policy
from ea_assistant.services.schema_validator import validate_json_schema

router = APIRouter()


@router.post("/morning-briefing", response_model=MorningBriefingResponse)
def create_morning_briefing(payload: MorningBriefingRequest) -> MorningBriefingResponse:
    try:
        response = call_morning_briefing_model(payload)
        response = enforce_action_policy(response)

        errors = validate_json_schema(
            response.model_dump(mode="json"),
            "schemas/responses/morning_briefing_response.schema.json",
        )
        if errors:
            raise HTTPException(
                status_code=422,
                detail={
                    "code": "schema_validation_failed",
                    "message": "Response did not match JSON schema.",
                    "errors": errors,
                },
            )
        return response
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "assistant_api_error",
                "message": str(exc),
            },
        ) from exc
