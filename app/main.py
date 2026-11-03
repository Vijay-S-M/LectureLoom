from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.config import Settings, get_settings
from app.schemas import ChatRequest, ChatResponse, UsageResponse
from app.services.llm import LLMService
from app.services.usage_tracker import UsageTracker, get_usage_tracker

app = FastAPI(
    title="LectureLoom API",
    description="Tamil Cross-Language Course Help Desk for Engineering Students",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SettingsDep = Annotated[Settings, Depends(get_settings)]
UsageTrackerDep = Annotated[UsageTracker, Depends(get_usage_tracker)]


def get_llm_service(
    settings: SettingsDep,
    tracker: UsageTrackerDep,
) -> LLMService:
    return LLMService(settings=settings, usage_tracker=tracker)


LLMServiceDep = Annotated[LLMService, Depends(get_llm_service)]


@app.get("/health")
def health(settings: SettingsDep) -> dict:
    """Liveness: the process is up. Must be fast and must not call the LLM or the DB."""
    return {"status": "ok", "app": settings.app_name, "environment": settings.environment}


@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    llm: LLMServiceDep,
):
    """Chat endpoint: queries the LLM with fallback support.

    Returns structured JSON or an SSE stream when stream=True.
    """
    if request.stream:
        return StreamingResponse(
            llm.generate_stream(
                message=request.message,
                history=request.history,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            ),
            media_type="text/event-stream",
        )

    return await llm.generate(
        message=request.message,
        history=request.history,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )


@app.get("/usage", response_model=UsageResponse)
def get_usage(tracker: UsageTrackerDep) -> UsageResponse:
    """Returns token consumption, latency, and cost totals by model."""
    return tracker.get_summary()
