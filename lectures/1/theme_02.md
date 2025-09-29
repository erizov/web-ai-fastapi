# Генерация вакансии

## Пока напрямую обратимся к API OpenAI

1. В requirements.txt добавьте модуль:
```
...
python-dotenv
```
и установите его:
```
pip install -r requirements.txt
```

2. Создайте файл .env и пропишите в нем ключ от сервиса OpenAI:
```
OPENAI_API_KEY = ключ от OpenAI
```

3. Создайте каталог `base`, нем файл `system_vacancy.md`:
```
Ты опытный HR-специалист и эксперт по созданию привлекательных и эффективных описаний вакансий. Сделай описание вакансии со следующими параметрами:

Должность: <Вакансия>,
Обязанности: <Обязанности>,
Требования: <Требования>,
Язык: <Язык>,
Условия: <Условия>,
Стиль подачи и прочие пожелания: <Пожелания>.

Описание должно быть привлекательным, убедительным и адаптивным под требования и язык"
```

4. Создайте ноутбук vacancy.ipynb с кодом в ячейке:
```
# Эксперимент по генерации вакансии из OpenAI

import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

# 1️⃣ Загружаем .env
load_dotenv()

# 2️⃣ Читаем system из файла
with open("base/system_vacancy.md", "r", encoding="utf-8") as f:
    system_content = f.read()

# 3️⃣ Значения вакансии (user) выносим в словарь
vacancy_data = {
    "Должность": "Веб-разработчик",
    "Обязанности": "Разработка веб-приложений, поддержка проектов, оптимизация",
    "Требования": "Опыт Python и JavaScript, знание FastAPI и React, командная работа",
    "Язык": "русский",
    "Условия": "гибкий график, удалённая работа, конкурентная зарплата",
    "Стиль подачи и прочие пожелания": "дружелюбный, мотивирующий, ориентирован на специалистов среднего уровня"
}

# 4️⃣ Формируем content для user
user_content = "\n".join([f"{k}: {v}" for k, v in vacancy_data.items()])

# 5️⃣ Формируем messages
messages = [
    {"role": "system", "content": system_content},
    {"role": "user", "content": f"Сделай описание вакансии со следующими параметрами:\n{user_content}"}
]

# 6️⃣ Асинхронный вызов OpenAI
async def generate_vacancy_description():
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = await client.chat.completions.create(
        model="gpt-4o-mini",        
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content

# 7️⃣ Запуск
description = await generate_vacancy_description()
print(description)
```

5. Запустите ячейку ноутбука.

## Добавим метод API для генерации вакансии

1. Создайте файл app/services/vacancy.py в каталоге app/services, предварительно создав каталог `services`:
```
# app/services/vacancy.py

from openai import AsyncOpenAI
import os

async def generate_vacancy_description(vacancy_data: dict, system_path: str = "base/system_vacancy.md"):
    # читаем system роль
    with open(system_path, "r", encoding="utf-8") as f:
        system_content = f.read()

    # формируем user content
    user_content = "\n".join([f"{k}: {v}" for k, v in vacancy_data.items()])

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": f"Сделай описание вакансии со следующими параметрами:\n{user_content}"}
    ]

    # создаём клиента AsyncOpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    client = AsyncOpenAI(api_key=api_key)

    # делаем запрос
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content
```

2. Создайте файл app/routes/vacancy.py:
```
# app/routes/vacancy.py

from fastapi import APIRouter, Body
from app.services.vacancy import generate_vacancy_description

router = APIRouter()

@router.post("/generate")
async def generate(vacancy_data: dict[str, str] = Body(...)):
    description = await generate_vacancy_description(vacancy_data)
    return {"vacancy_description": description}
```

3. Внесите изменения в main.py:
```
# app/main.py

from fastapi import FastAPI
import uvicorn
from .routes import examples, examples2, vacancy
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env
load_dotenv()

# Создаём FastAPI приложение
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Подключаем роуты
app.include_router(examples.router, prefix="/examples", tags=["examples"])
app.include_router(examples2.router, prefix="/examples", tags=["examples"])
app.include_router(vacancy.router, prefix="/vacancy", tags=["vacancy"])

# Запуск
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=True
    )
```

4. Добавьте в ноутбук Jupyter ячейку с кодом для тестирования метода:
```
import requests

vacancy_data = {
    "Должность": "Веб-разработчик",
    "Обязанности": "Разработка веб-приложений, поддержка проектов, оптимизация",
    "Требования": "Опыт Python и JavaScript, знание FastAPI и React, командная работа",
    "Язык": "русский",
    "Условия": "гибкий график, удалённая работа, конкурентная зарплата",
    "Стиль подачи и прочие пожелания": "дружелюбный, мотивирующий, ориентирован на специалистов среднего уровня"
}

response = requests.post('http://127.0.0.1:8000/vacancy/generate', json=vacancy_data)
result = response.json()
print(result['vacancy_description'])
```

5. Запустите проект:
```
python -m app.main  
```

6. Протестируйте с помощью ноутбука обращение по маршруту /vacancy/generate