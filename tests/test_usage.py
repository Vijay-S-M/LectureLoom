from app.services.llm import calculate_cost, estimate_tokens


def test_usage_initial_state(client):
    response = client.get("/usage")
    assert response.status_code == 200

    data = response.json()
    assert data["total_requests"] == 0
    assert data["total_tokens"] == 0
    assert data["total_cost_usd"] == 0.0
    assert data["by_model"] == {}
    assert data["recent_calls"] == []


def test_usage_increments_after_chat(client):
    # Perform first chat
    r1 = client.post("/chat", json={"message": "What is normalization?", "stream": False})
    assert r1.status_code == 200

    # Perform second chat
    r2 = client.post("/chat", json={"message": "What is a primary key?", "stream": False})
    assert r2.status_code == 200

    # Check usage
    usage_res = client.get("/usage")
    assert usage_res.status_code == 200

    data = usage_res.json()
    assert data["total_requests"] == 2
    assert data["total_tokens"] > 0
    assert data["total_prompt_tokens"] > 0
    assert data["total_completion_tokens"] > 0
    assert data["total_cost_usd"] >= 0.0
    assert len(data["recent_calls"]) == 2
    assert len(data["by_model"]) >= 1


def test_calculate_cost_function():
    # gpt-4o-mini: $0.15/1M prompt, $0.60/1M completion
    cost = calculate_cost("gpt-4o-mini", 1000, 1000)
    expected = (1000 * 0.15 + 1000 * 0.60) / 1_000_000.0
    assert abs(cost - expected) < 1e-9


def test_estimate_tokens_function():
    assert estimate_tokens("") == 0
    assert estimate_tokens("Hello world") > 0
    # Tamil Unicode tokens
    indic_tokens = estimate_tokens("டிரான்சிஸ்டர் எப்படி ஸ்விட்சாக வேலை செய்கிறது?")
    assert indic_tokens > 0
