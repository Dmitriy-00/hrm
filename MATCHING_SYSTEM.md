# Advanced Candidate-Vacancy Matching System

## Обзор

Продвинутая система анализа и подбора кандидатов с использованием множественных метрик, семантического анализа текста, анализа карьерных траекторий и оценки культурного соответствия.

## Архитектура системы

### 1. Базовый скоринг (ScoringService)
Основная система оценки совпадения кандидатов и вакансий.

#### Компоненты оценки:
- **Technologies (технологии)** - вес по умолчанию: 30%
  - Соответствие требуемых технологий
  - Уровень владения (proficiency)
  - Опыт работы с технологией (в месяцах)
  - Важность технологии (required/nice_to_have/plus)

- **Experience (опыт)** - вес по умолчанию: 20%
  - Общий опыт работы
  - Соответствие минимальным/максимальным требованиям
  - Штрафы за недостаток или избыток опыта

- **Skills (навыки)** - вес по умолчанию: 15%
  - Совпадение навыков из workplace
  - Анализ требуемых vs имеющихся навыков

- **Languages (языки)** - вес по умолчанию: 10%
  - Соответствие языковых требований
  - Уровни владения (A1-C2, native)
  - Обязательные vs желательные языки

- **Location (локация)** - вес по умолчанию: 10%
  - Удаленная работа
  - Готовность к релокации
  - Совпадение города/страны

- **Salary (зарплата)** - вес по умолчанию: 10%
  - Пересечение зарплатных ожиданий
  - Учет переговорной позиции

- **Industry (индустрия)** - вес по умолчанию: 3%
  - Опыт в релевантных отраслях

- **Standards (стандарты)** - вес по умолчанию: 2%
  - Знание методологий и стандартов

### 2. Семантический анализ (TextAnalysisService)

Анализирует текстовые описания для глубокого понимания соответствия.

#### Возможности:

**Taxonomy-based Skill Extraction:**
- Технические навыки: 60+ технологий (Python, JavaScript, Docker, Kubernetes, etc.)
- Фреймворки: React, Django, Spring Boot, и др.
- Инструменты: Git, Jira, Figma, и др.
- Методологии: Agile, Scrum, TDD, DevOps, и др.
- Soft skills: Leadership, Communication, Problem Solving, и др.

**Synonym Mapping:**
- js → javascript
- k8s → kubernetes
- ml → machine learning
- ts → typescript
- и др.

**Text Similarity:**
- Jaccard similarity для сравнения текстов
- Keyword overlap analysis
- Key phrase extraction (n-grams)

**Sentiment Analysis:**
- Анализ позитивных/негативных слов
- Оценка тональности резюме (0-100)

**Readability Score:**
- Оценка читаемости текста
- Анализ структуры предложений

#### Метрики:
- `bio_description_similarity` (0-100): семантическое сходство текстов
- `skill_extraction_match` (0-100): совпадение извлеченных навыков
- `keyword_overlap` (0-100): процент совпадающих ключевых слов
- `missing_keywords`: важные ключевые слова, отсутствующие у кандидата

### 3. Анализ карьерной траектории (CareerAnalysisService)

Глубокий анализ карьерного пути кандидата.

#### Career Trend (Карьерный тренд):
- **Direction** (направление):
  - `upward`: восходящая карьера
  - `stable`: стабильная карьера
  - `lateral`: горизонтальное движение
  - `downward`: нисходящая траектория

- **Growth Rate** (0-100): скорость карьерного роста
- **Consistency** (0-100): стабильность работы (tenure)
- **Specialization Level** (0-100): уровень специализации
- **Leadership Progression**: наличие карьерного роста в руководство
- **Technical Depth Growth**: рост технической экспертизы

#### Role Progression (Прогресс позиций):
- **Role Hierarchy**:
  ```
  intern (1) → junior (2) → developer (3) → middle (4) →
  senior (5) → tech_lead (6) → team_lead (7) → manager (8) →
  senior_manager (9) → director (10) → vp (11) → cto (12)
  ```
- **Promotions Count**: количество повышений
- **Avg Tenure**: средняя продолжительность работы
- **Job Hopping Score** (0-100): оценка стабильности (выше = стабильнее)
  - ≥36 мес: 95%
  - ≥30 мес: 85%
  - ≥24 мес: 75%
  - ≥18 мес: 60%
  - ≥12 мес: 40%
  - <12 мес: 20%
