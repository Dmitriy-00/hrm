"""
Advanced Scoring Service with deep analysis and ML-ready features.
Extends the base scoring service with semantic analysis, career trajectory evaluation,
and comprehensive matching explanations.
"""

from typing import List, Dict, Optional, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime
from dataclasses import dataclass, asdict

from app.db.models.candidate import Candidate
from app.db.models.vacancy import Vacancy
from app.db.models.workplace import Workplace
from app.db.models.vacancy_requirement import VacancyRequirement

from app.services.scoring_service import ScoringService
from app.services.text_analysis_service import TextAnalysisService, SkillExtraction
from app.services.career_analysis_service import CareerAnalysisService, CareerAnalysis

from app.models.schemas.scoring import (
    CandidateVacancyScore,
    ScoringWeights,
)


@dataclass
class SemanticMatchResult:
    """Result of semantic text matching."""
    bio_description_similarity: float
    skill_extraction_match: float
    keyword_overlap: float
    missing_keywords: List[str]
    key_phrases_match: List[str]


@dataclass
class CulturalFitScore:
    """Cultural fit assessment."""
    company_size_fit: float  # 0-100
    work_style_fit: float  # 0-100
    team_environment_fit: float  # 0-100
    values_alignment: float  # 0-100
    overall_fit: float  # 0-100
    fit_explanation: str


@dataclass
class AdvancedMatchingResult:
    """Comprehensive matching result with all analyses."""
    base_score: CandidateVacancyScore
    semantic_match: SemanticMatchResult
    career_analysis: CareerAnalysis
    cultural_fit: CulturalFitScore
    final_score: float  # Adjusted score after advanced analysis
    match_explanation: str
    detailed_strengths: List[str]
    detailed_concerns: List[str]
    recommendation: str  # 'highly_recommend', 'recommend', 'consider', 'not_recommend'
    ml_features: Dict[str, float]  # Features for ML training


