def test_chat_returns_structured_json(client):
    payload = {
        "message": "டிரான்சிஸ்டர் எப்படி ஸ்விட்சாக வேலை செய்கிறது?",
        "stream": False,
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0
    assert "model_used" in data
    assert data["tokens_in"] > 0
    assert data["tokens_out"] > 0
    assert data["cost_usd"] >= 0.0
    assert data["latency_ms"] >= 0.0
    assert isinstance(data["citations"], list)


def test_chat_streaming_sse(client):
    payload = {
        "message": "What is the difference between TCP and UDP?",
        "stream": True,
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    assert "text/event-stream" in response.headers.get("content-type", "")

    content = response.text
    assert "data: " in content
    assert '"done": true' in content


def test_chat_unanswerable_question_rejection(client):
    payload = {
        "message": "Who won the FIFA World Cup 2022?",
        "stream": False,
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200

    data = response.json()
    # Check that model politely notes lack of document support
    assert any(w in data["response"] for w in ["இல்லை", "பாடத்திட்ட", "LectureLoom", "ஆவணங்களில்"])
