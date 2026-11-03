
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the message author: 'user', 'assistant', or 'system'")
    content: str = Field(..., description="Content of the message")


class ChatRequest(BaseModel):
    message: str = Field(..., description="User question or input prompt", min_length=1)
    history: list[ChatMessage] = Field(default_factory=list, description="Prior conversation messages")
    stream: bool = Field(default=False, description="Whether to stream response chunks via SSE")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: int = Field(default=800, ge=1, le=4096, description="Maximum completion tokens")
    department: str | None = Field(default=None, description="Target department (e.g., 'CSE', 'ECE')")


class Citation(BaseModel):
    document: str = Field(..., description="Source lecture document name")
    page: int = Field(..., description="Page number where evidence is found")
    quote: str | None = Field(default=None, description="Relevant excerpt from the lecture text")
    timestamp: str | None = Field(default=None, description="Lecture timestamp for 'Watch this part'")


class ChatResponse(BaseModel):
    response: str = Field(..., description="Generated answer from the model")
    model_used: str = Field(..., description="Identifier of the model that generated the response")
    tokens_in: int = Field(..., description="Number of prompt/input tokens")
    tokens_out: int = Field(..., description="Number of completion/output tokens")
    cost_usd: float = Field(..., description="Calculated cost of the request in USD")
    latency_ms: float = Field(..., description="Total round-trip latency in milliseconds")
    citations: list[Citation] = Field(default_factory=list, description="Source citations")


class UsageRecord(BaseModel):
    id: int
    timestamp: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd: float
    latency_ms: float
    status: str


class ModelUsageSummary(BaseModel):
    calls: int
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    total_cost_usd: float


class UsageResponse(BaseModel):
    total_requests: int
    total_prompt_tokens: int
    total_completion_tokens: int
    total_tokens: int
    total_cost_usd: float
    by_model: dict[str, ModelUsageSummary]
    recent_calls: list[UsageRecord]
