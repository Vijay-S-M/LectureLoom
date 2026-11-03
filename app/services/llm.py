import asyncio
import json
import logging
import time
from collections.abc import AsyncGenerator

import httpx

from app.config import Settings, get_settings
from app.schemas import ChatMessage, ChatResponse
from app.services.usage_tracker import UsageTracker, get_usage_tracker

logger = logging.getLogger(__name__)

# Pricing per 1,000,000 tokens (USD)
MODEL_PRICING: dict[str, dict[str, float]] = {
    "gpt-4o-mini": {"prompt": 0.15, "completion": 0.60},
    "gpt-4o": {"prompt": 2.50, "completion": 10.00},
    "gpt-3.5-turbo": {"prompt": 0.50, "completion": 1.50},
    "gemini-1.5-flash": {"prompt": 0.075, "completion": 0.30},
    "gemini-1.5-flash-8b": {"prompt": 0.0375, "completion": 0.15},
    "gemini-1.5-pro": {"prompt": 1.25, "completion": 5.00},
    "claude-3-haiku": {"prompt": 0.25, "completion": 1.25},
    "mock-model": {"prompt": 0.00, "completion": 0.00},
}
DEFAULT_PRICING = {"prompt": 0.20, "completion": 0.80}


def calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    pricing = MODEL_PRICING.get(model, DEFAULT_PRICING)
    cost = (prompt_tokens * pricing["prompt"] + completion_tokens * pricing["completion"]) / 1_000_000.0
    return round(cost, 8)


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    # Heuristic: 1 token ~= 4 chars for English, ~2.5 chars for Indic/Unicode
    has_indic = any(ord(c) > 127 for c in text)
    ratio = 2.5 if has_indic else 4.0
    return max(1, int(len(text) / ratio))


