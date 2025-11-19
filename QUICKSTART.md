# Quick Start Guide - HRM Platform

Это руководство поможет вам запустить HRM Platform за 5 минут.

## Вариант 1: Быстрый старт с Docker (рекомендуется)

### Требования
- Docker
- Docker Compose

### Шаги

```bash
# 1. Клонировать репозиторий
git clone <repository-url>
cd hrm

# 2. Запустить PostgreSQL
docker compose up -d postgres

# 3. Подождать пока PostgreSQL запустится (5-10 секунд)
docker compose logs -f postgres
# Дождитесь сообщения "database system is ready to accept connections"

# 4. Запустить backend
docker compose up -d backend

# 5. Применить миграции
docker compose exec backend alembic upgrade head

# 6. Заполнить тестовыми данными
docker compose exec backend python scripts/seed_ontology.py
docker compose exec backend python scripts/seed_candidates.py
docker compose exec backend python scripts/seed_vacancies.py

# 7. Готово! API доступен на http://localhost:8000
```

Откройте в браузере:
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Вариант 2: Локальная разработка (без Docker)

### Требования
- Python 3.11+
- PostgreSQL 15+
- Redis (опционально)

### Шаги

```bash
# 1. Клонировать репозиторий
git clone <repository-url>
cd hrm/backend

# 2. Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Настроить .env файл
cp .env.example .env
# Отредактируйте .env и установите DATABASE_URL

# 5. Применить миграции
alembic upgrade head

# 6. Заполнить тестовыми данными
python scripts/seed_ontology.py
python scripts/seed_candidates.py
python scripts/seed_vacancies.py

# 7. Запустить сервер
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Вариант 3: Использование Makefile

Если у вас установлен `make`:

```bash
# Установить зависимости, применить миграции и заполнить данными
make setup

# Запустить dev сервер
make dev-backend
```

## Тестирование API

### 1. Проверка здоровья

```bash
curl http://localhost:8000/health
```

Ожидаемый ответ:
```json
{
  "status": "healthy",
  "environment": "development",
  "version": "0.1.0"
}
```

### 2. Получить список технологий

```bash
curl http://localhost:8000/api/v1/technologies
```

### 3. Получить список кандидатов

```bash
curl http://localhost:8000/api/v1/candidates
```

### 4. Найти вакансии для кандидата

```bash
# Сначала получите ID кандидата из предыдущего запроса
CANDIDATE_ID="<uuid>"

curl "http://localhost:8000/api/v1/matching/candidates/${CANDIDATE_ID}/vacancies?min_score=50"
```

### 5. Рассчитать скор для пары кандидат-вакансия

```bash
CANDIDATE_ID="<uuid>"
VACANCY_ID="<uuid>"

curl -X POST "http://localhost:8000/api/v1/matching/score?candidate_id=${CANDIDATE_ID}&vacancy_id=${VACANCY_ID}"
```

## Тестовые данные

После выполнения seed скриптов у вас будет:

### Кандидаты (3)
1. **Иван Петров** - Python Backend Developer (Middle, 4+ года)
   - Python, Django, PostgreSQL, Docker, Redis
   - Зарплата: 150-250k RUB

2. **Мария Смирнова** - Senior React Developer (6+ лет)
   - React, TypeScript, Next.js, Node.js
   - Зарплата: 200-300k RUB

3. **Алексей Козлов** - Full Stack Developer (Middle, 1.8 года)
   - Node.js, React, MongoDB
   - Зарплата: 120-200k RUB

### Вакансии (3)
1. **Senior Python Backend Developer** @ TechCorp
   - Python, Django, PostgreSQL, Docker, Redis (required)
   - Зарплата: 200-300k RUB

2. **Middle React Developer** @ StartupHub
   - React, TypeScript, Redux (required)
   - Зарплата: 150-220k RUB

3. **Full Stack Node.js + React** @ FinanceStream
   - Node.js, React, MongoDB (required)
   - Зарплата: 180-250k RUB net

### Онтология
- **Job Titles**: ~20 должностей (Backend, Frontend, Full Stack, DevOps, etc.)
- **Technologies**: ~40+ технологий (Python, JavaScript, React, Django, etc.)
- **Standards**: ~10 стандартов (Agile, SCRUM, REST, GraphQL, etc.)
- **Industries**: ~10 индустрий (IT, Finance, E-commerce, etc.)

## Тестирование скоринга

Запустите тестовый скрипт для проверки работы алгоритма:

```bash
cd backend
python scripts/test_scoring.py
```

Этот скрипт:
- Загрузит всех кандидатов и вакансии
- Рассчитает скоры для всех комбинаций
- Покажет детальные breakdown, highlights и concerns
- Проверит корректность всех компонентов скоринга

## Swagger UI

После запуска откройте http://localhost:8000/docs

В Swagger UI вы можете:
- Просмотреть все доступные endpoints
- Протестировать API прямо в браузере
- Посмотреть схемы запросов и ответов
- Скачать OpenAPI spec

## Примеры запросов

### Создать нового кандидата

```bash
curl -X POST "http://localhost:8000/api/v1/candidates" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test Candidate",
    "email": "test@example.com",
    "grade": "middle",
    "skills": ["Python", "FastAPI", "PostgreSQL"],
    "salary_min": 150000,
    "salary_max": 250000,
    "current_location": "Moscow"
  }'
```

### Создать вакансию

```bash
curl -X POST "http://localhost:8000/api/v1/vacancies" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Test Company",
    "position_name": "Senior Backend Developer",
    "grade": "senior",
    "min_experience_years": 3,
    "salary_min": 200000,
    "salary_max": 350000,
    "locations": [{"city": "Moscow", "remote": true}],
    "description": "We are looking for a senior backend developer"
  }'
```

### Расширенный поиск кандидатов

```bash
curl -X POST "http://localhost:8000/api/v1/candidates/search" \
  -H "Content-Type: application/json" \
  -d '{
    "grade": "middle",
    "min_experience_months": 24,
    "salary_max": 300000,
    "status": "active"
  }'
```

## Troubleshooting

### PostgreSQL не запускается

```bash
# Проверьте что порт 5432 свободен
lsof -i :5432

# Остановите все контейнеры
docker compose down

# Удалите volumes и запустите заново
docker compose down -v
docker compose up -d postgres
```

### Миграции не применяются

```bash
# Проверьте текущую версию
alembic current

# Проверьте историю
alembic history

# Если база пустая, примените миграции
alembic upgrade head
```

### Backend не запускается

```bash
# Проверьте логи
docker compose logs backend

# Или для локальной разработки
cd backend
uvicorn app.main:app --reload --log-level debug
```

## Следующие шаги

1. **Изучите API** - откройте Swagger UI и ознакомьтесь с endpoints
2. **Прочитайте документацию**:
   - [backend/docs/SCORING.md](backend/docs/SCORING.md) - алгоритм скоринга
   - [backend/docs/MIGRATIONS.md](backend/docs/MIGRATIONS.md) - работа с миграциями
3. **Экспериментируйте** - создавайте своих кандидатов и вакансии
4. **Тестируйте матчинг** - проверяйте как работает скоринг

## Полезные команды

```bash
# Посмотреть логи
make logs
# или
docker compose logs -f backend

# Остановить все
make down
# или
docker compose down

# Очистить все (включая volumes)
make clean
# или
docker compose down -v

# Запустить тесты
make test-backend

# Создать миграцию
make migrate-create
```

## Готово! 🎉

Теперь у вас запущен полнофункциональный HRM Platform API.

Для вопросов и предложений создавайте Issues в репозитории.
