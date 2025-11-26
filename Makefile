.PHONY: help build up down logs clean install-backend install-frontend migrate seed test

help:
	@echo "HRM Platform - Available commands:"
	@echo ""
	@echo "Docker commands:"
	@echo "  make build              - Build all Docker containers"
	@echo "  make up                 - Start all services"
	@echo "  make down               - Stop all services"
	@echo "  make logs               - Show logs from all services"
	@echo "  make clean              - Remove all containers and volumes"
	@echo ""
	@echo "Development commands:"
	@echo "  make install-backend    - Install backend dependencies"
	@echo "  make install-frontend   - Install frontend dependencies"
	@echo "  make dev-backend        - Run backend development server"
	@echo "  make dev-frontend       - Run frontend development server"
	@echo ""
	@echo "Database commands:"
	@echo "  make migrate            - Run database migrations"
	@echo "  make migrate-create     - Create new migration"
	@echo "  make seed               - Populate database with test data"
	@echo "  make seed-ontology      - Seed ontology data only"
	@echo "  make seed-candidates    - Seed candidates only"
	@echo "  make seed-vacancies     - Seed vacancies only"
	@echo ""
	@echo "Testing commands:"
	@echo "  make test-backend       - Run backend tests"
	@echo "  make test-frontend      - Run frontend tests"
	@echo "  make test-scoring       - Test scoring algorithm"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	rm -rf backend/__pycache__
	rm -rf backend/app/__pycache__
	rm -rf frontend/.next
	rm -rf frontend/node_modules

install-backend:
	cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

migrate:
	cd backend && alembic upgrade head

migrate-create:
	@read -p "Enter migration message: " msg; \
	cd backend && alembic revision --autogenerate -m "$$msg"

test-backend:
	cd backend && pytest

test-frontend:
	cd frontend && npm run test

dev-backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev

# Database seeding
seed: seed-ontology seed-candidates seed-vacancies
	@echo "✅ Database seeded with test data"

seed-ontology:
	cd backend && python scripts/seed_ontology.py

seed-candidates:
	cd backend && python scripts/seed_candidates.py

seed-vacancies:
	cd backend && python scripts/seed_vacancies.py

test-scoring:
	cd backend && python scripts/test_scoring.py

# Setup from scratch
setup: install-backend migrate seed
	@echo "✅ Backend setup complete!"
	@echo "Run 'make dev-backend' to start the server"
