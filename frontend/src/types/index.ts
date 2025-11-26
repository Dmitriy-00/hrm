/**
 * TypeScript types for HRM Platform
 */

export interface JobTitle {
  id: string;
  name: string;
  slug: string;
  parent_id?: string;
  level: number;
  path: string;
  aliases: string[];
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface Technology {
  id: string;
  name: string;
  slug: string;
  category: string;
  parent_id?: string;
  path: string;
  tags: string[];
  related_technologies: string[];
  difficulty_level: number;
  popularity_score: number;
  tech_metadata: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface Standard {
  id: string;
  name: string;
  slug: string;
  category: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface Industry {
  id: string;
  name: string;
  slug: string;
  parent_id?: string;
  level: number;
  path: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface Candidate {
  id: string;
  user_id?: string;
  full_name: string;
  email: string;
  phone?: string;
  telegram?: string;
  linkedin?: string;
  github?: string;
  portfolio?: string;
  job_title_id?: string;
  grade?: string;
  experience_months: number;
  bio?: string;
  skills: string[];
  current_location?: string;
  remote_work: boolean;
  relocation: boolean;
  relocation_preferences: string[];
  languages: LanguageProficiency[];
  citizenship: string[];
  work_permit: string[];
  salary_min?: number;
  salary_max?: number;
  salary_currency: string;
  salary_type: string;
  salary_period: string;
  employment_type: string[];
  notice_period_days?: number;
  status: string;
  resume_url?: string;
  cv_parsed_data: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface LanguageProficiency {
  language: string;
  level: string; // A1, A2, B1, B2, C1, C2, native
}

export interface Workplace {
  id: string;
  candidate_id: string;
  company_id?: string;
  company_name: string;
  industry_id?: string;
  position: string;
  job_title_id?: string;
  start_date: string;
  end_date?: string;
  is_current: boolean;
  duration_months?: number;
  location?: string;
  role?: string;
  team_size?: number;
  responsibilities: string[];
  achievements: string[];
  skills: string[];
  standards_used: string[];
  project_types: string[];
  technologies?: WorkplaceTechnology[];
  created_at: string;
  updated_at: string;
}

export interface WorkplaceTechnology {
  id: string;
  workplace_id: string;
  technology_id: string;
  technology?: Technology;
  proficiency: number;
  usage_intensity: string;
  experience_months?: number;
}

export interface Vacancy {
  id: string;
  company_id?: string;
  company_name: string;
  job_title_id?: string;
  position_name: string;
  grade?: string;
  min_experience_years?: number;
  max_experience_years?: number;
  locations: VacancyLocation[];
  timezone_requirements: string[];
  language_requirements: LanguageRequirement[];
  citizenship_allowed: string[];
  citizenship_restricted: string[];
  salary_min?: number;
  salary_max?: number;
  salary_currency: string;
  salary_type: string;
  salary_period: string;
  salary_negotiable: boolean;
  status: string;
  deadline?: string;
  description?: string;
  responsibilities: string[];
  interview_process: Record<string, any>;
  external_links: Record<string, string>;
  requirements?: VacancyRequirement[];
  created_by?: string;
  created_at: string;
  updated_at: string;
}

export interface VacancyLocation {
  city?: string;
  country?: string;
  remote?: boolean;
  office_address?: string;
}

export interface LanguageRequirement {
  language: string;
  min_level: string;
}

export interface VacancyRequirement {
  id: string;
  vacancy_id: string;
  technology_id: string;
  technology?: Technology;
  importance: 'required' | 'nice_to_have' | 'plus';
  min_experience_years?: number;
  proficiency_level: number;
  created_at: string;
}

// Matching and Scoring types
export interface TechnologyMatchDetail {
  technology_id: string;
  technology_name: string;
  candidate_proficiency: number;
  required_proficiency: number;
  candidate_experience_months: number;
  required_experience_months: number;
  importance: string;
  match_score: number;
}

export interface TechnologiesBreakdown {
  score: number;
  matched: number;
  required: number;
  details: TechnologyMatchDetail[];
}

export interface ExperienceBreakdown {
  score: number;
  candidate_years: number;
  required_min: number;
  required_max: number;
  is_within_range: boolean;
}

export interface SkillsBreakdown {
  score: number;
  matched: number;
  required: number;
  missing: string[];
}

export interface StandardsBreakdown {
  score: number;
  matched: number;
  required: number;
  missing: string[];
}

export interface IndustryBreakdown {
  score: number;
  has_experience: boolean;
  experience_months: number;
}

export interface LanguageMatch {
  language: string;
  candidate_level: number;
  required_level: number;
  is_met: boolean;
}

export interface LanguagesBreakdown {
  score: number;
  matched: string[];
  missing: string[];
  details: LanguageMatch[];
}

export interface LocationBreakdown {
  score: number;
  is_compatible: boolean;
  details: string;
}

export interface SalaryBreakdown {
  score: number;
  has_overlap: boolean;
  details: string;
}

export interface ScoreBreakdown {
  technologies: TechnologiesBreakdown;
  experience: ExperienceBreakdown;
  skills: SkillsBreakdown;
  standards: StandardsBreakdown;
  industry: IndustryBreakdown;
  languages: LanguagesBreakdown;
  location: LocationBreakdown;
  salary: SalaryBreakdown;
}

export interface BonusPoint {
  reason: string;
  points: number;
}

export interface CandidateVacancyScore {
  candidate_id: string;
  vacancy_id: string;
  total_score: number;
  breakdown: ScoreBreakdown;
  confidence_level: number;
  missing_critical_requirements: string[];
  bonus_points: BonusPoint[];
  match_quality: 'excellent' | 'good' | 'fair' | 'poor';
  calculated_at: string;
}

export interface MatchingResult {
  candidate_id: string;
  vacancy_id: string;
  candidate?: Partial<Candidate>;
  vacancy?: Partial<Vacancy>;
  score: CandidateVacancyScore;
  highlights: string[];
  concerns: string[];
  recommendation?: string;
}

export interface MatchingListResponse {
  items: MatchingResult[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// API Response types
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page?: number;
  page_size?: number;
  total_pages?: number;
}

export interface ApiError {
  detail: string;
  status_code?: number;
}
