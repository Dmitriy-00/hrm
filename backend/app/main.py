"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.db.database import engine, Base

# Import routers
from app.api.v1 import api_router


# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    ## HRM Platform API - Intelligent Candidate-Vacancy Matching System

    Автоматизированная система подбора IT-специалистов с интеллектуальным скорингом
    на основе семантического анализа навыков, технологий и опыта.

    ### Основные возможности

    * 🎯 **Интеллектуальный скоринг** - многоуровневая оценка соответствия (8 компонентов)
    * 🔍 **Расширенный поиск** - по технологиям, опыту, локации, зарплате
    * 📊 **Онтология компетенций** - иерархическая структура должностей и технологий
    * 🚀 **Real-time матчинг** - подбор кандидатов для вакансий и наоборот
    * 📈 **Аналитика** - insights, highlights и concerns для каждого матча

    ### Компоненты скоринга

    1. **Technologies** (40%) - соответствие технологий с учетом важности
    2. **Experience** (20%) - годы опыта работы
    3. **Skills** (15%) - soft skills и компетенции
    4. **Standards** (10%) - методологии разработки
    5. **Industry** (5%) - релевантный опыт в индустрии
    6. **Languages** (5%) - владение языками
    7. **Location** (3%) - совместимость локации
    8. **Salary** (2%) - соответствие зарплатных ожиданий

    ### Документация

    * [Алгоритм скоринга](https://github.com/yourusername/hrm/blob/main/backend/docs/SCORING.md)
    * [Работа с миграциями](https://github.com/yourusername/hrm/blob/main/backend/docs/MIGRATIONS.md)
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {"name": "Root", "description": "Root and health check endpoints"},
        {"name": "Job Titles", "description": "Ontology: Job titles hierarchy"},
        {"name": "Technologies", "description": "Ontology: Technologies and tools"},
        {"name": "Standards", "description": "Ontology: Development standards"},
        {"name": "Industries", "description": "Ontology: Industry classification"},
        {"name": "Candidates", "description": "Candidate profile management"},
        {"name": "Workplaces", "description": "Work history and experience"},
        {"name": "Vacancies", "description": "Job vacancy management"},
        {"name": "Matching", "description": "Intelligent candidate-vacancy matching and scoring"},
    ],
    contact={
        "name": "HRM Platform Team",
        "email": "support@hrm-platform.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to HRM Platform API",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": settings.VERSION,
    }


# Include API routers
app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
