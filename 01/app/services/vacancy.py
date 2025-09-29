import json
from openai import OpenAI
from openai import AsyncOpenAI
from app.models.vacancy import Vacancy
from app.config import OPENAI_API_KEY
from app.config import OPENAI_API_BASE

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

def parse_vacancy(description: str) -> Vacancy | dict:
    prompt = f"""
    Extract the following structured JSON fields from the job description:

    - job_title
    - company
    - location
    - employment_type
    - experience_level
    - skills
    - salary
    - description
    - requirements
    - responsibilities

    Job description:
    {description}

    Respond only with valid JSON following the schema.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        
        content = response.choices[0].message.content.strip("```json")
        print ("content ", content)
        data = json.loads(content)
        print ("data json.loads(content)", data)
        print ("Vacancy", Vacancy(**data).model_dump())
        return Vacancy(**data)

    except Exception as e:
        return {
            "parse_error": True,
            "error_message": str(e),
            "raw_output": content if "content" in locals() else None
        }

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
    asycClient = AsyncOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

    # делаем запрос
    response = await asycClient.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content