- **Role Diversity**: разнообразие ролей

#### Technical Growth (Технический рост):
- **Technologies Learned**: количество изученных технологий
- **Tech Stack Modernity** (0-100): современность технологий
  - Modern: React, Vue, Kubernetes, TypeScript, Go, Rust, ML, etc.
  - Legacy: COBOL, Fortran, VB6, Flash, etc.
- **Breadth vs Depth**:
  - `specialist`: ≤5 технологий (глубина)
  - `balanced`: 6-14 технологий
  - `generalist`: ≥15 технологий (широта)
- **Learning Velocity** (0-100): скорость освоения новых технологий
- **Tech Leadership**: опыт технического лидерства

#### Red Flags (Красные флаги):
- Частые смены работы (<1 года)
- Нисходящая траектория
- Отсутствие продвижений при длительной работе
- Пробелы в трудоустройстве

#### Career Stage (Карьерный этап):
- `junior`: начальный уровень
- `mid`: средний уровень
- `senior`: старший уровень
- `lead`: лидерские позиции
- `executive`: executive уровень

#### Potential Score (0-100):
Комплексная оценка потенциала на основе:
- Карьерного тренда (+20 за upward)
- Growth rate
- Consistency
- Количества продвижений (+5 за каждое)
- Job stability
- Технических навыков
- Штрафы за red flags (-8 за каждый)

### 4. Культурное соответствие (CulturalFitScore)

Оценка соответствия корпоративной культуре и рабочей среде.

#### Компоненты:
- **Company Size Fit** (0-100): соответствие размеру компании
- **Work Style Fit** (0-100):
  - Remote work preferences
  - Hybrid/office preferences
  - Relocation willingness
- **Team Environment Fit** (0-100):
  - Leadership experience для leadership ролей
  - Командный опыт
- **Values Alignment** (0-100):
  - На основе career consistency
  - Стабильность vs частые смены

### 5. Продвинутый скоринг (AdvancedScoringService)

Объединяет все компоненты для финального результата.

#### Final Score Calculation:
```
Final Score =
  Base Score × 0.60 +
  Semantic Match × 0.15 +
  Career Score × 0.15 +
  Cultural Fit × 0.10 -
  Red Flag Penalty
```

Where:
- **Base Score**: стандартный scoring (tech, exp, skills, etc.)
- **Semantic Match**: среднее из similarity, skill match, keyword overlap
- **Career Score**: среднее из growth rate, consistency, potential
- **Cultural Fit**: overall cultural fit score
- **Red Flag Penalty**: 3 балла за каждый red flag (max 10)

#### Recommendation Levels:
- **highly_recommend** (≥85): настоятельно рекомендуется
- **recommend** (70-84): рекомендуется
- **consider** (55-69): рассмотреть
- **not_recommend** (<55 или >2 missing critical requirements): не рекомендуется

#### Match Explanation:
Автоматически генерируется детальное объяснение:
- Общая оценка совпадения
- Техническое соответствие
- Уровень опыта
- Карьерная траектория
- Культурное соответствие
- Семантическое совпадение

### 6. ML Feature Extraction

Система извлекает 30+ нормализованных фичей (0-1) для машинного обучения:

#### Базовые скоринговые фичи:
- tech_score, experience_score, skills_score, language_score
- location_score, salary_score
- tech_matched_ratio, tech_required_count
- experience_years, experience_match

#### Семантические фичи:
- semantic_similarity, skill_extraction_match, keyword_overlap

#### Карьерные фичи:
- career_growth_rate, career_consistency, career_potential
- promotions_count, job_stability
- tech_breadth, tech_modernity
- has_leadership (binary)

#### Культурные фичи:
- cultural_fit, work_style_fit, team_fit

#### Метрики качества:
- red_flags_count, match_confidence
- missing_critical_ratio, salary_compatible
- career_stage_level, tech_breadth_type

## API Endpoints

### Advanced Matching

#### POST `/api/v1/advanced-matching/advanced-score`
Расчет продвинутого скоринга.

