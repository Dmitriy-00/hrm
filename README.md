# HRM Platform - Система подбора кандидатов и вакансий

Полнофункциональная платформа для автоматизированного подбора IT-специалистов, основанная на семантическом анализе навыков, технологий, опыта и требований.

## 🎯 Основные возможности

- **Интеллектуальный скоринг**: многоуровневая оценка соответствия кандидатов вакансиям
- **Семантический поиск**: поиск по навыкам, технологиям, опыту
- **Онтология компетенций**: иерархическая структура должностей, технологий и стандартов
- **Career Road Map**: автоматическая генерация карьерных траекторий
- **Аналитика рынка**: зарплатная статистика, спрос на технологии
- **Парсинг резюме**: автоматическое извлечение данных из CV

## 🏗️ Архитектура

Проект использует monorepo структуру:

```
hrm/
├── backend/         # FastAPI (Python 3.11+)
├── frontend/        # Next.js 14+ (React 18, TypeScript)
├── database/        # PostgreSQL migrations
└── docker-compose.yml
```

## 🛠️ Технологический стек

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: PostgreSQL 15+
- **Cache**: Redis
- **ORM**: SQLAlchemy
- **Migration**: Alembic
- **Validation**: Pydantic

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **UI Components**: shadcn/ui
- **State Management**: Zustand
- **Data Fetching**: TanStack Query (React Query)
- **Forms**: React Hook Form + Zod

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Reverse Proxy**: Nginx
- **File Storage**: MinIO / S3
- **Search**: PostgreSQL Full-Text Search (MVP) → ElasticSearch (future)

## 🚀 Быстрый старт

### Требования

- Docker и Docker Compose
- Node.js 18+ (для локальной разработки frontend)
- Python 3.11+ (для локальной разработки backend)

### Запуск с Docker

```bash
# Клонировать репозиторий
git clone <repository-url>
cd hrm

# Запустить все сервисы
docker-compose up -d

# Backend будет доступен на http://localhost:8000
# Frontend будет доступен на http://localhost:3000
```

### Локальная разработка

#### Backend

```bash
cd backend

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows

# Установить зависимости
pip install -r requirements.txt

# Запустить миграции
alembic upgrade head

# Запустить сервер
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# Установить зависимости
npm install

# Запустить dev server
npm run dev
```

## 📚 API Документация

После запуска backend, документация API доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Основные эндпоинты

#### Онтология
- `GET /api/v1/job-titles` - Список должностей
- `GET /api/v1/technologies` - Список технологий
- `GET /api/v1/standards` - Список стандартов
- `GET /api/v1/industries` - Список индустрий

#### Кандидаты
- `POST /api/v1/candidates` - Создать кандидата
- `GET /api/v1/candidates` - Список кандидатов
- `POST /api/v1/candidates/search` - Расширенный поиск
- `GET /api/v1/candidates/{id}` - Получить кандидата
- `PATCH /api/v1/candidates/{id}` - Обновить кандидата

#### История работы
- `POST /api/v1/workplaces` - Добавить место работы
- `GET /api/v1/workplaces/candidate/{id}` - История кандидата

#### Вакансии
- `POST /api/v1/vacancies` - Создать вакансию
- `GET /api/v1/vacancies` - Список вакансий
- `POST /api/v1/vacancies/search` - Расширенный поиск
- `PUT /api/v1/vacancies/{id}/requirements` - Обновить требования

#### Матчинг и скоринг
- `POST /api/v1/matching/score` - Рассчитать скор для пары кандидат-вакансия
- `GET /api/v1/matching/candidates/{id}/vacancies` - Найти вакансии для кандидата
- `GET /api/v1/matching/vacancies/{id}/candidates` - Найти кандидатов для вакансии
- `POST /api/v1/matching/batch-score` - Batch scoring с фильтрами

Подробная документация в файлах:
- [backend/docs/SCORING.md](backend/docs/SCORING.md) - Алгоритм скоринга
- [backend/docs/MIGRATIONS.md](backend/docs/MIGRATIONS.md) - Работа с миграциями

