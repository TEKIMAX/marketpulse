import pytest
from fastapi.testclient import TestClient

from app.main import app
import app.ai as ai_module

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "MarketPulse API is running"}

def test_analyze_success(monkeypatch):
    # Mock run_codex to return a predictable result
    def fake_run(prompt):
        assert prompt == "test prompt"
        return "fake analysis"
    monkeypatch.setattr(ai_module, "run_codex", fake_run)
    response = client.post("/api/ai/analyze", json={"prompt": "test prompt"})
    assert response.status_code == 200
    assert response.json() == {"analysis": "fake analysis"}

def test_analyze_failure(monkeypatch):
    # Mock run_codex to raise an error
    def fake_run_err(prompt):
        raise RuntimeError("fail")
    monkeypatch.setattr(ai_module, "run_codex", fake_run_err)
    response = client.post("/api/ai/analyze", json={"prompt": "any"})
    assert response.status_code == 500
    assert "fail" in response.json().get("detail", "")