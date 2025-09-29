# app/routes/vacancy.py

from fastapi import APIRouter, Body
from app.services.vacancy import generate_vacancy_description, evaluate_resume

router = APIRouter()

@router.post("/generate")
async def generate(vacancy_data: dict[str, str] = Body(...)):
    description = await generate_vacancy_description(vacancy_data)
    return {"vacancy_description": description}

@router.post("/evaluate")
async def evaluate(
    vacancy: str = Body(..., embed=True),
    resume: str = Body(..., embed=True)
):
    """
    Сравнение резюме с вакансией.
    """
    result = await evaluate_resume(vacancy, resume)
    return {"evaluation": result}