"""
Analytics API endpoints for dashboard metrics and statistics
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from app.db.database import get_db
from app.db.models.candidate import Candidate
from app.db.models.vacancy import Vacancy
from app.db.models.selection import Selection

router = APIRouter()


@router.get("/stats")
def get_analytics_stats(db: Session = Depends(get_db)):
    """
    Get overall statistics for dashboard
    """
    # Total candidates
    total_candidates = db.query(func.count(Candidate.id)).scalar() or 0

    # Total vacancies
    total_vacancies = db.query(func.count(Vacancy.id)).scalar() or 0

    # Active vacancies
    active_vacancies = db.query(func.count(Vacancy.id)).filter(
        Vacancy.status == "active"
    ).scalar() or 0

    # Total selections
    total_selections = db.query(func.count(Selection.id)).scalar() or 0

    # Hired count
    hired_count = db.query(func.count(Selection.id)).filter(
        Selection.status == "hired"
    ).scalar() or 0

    # Calculate trends (compare with last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    # New candidates in last 30 days
    new_candidates_30d = db.query(func.count(Candidate.id)).filter(
        Candidate.created_at >= thirty_days_ago
    ).scalar() or 0

    # New vacancies in last 30 days
    new_vacancies_30d = db.query(func.count(Vacancy.id)).filter(
        Vacancy.created_at >= thirty_days_ago
    ).scalar() or 0

    # Calculate trends as percentages (simplified)
    candidate_trend = round((new_candidates_30d / total_candidates * 100) if total_candidates > 0 else 0, 1)
    vacancy_trend = round((new_vacancies_30d / total_vacancies * 100) if total_vacancies > 0 else 0, 1)

    return {
        "total_candidates": total_candidates,
        "total_vacancies": total_vacancies,
        "active_vacancies": active_vacancies,
        "avg_match_score": 75.0,  # Mock value - in real implementation would calculate from matching service
        "top_matches": hired_count,
        "trends": {
            "candidates": candidate_trend,
            "vacancies": vacancy_trend,
        }
    }


@router.get("/chart/matches-by-score")
def get_matches_by_score_chart(db: Session = Depends(get_db)):
    """
    Get distribution of matches by score ranges
    Mock data - in real implementation would use cached matching results
    """
    # Mock data for demonstration
    total_selections = db.query(func.count(Selection.id)).scalar() or 0

    # Distribute selections across score ranges (mock distribution)
    ranges = [
        {"range": "0-20", "count": int(total_selections * 0.05)},
        {"range": "21-40", "count": int(total_selections * 0.10)},
        {"range": "41-60", "count": int(total_selections * 0.25)},
        {"range": "61-80", "count": int(total_selections * 0.35)},
        {"range": "81-100", "count": int(total_selections * 0.25)},
    ]

    return ranges


@router.get("/chart/vacancies-by-status")
def get_vacancies_by_status_chart(db: Session = Depends(get_db)):
    """
    Get vacancies grouped by status
    """
    results = db.query(
        Vacancy.status,
        func.count(Vacancy.id).label('count')
    ).group_by(Vacancy.status).all()

    return [
        {
            "status": result.status or "unknown",
            "count": result.count
        }
        for result in results
    ]


@router.get("/chart/candidates-by-grade")
def get_candidates_by_grade_chart(db: Session = Depends(get_db)):
    """
    Get candidates grouped by grade
    """
    results = db.query(
        Candidate.grade,
        func.count(Candidate.id).label('count')
    ).filter(
        Candidate.grade.isnot(None)
    ).group_by(Candidate.grade).all()

    return [
        {
            "grade": result.grade,
            "count": result.count
        }
        for result in results
    ]


@router.get("/top-matches")
def get_top_matches(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get top selections (candidate-vacancy pairs)
    """
    results = db.query(Selection).filter(
        Selection.status.in_(["offer", "hired"])
    ).order_by(
        desc(Selection.created_at)
    ).limit(limit).all()

    # Mock scores for demonstration - in real implementation would calculate from matching service
    from random import randint

    return [
        {
            "candidate_id": str(result.candidate_id),
            "vacancy_id": str(result.vacancy_id),
            "score": randint(80, 95),  # Mock score
            "candidate": {
                "full_name": result.candidate.full_name if result.candidate else None,
                "grade": result.candidate.grade if result.candidate else None,
            } if result.candidate else None,
            "vacancy": {
                "position_name": result.vacancy.position_name if result.vacancy else None,
                "company_name": result.vacancy.company_name if result.vacancy else None,
            } if result.vacancy else None,
        }
        for result in results
    ]