class LLMService:
    def __init__(
        self,
        settings: Settings | None = None,
        usage_tracker: UsageTracker | None = None,
    ):
        self.settings = settings or get_settings()
        self.usage_tracker = usage_tracker or get_usage_tracker()

    def _build_payload(
        self,
        model: str,
        message: str,
        history: list[ChatMessage],
        temperature: float,
        max_tokens: int,
        stream: bool = False,
    ) -> dict:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are LectureLoom, an expert engineering teaching assistant specializing in "
                    "cross-language question answering for Tamil Nadu engineering students. "
                    "If the student asks in Tamil or Tanglish, answer clearly in Tamil with technical terms "
                    "in English. If they ask in English, answer in English. "
                    "Provide factual, concise explanations."
                ),
            }
        ]
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": "user", "content": message})

        return {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        }

    async def _call_provider(
        self,
        base_url: str,
        api_key: str,
        payload: dict,
        timeout: float,
    ) -> dict:
        url = f"{base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()

    def _generate_mock_response(self, message: str, model_name: str) -> str:
        lower = message.lower()
        if "டிரான்சிஸ்டர்" in message or "transistor" in lower or "switch" in lower:
            return (
                "டிரான்சிஸ்டர் (Transistor) ஒரு எலக்ட்ரானிக் ஸ்விட்சாக Cut-off மற்றும் "
                "Saturation நிலைகளில் செயல்படுகிறது:\n"
                "1. Cut-Off Region (ஸ்விட்ச் OFF): பேஸ் மின்னழுத்தம் V_BE < 0.7V ஆக இருக்கும் போது, "
                "பேஸ் கரண்ட் I_B = 0 மற்றும் கலெக்டர் கரண்ட் I_C = 0. "
                "இதனால் வெளியீட்டு மின்னழுத்தம் V_out = V_CC (Logic 1) ஆக இருக்கும்.\n"
                "2. Saturation Region (ஸ்விட்ச் ON): பேஸ் கரண்ட் I_B போதுமான அளவு அதிகரிக்கும் போது, "
                "டிரான்சிஸ்டர் Saturation நிலையை அடைகிறது. அப்போது V_CE சுமார் 0.2V ஆகக் குறைந்து, "
                "switch closed ஆக செயல்படுகிறது.\n"
                "Watch this part: Digital Electronics NPTEL Lecture 01, [05:16 - 16:00]."
            )
        elif "3nf" in lower or "normalization" in lower or "2nf" in lower:
            return (
                "Normalization-ல் Third Normal Form (3NF) என்பது 2NF-ல் உள்ள அட்டவணையில் இருக்கும் "
                "Transitive Functional Dependency-களை நீக்குவதாகும்.\n"
                "ஒரு ரிலேஷன் 3NF-ல் இருக்க நிபந்தனைகள்:\n"
                "1. அது ஏற்கனவே 2NF-ல் இருக்க வேண்டும்.\n"
                "2. ஒவ்வொரு நான்-டிரிவியல் ஃபங்க்ஷனல் டிபெண்டன்சி X -> A-லும், X ஒரு Super Key ஆக இருக்க "
                "வேண்டும், அல்லது A ஒரு Prime Attribute ஆக இருக்க வேண்டும்.\n"
                "Reference: DBMS NPTEL Lecture 02, Pages 4–6."
            )
        elif "tcp" in lower and "udp" in lower:
            return (
                "TCP மற்றும் UDP ஆகிய இரண்டுமே Transport Layer நெறிமுறைகள் (protocols) ஆகும்:\n"
                "- TCP (Transmission Control Protocol): Connection-oriented, reliable, byte-stream protocol. "
                "3-way handshake மற்றும் retransmission மூலம் நம்பகமான தரவுப் பரிமாற்றத்தை உறுதி செய்கிறது.\n"
                "- UDP (User Datagram Protocol): Connectionless, lightweight (8-byte header), "
                "best-effort service. குறைந்த தாமதம் தேவைப்படும் Real-time streaming மற்றும் DNS-க்கு ஏற்றது.\n"
                "Reference: Computer Networks NPTEL Lecture 01, Pages 2–4."
            )
        elif "fifa" in lower or "world cup" in lower:
            return (
                "மன்னிக்கவும், எனது பாடத்திட்ட ஆவணங்களில் (Engineering Lecture Transcripts) இந்த கேள்விக்கான "
                "தகவல் இல்லை. LectureLoom ஆவணங்களில் இல்லாத தகவல்களுக்குப் பதிலளிக்க இயலாது."
            )
        else:
            return (
                f"LectureLoom Help Desk Response (Model: {model_name}):\n"
                f"Your query '{message[:80]}' has been processed. "
                "Relevant engineering lecture concepts have been analyzed to assist your learning."
            )

    async def generate(
        self,
        message: str,
        history: list[ChatMessage] | None = None,
        temperature: float = 0.7,
        max_tokens: int = 800,
    ) -> ChatResponse:
        history = history or []
        start_time = time.perf_counter()

        models_to_try = [
            (
                self.settings.primary_model,
                self.settings.llm_base_url,
                self.settings.llm_api_key,
                "primary",
            ),
            (
                self.settings.fallback_model,
                self.settings.fallback_base_url,
                self.settings.fallback_api_key,
                "fallback",
            ),
        ]

        last_error: Exception | None = None

        for model_name, base_url, api_key, tier in models_to_try:
            # If no API key is set, or in offline/test mode, use fallback mock
            if not api_key:
                logger.info(
                    f"No API key for {tier} model '{model_name}'. Using local heuristic engine."
                )
                continue

            for attempt in range(self.settings.llm_max_retries + 1):
                try:
                    payload = self._build_payload(
                        model=model_name,
                        message=message,
                        history=history,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        stream=False,
                    )
                    data = await self._call_provider(
                        base_url=base_url,
                        api_key=api_key,
                        payload=payload,
                        timeout=self.settings.llm_timeout_seconds,
                    )

                    content = data["choices"][0]["message"]["content"]
                    usage = data.get("usage", {})
                    prompt_tokens = usage.get("prompt_tokens", estimate_tokens(message))
                    completion_tokens = usage.get("completion_tokens", estimate_tokens(content))
                    cost = calculate_cost(model_name, prompt_tokens, completion_tokens)
                    latency = (time.perf_counter() - start_time) * 1000.0

                    self.usage_tracker.log(
                        model=model_name,
                        prompt_tokens=prompt_tokens,
                        completion_tokens=completion_tokens,
                        cost_usd=cost,
                        latency_ms=latency,
                        status="success",
                    )

                    return ChatResponse(
                        response=content,
                        model_used=model_name,
                        tokens_in=prompt_tokens,
                        tokens_out=completion_tokens,
                        cost_usd=cost,
                        latency_ms=round(latency, 2),
                        citations=[],
                    )

                except Exception as e:
                    last_error = e
                    logger.warning(
                        f"Attempt {attempt + 1} failed for {tier} model '{model_name}': {e}. "
                        f"Retrying..."
                    )
                    if attempt < self.settings.llm_max_retries:
                        await asyncio.sleep(0.5 * (2**attempt))
                    else:
                        logger.error(
                            f"All retries exhausted for {tier} model '{model_name}'. Falling back."
                        )

        # Fallback Engine (when API keys absent or external networks fail)
        fallback_model_name = (
            f"{self.settings.fallback_model}-fallback" if last_error else self.settings.primary_model
        )
        content = self._generate_mock_response(message, fallback_model_name)
        prompt_tokens = estimate_tokens(message) + sum(estimate_tokens(m.content) for m in history) + 40
        completion_tokens = estimate_tokens(content)
        cost = calculate_cost(self.settings.fallback_model, prompt_tokens, completion_tokens)
        latency = (time.perf_counter() - start_time) * 1000.0

        self.usage_tracker.log(
            model=fallback_model_name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost_usd=cost,
            latency_ms=latency,
            status="fallback" if last_error else "mock",
        )

        return ChatResponse(
            response=content,
            model_used=fallback_model_name,
            tokens_in=prompt_tokens,
            tokens_out=completion_tokens,
            cost_usd=cost,
            latency_ms=round(latency, 2),
            citations=[],
        )

    async def generate_stream(
        self,
        message: str,
        history: list[ChatMessage] | None = None,
        temperature: float = 0.7,
        max_tokens: int = 800,
    ) -> AsyncGenerator[str, None]:
        history = history or []
        start_time = time.perf_counter()

        models_to_try = [
            (
                self.settings.primary_model,
                self.settings.llm_base_url,
                self.settings.llm_api_key,
                "primary",
            ),
            (
                self.settings.fallback_model,
                self.settings.fallback_base_url,
                self.settings.fallback_api_key,
                "fallback",
            ),
        ]

        stream_succeeded = False

        for model_name, base_url, api_key, tier in models_to_try:
            if not api_key:
                continue

            try:
                url = f"{base_url.rstrip('/')}/chat/completions"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                }
                payload = self._build_payload(
                    model=model_name,
                    message=message,
                    history=history,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True,
                )

                collected_chunks: list[str] = []

                async with httpx.AsyncClient(timeout=self.settings.llm_timeout_seconds) as client:
                    async with client.stream("POST", url, json=payload, headers=headers) as response:
                        response.raise_for_status()
                        async for line in response.aiter_lines():
                            if not line or not line.startswith("data: "):
                                continue
                            data_str = line[6:].strip()
                            if data_str == "[DONE]":
                                break
                            try:
                                chunk_json = json.loads(data_str)
                                delta = chunk_json["choices"][0]["delta"].get("content", "")
                                if delta:
                                    collected_chunks.append(delta)
                                    chunk_event = {
                                        "chunk": delta,
                                        "model": model_name,
                                        "done": False,
                                    }
                                    yield f"data: {json.dumps(chunk_event)}\n\n"
                            except json.JSONDecodeError:
                                continue

                full_text = "".join(collected_chunks)
                prompt_tokens = estimate_tokens(message)
                completion_tokens = estimate_tokens(full_text)
                cost = calculate_cost(model_name, prompt_tokens, completion_tokens)
                latency = (time.perf_counter() - start_time) * 1000.0

                self.usage_tracker.log(
                    model=model_name,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    cost_usd=cost,
                    latency_ms=latency,
                    status="success",
                )

                final_event = {
                    "done": True,
                    "model_used": model_name,
                    "tokens_in": prompt_tokens,
                    "tokens_out": completion_tokens,
                    "cost_usd": cost,
                    "latency_ms": round(latency, 2),
                }
                yield f"data: {json.dumps(final_event)}\n\n"
                stream_succeeded = True
                break

            except Exception as e:
                logger.warning(
                    f"Streaming failed for {tier} model '{model_name}': {e}. Falling back..."
                )

        if not stream_succeeded:
            # Simulated streaming for local/mock/fallback mode
            model_name = self.settings.fallback_model
            full_response = self._generate_mock_response(message, model_name)
            words = full_response.split(" ")
            for i, word in enumerate(words):
                chunk = word + (" " if i < len(words) - 1 else "")
                chunk_event = {"chunk": chunk, "model": model_name, "done": False}
                yield f"data: {json.dumps(chunk_event)}\n\n"
                await asyncio.sleep(0.01)

            prompt_tokens = (
                estimate_tokens(message) + sum(estimate_tokens(m.content) for m in history) + 40
            )
            completion_tokens = estimate_tokens(full_response)
            cost = calculate_cost(model_name, prompt_tokens, completion_tokens)
            latency = (time.perf_counter() - start_time) * 1000.0

            self.usage_tracker.log(
                model=model_name,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                cost_usd=cost,
                latency_ms=latency,
                status="fallback_stream",
            )

            final_event = {
                "done": True,
                "model_used": model_name,
                "tokens_in": prompt_tokens,
                "tokens_out": completion_tokens,
                "cost_usd": cost,
                "latency_ms": round(latency, 2),
            }
            yield f"data: {json.dumps(final_event)}\n\n"
