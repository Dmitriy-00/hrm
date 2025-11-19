# Candidate-Vacancy Scoring System

## Overview

The scoring system provides intelligent matching between candidates and vacancies using a multi-dimensional algorithm that evaluates compatibility across 8 key areas.

## Scoring Components

### 1. Technologies (40% weight)
- Matches candidate's technology experience against vacancy requirements
- Considers:
  - Technology proficiency level (1-5 scale)
  - Years of experience with each technology
  - Importance level (required/nice_to_have/plus)
- Weighted scoring: required (1.0), nice_to_have (0.5), plus (0.25)

### 2. Experience (20% weight)
- Compares total work experience against requirements
- Handles min/max experience ranges
- Penalties for under-qualification
- Slight penalty for significant over-qualification

### 3. Skills (15% weight)
- Matches soft skills and general competencies
- Tracks matched and missing skills

### 4. Standards (10% weight)
- Evaluates familiarity with methodologies (Agile, SCRUM, etc.)
- Domain standards and best practices

### 5. Industry (5% weight)
- Checks for relevant industry experience
- Considers duration of industry exposure

### 6. Languages (5% weight)
- Validates language proficiency requirements
- Uses CEFR levels (A1-C2) and native
- Ensures minimum required levels are met

### 7. Location (3% weight)
- Evaluates location compatibility
- Considers remote work and relocation preferences

### 8. Salary (2% weight)
- Checks for salary range overlap
- Handles negotiable salaries

## Bonus Points

Additional points awarded for:
- **Excess Experience**: +1-5 points for significantly more experience than required
- **Diverse Experience**: +2 points for 3+ companies
- **Leadership**: +3 points for tech lead/team lead experience

## Match Quality Levels

- **Excellent** (≥80 points): Outstanding match, highly recommended
- **Good** (65-79 points): Strong match, recommended
- **Fair** (50-64 points): Acceptable match, worth considering
- **Poor** (<50 points): Significant gaps exist

## API Endpoints

### Calculate Score for Specific Pair
```
POST /api/v1/matching/score
Query Parameters:
  - candidate_id: UUID
  - vacancy_id: UUID
  - weights: Optional[ScoringWeights]

Response: CandidateVacancyScore
```

### Find Vacancies for Candidate
```
GET /api/v1/matching/candidates/{candidate_id}/vacancies
Query Parameters:
  - min_score: float (default: 50.0)
  - match_quality: string (excellent|good|fair|poor)
  - page: int
  - page_size: int
  - sort_by: string (score|confidence)
  - sort_order: string (asc|desc)

Response: MatchingListResponse
```

### Find Candidates for Vacancy
```
GET /api/v1/matching/vacancies/{vacancy_id}/candidates
Query Parameters: (same as above)

Response: MatchingListResponse
```

### Batch Scoring
```
POST /api/v1/matching/batch-score
Body: MatchingParams
  - Either candidate_id OR vacancy_id
  - Filters and pagination

Response: MatchingListResponse
```

## Response Structure

### CandidateVacancyScore
```json
{
  "candidate_id": "uuid",
  "vacancy_id": "uuid",
  "total_score": 75.5,
  "breakdown": {
    "technologies": {
      "score": 80.0,
      "matched": 4,
      "required": 5,
      "details": [...]
    },
    "experience": {...},
    "skills": {...},
    "standards": {...},
    "industry": {...},
    "languages": {...},
    "location": {...},
    "salary": {...}
  },
  "confidence_level": 85.0,
  "missing_critical_requirements": ["React", "TypeScript"],
  "bonus_points": [
    {
      "reason": "Leadership experience",
      "points": 3.0
    }
  ],
  "match_quality": "good",
  "calculated_at": "2024-01-15T10:30:00Z"
}
```

### MatchingResult
```json
{
  "candidate_id": "uuid",
  "vacancy_id": "uuid",
  "candidate": {...},  // Or null if searching for candidates
  "vacancy": {...},    // Or null if searching for vacancies
  "score": {...},      // CandidateVacancyScore
  "highlights": [
    "Strong technology match: 4/5 required technologies",
    "Excellent experience level: 6.5 years",
    "+ Leadership experience"
  ],
  "concerns": [
    "Missing 1 required technologies",
    "No experience in the required industry"
  ],
  "recommendation": null  // Future: AI-generated recommendation
}
```

## Customizing Weights

Default weights can be overridden per-request:

```json
{
  "technologies": 40,
  "experience": 20,
  "skills": 15,
  "standards": 10,
  "industry": 5,
  "languages": 5,
  "location": 3,
  "salary": 2
}
```

All weights must sum to 100.

## Testing

Run the test script to verify scoring with seed data:

```bash
cd backend
python scripts/test_scoring.py
```

This will:
1. Load candidates and vacancies from the database
2. Calculate scores for all combinations
3. Display detailed breakdowns, highlights, and concerns
4. Verify all scoring components work correctly

## Implementation Details

### Technology Matching
- Fetches all workplace technologies for the candidate
- Compares proficiency and experience for each required technology
- Applies importance-based weighting
- Calculates percentage of requirements met

### Experience Calculation
- Uses materialized `experience_months` field from candidate
- Automatically updated when workplaces are added/modified
- Compares against min/max requirements with smart scoring

### Language Proficiency
CEFR level mapping:
- A1 = 1 (Beginner)
- A2 = 2 (Elementary)
- B1 = 3 (Intermediate)
- B2 = 4 (Upper Intermediate)
- C1 = 5 (Advanced)
- C2 = 6 (Proficient)
- native = 7 (Native Speaker)

### Confidence Calculation
Based on:
- Data completeness (candidate profile filled out)
- Number of requirements evaluated
- Clarity of requirements (specific vs. vague)
- Amount of historical data available

## Future Enhancements

1. **AI Recommendations**: GPT-generated personalized recommendations
2. **Learning**: Adjust weights based on successful placements
3. **Clustering**: Group similar candidates/vacancies
4. **Trend Analysis**: Track market demand for specific skills
5. **Feedback Loop**: Incorporate recruiter feedback to improve scoring
