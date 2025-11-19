"""Seed script for ontology data (job titles, technologies, standards, industries)."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.services.job_title_service import JobTitleService
from app.services.technology_service import TechnologyService
from app.services.standard_service import StandardService
from app.services.industry_service import IndustryService
from app.models.schemas.job_title import JobTitleCreate
from app.models.schemas.technology import TechnologyCreate
from app.models.schemas.standard import StandardCreate
from app.models.schemas.industry import IndustryCreate


def seed_job_titles(db: Session):
    """Seed job titles."""
    print("Seeding job titles...")

    job_titles = [
        # Root
        JobTitleCreate(
            name="Developer",
            slug="developer",
            aliases=["Software Developer", "Software Engineer", "Programmer"],
            description="Software development professional",
        ),
        JobTitleCreate(
            name="Designer",
            slug="designer",
            aliases=["UI/UX Designer", "Product Designer"],
            description="Design professional",
        ),
        JobTitleCreate(
            name="Manager",
            slug="manager",
            aliases=["Project Manager", "Product Manager"],
            description="Management professional",
        ),
    ]

    created = {}
    for jt_data in job_titles:
        try:
            existing = JobTitleService.get_by_slug(db, jt_data.slug)
            if not existing:
                jt = JobTitleService.create(db, jt_data)
                created[jt.slug] = jt.id
                print(f"  ✓ Created: {jt.name}")
            else:
                created[existing.slug] = existing.id
                print(f"  - Exists: {existing.name}")
        except Exception as e:
            print(f"  ✗ Error creating {jt_data.name}: {e}")

    # Children of Developer
    developer_id = created.get("developer")
    if developer_id:
        developer_children = [
            JobTitleCreate(
                name="Backend Developer",
                slug="backend",
                parent_id=developer_id,
                description="Server-side development",
            ),
            JobTitleCreate(
                name="Frontend Developer",
                slug="frontend",
                parent_id=developer_id,
                description="Client-side development",
            ),
            JobTitleCreate(
                name="Full Stack Developer",
                slug="fullstack",
                parent_id=developer_id,
                description="Both frontend and backend",
            ),
            JobTitleCreate(
                name="Mobile Developer",
                slug="mobile",
                parent_id=developer_id,
                description="Mobile application development",
            ),
            JobTitleCreate(
                name="DevOps Engineer",
                slug="devops",
                parent_id=developer_id,
                description="Development and operations",
            ),
            JobTitleCreate(
                name="Data Engineer",
                slug="data-engineer",
                parent_id=developer_id,
                description="Data pipeline and infrastructure",
            ),
            JobTitleCreate(
                name="QA Engineer",
                slug="qa",
                parent_id=developer_id,
                description="Quality assurance and testing",
            ),
        ]

        for child_data in developer_children:
            try:
                existing = JobTitleService.get_by_slug(db, child_data.slug)
                if not existing:
                    child = JobTitleService.create(db, child_data)
                    created[child.slug] = child.id
                    print(f"    ✓ Created: {child.name}")
                else:
                    created[existing.slug] = existing.id
                    print(f"    - Exists: {existing.name}")
            except Exception as e:
                print(f"    ✗ Error creating {child_data.name}: {e}")

    # Grandchildren - Backend specializations
    backend_id = created.get("backend")
    if backend_id:
        backend_specializations = [
            JobTitleCreate(
                name="Python Developer",
                slug="python",
                parent_id=backend_id,
                description="Python backend development",
            ),
            JobTitleCreate(
                name="Java Developer",
                slug="java",
                parent_id=backend_id,
                description="Java backend development",
            ),
            JobTitleCreate(
                name="Node.js Developer",
                slug="nodejs",
                parent_id=backend_id,
                description="Node.js backend development",
            ),
            JobTitleCreate(
                name="Go Developer",
                slug="golang",
                parent_id=backend_id,
                description="Go backend development",
            ),
        ]

        for spec_data in backend_specializations:
            try:
                existing = JobTitleService.get_by_slug(db, spec_data.slug)
                if not existing:
                    spec = JobTitleService.create(db, spec_data)
                    print(f"      ✓ Created: {spec.name}")
                else:
                    print(f"      - Exists: {existing.name}")
            except Exception as e:
                print(f"      ✗ Error creating {spec_data.name}: {e}")

    # Frontend specializations
    frontend_id = created.get("frontend")
    if frontend_id:
        frontend_specializations = [
            JobTitleCreate(
                name="React Developer",
                slug="react",
                parent_id=frontend_id,
                description="React frontend development",
            ),
            JobTitleCreate(
                name="Vue Developer",
                slug="vue",
                parent_id=frontend_id,
                description="Vue.js frontend development",
            ),
            JobTitleCreate(
                name="Angular Developer",
                slug="angular",
                parent_id=frontend_id,
                description="Angular frontend development",
            ),
        ]

        for spec_data in frontend_specializations:
            try:
                existing = JobTitleService.get_by_slug(db, spec_data.slug)
                if not existing:
                    spec = JobTitleService.create(db, spec_data)
                    print(f"      ✓ Created: {spec.name}")
                else:
                    print(f"      - Exists: {existing.name}")
            except Exception as e:
                print(f"      ✗ Error creating {spec_data.name}: {e}")

    print(f"Job titles seeded successfully!\n")


def seed_technologies(db: Session):
    """Seed technologies."""
    print("Seeding technologies...")

    technologies = [
        # Programming Languages
        TechnologyCreate(
            name="Python",
            slug="python",
            category="language",
            tags=["backend", "scripting", "data-science", "ml"],
            difficulty_level=2,
            popularity_score=95,
            metadata={"official_site": "https://www.python.org"},
        ),
        TechnologyCreate(
            name="JavaScript",
            slug="javascript",
            category="language",
            tags=["frontend", "backend", "fullstack"],
            difficulty_level=2,
            popularity_score=98,
            metadata={"official_site": "https://developer.mozilla.org"},
        ),
        TechnologyCreate(
            name="TypeScript",
            slug="typescript",
            category="language",
            tags=["frontend", "backend", "fullstack"],
            difficulty_level=3,
            popularity_score=92,
            metadata={"official_site": "https://www.typescriptlang.org"},
        ),
        TechnologyCreate(
            name="Java",
            slug="java",
            category="language",
            tags=["backend", "enterprise"],
            difficulty_level=3,
            popularity_score=85,
            metadata={"official_site": "https://www.java.com"},
        ),
        TechnologyCreate(
            name="Go",
            slug="go",
            category="language",
            tags=["backend", "systems"],
            difficulty_level=3,
            popularity_score=78,
            metadata={"official_site": "https://go.dev"},
        ),
        TechnologyCreate(
            name="C#",
            slug="csharp",
            category="language",
            tags=["backend", "game-dev", "enterprise"],
            difficulty_level=3,
            popularity_score=75,
            metadata={"official_site": "https://docs.microsoft.com/dotnet/csharp"},
        ),
        TechnologyCreate(
            name="PHP",
            slug="php",
            category="language",
            tags=["backend", "web"],
            difficulty_level=2,
            popularity_score=70,
            metadata={"official_site": "https://www.php.net"},
        ),
        TechnologyCreate(
            name="Ruby",
            slug="ruby",
            category="language",
            tags=["backend", "web"],
            difficulty_level=2,
            popularity_score=65,
            metadata={"official_site": "https://www.ruby-lang.org"},
        ),
    ]

    created_techs = {}
    for tech_data in technologies:
        try:
            existing = TechnologyService.get_by_slug(db, tech_data.slug)
            if not existing:
                tech = TechnologyService.create(db, tech_data)
                created_techs[tech.slug] = tech.id
                print(f"  ✓ Created: {tech.name}")
            else:
                created_techs[existing.slug] = existing.id
                print(f"  - Exists: {existing.name}")
        except Exception as e:
            print(f"  ✗ Error creating {tech_data.name}: {e}")

    # Python frameworks
    python_id = created_techs.get("python")
    if python_id:
        python_frameworks = [
            TechnologyCreate(
                name="Django",
                slug="django",
                category="framework",
                parent_id=python_id,
                tags=["web", "fullstack", "orm"],
                difficulty_level=3,
                popularity_score=88,
                metadata={"official_site": "https://www.djangoproject.com"},
            ),
            TechnologyCreate(
                name="FastAPI",
                slug="fastapi",
                category="framework",
                parent_id=python_id,
                tags=["web", "api", "async"],
                difficulty_level=2,
                popularity_score=85,
                metadata={"official_site": "https://fastapi.tiangolo.com"},
            ),
            TechnologyCreate(
                name="Flask",
                slug="flask",
                category="framework",
                parent_id=python_id,
                tags=["web", "micro"],
                difficulty_level=2,
                popularity_score=80,
                metadata={"official_site": "https://flask.palletsprojects.com"},
            ),
        ]

        for fw_data in python_frameworks:
            try:
                existing = TechnologyService.get_by_slug(db, fw_data.slug)
                if not existing:
                    fw = TechnologyService.create(db, fw_data)
                    print(f"    ✓ Created: {fw.name}")
                else:
                    print(f"    - Exists: {existing.name}")
            except Exception as e:
                print(f"    ✗ Error creating {fw_data.name}: {e}")

    # JavaScript frameworks
    js_id = created_techs.get("javascript")
    if js_id:
        js_frameworks = [
            TechnologyCreate(
                name="React",
                slug="react",
                category="framework",
                parent_id=js_id,
                tags=["frontend", "ui", "spa"],
                difficulty_level=3,
                popularity_score=95,
                metadata={"official_site": "https://react.dev"},
            ),
            TechnologyCreate(
                name="Vue.js",
                slug="vuejs",
                category="framework",
                parent_id=js_id,
                tags=["frontend", "ui", "spa"],
                difficulty_level=2,
                popularity_score=82,
                metadata={"official_site": "https://vuejs.org"},
            ),
            TechnologyCreate(
                name="Angular",
                slug="angular",
                category="framework",
                parent_id=js_id,
                tags=["frontend", "ui", "spa"],
                difficulty_level=4,
                popularity_score=75,
                metadata={"official_site": "https://angular.io"},
            ),
            TechnologyCreate(
                name="Node.js",
                slug="nodejs",
                category="framework",
                parent_id=js_id,
                tags=["backend", "runtime"],
                difficulty_level=3,
                popularity_score=92,
                metadata={"official_site": "https://nodejs.org"},
            ),
        ]

        for fw_data in js_frameworks:
            try:
                existing = TechnologyService.get_by_slug(db, fw_data.slug)
                if not existing:
                    fw = TechnologyService.create(db, fw_data)
                    created_techs[fw.slug] = fw.id
                    print(f"    ✓ Created: {fw.name}")
                else:
                    created_techs[existing.slug] = existing.id
                    print(f"    - Exists: {existing.name}")
            except Exception as e:
                print(f"    ✗ Error creating {fw_data.name}: {e}")

    # React ecosystem
    react_id = created_techs.get("react")
    if react_id:
        react_ecosystem = [
            TechnologyCreate(
                name="Next.js",
                slug="nextjs",
                category="framework",
                parent_id=react_id,
                tags=["ssr", "fullstack", "react"],
                difficulty_level=3,
                popularity_score=90,
                metadata={"official_site": "https://nextjs.org"},
            ),
            TechnologyCreate(
                name="Redux",
                slug="redux",
                category="framework",
                parent_id=react_id,
                tags=["state-management", "react"],
                difficulty_level=3,
                popularity_score=78,
                metadata={"official_site": "https://redux.js.org"},
            ),
        ]

        for lib_data in react_ecosystem:
            try:
                existing = TechnologyService.get_by_slug(db, lib_data.slug)
                if not existing:
                    lib = TechnologyService.create(db, lib_data)
                    print(f"      ✓ Created: {lib.name}")
                else:
                    print(f"      - Exists: {existing.name}")
            except Exception as e:
                print(f"      ✗ Error creating {lib_data.name}: {e}")

    # Databases
    databases = [
        TechnologyCreate(
            name="PostgreSQL",
            slug="postgresql",
            category="database",
            tags=["sql", "relational"],
            difficulty_level=3,
            popularity_score=88,
            metadata={"official_site": "https://www.postgresql.org"},
        ),
        TechnologyCreate(
            name="MongoDB",
            slug="mongodb",
            category="database",
            tags=["nosql", "document"],
            difficulty_level=2,
            popularity_score=82,
            metadata={"official_site": "https://www.mongodb.com"},
        ),
        TechnologyCreate(
            name="Redis",
            slug="redis",
            category="database",
            tags=["nosql", "cache", "key-value"],
            difficulty_level=2,
            popularity_score=85,
            metadata={"official_site": "https://redis.io"},
        ),
        TechnologyCreate(
            name="MySQL",
            slug="mysql",
            category="database",
            tags=["sql", "relational"],
            difficulty_level=2,
            popularity_score=80,
            metadata={"official_site": "https://www.mysql.com"},
        ),
    ]

    for db_data in databases:
        try:
            existing = TechnologyService.get_by_slug(db, db_data.slug)
            if not existing:
                database = TechnologyService.create(db, db_data)
                print(f"  ✓ Created: {database.name}")
            else:
                print(f"  - Exists: {existing.name}")
        except Exception as e:
            print(f"  ✗ Error creating {db_data.name}: {e}")

    # DevOps tools
    devops_tools = [
        TechnologyCreate(
            name="Docker",
            slug="docker",
            category="devops",
            tags=["container", "deployment"],
            difficulty_level=3,
            popularity_score=92,
            metadata={"official_site": "https://www.docker.com"},
        ),
        TechnologyCreate(
            name="Kubernetes",
            slug="kubernetes",
            category="devops",
            tags=["orchestration", "container"],
            difficulty_level=4,
            popularity_score=88,
            metadata={"official_site": "https://kubernetes.io"},
        ),
        TechnologyCreate(
            name="Git",
            slug="git",
            category="devops",
            tags=["version-control"],
            difficulty_level=2,
            popularity_score=98,
            metadata={"official_site": "https://git-scm.com"},
        ),
        TechnologyCreate(
            name="GitHub Actions",
            slug="github-actions",
            category="devops",
            tags=["ci-cd", "automation"],
            difficulty_level=2,
            popularity_score=85,
            metadata={"official_site": "https://github.com/features/actions"},
        ),
    ]

    for tool_data in devops_tools:
        try:
            existing = TechnologyService.get_by_slug(db, tool_data.slug)
            if not existing:
                tool = TechnologyService.create(db, tool_data)
                print(f"  ✓ Created: {tool.name}")
            else:
                print(f"  - Exists: {existing.name}")
        except Exception as e:
            print(f"  ✗ Error creating {tool_data.name}: {e}")

    print(f"Technologies seeded successfully!\n")


def seed_standards(db: Session):
    """Seed standards and methodologies."""
    print("Seeding standards...")

    standards = [
        # Methodologies
        StandardCreate(
            name="Agile",
            type="methodology",
            category="Development Methodology",
            path="methodology.agile",
            description="Iterative development methodology",
            difficulty=2,
            importance_by_grade={
                "junior": 60,
                "middle": 80,
                "senior": 90,
                "lead": 95,
                "architect": 90,
            },
        ),
        StandardCreate(
            name="Scrum",
            type="methodology",
            category="Development Methodology",
            path="methodology.agile.scrum",
            description="Agile framework for project management",
            difficulty=2,
            importance_by_grade={
                "junior": 50,
                "middle": 75,
                "senior": 85,
                "lead": 95,
                "architect": 85,
            },
        ),
        StandardCreate(
            name="Kanban",
            type="methodology",
            category="Development Methodology",
            path="methodology.kanban",
            description="Visual workflow management method",
            difficulty=1,
            importance_by_grade={
                "junior": 40,
                "middle": 70,
                "senior": 80,
                "lead": 90,
                "architect": 80,
            },
        ),
        # Principles
        StandardCreate(
            name="SOLID",
            type="principle",
            category="Design Principles",
            path="principle.solid",
            description="Five design principles for OOP",
            difficulty=3,
            importance_by_grade={
                "junior": 40,
                "middle": 80,
                "senior": 95,
                "lead": 95,
                "architect": 100,
            },
        ),
        StandardCreate(
            name="DRY",
            type="principle",
            category="Design Principles",
            path="principle.dry",
            description="Don't Repeat Yourself principle",
            difficulty=2,
            importance_by_grade={
                "junior": 60,
                "middle": 85,
                "senior": 90,
                "lead": 90,
                "architect": 90,
            },
        ),
        StandardCreate(
            name="KISS",
            type="principle",
            category="Design Principles",
            path="principle.kiss",
            description="Keep It Simple, Stupid principle",
            difficulty=1,
            importance_by_grade={
                "junior": 70,
                "middle": 85,
                "senior": 90,
                "lead": 90,
                "architect": 90,
            },
        ),
        # Practices
        StandardCreate(
            name="TDD",
            type="pattern",
            category="Testing",
            path="practice.tdd",
            description="Test-Driven Development",
            difficulty=3,
            importance_by_grade={
                "junior": 30,
                "middle": 70,
                "senior": 85,
                "lead": 90,
                "architect": 85,
            },
        ),
        StandardCreate(
            name="CI/CD",
            type="pattern",
            category="DevOps",
            path="practice.cicd",
            description="Continuous Integration/Continuous Deployment",
            difficulty=3,
            importance_by_grade={
                "junior": 40,
                "middle": 75,
                "senior": 90,
                "lead": 95,
                "architect": 90,
            },
        ),
        # Protocols
        StandardCreate(
            name="REST",
            type="protocol",
            category="API",
            path="protocol.rest",
            description="Representational State Transfer",
            difficulty=2,
            importance_by_grade={
                "junior": 70,
                "middle": 90,
                "senior": 95,
                "lead": 90,
                "architect": 90,
            },
        ),
        StandardCreate(
            name="GraphQL",
            type="protocol",
            category="API",
            path="protocol.graphql",
            description="Query language for APIs",
            difficulty=3,
            importance_by_grade={
                "junior": 30,
                "middle": 60,
                "senior": 75,
                "lead": 80,
                "architect": 80,
            },
        ),
    ]

    for std_data in standards:
        try:
            std = StandardService.create(db, std_data)
            print(f"  ✓ Created: {std.name}")
        except Exception as e:
            print(f"  ✗ Error creating {std_data.name}: {e}")

    print(f"Standards seeded successfully!\n")


def seed_industries(db: Session):
    """Seed industries."""
    print("Seeding industries...")

    industries = [
        # Root industries
        IndustryCreate(
            name="FinTech",
            path="fintech",
            description="Financial technology",
            compliance_requirements=["PCI-DSS", "SOX", "GDPR"],
            typical_challenges=["Security", "Compliance", "Real-time processing"],
        ),
        IndustryCreate(
            name="HealthTech",
            path="healthtech",
            description="Healthcare technology",
            compliance_requirements=["HIPAA", "GDPR", "FDA"],
            typical_challenges=["Privacy", "Data security", "Interoperability"],
        ),
        IndustryCreate(
            name="EdTech",
            path="edtech",
            description="Educational technology",
            compliance_requirements=["FERPA", "COPPA", "GDPR"],
            typical_challenges=["Accessibility", "Scalability", "Engagement"],
        ),
        IndustryCreate(
            name="E-commerce",
            path="ecommerce",
            description="Electronic commerce",
            compliance_requirements=["PCI-DSS", "GDPR"],
            typical_challenges=["Scalability", "Performance", "Security"],
        ),
        IndustryCreate(
            name="GameDev",
            path="gamedev",
            description="Game development",
            typical_challenges=["Performance", "Real-time rendering", "Multiplayer"],
        ),
    ]

    created_industries = {}
    for ind_data in industries:
        try:
            existing = IndustryService.get_by_path(db, ind_data.path)
            if not existing:
                ind = IndustryService.create(db, ind_data)
                created_industries[ind.path] = ind.id
                print(f"  ✓ Created: {ind.name}")
            else:
                created_industries[existing.path] = existing.id
                print(f"  - Exists: {existing.name}")
        except Exception as e:
            print(f"  ✗ Error creating {ind_data.name}: {e}")

    # FinTech sub-industries
    fintech_id = created_industries.get("fintech")
    if fintech_id:
        fintech_children = [
            IndustryCreate(
                name="Banking",
                path="fintech.banking",
                parent_id=fintech_id,
                description="Digital banking solutions",
            ),
            IndustryCreate(
                name="Blockchain",
                path="fintech.blockchain",
                parent_id=fintech_id,
                description="Blockchain and cryptocurrency",
            ),
            IndustryCreate(
                name="Payments",
                path="fintech.payments",
                parent_id=fintech_id,
                description="Payment processing systems",
            ),
        ]

        for child_data in fintech_children:
            try:
                existing = IndustryService.get_by_path(db, child_data.path)
                if not existing:
                    child = IndustryService.create(db, child_data)
                    print(f"    ✓ Created: {child.name}")
                else:
                    print(f"    - Exists: {existing.name}")
            except Exception as e:
                print(f"    ✗ Error creating {child_data.name}: {e}")

    print(f"Industries seeded successfully!\n")


def main():
    """Main seed function."""
    print("=" * 60)
    print("Starting ontology seeding...")
    print("=" * 60)
    print()

    db = SessionLocal()
    try:
        seed_job_titles(db)
        seed_technologies(db)
        seed_standards(db)
        seed_industries(db)

        print("=" * 60)
        print("✓ All ontology data seeded successfully!")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
