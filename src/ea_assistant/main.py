from fastapi import FastAPI
from ea_assistant.routes.health import router as health_router
from ea_assistant.routes.morning_briefing import router as morning_briefing_router

app = FastAPI(
    title="M365 Executive Assistant API",
    version="0.1.0",
    description="Controlled Executive Assistant API for Power Automate + Azure OpenAI.",
)

app.include_router(health_router)
app.include_router(morning_briefing_router, prefix="/api/v1")
