import pytest
from app.services.vacancy import parse_vacancy
from app.models.vacancy import Vacancy

def test_parse_vacancy_success(monkeypatch):
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

    result = parse_vacancy("dummy text")
    assert isinstance(result, Vacancy)
    assert result.job_title == "Senior Python Developer"

def test_parse_vacancy_invalid_json(monkeypatch):
    class DummyResponse:
        choices = [type("obj", (), {"message": type("obj2", (), {"content": "INVALID_JSON"})})]

    def dummy_chat_completions_create(*args, **kwargs):
        return DummyResponse()

    monkeypatch.setattr("app.services.vacancy.client.chat.completions.create", dummy_chat_completions_create)

    result = parse_vacancy("dummy text")
    assert isinstance(result, dict)
    assert result.get("parse_error") is True
