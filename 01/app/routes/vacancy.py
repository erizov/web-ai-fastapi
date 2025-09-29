from fastapi import APIRouter
from pydantic import BaseModel
from app.models.vacancy import Vacancy
from app.services.vacancy import parse_vacancy

router = APIRouter()

class VacancyRequest(BaseModel):
    description: str

@router.post("/vacancy/parse")
def vacancy_parse(request: VacancyRequest):
    result = parse_vacancy(request.description)
    return result
