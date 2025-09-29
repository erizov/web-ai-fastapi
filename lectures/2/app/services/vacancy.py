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

async def evaluate_resume(vacancy_text: str, resume_text: str, system_path: str = "base/system_evaluate.md"):
    """
    Сравнивает резюме и вакансию по заданному промпту.
    Возвращает структурированный отчет.
    """

    # читаем system-промпт
    with open(system_path, "r", encoding="utf-8") as f:
        system_content = f.read()

    # формируем user-промпт
    user_content = (
        f"Вакансия:\n{vacancy_text}\n\n"
        f"Резюме:\n{resume_text}\n\n"
        "Сравни резюме с вакансией и выдай отчет по критериям."
    )

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}
    ]

    # клиент OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    client = AsyncOpenAI(api_key=api_key)

    # делаем запрос
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content