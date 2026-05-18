from fastapi import APIRouter
from ea_assistant.config.settings import get_settings

router = APIRouter()


@router.get("/health")
def health() -> dict:
    settings = get_settings()
    return {
        "status": "ok",
        "environment": settings.assistant_env,
        "model_calls_enabled": settings.enable_model_calls,
    }
