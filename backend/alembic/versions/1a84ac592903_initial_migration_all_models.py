"""Initial migration: all models

Revision ID: 1a84ac592903
Revises:
Create Date: 2025-11-19 06:19:41.060549

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1a84ac592903'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create UUID extension
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True, index=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255)),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_superuser', sa.Boolean(), default=False),
        sa.Column('role', sa.String(20), default='user'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Job Titles table (ontology)
    op.create_table(
        'job_titles',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('slug', sa.String(255), nullable=False, unique=True, index=True),
        sa.Column('parent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('job_titles.id'), nullable=True),
        sa.Column('level', sa.Integer(), nullable=False, default=0),
        sa.Column('path', sa.String(500), nullable=False, index=True),
        sa.Column('aliases', postgresql.ARRAY(sa.String()), default=[]),
        sa.Column('description', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Technologies table (ontology)
    op.create_table(
        'technologies',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('slug', sa.String(255), nullable=False, unique=True, index=True),
        sa.Column('category', sa.String(50), nullable=False, index=True),
        sa.Column('parent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('technologies.id'), nullable=True),
        sa.Column('path', sa.String(500), nullable=False, index=True),
        sa.Column('tags', postgresql.ARRAY(sa.String()), default=[]),
        sa.Column('related_technologies', postgresql.ARRAY(postgresql.UUID(as_uuid=True)), default=[]),
        sa.Column('difficulty_level', sa.Integer(), default=3),
        sa.Column('popularity_score', sa.Integer(), default=50),
        sa.Column('tech_metadata', postgresql.JSON(), default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Standards table (ontology)
    op.create_table(
        'standards',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('slug', sa.String(255), nullable=False, unique=True, index=True),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Industries table (ontology)
    op.create_table(
        'industries',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('slug', sa.String(255), nullable=False, unique=True, index=True),
        sa.Column('parent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('industries.id'), nullable=True),
        sa.Column('level', sa.Integer(), nullable=False, default=0),
        sa.Column('path', sa.String(500), nullable=False, index=True),
        sa.Column('description', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Candidates table
    op.create_table(
        'candidates',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('full_name', sa.String(255), nullable=False, index=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True, index=True),
        sa.Column('phone', sa.String(50)),
        sa.Column('telegram', sa.String(100)),
        sa.Column('linkedin', sa.String(255)),
        sa.Column('github', sa.String(255)),
        sa.Column('portfolio', sa.String(255)),
        sa.Column('job_title_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('job_titles.id'), nullable=True),
        sa.Column('grade', sa.String(20), index=True),
        sa.Column('experience_months', sa.Integer(), default=0),
        sa.Column('bio', sa.Text()),
        sa.Column('skills', postgresql.JSON(), default=[]),
        sa.Column('current_location', sa.String(255)),
        sa.Column('remote_work', sa.Boolean(), default=True),
        sa.Column('relocation', sa.Boolean(), default=False),
        sa.Column('relocation_preferences', postgresql.ARRAY(sa.String()), default=[]),
        sa.Column('languages', postgresql.JSON(), default=[]),
        sa.Column('citizenship', postgresql.ARRAY(sa.String()), default=[]),
        sa.Column('work_permit', postgresql.ARRAY(sa.String()), default=[]),
        sa.Column('salary_min', sa.Integer()),
        sa.Column('salary_max', sa.Integer()),
        sa.Column('salary_currency', sa.String(3), default='USD'),
        sa.Column('salary_type', sa.String(20), default='gross'),
        sa.Column('salary_period', sa.String(20), default='month'),
        sa.Column('employment_type', postgresql.ARRAY(sa.String()), default=['full_time']),
        sa.Column('notice_period_days', sa.Integer()),
        sa.Column('status', sa.String(20), default='active', index=True),
        sa.Column('resume_url', sa.String(500)),
        sa.Column('cv_parsed_data', postgresql.JSON(), default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Companies table
    op.create_table(
        'companies',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, unique=True, index=True),
        sa.Column('website', sa.String(255)),
        sa.Column('industry_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('industries.id'), nullable=True),
        sa.Column('size', sa.String(20)),
        sa.Column('description', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Workplaces table
    op.create_table(
        'workplaces',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('candidate_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('candidates.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('companies.id'), nullable=True),
        sa.Column('company_name', sa.String(255), nullable=False),
        sa.Column('industry_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('industries.id'), nullable=True),
        sa.Column('position', sa.String(255), nullable=False),
        sa.Column('job_title_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('job_titles.id'), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('is_current', sa.Boolean(), default=False),
        sa.Column('duration_months', sa.Integer()),
        sa.Column('location', sa.String(255)),
        sa.Column('role', sa.String(50)),
        sa.Column('team_size', sa.Integer()),
        sa.Column('responsibilities', postgresql.ARRAY(sa.String()), default=[]),
        sa.Column('achievements', postgresql.ARRAY(sa.String()), default=[]),
        sa.Column('skills', postgresql.JSON(), default=[]),
        sa.Column('standards_used', postgresql.JSON(), default=[]),
        sa.Column('project_types', postgresql.ARRAY(sa.String()), default=[]),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Workplace Technologies table (many-to-many with additional fields)
    op.create_table(
        'workplace_technologies',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('workplace_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('workplaces.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('technology_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('technologies.id'), nullable=False, index=True),
        sa.Column('proficiency', sa.Integer(), default=3),
        sa.Column('usage_intensity', sa.String(20), default='secondary'),
        sa.Column('experience_months', sa.Integer()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint('workplace_id', 'technology_id', name='unique_workplace_technology'),
    )

    # Vacancies table
    op.create_table(
        'vacancies',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('companies.id'), nullable=True),
        sa.Column('company_name', sa.String(255), nullable=False, index=True),
        sa.Column('job_title_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('job_titles.id'), nullable=True),
        sa.Column('position_name', sa.String(255), nullable=False, index=True),
        sa.Column('grade', sa.String(20), index=True),
        sa.Column('min_experience_years', sa.Integer()),
        sa.Column('max_experience_years', sa.Integer()),
        sa.Column('locations', postgresql.JSON(), default=[]),
        sa.Column('timezone_requirements', postgresql.ARRAY(sa.String()), default=[]),
        sa.Column('language_requirements', postgresql.JSON(), default=[]),
        sa.Column('citizenship_allowed', postgresql.ARRAY(sa.String()), default=[]),
        sa.Column('citizenship_restricted', postgresql.ARRAY(sa.String()), default=[]),
        sa.Column('salary_min', sa.Integer()),
        sa.Column('salary_max', sa.Integer()),
        sa.Column('salary_currency', sa.String(3), default='USD'),
        sa.Column('salary_type', sa.String(20), default='gross'),
        sa.Column('salary_period', sa.String(20), default='month'),
        sa.Column('salary_negotiable', sa.Boolean(), default=True),
        sa.Column('status', sa.String(20), default='active', index=True),
        sa.Column('deadline', sa.Date()),
        sa.Column('description', sa.Text()),
        sa.Column('responsibilities', postgresql.ARRAY(sa.String()), default=[]),
        sa.Column('interview_process', postgresql.JSON(), default={}),
        sa.Column('external_links', postgresql.JSON(), default={}),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Vacancy Requirements table
    op.create_table(
        'vacancy_requirements',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('vacancy_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('vacancies.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('technology_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('technologies.id'), nullable=False, index=True),
        sa.Column('importance', sa.String(20), default='required'),
        sa.Column('min_experience_years', sa.Integer()),
        sa.Column('proficiency_level', sa.Integer(), default=3),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint('vacancy_id', 'technology_id', name='unique_vacancy_requirement'),
    )

    # Selection (candidate-vacancy matches) table
    op.create_table(
        'selections',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('candidate_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('candidates.id'), nullable=False, index=True),
        sa.Column('vacancy_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('vacancies.id'), nullable=False, index=True),
        sa.Column('score', sa.Float()),
        sa.Column('status', sa.String(50), default='new', index=True),
        sa.Column('stage', sa.String(50)),
        sa.Column('added_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('notes', sa.Text()),
        sa.Column('interview_feedback', postgresql.JSON(), default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.UniqueConstraint('candidate_id', 'vacancy_id', name='unique_candidate_vacancy'),
    )

    # Create indexes
    op.create_index('idx_workplaces_candidate', 'workplaces', ['candidate_id'])
    op.create_index('idx_workplaces_dates', 'workplaces', ['start_date', 'end_date'])
    op.create_index('idx_vacancy_requirements_vacancy', 'vacancy_requirements', ['vacancy_id'])
    op.create_index('idx_selections_candidate_vacancy', 'selections', ['candidate_id', 'vacancy_id'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('selections')
    op.drop_table('vacancy_requirements')
    op.drop_table('vacancies')
    op.drop_table('workplace_technologies')
    op.drop_table('workplaces')
    op.drop_table('companies')
    op.drop_table('candidates')
    op.drop_table('industries')
    op.drop_table('standards')
    op.drop_table('technologies')
    op.drop_table('job_titles')
    op.drop_table('users')
