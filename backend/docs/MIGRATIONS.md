# Database Migrations Guide

## Overview

This project uses Alembic for managing database migrations with PostgreSQL.

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Database

Copy `.env.example` to `.env` and configure your database connection:

```bash
cp .env.example .env
```

Edit `.env`:
```
DATABASE_URL=postgresql://hrm_user:hrm_password@localhost:5432/hrm_db
```

**Important**: `CORS_ORIGINS` must be a JSON array:
```
CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]
```

## Running Migrations

### Using Docker Compose (Recommended)

```bash
# Start PostgreSQL
docker compose up -d postgres

# Run migrations
docker compose exec backend alembic upgrade head

# Or run from host (if dependencies installed locally)
cd backend
alembic upgrade head
```

### Local PostgreSQL

```bash
cd backend
alembic upgrade head
```

## Common Migration Commands

### View Migration History

```bash
alembic history
```

### Check Current Version

```bash
alembic current
```

### Upgrade to Latest

```bash
alembic upgrade head
```

### Downgrade One Version

```bash
alembic downgrade -1
```

### Downgrade to Specific Version

```bash
alembic downgrade <revision_id>
```

### Create New Migration

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Create empty migration
alembic revision -m "Description of changes"
```

## Initial Migration

The initial migration (`1a84ac592903`) creates all core tables:

### Ontology Tables
- `job_titles` - Hierarchical job title taxonomy
- `technologies` - Technology stack with categories
- `standards` - Development standards and methodologies
- `industries` - Industry classification

### Core Tables
- `users` - System users (recruiters, admins)
- `candidates` - Candidate profiles
- `companies` - Company registry
- `workplaces` - Candidate work history
- `workplace_technologies` - Technologies used at each workplace
- `vacancies` - Job vacancies
- `vacancy_requirements` - Technology requirements for vacancies
- `selections` - Candidate-vacancy matches with scoring

## Database Schema

### Key Relationships

```
Users ─┬─> Candidates
       ├─> Vacancies (created_by)
       └─> Selections (added_by)

JobTitles ──> Candidates, Vacancies, Workplaces
Technologies ──> WorkplaceTechnologies, VacancyRequirements
Industries ──> Companies, Workplaces

Candidates ──> Workplaces ──> WorkplaceTechnologies
Vacancies ──> VacancyRequirements

Selections: Candidates × Vacancies (with score)
```

### Special Features

1. **Hierarchical Structures** (Job Titles, Technologies, Industries)
   - Uses materialized path pattern
   - `parent_id` for tree structure
   - `path` for efficient subtree queries
   - `level` for depth tracking

2. **UUID Primary Keys**
   - All tables use UUID for primary keys
   - Enables distributed systems
   - Better security (no enumeration)

3. **Timestamps**
   - `created_at` - automatic on insert
   - `updated_at` - automatic on update

4. **JSON Fields**
   - `skills`, `languages` - flexible arrays
   - `cv_parsed_data`, `interview_feedback` - structured data
   - Enables schema evolution without migrations

## Seed Data

After running migrations, populate with seed data:

```bash
# Ontology (job titles, technologies, standards, industries)
python scripts/seed_ontology.py

# Test candidates
python scripts/seed_candidates.py

# Test vacancies
python scripts/seed_vacancies.py
```

## Troubleshooting

### Connection Error

```
psycopg2.OperationalError: connection to server at "localhost", port 5432 failed
```

**Solution**: Ensure PostgreSQL is running
```bash
docker compose up -d postgres
# Or start local PostgreSQL service
sudo systemctl start postgresql
```

### Permission Error

```
ERROR: permission denied to create extension "uuid-ossp"
```

**Solution**: Grant superuser or extension creation privileges
```sql
ALTER USER hrm_user CREATEDB;
-- Or connect as superuser
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### Migration Already Applied

```
alembic.util.exc.CommandError: Target database is not up to date
```

**Solution**: Check current version and upgrade
```bash
alembic current
alembic upgrade head
```

### Alembic Can't Find Models

**Solution**: Ensure all models are imported in `app/db/base.py`

## Best Practices

1. **Always Review Auto-Generated Migrations**
   - Check for missing indexes
   - Verify foreign key constraints
   - Add data migrations if needed

2. **Test Migrations**
   - Test both upgrade and downgrade
   - Verify on copy of production data
   - Check performance on large datasets

3. **Version Control**
   - Commit migrations with code changes
   - Never modify applied migrations
   - Use descriptive migration messages

4. **Production Deployments**
   - Backup database before migration
   - Test migrations on staging first
   - Plan for rollback if needed
   - Consider zero-downtime strategies

## Migration Strategy

### Development
```bash
# Make model changes
# Generate migration
alembic revision --autogenerate -m "Add new field"
# Review and edit if needed
# Test migration
alembic upgrade head
alembic downgrade -1
alembic upgrade head
```

### Production
```bash
# Backup
pg_dump hrm_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Run migration
alembic upgrade head

# If issues occur
alembic downgrade -1  # Rollback
# Or restore from backup
```

## Known Issues

1. **Reserved Column Names**
   - `metadata` is reserved in SQLAlchemy
   - Use `tech_metadata` or similar alternatives

2. **Array Default Values**
   - PostgreSQL arrays need proper defaults
   - Use `default=[]` in Column definition

3. **JSON Fields**
   - Use `postgresql.JSON()` for better typing
   - Default to `{}` or `[]` as appropriate

## References

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Arrays](https://www.postgresql.org/docs/current/arrays.html)
- [PostgreSQL JSON](https://www.postgresql.org/docs/current/datatype-json.html)