**Request:**
```json
{
  "candidate_id": "uuid",
  "vacancy_id": "uuid",
  "weights": {
    "technologies": 30,
    "experience": 20,
    "skills": 15,
    "languages": 10,
    "location": 10,
    "salary": 10,
    "industry": 3,
    "standards": 2
  },
  "include_ml_features": false
}
```

**Response:**
```json
{
  "base_score": { /* CandidateVacancyScore */ },
  "semantic_match": {
    "bio_description_similarity": 75.5,
    "skill_extraction_match": 82.3,
    "keyword_overlap": 68.2,
    "missing_keywords": ["docker", "kubernetes"],
    "key_phrases_match": ["full stack", "team leadership"]
  },
  "career_analysis": {
    "career_trend": {
      "direction": "upward",
      "growth_rate": 85.0,
      "consistency": 78.0,
      "specialization_level": 65.0,
      "leadership_progression": true,
      "technical_depth_growth": true
    },
    "role_progression": {
      "role_levels": ["developer", "senior", "tech_lead"],
      "promotions_count": 2,
      "avg_tenure_months": 28.5,
      "job_hopping_score": 80.0,
      "role_diversity_score": 75.0
    },
    "technical_growth": {
      "technologies_learned": 12,
      "tech_stack_modernity": 85.0,
      "breadth_vs_depth": "balanced",
      "learning_velocity": 75.0,
      "tech_leadership": true
    },
    "red_flags": [],
    "strengths": [
      "Strong upward career trajectory",
      "Multiple promotions",
      "Modern technology stack"
    ],
    "career_stage": "senior",
    "potential_score": 88.5
  },
  "cultural_fit": {
    "company_size_fit": 70.0,
    "work_style_fit": 100.0,
    "team_environment_fit": 95.0,
    "values_alignment": 85.0,
    "overall_fit": 87.5,
    "fit_explanation": "Remote work preferences align; Has leadership experience"
  },
  "final_score": 87.5,
  "match_explanation": "This is an excellent match...",
  "detailed_strengths": [...],
  "detailed_concerns": [...],
  "recommendation": "highly_recommend",
  "ml_features": { /* 30+ normalized features */ }
}
```

#### POST `/api/v1/advanced-matching/batch-score`
Массовая оценка кандидатов.

**Request:**
```json
{
  "vacancy_id": "uuid",
  "candidate_ids": ["uuid1", "uuid2", ...],
  "use_advanced_scoring": true,
  "include_ml_features": false
}
```

**Response:**
```json
{
  "vacancy_id": "uuid",
  "results": [ /* Array of AdvancedMatchingResult */ ],
  "processing_time_seconds": 2.45,
  "total_candidates": 50
}
```

#### GET `/api/v1/advanced-matching/career-analysis/{candidate_id}`
Анализ карьеры кандидата.

**Response:** `CareerAnalysis` object

#### POST `/api/v1/advanced-matching/text-analysis/extract-skills`
Извлечение навыков из текста.

**Request:**
```json
{
  "text": "Senior Python developer with 5 years experience in Django..."
}
```

**Response:**
```json
{
  "technical_skills": ["python", "django", ...],
  "soft_skills": ["leadership", ...],
  "tools": ["git", "docker", ...],
  "frameworks": ["django", "react", ...],
  "methodologies": ["agile", "scrum", ...]
}
```

#### POST `/api/v1/advanced-matching/text-analysis/similarity`
Расчет семантической схожести текстов.

**Request:**
```json
{
  "text1": "...",
  "text2": "..."
}
```

**Response:**
```json
{
  "similarity_score": 75.5,
  "interpretation": "Very similar"
}
```

#### GET `/api/v1/advanced-matching/matching/recommendations/{vacancy_id}`
Получить рекомендованных кандидатов.

**Query params:**
- `min_score`: минимальный балл (default: 60.0)
- `limit`: количество результатов (default: 20)

**Response:**
```json
{
  "vacancy_id": "uuid",
  "candidates": [
    {
      "candidate_id": "uuid",
      "candidate_name": "John Doe",
      "score": 92.5,
      "recommendation": "highly_recommend",
      "match_quality": "excellent",
      "highlights": ["...", "...", "..."],
      "concerns": ["...", "...", "..."]
    }
  ],
  "total_found": 15,
  "min_score_threshold": 60.0
}
```

#### POST `/api/v1/advanced-matching/explain-match`
Детальное объяснение совпадения.

