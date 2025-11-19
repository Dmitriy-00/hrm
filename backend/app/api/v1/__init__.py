"""API v1 routes."""

from fastapi import APIRouter

from app.api.v1.endpoints import job_titles, technologies, standards, industries, candidates, workplaces, vacancies, matching, analytics, advanced_matching

api_router = APIRouter()

# Ontology/References
api_router.include_router(job_titles.router, prefix="/job-titles", tags=["Job Titles"])
api_router.include_router(technologies.router, prefix="/technologies", tags=["Technologies"])
api_router.include_router(standards.router, prefix="/standards", tags=["Standards"])
api_router.include_router(industries.router, prefix="/industries", tags=["Industries"])

# Core entities
api_router.include_router(candidates.router, prefix="/candidates", tags=["Candidates"])
api_router.include_router(workplaces.router, prefix="/workplaces", tags=["Workplaces"])
api_router.include_router(vacancies.router, prefix="/vacancies", tags=["Vacancies"])

# Matching/Scoring
api_router.include_router(matching.router, prefix="/matching", tags=["Matching"])
api_router.include_router(advanced_matching.router, prefix="/advanced-matching", tags=["Advanced Matching"])

# Analytics
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
