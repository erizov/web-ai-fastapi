# Vacancy Parser API (FastAPI + GPT)

Этот проект реализует API для парсинга текстов вакансий.

## Запуск

```bash
uvicorn app.main:app --reload
```

Документация API: http://127.0.0.1:8000/docs

🔎 Пример запроса

POST /vacancy/parse

{
  "description": "Компания TechSolutions ищет Senior Python разработчика для удалённой работы..."
}


Пример ответа:

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

✅ Тестирование
Юнит- и интеграционные тесты
pytest -v

Тест через Jupyter Notebook

Открой vacancy.ipynb и выполни ячейку с примером запроса:

import requests

url = "http://127.0.0.1:8000/vacancy/parse"
data = {"text": "Компания TechSolutions ищет Senior Python разработчика..."}

response = requests.post(url, json=data)
print(response.json())

[Running] python -u "c:\Python\FastAPI\hw1ProxyTests\vacancy.ipynb"

INFO:     Application startup complete.
content 
{
    "job_title": "Senior Python разработчик",
    "company": "TechSolutions",
    "location": "удалённая работа",
    "employment_type": "удалённая",
    "experience_level": "Senior",
    "skills": [
        "Python",
        "Django",
        "REST API",
        "PostgreSQL",
        "Git"
    ],
    "salary": "200 000–250 000 руб.",
    "description": "Компания TechSolutions ищет Senior Python разработчика для удалённой работы.",
    "requirements": [
        "знание Git",
        "умение работать в команде",
        "внимательность к деталям"
    ],
    "responsibilities": [
        "разработка и поддержка веб-приложений",
        "участие в проектировании архитектуры"
    ]
}

INFO:     127.0.0.1:51078 - "POST /vacancy/parse HTTP/1.1" 200 OK

🛡 Обработка ошибок

Если GPT вернёт невалидный JSON, API не упадёт, а вернёт:

{
  "parse_error": true,
  "error_message": "Expecting value: line 1 column 1 (char 0)",
  "raw_output": "INVALID_JSON"
}

