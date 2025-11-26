"""Seed script for vacancy data."""

import sys
import os
from datetime import date, timedelta
from uuid import uuid4

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.services.vacancy_service import VacancyService
from app.services.job_title_service import JobTitleService
from app.services.technology_service import TechnologyService
from app.db.models.workplace import Company
from app.models.schemas.vacancy import (
    VacancyCreate,
    VacancyRequirementSchema,
    LocationSchema,
    LanguageRequirementSchema,
)


def get_or_create_company(db: Session, name: str, size: str = "medium") -> Company:
    """Get or create a company."""
    company = db.query(Company).filter(Company.name == name).first()
    if not company:
        company = Company(
            name=name,
            description=f"{name} - Leading technology company",
            website=f"https://{name.lower().replace(' ', '')}.com",
            size=size,
        )
        db.add(company)
        db.commit()
        db.refresh(company)
    return company


def seed_vacancies(db: Session):
    """Seed test vacancies."""
    print("Seeding vacancies...")

    # Get or create companies
    company1 = get_or_create_company(db, "TechCorp", "large")
    company2 = get_or_create_company(db, "StartupHub", "startup")
    company3 = get_or_create_company(db, "FinanceStream", "enterprise")

    # Create a mock recruiter user ID
    recruiter_id = uuid4()

    # Get some job titles and technologies
    python_dev = JobTitleService.get_by_slug(db, "python")
    react_dev = JobTitleService.get_by_slug(db, "react")
    fullstack_dev = JobTitleService.get_by_slug(db, "fullstack")

    python_tech = TechnologyService.get_by_slug(db, "python")
    django_tech = TechnologyService.get_by_slug(db, "django")
    fastapi_tech = TechnologyService.get_by_slug(db, "fastapi")
    react_tech = TechnologyService.get_by_slug(db, "react")
    typescript_tech = TechnologyService.get_by_slug(db, "typescript")
    postgres_tech = TechnologyService.get_by_slug(db, "postgresql")
    docker_tech = TechnologyService.get_by_slug(db, "docker")
    nodejs_tech = TechnologyService.get_by_slug(db, "nodejs")

    # Vacancy 1: Senior Python Backend Developer
    vacancy1_data = VacancyCreate(
        company_id=company1.id,
        company_name=company1.name,
        job_title_id=python_dev.id if python_dev else None,
        position_name="Senior Python Backend Developer",
        grade="senior",
        min_experience_years=4,
        max_experience_years=7,
        locations=[
            LocationSchema(
                country="Russia",
                city="Moscow",
                remote=True,
                relocation=False,
            ),
            LocationSchema(
                country="Russia",
                city="Saint Petersburg",
                remote=True,
                relocation=True,
            ),
        ],
        timezone_requirements=["Europe/Moscow"],
        language_requirements=[
            LanguageRequirementSchema(
                language="English",
                min_level="B2",
                required=True,
            ),
            LanguageRequirementSchema(
                language="Russian",
                min_level="native",
                required=True,
            ),
        ],
        citizenship_allowed=["Russia"],
        citizenship_restricted=[],
        salary_min=200000,
        salary_max=300000,
        salary_currency="RUB",
        salary_type="gross",
        salary_period="month",
        salary_negotiable=True,
        status="active",
        deadline=date.today() + timedelta(days=30),
        description="""We are looking for a Senior Python Backend Developer to join our growing team.

You will be working on high-load microservices that process millions of requests daily.
The ideal candidate has strong experience with Python, async programming, and distributed systems.

What we offer:
- Competitive salary and benefits
- Flexible schedule and remote work
- Professional development opportunities
- Modern tech stack
- Challenging projects

Requirements:
- 4+ years of Python development experience
- Strong knowledge of Django or FastAPI
- Experience with PostgreSQL and Redis
- Understanding of microservices architecture
- Good English (B2+) for technical documentation""",
        responsibilities=[
            "Design and implement backend services",
            "Optimize database queries and API performance",
            "Write clean, testable code",
            "Participate in code reviews",
            "Mentor junior developers",
        ],
        interview_process={
            "stages": [
                {"name": "HR Interview", "type": "screening", "duration_minutes": 30, "order": 1},
                {"name": "Technical Interview", "type": "technical", "duration_minutes": 60, "order": 2},
                {"name": "System Design", "type": "technical", "duration_minutes": 90, "order": 3},
                {"name": "Final Interview", "type": "final", "duration_minutes": 45, "order": 4},
            ]
        },
        external_links=[],
        created_by=recruiter_id,
        requirements=[
            VacancyRequirementSchema(
                technology_id=python_tech.id if python_tech else uuid4(),
                importance="required",
                min_experience_years=4,
                proficiency_level=4,
            ),
            VacancyRequirementSchema(
                technology_id=django_tech.id if django_tech else uuid4(),
                importance="required",
                min_experience_years=2,
                proficiency_level=4,
            ),
            VacancyRequirementSchema(
                technology_id=postgres_tech.id if postgres_tech else uuid4(),
                importance="required",
                min_experience_years=2,
                proficiency_level=3,
            ),
            VacancyRequirementSchema(
                technology_id=docker_tech.id if docker_tech else uuid4(),
                importance="nice_to_have",
                min_experience_years=1,
                proficiency_level=3,
            ),
        ] if python_tech and django_tech and postgres_tech else [],
    )

    try:
        vacancy1 = VacancyService.create(db, vacancy1_data)
        print(f"  ✓ Created: {vacancy1.position_name} at {vacancy1.company_name}")
    except Exception as e:
        print(f"  ✗ Error creating vacancy 1: {e}")

    # Vacancy 2: Middle React Developer
    vacancy2_data = VacancyCreate(
        company_id=company2.id,
        company_name=company2.name,
        job_title_id=react_dev.id if react_dev else None,
        position_name="Middle React Developer",
        grade="middle",
        min_experience_years=2,
        max_experience_years=4,
        locations=[
            LocationSchema(
                country="Russia",
                city="Moscow",
                remote=True,
                relocation=False,
            ),
        ],
        timezone_requirements=["Europe/Moscow"],
        language_requirements=[
            LanguageRequirementSchema(
                language="English",
                min_level="B1",
                required=True,
            ),
        ],
        citizenship_allowed=["Russia"],
        salary_min=150000,
        salary_max=220000,
        salary_currency="RUB",
        salary_type="gross",
        salary_period="month",
        salary_negotiable=True,
        status="active",
        deadline=date.today() + timedelta(days=45),
        description="""Join our startup as a Middle React Developer!

We're building a modern SaaS platform and need a talented frontend developer.
You'll work on cutting-edge features using React, TypeScript, and Next.js.

What we offer:
- Startup equity options
- Flexible remote work
- Fast-paced environment
- Direct impact on product

Requirements:
- 2+ years of React development
- Experience with TypeScript
- Knowledge of modern state management (Redux, MobX, or Zustand)
- Understanding of responsive design""",
        responsibilities=[
            "Develop new features for our SaaS platform",
            "Collaborate with designers and backend team",
            "Optimize application performance",
            "Write unit and integration tests",
        ],
        interview_process={
            "stages": [
                {"name": "Initial Call", "type": "screening", "duration_minutes": 20, "order": 1},
                {"name": "Test Task", "type": "test_task", "duration_minutes": 180, "order": 2},
                {"name": "Technical Interview", "type": "technical", "duration_minutes": 60, "order": 3},
                {"name": "Founders Interview", "type": "final", "duration_minutes": 30, "order": 4},
            ]
        },
        created_by=recruiter_id,
        requirements=[
            VacancyRequirementSchema(
                technology_id=react_tech.id if react_tech else uuid4(),
                importance="required",
                min_experience_years=2,
                proficiency_level=3,
            ),
            VacancyRequirementSchema(
                technology_id=typescript_tech.id if typescript_tech else uuid4(),
                importance="required",
                min_experience_years=1,
                proficiency_level=3,
            ),
        ] if react_tech and typescript_tech else [],
    )

    try:
        vacancy2 = VacancyService.create(db, vacancy2_data)
        print(f"  ✓ Created: {vacancy2.position_name} at {vacancy2.company_name}")
    except Exception as e:
        print(f"  ✗ Error creating vacancy 2: {e}")

    # Vacancy 3: Full Stack Developer
    vacancy3_data = VacancyCreate(
        company_id=company3.id,
        company_name=company3.name,
        job_title_id=fullstack_dev.id if fullstack_dev else None,
        position_name="Full Stack Developer (Node.js + React)",
        grade="middle",
        min_experience_years=3,
        max_experience_years=5,
        locations=[
            LocationSchema(
                country="Russia",
                city="Saint Petersburg",
                remote=False,
                relocation=True,
            ),
        ],
        timezone_requirements=["Europe/Moscow"],
        language_requirements=[
            LanguageRequirementSchema(
                language="English",
                min_level="B2",
                required=True,
            ),
        ],
        citizenship_allowed=["Russia", "Belarus", "Kazakhstan"],
        salary_min=180000,
        salary_max=250000,
        salary_currency="RUB",
        salary_type="net",
        salary_period="month",
        salary_negotiable=False,
        status="active",
        deadline=date.today() + timedelta(days=20),
        description="""FinanceStream is hiring a Full Stack Developer for our FinTech platform.

You'll be working on both frontend (React) and backend (Node.js) of our financial services.
Security, reliability, and performance are critical in our domain.

What we offer:
- Competitive compensation
- Health insurance and benefits
- Professional certifications support
- Office in the city center

Requirements:
- 3+ years of full stack development
- Strong Node.js and React skills
- Experience with PostgreSQL
- Understanding of security best practices
- FinTech experience is a plus""",
        responsibilities=[
            "Develop full stack features for financial platform",
            "Ensure code quality and security standards",
            "Integrate with third-party payment systems",
            "Participate in architecture decisions",
        ],
        interview_process={
            "stages": [
                {"name": "Phone Screen", "type": "screening", "duration_minutes": 30, "order": 1},
                {"name": "Technical Interview", "type": "technical", "duration_minutes": 90, "order": 2},
                {"name": "Team Interview", "type": "technical", "duration_minutes": 60, "order": 3},
                {"name": "Final Interview", "type": "final", "duration_minutes": 45, "order": 4},
            ]
        },
        created_by=recruiter_id,
        requirements=[
            VacancyRequirementSchema(
                technology_id=nodejs_tech.id if nodejs_tech else uuid4(),
                importance="required",
                min_experience_years=3,
                proficiency_level=4,
            ),
            VacancyRequirementSchema(
                technology_id=react_tech.id if react_tech else uuid4(),
                importance="required",
                min_experience_years=2,
                proficiency_level=3,
            ),
            VacancyRequirementSchema(
                technology_id=postgres_tech.id if postgres_tech else uuid4(),
                importance="required",
                min_experience_years=2,
                proficiency_level=3,
            ),
        ] if nodejs_tech and react_tech and postgres_tech else [],
    )

    try:
        vacancy3 = VacancyService.create(db, vacancy3_data)
        print(f"  ✓ Created: {vacancy3.position_name} at {vacancy3.company_name}")
    except Exception as e:
        print(f"  ✗ Error creating vacancy 3: {e}")

    print(f"Vacancies seeded successfully!\n")


def main():
    """Main seed function."""
    print("=" * 60)
    print("Starting vacancy seeding...")
    print("=" * 60)
    print()

    db = SessionLocal()
    try:
        seed_vacancies(db)

        print("=" * 60)
        print("✓ All vacancy data seeded successfully!")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
