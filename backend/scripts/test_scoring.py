"""Test script for scoring functionality."""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.services.candidate_service import CandidateService
from app.services.vacancy_service import VacancyService
from app.services.scoring_service import ScoringService
from app.models.schemas.scoring import ScoringWeights


def test_scoring():
    """Test scoring functionality with seed data."""
    # Create database connection (using default SQLite for testing)
    DATABASE_URL = "sqlite:///./test_hrm.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        print("=" * 80)
        print("Testing Candidate-Vacancy Scoring")
        print("=" * 80)
        print()

        # Get all candidates and vacancies
        candidates, _ = CandidateService.get_all(db, limit=100)
        vacancies = VacancyService.get_active(db, limit=100)

        if not candidates:
            print("❌ No candidates found. Please run seed_candidates.py first.")
            return

        if not vacancies:
            print("❌ No vacancies found. Please run seed_vacancies.py first.")
            return

        print(f"Found {len(candidates)} candidates and {len(vacancies)} vacancies")
        print()

        # Test scoring for each candidate-vacancy pair
        for candidate in candidates[:3]:  # Test first 3 candidates
            print(f"\n{'=' * 80}")
            print(f"Candidate: {candidate.full_name} ({candidate.grade})")
            print(f"Experience: {candidate.experience_months / 12:.1f} years")
            print(f"{'=' * 80}\n")

            for vacancy in vacancies[:3]:  # Test first 3 vacancies
                print(f"\n--- Vacancy: {vacancy.position_name} at {vacancy.company_name} ---")

                try:
                    # Calculate score
                    score = ScoringService.calculate_score(
                        db, candidate, vacancy, ScoringWeights()
                    )

                    # Print results
                    print(f"\n✅ Total Score: {score.total_score:.1f}/100")
                    print(f"Match Quality: {score.match_quality.upper()}")
                    print(f"Confidence: {score.confidence_level:.1f}%")

                    # Print breakdown
                    print(f"\nScore Breakdown:")
                    print(f"  • Technologies: {score.breakdown.technologies.score:.1f}/100 "
                          f"({score.breakdown.technologies.matched}/{score.breakdown.technologies.required} matched)")
                    print(f"  • Experience: {score.breakdown.experience.score:.1f}/100")
                    print(f"  • Skills: {score.breakdown.skills.score:.1f}/100 "
                          f"({score.breakdown.skills.matched}/{score.breakdown.skills.required} matched)")
                    print(f"  • Standards: {score.breakdown.standards.score:.1f}/100")
                    print(f"  • Industry: {score.breakdown.industry.score:.1f}/100")
                    print(f"  • Languages: {score.breakdown.languages.score:.1f}/100")
                    print(f"  • Location: {score.breakdown.location.score:.1f}/100")
                    print(f"  • Salary: {score.breakdown.salary.score:.1f}/100")

                    # Print highlights
                    highlights = ScoringService.generate_highlights(score)
                    if highlights:
                        print(f"\n✨ Highlights:")
                        for highlight in highlights:
                            print(f"  + {highlight}")

                    # Print concerns
                    concerns = ScoringService.generate_concerns(score)
                    if concerns:
                        print(f"\n⚠️  Concerns:")
                        for concern in concerns:
                            print(f"  - {concern}")

                    # Print bonus points
                    if score.bonus_points:
                        print(f"\n🎁 Bonus Points:")
                        for bonus in score.bonus_points:
                            print(f"  + {bonus.reason}: +{bonus.points} points")

                    # Print missing critical requirements
                    if score.missing_critical_requirements:
                        print(f"\n❌ Missing Critical Requirements:")
                        for req in score.missing_critical_requirements:
                            print(f"  - {req}")

                except Exception as e:
                    print(f"❌ Error calculating score: {str(e)}")
                    import traceback
                    traceback.print_exc()

        print("\n" + "=" * 80)
        print("✅ Scoring test completed!")
        print("=" * 80)

    finally:
        db.close()


if __name__ == "__main__":
    test_scoring()
