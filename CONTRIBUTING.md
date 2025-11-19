# Contributing to HRM Platform

## Development Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (if running locally)

### Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd hrm
```

2. Start all services with Docker:
```bash
make up
```

3. Access the services:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local
cp .env.local.example .env.local

# Start dev server
npm run dev
```

## Code Style

### Python

- Use Black for formatting
- Use isort for import sorting
- Follow PEP 8
- Type hints are required
- Docstrings for public functions

```bash
# Format code
black .
isort .

# Lint
flake8
mypy .
```

### TypeScript/React

- Use ESLint + Prettier
- Follow Airbnb style guide
- Functional components with hooks
- TypeScript strict mode

```bash
# Lint
npm run lint

# Type check
npm run type-check
```

## Database Migrations

Create a new migration:
```bash
make migrate-create
# or
cd backend && alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
make migrate
# or
cd backend && alembic upgrade head
```

## Testing

### Backend Tests

```bash
cd backend
pytest

# With coverage
pytest --cov=app --cov-report=html
```

### Frontend Tests

```bash
cd frontend
npm run test

# With coverage
npm run test:coverage
```

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Write/update tests
4. Ensure all tests pass
5. Update documentation if needed
6. Submit a pull request

## Commit Messages

Follow conventional commits:

- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation changes
- `style:` code formatting
- `refactor:` code refactoring
- `test:` adding tests
- `chore:` maintenance tasks

Example:
```
feat: add candidate search endpoint

- Implement search by skills
- Add pagination support
- Add filtering by location
```

## Project Structure

```
hrm/
├── backend/           # Python FastAPI backend
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── core/     # Configuration
│   │   ├── db/       # Database models
│   │   ├── models/   # Pydantic schemas
│   │   ├── services/ # Business logic
│   │   └── utils/    # Utilities
│   └── tests/
├── frontend/         # Next.js frontend
│   ├── src/
│   │   ├── app/     # Next.js pages
│   │   ├── components/
│   │   ├── lib/
│   │   └── types/
│   └── public/
└── database/         # Database scripts
```

## Questions?

Open an issue or reach out to the maintainers.
