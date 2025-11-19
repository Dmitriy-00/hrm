.PHONY: help build up down logs clean install-backend install-frontend migrate test

help:
	@echo "HRM Platform - Available commands:"
	@echo "  make build              - Build all Docker containers"
	@echo "  make up                 - Start all services"
	@echo "  make down               - Stop all services"
	@echo "  make logs               - Show logs from all services"
	@echo "  make clean              - Remove all containers and volumes"
	@echo "  make install-backend    - Install backend dependencies"
	@echo "  make install-frontend   - Install frontend dependencies"
	@echo "  make migrate            - Run database migrations"
	@echo "  make test               - Run tests"

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