class AdvancedScoringService:
    """Advanced scoring service with deep analysis."""

    @staticmethod
    def calculate_advanced_score(
        db: Session,
        candidate: Candidate,
        vacancy: Vacancy,
        weights: ScoringWeights = ScoringWeights(),
        include_ml_features: bool = True,
    ) -> AdvancedMatchingResult:
        """
        Calculate comprehensive matching score with advanced analysis.
        """
        # Get base score from standard scoring service
        base_score = ScoringService.calculate_score(db, candidate, vacancy, weights)

        # Get workplaces for advanced analysis
        workplaces = (
            db.query(Workplace)
            .filter(Workplace.candidate_id == candidate.id)
            .all()
        )

        # Perform semantic analysis
        semantic_match = AdvancedScoringService._analyze_semantic_match(
            candidate, vacancy, workplaces
        )

        # Analyze career trajectory
        career_analysis = CareerAnalysisService.analyze_career(
            workplaces, candidate.grade
        )

        # Assess cultural fit
        cultural_fit = AdvancedScoringService._assess_cultural_fit(
            candidate, vacancy, workplaces
        )

        # Calculate final adjusted score
        final_score = AdvancedScoringService._calculate_final_score(
            base_score.total_score,
            semantic_match,
            career_analysis,
            cultural_fit,
        )

        # Generate detailed explanation
        match_explanation = AdvancedScoringService._generate_explanation(
            base_score, semantic_match, career_analysis, cultural_fit, final_score
        )

        # Generate detailed strengths and concerns
        detailed_strengths = AdvancedScoringService._generate_detailed_strengths(
            base_score, semantic_match, career_analysis, cultural_fit
        )
        detailed_concerns = AdvancedScoringService._generate_detailed_concerns(
            base_score, semantic_match, career_analysis, cultural_fit
        )

        # Determine recommendation
        recommendation = AdvancedScoringService._determine_recommendation(
            final_score, len(base_score.missing_critical_requirements), career_analysis
        )

        # Extract ML features if requested
        ml_features = {}
        if include_ml_features:
            ml_features = AdvancedScoringService._extract_ml_features(
                base_score, semantic_match, career_analysis, cultural_fit,
                candidate, vacancy
            )

        return AdvancedMatchingResult(
            base_score=base_score,
            semantic_match=semantic_match,
            career_analysis=career_analysis,
            cultural_fit=cultural_fit,
            final_score=round(final_score, 2),
            match_explanation=match_explanation,
            detailed_strengths=detailed_strengths,
            detailed_concerns=detailed_concerns,
            recommendation=recommendation,
            ml_features=ml_features,
        )

    @staticmethod
    def _analyze_semantic_match(
        candidate: Candidate,
        vacancy: Vacancy,
        workplaces: List[Workplace],
    ) -> SemanticMatchResult:
        """Perform semantic text analysis."""
        # Combine candidate's text data
        candidate_text = f"{candidate.bio or ''} {candidate.summary or ''}"
        for wp in workplaces:
            candidate_text += f" {wp.description or ''}"

        # Combine vacancy text data
        vacancy_text = f"{vacancy.description or ''} {vacancy.responsibilities or ''}"

        # Calculate text similarity
        similarity = TextAnalysisService.calculate_text_similarity(
            candidate_text, vacancy_text
        )

        # Extract skills from both
        candidate_skills = TextAnalysisService.extract_skills(candidate_text)
        vacancy_skills = TextAnalysisService.extract_skills(vacancy_text)

        # Calculate skill-based match
        skill_scores = TextAnalysisService.calculate_skill_match_score(
            candidate_skills, vacancy_skills
        )
        avg_skill_match = sum(skill_scores.values()) / len(skill_scores) if skill_scores else 50.0

        # Extract keywords
        cand_keywords = set(TextAnalysisService.extract_keywords(candidate_text, top_n=30))
        vac_keywords = set(TextAnalysisService.extract_keywords(vacancy_text, top_n=30))

        # Calculate keyword overlap
        if vac_keywords:
            keyword_overlap = (len(cand_keywords.intersection(vac_keywords)) / len(vac_keywords)) * 100
        else:
            keyword_overlap = 0.0

        # Find missing important keywords
        missing_keywords = list(vac_keywords - cand_keywords)[:10]  # Top 10 missing

        # Find matching key phrases
        cand_phrases = TextAnalysisService._extract_key_phrases(candidate_text, max_phrases=10)
        vac_phrases = TextAnalysisService._extract_key_phrases(vacancy_text, max_phrases=10)
        matching_phrases = [p for p in cand_phrases if p in vac_phrases]

        return SemanticMatchResult(
            bio_description_similarity=similarity,
            skill_extraction_match=avg_skill_match,
            keyword_overlap=keyword_overlap,
            missing_keywords=missing_keywords,
            key_phrases_match=matching_phrases,
        )

    @staticmethod
    def _assess_cultural_fit(
        candidate: Candidate,
        vacancy: Vacancy,
        workplaces: List[Workplace],
    ) -> CulturalFitScore:
        """Assess cultural and organizational fit."""
        scores = []
        explanations = []

        # Company size fit
        # (Would need company size data - placeholder for now)
        company_size_fit = 70.0
        scores.append(company_size_fit)

        # Work style fit (remote/hybrid/office)
        if vacancy.locations:
            remote_compatible = any(loc.get('remote', False) for loc in vacancy.locations)
            if candidate.remote_work and remote_compatible:
                work_style_fit = 100.0
                explanations.append("Remote work preferences align")
            elif not candidate.remote_work and not remote_compatible:
                work_style_fit = 90.0
                explanations.append("On-site work preferences align")
            else:
                work_style_fit = 50.0
                explanations.append("Work location preferences differ")
        else:
            work_style_fit = 70.0

        scores.append(work_style_fit)

        # Team environment fit (based on career history)
        # Analyze if candidate has experience in similar team structures
        has_team_experience = any(wp.role in ['tech_lead', 'team_lead', 'manager'] for wp in workplaces)
        requires_leadership = vacancy.position_name and ('lead' in vacancy.position_name.lower() or 'manager' in vacancy.position_name.lower())

        if requires_leadership and has_team_experience:
            team_environment_fit = 95.0
            explanations.append("Has leadership experience matching requirements")
        elif not requires_leadership:
            team_environment_fit = 80.0
        else:
            team_environment_fit = 60.0
            explanations.append("Limited leadership experience for leadership role")

        scores.append(team_environment_fit)

        # Values alignment (based on career stability, growth pattern)
        career_analysis = CareerAnalysisService.analyze_career(workplaces, candidate.grade)
        if career_analysis.career_trend.consistency >= 70:
            values_alignment = 85.0
            explanations.append("Stable career history indicates reliability")
        elif career_analysis.career_trend.consistency >= 50:
            values_alignment = 70.0
        else:
            values_alignment = 55.0
            explanations.append("Frequent job changes may indicate values misalignment")

        scores.append(values_alignment)

        # Calculate overall fit
        overall_fit = sum(scores) / len(scores)

        fit_explanation = "; ".join(explanations) if explanations else "Standard cultural fit assessment"

        return CulturalFitScore(
            company_size_fit=company_size_fit,
            work_style_fit=work_style_fit,
            team_environment_fit=team_environment_fit,
            values_alignment=values_alignment,
            overall_fit=round(overall_fit, 2),
            fit_explanation=fit_explanation,
        )

    @staticmethod
    def _calculate_final_score(
        base_score: float,
        semantic_match: SemanticMatchResult,
        career_analysis: CareerAnalysis,
        cultural_fit: CulturalFitScore,
    ) -> float:
        """Calculate final adjusted score incorporating all factors."""
        # Start with base score (weight 60%)
        final = base_score * 0.60

        # Add semantic matching (weight 15%)
        semantic_avg = (
            semantic_match.bio_description_similarity * 0.4 +
            semantic_match.skill_extraction_match * 0.4 +
            semantic_match.keyword_overlap * 0.2
        )
        final += semantic_avg * 0.15

        # Add career trajectory (weight 15%)
        career_score = (
            career_analysis.career_trend.growth_rate * 0.3 +
            career_analysis.career_trend.consistency * 0.3 +
            career_analysis.potential_score * 0.4
        )
        final += career_score * 0.15

        # Add cultural fit (weight 10%)
        final += cultural_fit.overall_fit * 0.10

        # Apply penalties for red flags
        red_flag_penalty = min(10.0, len(career_analysis.red_flags) * 3)
        final -= red_flag_penalty

        # Ensure score is between 0 and 100
        return max(0.0, min(100.0, final))

    @staticmethod
    def _generate_explanation(
        base_score: CandidateVacancyScore,
        semantic_match: SemanticMatchResult,
        career_analysis: CareerAnalysis,
        cultural_fit: CulturalFitScore,
        final_score: float,
    ) -> str:
        """Generate comprehensive match explanation."""
        explanation_parts = []

        # Overall match quality
        if final_score >= 85:
            explanation_parts.append("This is an excellent match with strong alignment across all dimensions.")
        elif final_score >= 70:
            explanation_parts.append("This is a good match with solid alignment in key areas.")
        elif final_score >= 55:
            explanation_parts.append("This is a fair match with some gaps that should be considered.")
        else:
            explanation_parts.append("This is a poor match with significant gaps.")

        # Technical match
        if base_score.breakdown.technologies.score >= 80:
            explanation_parts.append(f"Strong technical match ({base_score.breakdown.technologies.matched}/{base_score.breakdown.technologies.required} required technologies).")
        elif base_score.breakdown.technologies.score >= 60:
            explanation_parts.append("Moderate technical match with some skill gaps.")
        else:
            explanation_parts.append("Weak technical match - significant skill development needed.")

        # Experience level
        if base_score.breakdown.experience.score >= 80:
            explanation_parts.append("Experience level aligns well with requirements.")
        elif base_score.breakdown.experience.score < 50:
            explanation_parts.append("Experience level below requirements.")

        # Career trajectory
        if career_analysis.career_trend.direction == 'upward':
            explanation_parts.append("Candidate shows strong career growth trajectory.")
        elif career_analysis.career_trend.direction == 'downward':
            explanation_parts.append("Career trajectory shows concerning downward trend.")

        # Cultural fit
        if cultural_fit.overall_fit >= 75:
            explanation_parts.append("Good cultural and organizational fit.")
        elif cultural_fit.overall_fit < 60:
            explanation_parts.append("Cultural fit may require additional consideration.")

        # Semantic match
        if semantic_match.bio_description_similarity >= 60:
            explanation_parts.append("Candidate's background aligns semantically with job description.")

        return " ".join(explanation_parts)

    @staticmethod
    def _generate_detailed_strengths(
        base_score: CandidateVacancyScore,
        semantic_match: SemanticMatchResult,
        career_analysis: CareerAnalysis,
        cultural_fit: CulturalFitScore,
    ) -> List[str]:
        """Generate comprehensive list of strengths."""
        strengths = []

        # Add base score highlights
        strengths.extend(ScoringService.generate_highlights(base_score))

        # Add career strengths
        strengths.extend(career_analysis.strengths)

        # Add semantic match strengths
        if semantic_match.bio_description_similarity >= 70:
            strengths.append(f"High semantic similarity between profile and job description ({semantic_match.bio_description_similarity:.0f}%)")

        if semantic_match.skill_extraction_match >= 75:
            strengths.append(f"Strong skill set match ({semantic_match.skill_extraction_match:.0f}%)")

        if semantic_match.keyword_overlap >= 60:
            strengths.append(f"Excellent keyword overlap ({semantic_match.keyword_overlap:.0f}%)")

        # Add cultural fit strengths
        if cultural_fit.work_style_fit >= 80:
            strengths.append("Work style preferences align well")

        if cultural_fit.team_environment_fit >= 80:
            strengths.append("Good fit for team environment")

        # Career stage match
        if career_analysis.career_stage in ['senior', 'lead', 'executive']:
            strengths.append(f"Experienced professional at {career_analysis.career_stage} level")

        return strengths

    @staticmethod
    def _generate_detailed_concerns(
        base_score: CandidateVacancyScore,
        semantic_match: SemanticMatchResult,
        career_analysis: CareerAnalysis,
        cultural_fit: CulturalFitScore,
    ) -> List[str]:
        """Generate comprehensive list of concerns."""
        concerns = []

        # Add base score concerns
        concerns.extend(ScoringService.generate_concerns(base_score))

        # Add career red flags
        concerns.extend(career_analysis.red_flags)

        # Add semantic match concerns
        if semantic_match.bio_description_similarity < 40:
            concerns.append(f"Low semantic similarity between profile and job description ({semantic_match.bio_description_similarity:.0f}%)")

        if semantic_match.missing_keywords:
            concerns.append(f"Missing important keywords: {', '.join(semantic_match.missing_keywords[:5])}")

        # Cultural fit concerns
        if cultural_fit.work_style_fit < 60:
            concerns.append("Work style preferences may not align")

        if cultural_fit.team_environment_fit < 60:
            concerns.append("May not be ideal fit for team environment")

        if cultural_fit.values_alignment < 60:
            concerns.append("Potential values or culture misalignment")

        # Career concerns
        if career_analysis.potential_score < 50:
            concerns.append(f"Lower growth potential score ({career_analysis.potential_score:.0f}%)")

        return concerns

    @staticmethod
    def _determine_recommendation(
        final_score: float,
        missing_critical_count: int,
        career_analysis: CareerAnalysis,
    ) -> str:
        """Determine hiring recommendation."""
        # Check for disqualifying factors
        if missing_critical_count > 2:
            return 'not_recommend'

        # Check for major red flags
        serious_red_flags = any(
            'downward' in flag.lower() or 'stability' in flag.lower()
            for flag in career_analysis.red_flags
        )

        if serious_red_flags and final_score < 70:
            return 'not_recommend'

        # Determine based on score
        if final_score >= 85:
            return 'highly_recommend'
        elif final_score >= 70:
            return 'recommend'
        elif final_score >= 55:
            return 'consider'
        else:
            return 'not_recommend'

    @staticmethod
    def _extract_ml_features(
        base_score: CandidateVacancyScore,
        semantic_match: SemanticMatchResult,
        career_analysis: CareerAnalysis,
        cultural_fit: CulturalFitScore,
        candidate: Candidate,
        vacancy: Vacancy,
    ) -> Dict[str, float]:
        """
        Extract features for ML model training.
        Returns normalized features (0-1 range) suitable for ML algorithms.
        """
        features = {}

        # Base scoring features
        features['tech_score'] = base_score.breakdown.technologies.score / 100
        features['experience_score'] = base_score.breakdown.experience.score / 100
        features['skills_score'] = base_score.breakdown.skills.score / 100
        features['language_score'] = base_score.breakdown.languages.score / 100
        features['location_score'] = base_score.breakdown.location.score / 100
        features['salary_score'] = base_score.breakdown.salary.score / 100

        # Technology matching features
        features['tech_matched_ratio'] = (
            base_score.breakdown.technologies.matched / base_score.breakdown.technologies.required
            if base_score.breakdown.technologies.required > 0 else 1.0
        )
        features['tech_required_count'] = min(1.0, base_score.breakdown.technologies.required / 10)

        # Experience features
        features['experience_years'] = min(1.0, (candidate.experience_months or 0) / (15 * 12))  # Normalize to 15 years
        features['experience_match'] = 1.0 if base_score.breakdown.experience.score >= 80 else 0.5

        # Semantic features
        features['semantic_similarity'] = semantic_match.bio_description_similarity / 100
        features['skill_extraction_match'] = semantic_match.skill_extraction_match / 100
        features['keyword_overlap'] = semantic_match.keyword_overlap / 100

        # Career trajectory features
        features['career_growth_rate'] = career_analysis.career_trend.growth_rate / 100
        features['career_consistency'] = career_analysis.career_trend.consistency / 100
        features['career_potential'] = career_analysis.potential_score / 100
        features['promotions_count'] = min(1.0, career_analysis.role_progression.promotions_count / 5)
        features['job_stability'] = career_analysis.role_progression.job_hopping_score / 100
        features['tech_breadth'] = min(1.0, career_analysis.technical_growth.technologies_learned / 20)
        features['tech_modernity'] = career_analysis.technical_growth.tech_stack_modernity / 100
        features['has_leadership'] = 1.0 if career_analysis.career_trend.leadership_progression else 0.0

        # Cultural fit features
        features['cultural_fit'] = cultural_fit.overall_fit / 100
        features['work_style_fit'] = cultural_fit.work_style_fit / 100
        features['team_fit'] = cultural_fit.team_environment_fit / 100

        # Red flags (negative feature)
        features['red_flags_count'] = min(1.0, len(career_analysis.red_flags) / 5)

        # Confidence and quality metrics
        features['match_confidence'] = base_score.confidence_level / 100
        features['missing_critical_ratio'] = min(1.0, len(base_score.missing_critical_requirements) / 5)

        # Salary compatibility
        features['salary_compatible'] = 1.0 if base_score.breakdown.salary.overlap else 0.0

        # Career stage encoding (one-hot style)
        stage_values = {
            'junior': 0.2,
            'mid': 0.4,
            'senior': 0.6,
            'lead': 0.8,
            'executive': 1.0,
        }
        features['career_stage_level'] = stage_values.get(career_analysis.career_stage, 0.4)

        # Technical depth vs breadth
        breadth_values = {
            'specialist': 0.2,
            'balanced': 0.5,
            'generalist': 0.8,
        }
        features['tech_breadth_type'] = breadth_values.get(
            career_analysis.technical_growth.breadth_vs_depth, 0.5
        )

        return features
