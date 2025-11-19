"""API v1 routes."""

from fastapi import APIRouter

from app.api.v1.endpoints import job_titles, technologies, standards, industries, candidates, workplaces

api_router = APIRouter()

# Ontology/References
api_router.include_router(job_titles.router, prefix="/job-titles", tags=["Job Titles"])
api_router.include_router(technologies.router, prefix="/technologies", tags=["Technologies"])
api_router.include_router(standards.router, prefix="/standards", tags=["Standards"])
api_router.include_router(industries.router, prefix="/industries", tags=["Industries"])

# Core entities
api_router.include_router(candidates.router, prefix="/candidates", tags=["Candidates"])
api_router.include_router(workplaces.router, prefix="/workplaces", tags=["Workplaces"])
