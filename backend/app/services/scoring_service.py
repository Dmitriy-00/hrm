"""Scoring service for candidate-vacancy matching."""

from typing import List, Tuple, Dict, Set
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.models.candidate import Candidate
from app.db.models.vacancy import Vacancy
from app.db.models.workplace import Workplace, WorkplaceTechnology
from app.db.models.vacancy_requirement import VacancyRequirement
from app.db.models.technology import Technology
from app.models.schemas.scoring import (
    CandidateVacancyScore,
    ScoreBreakdown,
    TechnologiesBreakdown,
    TechnologyMatchDetail,
    ExperienceBreakdown,
    SkillsBreakdown,
    StandardsBreakdown,
    IndustryBreakdown,
    LanguagesBreakdown,
    LanguageMatch,
    LocationBreakdown,
    SalaryBreakdown,
    BonusPoint,
    ScoringWeights,
)


# Language proficiency levels mapping
LANGUAGE_LEVELS = {
    "A1": 1,
    "A2": 2,
    "B1": 3,
    "B2": 4,
    "C1": 5,
    "C2": 6,
    "native": 7,
}


class ScoringService:
    """Service for candidate-vacancy matching and scoring."""

    @staticmethod
    def calculate_score(
        db: Session,
        candidate: Candidate,
        vacancy: Vacancy,
        weights: ScoringWeights = ScoringWeights(),
    ) -> CandidateVacancyScore:
        """
        Calculate matching score between candidate and vacancy.

        Returns score from 0 to 100 with detailed breakdown.
        """
        # Get candidate's workplaces and technologies
        workplaces = (
            db.query(Workplace)
            .filter(Workplace.candidate_id == candidate.id)
            .all()
        )

        # Get vacancy requirements
        requirements = (
            db.query(VacancyRequirement)
            .filter(VacancyRequirement.vacancy_id == vacancy.id)
            .all()
        )

        # Calculate each component
        tech_breakdown = ScoringService._score_technologies(
            db, candidate, workplaces, requirements
        )
        exp_breakdown = ScoringService._score_experience(candidate, vacancy)
        skills_breakdown = ScoringService._score_skills(workplaces, vacancy)
        standards_breakdown = ScoringService._score_standards(workplaces, vacancy)
        industry_breakdown = ScoringService._score_industry(workplaces, vacancy)
        languages_breakdown = ScoringService._score_languages(candidate, vacancy)
        location_breakdown = ScoringService._score_location(candidate, vacancy)
        salary_breakdown = ScoringService._score_salary(candidate, vacancy)

        # Calculate weighted total score
        total_score = (
            tech_breakdown.score * weights.technologies / 100 +
            exp_breakdown.score * weights.experience / 100 +
            skills_breakdown.score * weights.skills / 100 +
            standards_breakdown.score * weights.standards / 100 +
            industry_breakdown.score * weights.industry / 100 +
            languages_breakdown.score * weights.languages / 100 +
            location_breakdown.score * weights.location / 100 +
            salary_breakdown.score * weights.salary / 100
        )

        # Calculate confidence level
        confidence = ScoringService._calculate_confidence(
            tech_breakdown, exp_breakdown, skills_breakdown
        )

        # Identify missing critical requirements
        missing_critical = ScoringService._get_missing_critical_requirements(
            tech_breakdown, languages_breakdown
        )

        # Calculate bonus points
        bonus_points = ScoringService._calculate_bonus_points(
            candidate, vacancy, workplaces
        )

        # Add bonus points to total score (capped at 100)
        total_bonus = sum(bp.points for bp in bonus_points)
        total_score = min(100.0, total_score + total_bonus)

        # Determine match quality
        match_quality = ScoringService._determine_match_quality(
            total_score, len(missing_critical)
        )

        return CandidateVacancyScore(
            candidate_id=candidate.id,
            vacancy_id=vacancy.id,
            total_score=round(total_score, 2),
            breakdown=ScoreBreakdown(
                technologies=tech_breakdown,
                experience=exp_breakdown,
                skills=skills_breakdown,
                standards=standards_breakdown,
                industry=industry_breakdown,
                languages=languages_breakdown,
                location=location_breakdown,
                salary=salary_breakdown,
            ),
            confidence_level=round(confidence, 2),
            missing_critical_requirements=missing_critical,
            bonus_points=bonus_points,
            match_quality=match_quality,
            calculated_at=datetime.utcnow(),
        )

    @staticmethod
    def _score_technologies(
        db: Session,
        candidate: Candidate,
        workplaces: List[Workplace],
        requirements: List[VacancyRequirement],
    ) -> TechnologiesBreakdown:
        """Score technology matching (max 100 points)."""
        if not requirements:
            return TechnologiesBreakdown(score=100.0, matched=0, required=0, details=[])

        # Build candidate's technology experience map
        candidate_tech_map: Dict[UUID, Tuple[int, int]] = {}  # tech_id -> (proficiency, months)

        for workplace in workplaces:
            for wt in workplace.technologies:
                tech_id = wt.technology_id
                if tech_id not in candidate_tech_map:
                    candidate_tech_map[tech_id] = (wt.proficiency, workplace.duration_months or 0)
                else:
                    # Use max proficiency and sum months
                    existing_prof, existing_months = candidate_tech_map[tech_id]
                    candidate_tech_map[tech_id] = (
                        max(existing_prof, wt.proficiency),
                        existing_months + (workplace.duration_months or 0),
                    )

        # Evaluate each requirement
        required_count = sum(1 for r in requirements if r.importance == "required")
        total_score = 0.0
        matched_count = 0
        details = []

        for req in requirements:
            tech = db.query(Technology).filter(Technology.id == req.technology_id).first()
            tech_name = tech.name if tech else "Unknown"

            if req.technology_id in candidate_tech_map:
                cand_prof, cand_months = candidate_tech_map[req.technology_id]
                req_prof = req.proficiency_level or 3
                req_months = (req.min_experience_years or 0) * 12

                # Calculate proficiency match (0-100)
                prof_score = min(100, (cand_prof / req_prof) * 100) if req_prof > 0 else 100

                # Calculate experience match (0-100)
                exp_score = min(100, (cand_months / req_months) * 100) if req_months > 0 else 100

                # Combined match score for this technology
                tech_match_score = (prof_score + exp_score) / 2

                # Weight by importance
                if req.importance == "required":
                    weight = 1.0
                    if tech_match_score >= 50:
                        matched_count += 1
                elif req.importance == "nice_to_have":
                    weight = 0.5
                else:  # plus
                    weight = 0.25

                total_score += tech_match_score * weight

                details.append(
                    TechnologyMatchDetail(
                        technology_id=req.technology_id,
                        technology_name=tech_name,
                        candidate_proficiency=cand_prof,
                        required_proficiency=req_prof,
                        candidate_experience_months=cand_months,
                        required_experience_months=req_months,
                        importance=req.importance,
                        match_score=round(tech_match_score, 2),
                    )
                )
            else:
                # Technology not found in candidate's experience
                if req.importance == "required":
                    # 0 points for missing required technology
                    total_score += 0
                else:
                    # No penalty for missing nice-to-have
                    pass

                details.append(
                    TechnologyMatchDetail(
                        technology_id=req.technology_id,
                        technology_name=tech_name,
                        candidate_proficiency=0,
                        required_proficiency=req.proficiency_level or 3,
                        candidate_experience_months=0,
                        required_experience_months=(req.min_experience_years or 0) * 12,
                        importance=req.importance,
                        match_score=0.0,
                    )
                )

        # Normalize score
        total_weight = sum(
            1.0 if r.importance == "required" else (0.5 if r.importance == "nice_to_have" else 0.25)
            for r in requirements
        )
        final_score = (total_score / total_weight) if total_weight > 0 else 100.0

        return TechnologiesBreakdown(
            score=min(100.0, round(final_score, 2)),
            matched=matched_count,
            required=required_count,
            details=details,
        )

    @staticmethod
    def _score_experience(candidate: Candidate, vacancy: Vacancy) -> ExperienceBreakdown:
        """Score experience matching (max 100 points)."""
        cand_months = candidate.experience_months or 0
        cand_years = round(cand_months / 12, 1)

        req_min_months = (vacancy.min_experience_years or 0) * 12
        req_max_months = (vacancy.max_experience_years * 12) if vacancy.max_experience_years else None
        req_min_years = vacancy.min_experience_years or 0
        req_max_years = vacancy.max_experience_years

        # Calculate score
        if req_min_months == 0 and req_max_months is None:
            # No experience requirements
            score = 100.0
        elif req_max_months is None:
            # Only minimum requirement
            if cand_months >= req_min_months:
                score = 100.0
            else:
                # Penalty for lacking experience
                score = max(0, (cand_months / req_min_months) * 100)
        else:
            # Range requirement
            if req_min_months <= cand_months <= req_max_months:
                # Perfect match
                score = 100.0
            elif cand_months < req_min_months:
                # Below minimum
                score = max(0, (cand_months / req_min_months) * 80)  # Max 80% if below
            else:
                # Above maximum (slight penalty for overqualification)
                excess = cand_months - req_max_months
                penalty = min(20, excess / 12 * 2)  # 2% penalty per year over
                score = max(80, 100 - penalty)

        return ExperienceBreakdown(
            score=round(score, 2),
            candidate_months=cand_months,
            candidate_years=cand_years,
            required_min_months=req_min_months,
            required_max_months=req_max_months,
            required_min_years=req_min_years,
            required_max_years=req_max_years,
        )

    @staticmethod
    def _score_skills(workplaces: List[Workplace], vacancy: Vacancy) -> SkillsBreakdown:
        """Score skills matching (max 100 points)."""
        # Extract all skills from candidate's workplaces
        candidate_skills = set()
        for workplace in workplaces:
            for skill in workplace.skills:
                candidate_skills.add(skill.get("skill_name", "").lower())

        # For now, we don't have explicit skill requirements in vacancy
        # This can be enhanced later
        # Returning 100 as placeholder
        return SkillsBreakdown(
            score=100.0,
            matched=len(candidate_skills),
            required=0,
            missing=[],
        )

    @staticmethod
    def _score_standards(workplaces: List[Workplace], vacancy: Vacancy) -> StandardsBreakdown:
        """Score standards/methodologies matching (max 100 points)."""
        # Extract all standards from candidate's workplaces
        candidate_standards = set()
        for workplace in workplaces:
            for std in workplace.standards_used:
                candidate_standards.add(std.get("standard_id"))

        # For now, we don't have explicit standard requirements in vacancy
        # This can be enhanced later
        return StandardsBreakdown(
            score=100.0,
            matched=len(candidate_standards),
            required=0,
        )

    @staticmethod
    def _score_industry(workplaces: List[Workplace], vacancy: Vacancy) -> IndustryBreakdown:
        """Score industry experience matching (max 100 points)."""
        # Get all industries from candidate's workplaces
        candidate_industries = set()
        total_months = 0

        for workplace in workplaces:
            for industry_id in workplace.industry_ids:
                candidate_industries.add(industry_id)
                total_months += workplace.duration_months or 0

        # For now, vacancy doesn't have industry requirements
        # This can be enhanced later
        has_experience = len(candidate_industries) > 0
        score = 100.0 if has_experience else 50.0

        return IndustryBreakdown(
            score=score,
            has_experience=has_experience,
            experience_months=total_months,
        )

    @staticmethod
    def _score_languages(candidate: Candidate, vacancy: Vacancy) -> LanguagesBreakdown:
        """Score language requirements matching (max 100 points)."""
        if not vacancy.language_requirements:
            return LanguagesBreakdown(score=100.0, matched=[], missing=[])

        # Build candidate's language map
        candidate_langs = {
            lang.get("language", "").lower(): lang.get("proficiency", "")
            for lang in candidate.languages
        }

        matched = []
        missing = []
        required_count = 0
        met_count = 0

        for lang_req in vacancy.language_requirements:
            lang_name = lang_req.get("language", "").lower()
            required_level = lang_req.get("min_level", "B1")
            is_required = lang_req.get("required", True)

            if is_required:
                required_count += 1

            if lang_name in candidate_langs:
                candidate_level = candidate_langs[lang_name]
                candidate_level_num = LANGUAGE_LEVELS.get(candidate_level, 0)
                required_level_num = LANGUAGE_LEVELS.get(required_level, 3)

                meets_requirement = candidate_level_num >= required_level_num

                matched.append(
                    LanguageMatch(
                        language=lang_req.get("language", ""),
                        candidate_level=candidate_level,
                        required_level=required_level,
                        meets_requirement=meets_requirement,
                    )
                )

                if meets_requirement and is_required:
                    met_count += 1
            else:
                if is_required:
                    missing.append(lang_req.get("language", ""))

        # Calculate score
        if required_count == 0:
            score = 100.0
        else:
            score = (met_count / required_count) * 100

        return LanguagesBreakdown(
            score=round(score, 2),
            matched=matched,
            missing=missing,
        )

    @staticmethod
    def _score_location(candidate: Candidate, vacancy: Vacancy) -> LocationBreakdown:
        """Score location compatibility (max 100 points)."""
        if not vacancy.locations:
            return LocationBreakdown(score=100.0, compatible=True, details="No location restrictions")

        compatible = False
        details_list = []

        for location in vacancy.locations:
            loc_country = location.get("country", "")
            loc_city = location.get("city", "")
            loc_remote = location.get("remote", False)
            loc_relocation = location.get("relocation", False)

            # Check if candidate matches this location
            if candidate.remote_work and loc_remote:
                compatible = True
                details_list.append(f"Remote work available in {loc_country}")
            elif candidate.relocation and loc_relocation:
                compatible = True
                details_list.append(f"Relocation to {loc_city}, {loc_country}")
            elif candidate.city == loc_city and candidate.country == loc_country:
                compatible = True
                details_list.append(f"Already in {loc_city}, {loc_country}")

        score = 100.0 if compatible else 0.0
        details = "; ".join(details_list) if details_list else "Location not compatible"

        return LocationBreakdown(
            score=score,
            compatible=compatible,
            details=details,
        )

    @staticmethod
    def _score_salary(candidate: Candidate, vacancy: Vacancy) -> SalaryBreakdown:
        """Score salary compatibility (max 100 points)."""
        cand_min = candidate.salary_min
        cand_max = candidate.salary_max
        vac_min = vacancy.salary_min
        vac_max = vacancy.salary_max

        # Check for overlap
        overlap = False
        details = ""

        if not cand_min and not cand_max:
            # Candidate didn't specify salary
            score = 100.0
            details = "Candidate salary expectations not specified"
        elif not vac_min and not vac_max:
            # Vacancy didn't specify salary
            score = 100.0 if vacancy.salary_negotiable else 50.0
            details = "Vacancy salary not specified, negotiable" if vacancy.salary_negotiable else "Vacancy salary not specified"
        else:
            # Both specified - check overlap
            cand_min = cand_min or 0
            cand_max = cand_max or float('inf')
            vac_min = vac_min or 0
            vac_max = vac_max or float('inf')

            overlap = not (cand_max < vac_min or vac_max < cand_min)

            if overlap:
                score = 100.0
                details = "Salary expectations overlap"
            elif vacancy.salary_negotiable:
                score = 70.0
                details = "Salary mismatch, but negotiable"
            else:
                score = 0.0
                details = "Salary expectations don't match"

        return SalaryBreakdown(
            score=score,
            candidate_min=candidate.salary_min,
            candidate_max=candidate.salary_max,
            vacancy_min=vacancy.salary_min,
            vacancy_max=vacancy.salary_max,
            overlap=overlap,
            details=details,
        )

    @staticmethod
    def _calculate_confidence(
        tech: TechnologiesBreakdown,
        exp: ExperienceBreakdown,
        skills: SkillsBreakdown,
    ) -> float:
        """Calculate confidence in the score (0-100)."""
        # Higher confidence if we have more data
        confidence = 50.0  # Base confidence

        # Boost confidence based on technology matches
        if tech.required > 0:
            confidence += (tech.matched / tech.required) * 30

        # Boost confidence based on experience data
        if exp.candidate_months > 0:
            confidence += 20

        return min(100.0, confidence)

    @staticmethod
    def _get_missing_critical_requirements(
        tech: TechnologiesBreakdown,
        languages: LanguagesBreakdown,
    ) -> List[str]:
        """Get list of missing critical requirements."""
        missing = []

        # Missing required technologies
        for detail in tech.details:
            if detail.importance == "required" and detail.match_score < 50:
                missing.append(f"{detail.technology_name} (required)")

        # Missing required languages
        for lang in languages.missing:
            missing.append(f"{lang} language (required)")

        return missing

    @staticmethod
    def _calculate_bonus_points(
        candidate: Candidate,
        vacancy: Vacancy,
        workplaces: List[Workplace],
    ) -> List[BonusPoint]:
        """Calculate bonus points for additional qualifications."""
        bonus_points = []

        # Bonus for having more experience than required
        if vacancy.max_experience_years:
            excess_years = (candidate.experience_months / 12) - vacancy.max_experience_years
            if excess_years > 2:
                bonus_points.append(
                    BonusPoint(
                        reason="Significantly more experienced than required",
                        points=min(5.0, excess_years),
                    )
                )

        # Bonus for multiple companies (diverse experience)
        if len(workplaces) >= 3:
            bonus_points.append(
                BonusPoint(
                    reason="Diverse experience across multiple companies",
                    points=2.0,
                )
            )

        # Bonus for leadership experience
        for workplace in workplaces:
            if workplace.role in ["tech_lead", "team_lead", "manager"]:
                bonus_points.append(
                    BonusPoint(
                        reason="Leadership experience",
                        points=3.0,
                    )
                )
                break

        return bonus_points

    @staticmethod
    def _determine_match_quality(total_score: float, missing_critical_count: int) -> str:
        """Determine overall match quality."""
        if missing_critical_count > 2:
            return "poor"
        elif total_score >= 80:
            return "excellent"
        elif total_score >= 65:
            return "good"
        elif total_score >= 50:
            return "fair"
        else:
            return "poor"

    @staticmethod
    def generate_highlights(score: CandidateVacancyScore) -> List[str]:
        """Generate list of positive highlights from the score."""
        highlights = []

        # Technology matches
        if score.breakdown.technologies.score >= 80:
            matched = score.breakdown.technologies.matched
            required = score.breakdown.technologies.required
            highlights.append(
                f"Strong technology match: {matched}/{required} required technologies"
            )

        # Experience match
        if score.breakdown.experience.score >= 80:
            highlights.append(
                f"Excellent experience level: {score.breakdown.experience.candidate_years:.1f} years"
            )

        # Languages
        if score.breakdown.languages.score >= 90:
            highlights.append(
                f"All language requirements met ({len(score.breakdown.languages.matched)} languages)"
            )

        # Location compatibility
        if score.breakdown.location.score == 100:
            highlights.append(score.breakdown.location.details)

        # Salary compatibility
        if score.breakdown.salary.score >= 80:
            highlights.append(score.breakdown.salary.details)

        # Industry experience
        if score.breakdown.industry.has_experience and score.breakdown.industry.experience_months > 12:
            years = score.breakdown.industry.experience_months / 12
            highlights.append(f"Relevant industry experience: {years:.1f} years")

        # Standards
        if score.breakdown.standards.score >= 80:
            highlights.append(
                f"Matches {score.breakdown.standards.matched}/{score.breakdown.standards.required} required standards"
            )

        # Bonus points
        if score.bonus_points:
            for bonus in score.bonus_points:
                highlights.append(f"+ {bonus.reason}")

        # Overall match quality
        if score.match_quality == "excellent":
            highlights.append("Excellent overall match!")

        return highlights

    @staticmethod
    def generate_concerns(score: CandidateVacancyScore) -> List[str]:
        """Generate list of concerns/gaps from the score."""
        concerns = []

        # Missing critical requirements
        if score.missing_critical_requirements:
            concerns.append(
                f"Missing critical requirements: {', '.join(score.missing_critical_requirements)}"
            )

        # Technology gaps
        if score.breakdown.technologies.score < 50:
            missing_count = score.breakdown.technologies.required - score.breakdown.technologies.matched
            concerns.append(f"Missing {missing_count} required technologies")

        # Experience concerns
        if score.breakdown.experience.score < 50:
            concerns.append(score.breakdown.experience.details if hasattr(score.breakdown.experience, 'details') else "Experience level does not match requirements")

        # Language gaps
        if score.breakdown.languages.missing:
            concerns.append(
                f"Missing languages: {', '.join(score.breakdown.languages.missing)}"
            )

        # Location incompatibility
        if score.breakdown.location.score < 50:
            concerns.append(score.breakdown.location.details)

        # Salary mismatch
        if score.breakdown.salary.score < 50:
            concerns.append(score.breakdown.salary.details)

        # Skills gaps
        if score.breakdown.skills.missing:
            concerns.append(
                f"Missing skills: {', '.join(score.breakdown.skills.missing[:3])}"
                + (f" and {len(score.breakdown.skills.missing) - 3} more" if len(score.breakdown.skills.missing) > 3 else "")
            )

        # No industry experience
        if not score.breakdown.industry.has_experience:
            concerns.append("No experience in the required industry")

        # Overall match quality
        if score.match_quality == "poor":
            concerns.append("Overall match quality is poor - significant gaps exist")

        return concerns
