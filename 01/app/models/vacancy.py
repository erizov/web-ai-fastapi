from typing import List, Optional
from pydantic import BaseModel

class Vacancy(BaseModel):
    job_title: str
    company: str
    location: Optional[str] = None
    employment_type: Optional[str] = None
    experience_level: Optional[str] = None
    skills: List[str] = []
    salary: Optional[str] = None
    description: Optional[str] = None
    requirements: List[str] = []
    responsibilities: List[str] = []
