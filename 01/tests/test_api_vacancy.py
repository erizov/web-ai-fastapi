import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_vacancy_parse_success(monkeypatch):
    class DummyResponse:
        choices = [type("obj", (), {"message": type("obj2", (), {"content": """
        {
          "job_title": "Senior Python Developer",
          "company": "TechSolutions",
          "location": "удалённо",
          "employment_type": null,
          "experience_level": "senior",
          "skills": ["Python", "Django", "REST API", "PostgreSQL", "Git"],
          "salary": "200000-250000 руб",
          "description": "Разработка и поддержка веб-приложений, участие в проектировании архитектуры.",
          "requirements": ["знание Git", "умение работать в команде", "внимательность к деталям"],
          "responsibilities": ["разработка и поддержка веб-приложений", "участие в проектировании архитектуры"]
        }
        """})})]

    def dummy_chat_completions_create(*args, **kwargs):
        return DummyResponse()

    monkeypatch.setattr("app.services.vacancy.client.chat.completions.create", dummy_chat_completions_create)

    response = client.post("/vacancy/parse", json={"description": "Vacancy text"})
    assert response.status_code == 200
    data = response.json()
    assert data["job_title"] == "Senior Python Developer"
    assert "Python" in data["skills"]

def test_vacancy_parse_invalid_json(monkeypatch):
    class DummyResponse:
        choices = [type("obj", (), {"message": type("obj2", (), {"content": "INVALID_JSON"})})]

    def dummy_chat_completions_create(*args, **kwargs):
        return DummyResponse()

    monkeypatch.setattr("app.services.vacancy.client.chat.completions.create", dummy_chat_completions_create)

    response = client.post("/vacancy/parse", json={"description": "Vacancy text"})
    assert response.status_code == 200
    data = response.json()
    assert data["error_message"].startswith("Expecting value:") is True