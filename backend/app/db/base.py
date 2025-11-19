"""Import all models here for Alembic to detect them."""

from app.db.database import Base

# Import all models
from app.db.models.user import User
from app.db.models.job_title import JobTitle
from app.db.models.technology import Technology
from app.db.models.standard import Standard
from app.db.models.industry import Industry
from app.db.models.workplace import Company, Workplace, WorkplaceTechnology
from app.db.models.candidate import Candidate
from app.db.models.vacancy import Vacancy
from app.db.models.vacancy_requirement import VacancyRequirement
from app.db.models.selection import Selection
