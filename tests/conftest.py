import pytest
from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.main import app
from app.services.usage_tracker import UsageTracker, get_usage_tracker


@pytest.fixture
def client():
    test_tracker = UsageTracker(db_path=":memory:")
    app.dependency_overrides[get_settings] = lambda: Settings(
        app_name="examate-rag",
        environment="test",
        usage_db_path=":memory:",
    )
    app.dependency_overrides[get_usage_tracker] = lambda: test_tracker

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
