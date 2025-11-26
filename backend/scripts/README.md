# Database Seed Scripts

This directory contains scripts for seeding the database with initial data.

## Available Scripts

### seed_ontology.py

Seeds the ontology data (reference dictionaries):
- **Job Titles**: Hierarchical structure of job positions
- **Technologies**: Programming languages, frameworks, databases, tools
- **Standards**: Methodologies, principles, protocols, patterns
- **Industries**: Industry classifications and sub-industries

**Usage:**

```bash
# From backend directory
python scripts/seed_ontology.py

# Or with Docker
docker-compose exec backend python scripts/seed_ontology.py
```

**What gets seeded:**

1. **Job Titles** (~20 items):
   - Developer → Backend → Python, Java, Node.js, Go
   - Developer → Frontend → React, Vue, Angular
   - Developer → Full Stack, Mobile, DevOps, Data Engineer, QA
   - Designer
   - Manager

2. **Technologies** (~40+ items):
   - Languages: Python, JavaScript, TypeScript, Java, Go, C#, PHP, Ruby
   - Frameworks: Django, FastAPI, Flask, React, Vue, Angular, Node.js, Next.js
   - Databases: PostgreSQL, MongoDB, Redis, MySQL
   - DevOps: Docker, Kubernetes, Git, GitHub Actions

3. **Standards** (~10 items):
   - Methodologies: Agile, Scrum, Kanban
   - Principles: SOLID, DRY, KISS
   - Practices: TDD, CI/CD
   - Protocols: REST, GraphQL

4. **Industries** (~8 items):
   - FinTech → Banking, Blockchain, Payments
   - HealthTech
   - EdTech
   - E-commerce
   - GameDev

## Notes

- Scripts are idempotent - safe to run multiple times
- Existing records are skipped
- Hierarchical relationships are preserved
- All data includes metadata and descriptions