**Request:**
```json
{
  "candidate_id": "uuid",
  "vacancy_id": "uuid"
}
```

**Response:**
```json
{
  "candidate": { "id": "...", "name": "...", "grade": "..." },
  "vacancy": { "id": "...", "position": "...", "company": "..." },
  "final_score": 87.5,
  "recommendation": "highly_recommend",
  "explanation": "...",
  "breakdown": {
    "technical": 85.0,
    "experience": 90.0,
    "cultural_fit": 87.5,
    "semantic_match": 75.5,
    "career_potential": 88.5
  },
  "strengths": [...],
  "concerns": [...],
  "career_insights": {
    "stage": "senior",
    "trajectory": "upward",
    "growth_rate": 85.0,
    "red_flags": []
  },
  "missing_requirements": []
}
```

## Использование

### Пример 1: Простой расчет скоринга

```python
from app.services.advanced_scoring_service import AdvancedScoringService
from app.models.schemas.scoring import ScoringWeights

result = AdvancedScoringService.calculate_advanced_score(
    db=db,
    candidate=candidate,
    vacancy=vacancy,
    weights=ScoringWeights(),
    include_ml_features=False
)

print(f"Final Score: {result.final_score}")
print(f"Recommendation: {result.recommendation}")
print(f"Explanation: {result.match_explanation}")
```

### Пример 2: Анализ карьеры

```python
from app.services.career_analysis_service import CareerAnalysisService

analysis = CareerAnalysisService.analyze_career(
    workplaces=workplaces,
    candidate_grade="Senior"
)

print(f"Career Stage: {analysis.career_stage}")
print(f"Trajectory: {analysis.career_trend.direction}")
print(f"Potential: {analysis.potential_score}")
print(f"Red Flags: {analysis.red_flags}")
```

### Пример 3: Извлечение навыков

```python
from app.services.text_analysis_service import TextAnalysisService

skills = TextAnalysisService.extract_skills(resume_text)

print(f"Technical Skills: {skills.technical_skills}")
print(f"Frameworks: {skills.frameworks}")
print(f"Tools: {skills.tools}")
```

### Пример 4: ML Feature Extraction

```python
result = AdvancedScoringService.calculate_advanced_score(
    db=db,
    candidate=candidate,
    vacancy=vacancy,
    include_ml_features=True
)

# Получить фичи для ML модели
features = result.ml_features
# features содержит 30+ нормализованных фичей (0-1)

# Можно использовать для обучения ML модели:
# X_train.append(list(features.values()))
# y_train.append(1 if hired else 0)
```

## Преимущества системы

### 1. Многомерный анализ
- 8 основных метрик базового скоринга
- Семантический анализ текста
- Анализ карьерной траектории
- Оценка культурного соответствия

### 2. Глубокое понимание
- Не просто совпадение ключевых слов
- Анализ карьерного пути и потенциала
- Идентификация red flags
- Оценка soft skills и культурного fit

### 3. Transparency (Прозрачность)
- Детальные объяснения решений
- Breakdown по всем компонентам
- Списки strengths и concerns
- Рекомендации с обоснованием

### 4. ML-Ready
- Извлечение нормализованных фичей
- Готовность к обучению моделей
- Можно использовать для:
  - Предсказания успешности найма
  - Ranking кандидатов
  - Automatic screening

### 5. Масштабируемость
- Batch processing
- Эффективная обработка больших объемов
- Кэширование результатов
- Background tasks поддержка

## Roadmap и улучшения

### Ближайшие улучшения:
1. **NLP Enhancement**
   - BERT/Transformer embeddings
   - Named Entity Recognition
   - Resume parsing

2. **ML Models**
   - Gradient Boosting для ranking
   - Neural networks для matching
   - Transfer learning

3. **Additional Factors**
   - Education matching
   - Certification analysis
   - Publication/portfolio analysis
   - Social media analysis

4. **Performance**
   - Redis caching
   - Async processing
   - Elasticsearch integration

5. **UI Integration**
   - Visual explanations
   - Interactive dashboards
   - Real-time matching

## Тестирование

Система включает unit tests для всех компонентов:
- `tests/services/test_text_analysis_service.py`
- `tests/services/test_career_analysis_service.py`
- `tests/services/test_advanced_scoring_service.py`

## Лицензия

MIT License
