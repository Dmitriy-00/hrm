# HRM Platform Frontend

Next.js 14 приложение для работы с HRM Platform API.

## Технологии

- **Next.js 14** с App Router
- **TypeScript** в strict mode
- **TailwindCSS** для стилей
- **React Query** для работы с API
- **Zustand** для state management
- **React Hook Form + Zod** для форм
- **Radix UI** компоненты
- **Lucide React** иконки

## Быстрый старт

### Установка зависимостей

```bash
npm install
```

### Настройка окружения

Создайте `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Запуск

```bash
# Development
npm run dev

# Build
npm run build

# Production
npm start

# Lint
npm run lint
```

Приложение будет доступно на http://localhost:3000

## Структура проекта

```
src/
├── app/                    # Next.js App Router pages
│   ├── page.tsx           # Главная страница (Dashboard)
│   ├── layout.tsx         # Root layout
│   ├── candidates/        # Страницы кандидатов (TODO)
│   ├── vacancies/         # Страницы вакансий (TODO)
│   └── ontology/          # Страницы онтологии (TODO)
├── components/            # React компоненты
│   └── Navigation.tsx     # Главная навигация
├── lib/                   # Утилиты и hooks
│   ├── api.ts            # Axios клиент с interceptors
│   ├── providers.tsx     # React Query provider
│   ├── utils.ts          # Утилиты
│   └── hooks/            # Custom hooks
│       ├── useCandidates.ts
│       ├── useVacancies.ts
│       ├── useMatching.ts
│       └── useOntology.ts
└── types/                # TypeScript типы
    └── index.ts          # Все типы API

```

## Основные компоненты

### API Client (`lib/api.ts`)

Axios клиент с автоматической обработкой:
- Authorization headers (JWT)
- Error handling
- Base URL configuration

### React Query Hooks

#### Candidates
```typescript
import { useCandidates, useCandidate, useCreateCandidate } from '@/lib/hooks/useCandidates';

// Список кандидатов
const { data, isLoading } = useCandidates({ status: 'active' });

// Один кандидат
const { data: candidate } = useCandidate(id);

// Создание
const createMutation = useCreateCandidate();
await createMutation.mutateAsync(candidateData);
```

#### Vacancies
```typescript
import { useVacancies, useVacancy, useCreateVacancy } from '@/lib/hooks/useVacancies';

const { data: vacancies } = useVacancies({ status: 'active' });
```

#### Matching
```typescript
import { useFindVacanciesForCandidate, useCalculateScore } from '@/lib/hooks/useMatching';

// Найти вакансии для кандидата
const { data: matches } = useFindVacanciesForCandidate(candidateId, {
  min_score: 50,
  page: 1,
  page_size: 20
});

// Рассчитать скор
const scoreMutation = useCalculateScore();
const score = await scoreMutation.mutateAsync({ candidateId, vacancyId });
```

## Текущий статус

### ✅ Реализовано

- [x] Базовая структура Next.js 14
- [x] TypeScript конфигурация
- [x] TailwindCSS настройка
- [x] API клиент (Axios)
- [x] React Query setup
- [x] TypeScript типы для всех API entities
- [x] Custom hooks для всех endpoints
- [x] Главная страница (Dashboard)
- [x] Навигация
- [x] Root layout с providers

### 🚧 В разработке

- [ ] Страница списка кандидатов
- [ ] Страница деталей кандидата
- [ ] Страница списка вакансий
- [ ] Страница деталей вакансии
- [ ] Интерфейс матчинга с визуализацией скоров
- [ ] Страницы онтологии
- [ ] Формы создания/редактирования
- [ ] Компоненты для отображения скоров

### 📋 Планируется

- [ ] Аутентификация UI
- [ ] Advanced search компонент
- [ ] Filters sidebar
- [ ] Score visualization components
- [ ] Charts и аналитика
- [ ] Unit тесты
- [ ] E2E тесты

## API Integration

Backend API должен быть запущен на `http://localhost:8000`

```bash
# В папке backend
alembic upgrade head
python scripts/seed_ontology.py
python scripts/seed_candidates.py
python scripts/seed_vacancies.py
uvicorn app.main:app --reload
```

API документация: http://localhost:8000/docs

## Разработка

### Добавление новой страницы

1. Создайте папку в `src/app/`
2. Добавьте `page.tsx` и `layout.tsx` (опционально)
3. Используйте существующие hooks для API

Пример:
```typescript
// src/app/candidates/page.tsx
'use client';

import { useCandidates } from '@/lib/hooks/useCandidates';

export default function CandidatesPage() {
  const { data, isLoading } = useCandidates();

  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      {data?.items.map(candidate => (
        <div key={candidate.id}>{candidate.full_name}</div>
      ))}
    </div>
  );
}
```

### Добавление нового компонента

Компоненты размещайте в `src/components/`

```typescript
// src/components/CandidateCard.tsx
import type { Candidate } from '@/types';

interface Props {
  candidate: Candidate;
}

export function CandidateCard({ candidate }: Props) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold">{candidate.full_name}</h3>
      <p className="text-gray-600">{candidate.email}</p>
    </div>
  );
}
```

## Стилизация

Проект использует TailwindCSS. Основные классы:

```typescript
// Layouts
"container mx-auto px-4"
"grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
"flex items-center justify-between"

// Cards
"bg-white rounded-lg shadow p-6"
"border border-gray-200 hover:border-blue-500"

// Buttons
"px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"

// Text
"text-2xl font-bold text-gray-900"
"text-sm text-gray-600"
```

## Типы

Все типы API находятся в `src/types/index.ts` и соответствуют Pydantic моделям backend.

Основные типы:
- `Candidate` - кандидат
- `Vacancy` - вакансия
- `CandidateVacancyScore` - результат скоринга
- `MatchingResult` - результат матчинга
- `Technology`, `JobTitle`, `Standard`, `Industry` - онтология

## Troubleshooting

### CORS errors

Убедитесь что backend запущен с правильной CORS конфигурацией:

```python
# backend/.env
CORS_ORIGINS=["http://localhost:3000"]
```

### API connection refused

Проверьте что backend запущен:
```bash
curl http://localhost:8000/health
```

### Build errors

```bash
# Очистить кеш
rm -rf .next
npm run build
```

## Полезные ссылки

- [Next.js Documentation](https://nextjs.org/docs)
- [TailwindCSS](https://tailwindcss.com/docs)
- [React Query](https://tanstack.com/query/latest/docs/react/overview)
- [Radix UI](https://www.radix-ui.com/)
- [Backend API Docs](http://localhost:8000/docs)
