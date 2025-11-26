"""Seed script for candidate data."""

import sys
import os
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.services.candidate_service import CandidateService
from app.services.workplace_service import WorkplaceService
from app.services.job_title_service import JobTitleService
from app.services.technology_service import TechnologyService
from app.models.schemas.candidate import CandidateCreate
from app.models.schemas.workplace import (
    WorkplaceCreate,
    WorkplaceTechnologySchema,
    WorkplaceSkillSchema,
)


def seed_candidates(db: Session):
    """Seed test candidates."""
    print("Seeding candidates...")

    # Get some job titles and technologies
    python_dev = JobTitleService.get_by_slug(db, "python")
    react_dev = JobTitleService.get_by_slug(db, "react")
    fullstack_dev = JobTitleService.get_by_slug(db, "fullstack")

    python_tech = TechnologyService.get_by_slug(db, "python")
    django_tech = TechnologyService.get_by_slug(db, "django")
    fastapi_tech = TechnologyService.get_by_slug(db, "fastapi")
    react_tech = TechnologyService.get_by_slug(db, "react")
    postgres_tech = TechnologyService.get_by_slug(db, "postgresql")
    docker_tech = TechnologyService.get_by_slug(db, "docker")
    nodejs_tech = TechnologyService.get_by_slug(db, "nodejs")
    typescript_tech = TechnologyService.get_by_slug(db, "typescript")

    # Candidate 1: Python Backend Developer
    candidate1_data = CandidateCreate(
        first_name="Иван",
        last_name="Петров",
        email="ivan.petrov@example.com",
        phone="+7 (999) 123-45-67",
        job_title_id=python_dev.id if python_dev else None,
        current_job_title="Python Backend Developer",
        grade="middle",
        country="Russia",
        city="Moscow",
        timezone="Europe/Moscow",
        citizenship=["Russia"],
        relocation=False,
        remote_work=True,
        languages=[
            {"language": "Russian", "proficiency": "native"},
            {"language": "English", "proficiency": "B2"},
        ],
        contacts={
            "telegram": "@ivan_petrov",
            "github": "github.com/ivanpetrov",
            "linkedin": "linkedin.com/in/ivanpetrov",
        },
        about_me="Experienced Python backend developer with 4+ years of experience. "
        "Specialized in building scalable APIs and microservices. "
        "Strong knowledge of Django, FastAPI, and PostgreSQL.",
        status="active",
    )

    try:
        existing = CandidateService.get_by_email(db, candidate1_data.email)
        if not existing:
            candidate1 = CandidateService.create(db, candidate1_data)
            print(f"  ✓ Created: {candidate1.first_name} {candidate1.last_name}")

            # Add work experience
            if python_tech and django_tech and postgres_tech:
                workplace1 = WorkplaceCreate(
                    candidate_id=candidate1.id,
                    company_name="Tech Solutions LLC",
                    company_size="medium",
                    position_name="Python Backend Developer",
                    grade="middle",
                    start_date=date.today() - relativedelta(years=2, months=3),
                    end_date=None,  # Current job
                    description="Developing and maintaining backend services for e-commerce platform",
                    achievements=[
                        "Optimized API response time by 40%",
                        "Implemented CI/CD pipeline",
                        "Migrated monolith to microservices",
                    ],
                    technologies=[
                        WorkplaceTechnologySchema(
                            technology_id=python_tech.id,
                            proficiency=4,
                            usage_intensity="primary",
                        ),
                        WorkplaceTechnologySchema(
                            technology_id=django_tech.id,
                            proficiency=4,
                            usage_intensity="primary",
                        ),
                        WorkplaceTechnologySchema(
                            technology_id=postgres_tech.id,
                            proficiency=3,
                            usage_intensity="secondary",
                        ),
                        WorkplaceTechnologySchema(
                            technology_id=docker_tech.id if docker_tech else None,
                            proficiency=3,
                            usage_intensity="secondary",
                        ) if docker_tech else None,
                    ],
                    skills=[
                        WorkplaceSkillSchema(
                            skill_name="REST API Design",
                            skill_category="Backend",
                            proficiency=4,
                        ),
                        WorkplaceSkillSchema(
                            skill_name="Database Optimization",
                            skill_category="Database",
                            proficiency=3,
                        ),
                    ],
                    project_types=["greenfield", "legacy"],
                    team_size=8,
                    role="individual_contributor",
                )
                WorkplaceService.create(db, workplace1)
                print(f"    ✓ Added current workplace")

                # Previous job
                workplace2 = WorkplaceCreate(
                    candidate_id=candidate1.id,
                    company_name="StartupX",
                    company_size="startup",
                    position_name="Junior Python Developer",
                    grade="junior",
                    start_date=date.today() - relativedelta(years=4, months=3),
                    end_date=date.today() - relativedelta(years=2, months=3),
                    description="Full-stack development for SaaS platform",
                    achievements=["Built user authentication system", "Implemented payment integration"],
                    technologies=[
                        WorkplaceTechnologySchema(
                            technology_id=python_tech.id,
                            proficiency=3,
                            usage_intensity="primary",
                        ),
                        WorkplaceTechnologySchema(
                            technology_id=fastapi_tech.id if fastapi_tech else None,
                            proficiency=3,
                            usage_intensity="primary",
                        ) if fastapi_tech else None,
                    ],
                    project_types=["greenfield"],
                    team_size=4,
                    role="individual_contributor",
                )
                WorkplaceService.create(db, workplace2)
                print(f"    ✓ Added previous workplace")
        else:
            print(f"  - Exists: {existing.first_name} {existing.last_name}")
    except Exception as e:
        print(f"  ✗ Error creating candidate 1: {e}")

    # Candidate 2: React Frontend Developer
    candidate2_data = CandidateCreate(
        first_name="Мария",
        last_name="Смирнова",
        email="maria.smirnova@example.com",
        phone="+7 (999) 234-56-78",
        job_title_id=react_dev.id if react_dev else None,
        current_job_title="Senior React Developer",
        grade="senior",
        country="Russia",
        city="Saint Petersburg",
        timezone="Europe/Moscow",
        citizenship=["Russia"],
        relocation=True,
        remote_work=True,
        languages=[
            {"language": "Russian", "proficiency": "native"},
            {"language": "English", "proficiency": "C1"},
        ],
        contacts={
            "telegram": "@maria_frontend",
            "github": "github.com/mariasmirnova",
            "portfolio": "mariasmirnova.dev",
        },
        about_me="Senior frontend developer with 6+ years of experience in React ecosystem. "
        "Passionate about building performant and accessible user interfaces. "
        "Experience with Next.js, TypeScript, and modern state management.",
        status="passive",
    )

    try:
        existing = CandidateService.get_by_email(db, candidate2_data.email)
        if not existing:
            candidate2 = CandidateService.create(db, candidate2_data)
            print(f"  ✓ Created: {candidate2.first_name} {candidate2.last_name}")

            # Add work experience
            if react_tech and typescript_tech:
                workplace = WorkplaceCreate(
                    candidate_id=candidate2.id,
                    company_name="Digital Agency Pro",
                    company_size="large",
                    position_name="Senior Frontend Developer",
                    grade="senior",
                    start_date=date.today() - relativedelta(years=3),
                    end_date=None,
                    description="Leading frontend development for enterprise clients",
                    achievements=[
                        "Reduced bundle size by 50%",
                        "Implemented design system",
                        "Mentored 4 junior developers",
                    ],
                    technologies=[
                        WorkplaceTechnologySchema(
                            technology_id=react_tech.id,
                            proficiency=5,
                            usage_intensity="primary",
                        ),
                        WorkplaceTechnologySchema(
                            technology_id=typescript_tech.id,
                            proficiency=4,
                            usage_intensity="primary",
                        ),
                    ],
                    skills=[
                        WorkplaceSkillSchema(
                            skill_name="Component Architecture",
                            skill_category="Frontend",
                            proficiency=5,
                        ),
                        WorkplaceSkillSchema(
                            skill_name="Performance Optimization",
                            skill_category="Frontend",
                            proficiency=4,
                        ),
                    ],
                    project_types=["greenfield", "migration"],
                    team_size=12,
                    role="tech_lead",
                )
                WorkplaceService.create(db, workplace)
                print(f"    ✓ Added workplace")
        else:
            print(f"  - Exists: {existing.first_name} {existing.last_name}")
    except Exception as e:
        print(f"  ✗ Error creating candidate 2: {e}")

    # Candidate 3: Full Stack Developer
    candidate3_data = CandidateCreate(
        first_name="Алексей",
        last_name="Козлов",
        email="alex.kozlov@example.com",
        phone="+7 (999) 345-67-89",
        job_title_id=fullstack_dev.id if fullstack_dev else None,
        current_job_title="Full Stack Developer",
        grade="middle",
        country="Russia",
        city="Novosibirsk",
        timezone="Asia/Novosibirsk",
        citizenship=["Russia"],
        relocation=False,
        remote_work=True,
        languages=[
            {"language": "Russian", "proficiency": "native"},
            {"language": "English", "proficiency": "B1"},
        ],
        contacts={
            "telegram": "@alex_fullstack",
            "github": "github.com/alexkozlov",
        },
        about_me="Full stack developer with experience in both frontend and backend. "
        "Comfortable with React, Node.js, and Python. "
        "Looking for challenging projects with modern tech stack.",
        status="active",
    )

    try:
        existing = CandidateService.get_by_email(db, candidate3_data.email)
        if not existing:
            candidate3 = CandidateService.create(db, candidate3_data)
            print(f"  ✓ Created: {candidate3.first_name} {candidate3.last_name}")

            # Add work experience
            if nodejs_tech and react_tech and postgres_tech:
                workplace = WorkplaceCreate(
                    candidate_id=candidate3.id,
                    company_name="FinTech Innovations",
                    company_size="medium",
                    position_name="Full Stack Developer",
                    grade="middle",
                    start_date=date.today() - relativedelta(years=1, months=8),
                    end_date=None,
                    description="Full stack development for fintech products",
                    achievements=[
                        "Built admin dashboard from scratch",
                        "Integrated payment gateway",
                    ],
                    technologies=[
                        WorkplaceTechnologySchema(
                            technology_id=nodejs_tech.id,
                            proficiency=4,
                            usage_intensity="primary",
                        ),
                        WorkplaceTechnologySchema(
                            technology_id=react_tech.id,
                            proficiency=3,
                            usage_intensity="primary",
                        ),
                        WorkplaceTechnologySchema(
                            technology_id=postgres_tech.id,
                            proficiency=3,
                            usage_intensity="secondary",
                        ),
                    ],
                    project_types=["greenfield"],
                    team_size=6,
                    role="individual_contributor",
                )
                WorkplaceService.create(db, workplace)
                print(f"    ✓ Added workplace")
        else:
            print(f"  - Exists: {existing.first_name} {existing.last_name}")
    except Exception as e:
        print(f"  ✗ Error creating candidate 3: {e}")

    print(f"Candidates seeded successfully!\n")


def main():
    """Main seed function."""
    print("=" * 60)
    print("Starting candidate seeding...")
    print("=" * 60)
    print()

    db = SessionLocal()
    try:
        seed_candidates(db)

        print("=" * 60)
        print("✓ All candidate data seeded successfully!")
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
