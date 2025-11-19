"""
Career Trajectory Analysis Service.
Analyzes candidate's career path, growth patterns, and future potential.
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
from app.db.models.workplace import Workplace


@dataclass
class CareerTrend:
    """Career growth trend."""
    direction: str  # 'upward', 'stable', 'lateral', 'downward'
    growth_rate: float  # 0-100
    consistency: float  # 0-100
    specialization_level: float  # 0-100
    leadership_progression: bool
    technical_depth_growth: bool


@dataclass
class RoleProgression:
    """Role progression analysis."""
    role_levels: List[str]  # Chronological list of role levels
    promotions_count: int
    avg_tenure_months: float
    job_hopping_score: float  # 0-100 (higher = more stable)
    role_diversity_score: float  # 0-100


@dataclass
class TechnicalGrowth:
    """Technical skill growth analysis."""
    technologies_learned: int
    tech_stack_modernity: float  # 0-100
    breadth_vs_depth: str  # 'specialist', 'generalist', 'balanced'
    learning_velocity: float  # 0-100
    tech_leadership: bool


@dataclass
class CareerAnalysis:
    """Comprehensive career analysis."""
    career_trend: CareerTrend
    role_progression: RoleProgression
    technical_growth: TechnicalGrowth
    red_flags: List[str]
    strengths: List[str]
    career_stage: str  # 'junior', 'mid', 'senior', 'lead', 'executive'
    potential_score: float  # 0-100


class CareerAnalysisService:
    """Service for analyzing candidate career trajectories."""

    # Role hierarchy mapping
    ROLE_HIERARCHY = {
        'intern': 1,
        'junior': 2,
        'developer': 3,
        'middle': 4,
        'senior': 5,
        'tech_lead': 6,
        'team_lead': 7,
        'manager': 8,
        'senior_manager': 9,
        'director': 10,
        'vp': 11,
        'cto': 12,
    }

    # Modern vs legacy technologies (for modernity score)
    MODERN_TECH_KEYWORDS = {
        'react', 'vue', 'angular', 'svelte', 'next.js', 'typescript',
        'go', 'rust', 'kotlin', 'swift', 'docker', 'kubernetes',
        'aws', 'azure', 'gcp', 'terraform', 'graphql', 'grpc',
        'microservices', 'serverless', 'ci/cd', 'devops',
        'machine learning', 'deep learning', 'ai', 'blockchain',
    }

    LEGACY_TECH_KEYWORDS = {
        'cobol', 'fortran', 'perl', 'vb6', 'asp.net webforms',
        'silverlight', 'flash', 'jquery', 'backbone',
    }

    @staticmethod
    def analyze_career(
        workplaces: List[Workplace],
        candidate_grade: Optional[str] = None
    ) -> CareerAnalysis:
        """
        Perform comprehensive career analysis.
        """
        if not workplaces:
            return CareerAnalysisService._empty_analysis()

        # Sort workplaces by start date (oldest first)
        sorted_workplaces = sorted(
            workplaces,
            key=lambda w: w.start_date or datetime.min
        )

        # Analyze different aspects
        career_trend = CareerAnalysisService._analyze_career_trend(sorted_workplaces)
        role_progression = CareerAnalysisService._analyze_role_progression(sorted_workplaces)
        technical_growth = CareerAnalysisService._analyze_technical_growth(sorted_workplaces)

        # Identify red flags
        red_flags = CareerAnalysisService._identify_red_flags(
            sorted_workplaces, role_progression
        )

        # Identify strengths
        strengths = CareerAnalysisService._identify_strengths(
            career_trend, role_progression, technical_growth
        )

        # Determine career stage
        career_stage = CareerAnalysisService._determine_career_stage(
            sorted_workplaces, candidate_grade
        )

        # Calculate potential score
        potential_score = CareerAnalysisService._calculate_potential_score(
            career_trend, role_progression, technical_growth, red_flags
        )

        return CareerAnalysis(
            career_trend=career_trend,
            role_progression=role_progression,
            technical_growth=technical_growth,
            red_flags=red_flags,
            strengths=strengths,
            career_stage=career_stage,
            potential_score=potential_score,
        )

    @staticmethod
    def _analyze_career_trend(workplaces: List[Workplace]) -> CareerTrend:
        """Analyze overall career growth trend."""
        if len(workplaces) < 2:
            return CareerTrend(
                direction='stable',
                growth_rate=50.0,
                consistency=50.0,
                specialization_level=50.0,
                leadership_progression=False,
                technical_depth_growth=False,
            )

        # Analyze role level progression
        role_levels = []
        for wp in workplaces:
            level = CareerAnalysisService.ROLE_HIERARCHY.get(wp.role, 3)
            role_levels.append(level)

        # Determine direction
        if len(role_levels) >= 2:
            first_half_avg = sum(role_levels[:len(role_levels)//2]) / (len(role_levels)//2)
            second_half_avg = sum(role_levels[len(role_levels)//2:]) / (len(role_levels) - len(role_levels)//2)

            if second_half_avg > first_half_avg + 1:
                direction = 'upward'
                growth_rate = min(100.0, (second_half_avg - first_half_avg) * 20)
            elif second_half_avg < first_half_avg - 1:
                direction = 'downward'
                growth_rate = max(0.0, 50 - (first_half_avg - second_half_avg) * 20)
            elif abs(second_half_avg - first_half_avg) <= 1:
                direction = 'stable'
                growth_rate = 60.0
            else:
                direction = 'lateral'
                growth_rate = 55.0
        else:
            direction = 'stable'
            growth_rate = 50.0

        # Calculate consistency (less job hopping = more consistent)
        avg_tenure = sum(wp.duration_months or 12 for wp in workplaces) / len(workplaces)
        if avg_tenure >= 36:  # 3+ years average
            consistency = 90.0
        elif avg_tenure >= 24:  # 2+ years
            consistency = 75.0
        elif avg_tenure >= 18:  # 1.5+ years
            consistency = 60.0
        elif avg_tenure >= 12:  # 1+ years
            consistency = 45.0
        else:
            consistency = 30.0

        # Check leadership progression
        leadership_roles = {'tech_lead', 'team_lead', 'manager', 'senior_manager', 'director', 'vp', 'cto'}
        has_leadership = any(wp.role in leadership_roles for wp in workplaces)
        leadership_progression = has_leadership and direction == 'upward'

        # Check technical depth growth (number of technologies increasing)
        tech_counts = [len(wp.technologies) for wp in workplaces if wp.technologies]
        technical_depth_growth = len(tech_counts) >= 2 and tech_counts[-1] > tech_counts[0]

        # Specialization level (focus on similar roles/industries)
        roles_set = set(wp.role for wp in workplaces)
        specialization_level = max(0.0, 100 - len(roles_set) * 15)

        return CareerTrend(
            direction=direction,
            growth_rate=growth_rate,
            consistency=consistency,
            specialization_level=specialization_level,
            leadership_progression=leadership_progression,
            technical_depth_growth=technical_depth_growth,
        )

    @staticmethod
    def _analyze_role_progression(workplaces: List[Workplace]) -> RoleProgression:
        """Analyze role progression patterns."""
        if not workplaces:
            return RoleProgression([], 0, 0.0, 0.0, 0.0)

        # Get role levels
        role_levels = [
            CareerAnalysisService.ROLE_HIERARCHY.get(wp.role, 3)
            for wp in workplaces
        ]

        # Count promotions (role level increases)
        promotions = 0
        for i in range(1, len(role_levels)):
            if role_levels[i] > role_levels[i-1]:
                promotions += 1

        # Calculate average tenure
        valid_durations = [wp.duration_months for wp in workplaces if wp.duration_months]
        avg_tenure = sum(valid_durations) / len(valid_durations) if valid_durations else 18.0

        # Job hopping score (stability)
        if avg_tenure >= 36:
            job_hopping_score = 95.0
        elif avg_tenure >= 30:
            job_hopping_score = 85.0
        elif avg_tenure >= 24:
            job_hopping_score = 75.0
        elif avg_tenure >= 18:
            job_hopping_score = 60.0
        elif avg_tenure >= 12:
            job_hopping_score = 40.0
        else:
            job_hopping_score = 20.0

        # Role diversity (different types of roles)
        unique_roles = len(set(wp.role for wp in workplaces))
        role_diversity_score = min(100.0, unique_roles * 25)

        return RoleProgression(
            role_levels=[wp.role for wp in workplaces],
            promotions_count=promotions,
            avg_tenure_months=avg_tenure,
            job_hopping_score=job_hopping_score,
            role_diversity_score=role_diversity_score,
        )

    @staticmethod
    def _analyze_technical_growth(workplaces: List[Workplace]) -> TechnicalGrowth:
        """Analyze technical skill development."""
        if not workplaces:
            return TechnicalGrowth(0, 50.0, 'balanced', 50.0, False)

        # Count unique technologies across all workplaces
        all_techs = set()
        tech_by_workplace = []

        for wp in workplaces:
            wp_techs = set()
            for wt in wp.technologies:
                if wt.technology and wt.technology.name:
                    tech_name = wt.technology.name.lower()
                    all_techs.add(tech_name)
                    wp_techs.add(tech_name)
            tech_by_workplace.append(wp_techs)

        technologies_learned = len(all_techs)

        # Calculate tech stack modernity
        modern_count = 0
        legacy_count = 0

        for tech in all_techs:
            if any(modern in tech for modern in CareerAnalysisService.MODERN_TECH_KEYWORDS):
                modern_count += 1
            if any(legacy in tech for legacy in CareerAnalysisService.LEGACY_TECH_KEYWORDS):
                legacy_count += 1

        total_categorized = modern_count + legacy_count
        if total_categorized > 0:
            tech_stack_modernity = (modern_count / total_categorized) * 100
        else:
            tech_stack_modernity = 70.0  # Default moderate score

        # Breadth vs depth analysis
        if technologies_learned <= 5:
            breadth_vs_depth = 'specialist'
        elif technologies_learned >= 15:
            breadth_vs_depth = 'generalist'
        else:
            breadth_vs_depth = 'balanced'

        # Learning velocity (new techs per year)
        if len(workplaces) > 1 and workplaces[0].start_date:
            total_months = sum(wp.duration_months or 12 for wp in workplaces)
            if total_months > 0:
                techs_per_year = (technologies_learned / total_months) * 12
                learning_velocity = min(100.0, techs_per_year * 25)
            else:
                learning_velocity = 50.0
        else:
            learning_velocity = 50.0

        # Check for tech leadership
        leadership_roles = {'tech_lead', 'team_lead', 'manager'}
        tech_leadership = any(wp.role in leadership_roles for wp in workplaces)

        return TechnicalGrowth(
            technologies_learned=technologies_learned,
            tech_stack_modernity=tech_stack_modernity,
            breadth_vs_depth=breadth_vs_depth,
            learning_velocity=learning_velocity,
            tech_leadership=tech_leadership,
        )

    @staticmethod
    def _identify_red_flags(
        workplaces: List[Workplace],
        role_progression: RoleProgression
    ) -> List[str]:
        """Identify potential red flags in career history."""
        red_flags = []

        # Job hopping (too many short stints)
        short_stints = sum(1 for wp in workplaces if (wp.duration_months or 0) < 12)
        if short_stints >= 3:
            red_flags.append(f"Multiple short job tenures ({short_stints} positions under 1 year)")
        elif short_stints >= 2:
            red_flags.append(f"Some short job tenures ({short_stints} positions under 1 year)")

        # Employment gaps (if we had dates we could check this)
        # Placeholder for future implementation

        # Downward trajectory
        if len(role_progression.role_levels) >= 3:
            last_three = role_progression.role_levels[-3:]
            last_three_levels = [CareerAnalysisService.ROLE_HIERARCHY.get(r, 3) for r in last_three]
            if last_three_levels[-1] < last_three_levels[0]:
                red_flags.append("Recent downward career movement")

        # Too much job hopping
        if role_progression.job_hopping_score < 40:
            red_flags.append("Frequent job changes may indicate instability")

        # No promotions over long period
        if len(workplaces) >= 4 and role_progression.promotions_count == 0:
            red_flags.append("No promotions or role advancement over multiple positions")

        return red_flags

    @staticmethod
    def _identify_strengths(
        career_trend: CareerTrend,
        role_progression: RoleProgression,
        technical_growth: TechnicalGrowth
    ) -> List[str]:
        """Identify career strengths."""
        strengths = []

        # Upward trajectory
        if career_trend.direction == 'upward':
            strengths.append(f"Strong upward career trajectory (growth rate: {career_trend.growth_rate:.0f}%)")

        # Career consistency
        if career_trend.consistency >= 75:
            strengths.append("Consistent career path with stable job tenure")

        # Promotions
        if role_progression.promotions_count >= 2:
            strengths.append(f"Multiple promotions ({role_progression.promotions_count} career advancements)")

        # Leadership progression
        if career_trend.leadership_progression:
            strengths.append("Demonstrated leadership growth")

        # Technical breadth
        if technical_growth.technologies_learned >= 10:
            strengths.append(f"Broad technical expertise ({technical_growth.technologies_learned} technologies)")

        # Modern tech stack
        if technical_growth.tech_stack_modernity >= 70:
            strengths.append("Works with modern technology stack")

        # Learning velocity
        if technical_growth.learning_velocity >= 70:
            strengths.append("Fast learner with high technology adoption rate")

        # Technical leadership
        if technical_growth.tech_leadership:
            strengths.append("Technical leadership experience")

        # Specialization
        if career_trend.specialization_level >= 70:
            strengths.append("Strong specialization and focus")

        return strengths

    @staticmethod
    def _determine_career_stage(
        workplaces: List[Workplace],
        candidate_grade: Optional[str]
    ) -> str:
        """Determine candidate's career stage."""
        # First try to use candidate grade if available
        if candidate_grade:
            grade_lower = candidate_grade.lower()
            if 'junior' in grade_lower or 'trainee' in grade_lower:
                return 'junior'
            elif 'senior' in grade_lower or 'staff' in grade_lower:
                return 'senior'
            elif 'lead' in grade_lower or 'principal' in grade_lower:
                return 'lead'
            elif 'director' in grade_lower or 'vp' in grade_lower or 'cto' in grade_lower:
                return 'executive'
            else:
                return 'mid'

        # Fall back to analyzing workplaces
        if not workplaces:
            return 'mid'

        # Look at most recent role
        latest_role = workplaces[-1].role
        latest_level = CareerAnalysisService.ROLE_HIERARCHY.get(latest_role, 3)

        # Calculate total experience
        total_months = sum(wp.duration_months or 12 for wp in workplaces)
        total_years = total_months / 12

        # Determine stage based on level and experience
        if latest_level >= 10:  # Director+
            return 'executive'
        elif latest_level >= 6:  # Tech/Team Lead+
            return 'lead'
        elif latest_level >= 5:  # Senior
            return 'senior'
        elif latest_level >= 3 and total_years >= 3:  # Mid with experience
            return 'mid'
        else:
            return 'junior'

    @staticmethod
    def _calculate_potential_score(
        career_trend: CareerTrend,
        role_progression: RoleProgression,
        technical_growth: TechnicalGrowth,
        red_flags: List[str]
    ) -> float:
        """Calculate overall potential score."""
        # Start with base score
        score = 50.0

        # Career trend factors
        if career_trend.direction == 'upward':
            score += 20
        elif career_trend.direction == 'stable':
            score += 10

        score += (career_trend.growth_rate - 50) * 0.2
        score += (career_trend.consistency - 50) * 0.15

        # Role progression factors
        score += role_progression.promotions_count * 5
        score += (role_progression.job_hopping_score - 50) * 0.1

        # Technical growth factors
        score += min(15, technical_growth.technologies_learned)
        score += (technical_growth.tech_stack_modernity - 50) * 0.15
        score += (technical_growth.learning_velocity - 50) * 0.1

        if technical_growth.tech_leadership:
            score += 10

        # Penalize red flags
        score -= len(red_flags) * 8

        # Ensure score is between 0 and 100
        return max(0.0, min(100.0, round(score, 2)))

    @staticmethod
    def _empty_analysis() -> CareerAnalysis:
        """Return empty analysis for candidates with no workplace data."""
        return CareerAnalysis(
            career_trend=CareerTrend('stable', 50.0, 50.0, 50.0, False, False),
            role_progression=RoleProgression([], 0, 0.0, 50.0, 50.0),
            technical_growth=TechnicalGrowth(0, 50.0, 'balanced', 50.0, False),
            red_flags=['No workplace history available'],
            strengths=[],
            career_stage='unknown',
            potential_score=50.0,
        )