## 🗄️ База данных

### Основные таблицы

- `job_titles` - иерархия должностей
- `technologies` - технологии и инструменты
- `standards` - методологии и стандарты
- `industries` - отрасли
- `candidates` - профили кандидатов
- `workplaces` - опыт работы
- `vacancies` - вакансии
- `vacancy_requirements` - требования к вакансиям
- `selections` - процесс отбора

### Миграции

```bash
# Применить миграции
alembic upgrade head

# Откатить миграцию
alembic downgrade -1

# Создать новую миграцию
alembic revision --autogenerate -m "description"

# Просмотреть историю
alembic history

# Проверить текущую версию
alembic current
```

### Заполнение тестовыми данными

```bash
cd backend

# Онтология (должности, технологии, стандарты, индустрии)
python scripts/seed_ontology.py

# Тестовые кандидаты (3 кандидата с полными профилями)
python scripts/seed_candidates.py

# Тестовые вакансии (3 вакансии с требованиями)
python scripts/seed_vacancies.py

# Тест скоринга
python scripts/test_scoring.py
```

Подробная документация: [backend/docs/MIGRATIONS.md](backend/docs/MIGRATIONS.md)

## 🧪 Тестирование

### Backend

```bash
cd backend
pytest
```

### Frontend

```bash
cd frontend
npm run test
```

## 📦 Модули системы

### MVP (Фаза 1) - В РАЗРАБОТКЕ
- [x] Базовая структура проекта
- [x] База данных и миграции (Alembic)
- [x] Онтология (должности, технологии, стандарты, индустрии)
- [x] CRUD для кандидатов + история работы
- [x] CRUD для вакансий + требования
- [x] Расширенный поиск (по технологиям, опыту, локации, зарплате)
- [x] Полный скоринг (8 компонентов: технологии, опыт, навыки, стандарты, индустрия, языки, локация, зарплата)
- [x] API для матчинга кандидатов и вакансий
- [x] Seed скрипты для тестовых данных
- [ ] Аутентификация (JWT)
- [ ] UI для профиля кандидата
- [ ] UI для вакансий и матчинга

### Фаза 2
- [ ] Расширенный скоринг (все параметры)
- [ ] Модуль отбора (selection pipeline)
- [ ] Календарь интервью
- [ ] Базовая аналитика

### Фаза 3
- [ ] Парсер резюме (OCR + NLP)
- [ ] Road Map генератор
- [ ] Банк тестовых вопросов
- [ ] Система уведомлений

### Фаза 4
- [ ] ML-модель для скоринга
- [ ] Интеграция с job boards (hh.ru, LinkedIn)
- [ ] Расширенная аналитика
- [ ] Мобильное приложение

## 🔐 Безопасность

- HTTPS для всех соединений
- JWT токены для аутентификации
- RBAC (Role-Based Access Control)
- Шифрование персональных данных
- GDPR compliance
- Rate limiting
- SQL injection защита (параметризованные запросы)

## 📊 Производительность

- Поиск: < 500ms
- Скоринг: < 200ms
- Поддержка 10,000+ одновременных пользователей
- Кэширование частых запросов (Redis)
- Индексы БД для критичных запросов

## 🤝 Разработка

### Правила кода

- TypeScript в strict mode
- Python type hints обязательны
- ESLint + Prettier для форматирования
- Black + isort для Python
- Покрытие тестами > 80%
- Code review обязателен

### Commit Convention

```
feat: добавить новую функциональность
fix: исправить баг
docs: обновить документацию
style: форматирование кода
refactor: рефакторинг
test: добавить тесты
chore: обновить зависимости
```

## 📝 Лицензия

MIT

## 👥 Команда

- Backend: Python/FastAPI
- Frontend: React/Next.js/TypeScript
- DevOps: Docker/CI/CD

## 📞 Контакты

Для вопросов и предложений создавайте Issues в репозитории.
