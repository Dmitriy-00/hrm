/**
 * React Query hooks for Analytics API
 */
import { useQuery } from '@tanstack/react-query';
import api from '../api';

export interface AnalyticsStats {
  total_candidates: number;
  total_vacancies: number;
  active_vacancies: number;
  avg_match_score: number;
  top_matches: number;
  trends: {
    candidates: number;
    vacancies: number;
  };
}

export interface MatchesByScore {
  range: string;
  count: number;
}

export interface VacancyByStatus {
  status: string;
  count: number;
}

export interface CandidateByGrade {
  grade: string;
  count: number;
}

export interface TopMatch {
  candidate_id: string;
  vacancy_id: string;
  score: number;
  candidate: {
    full_name: string;
    grade: string;
  } | null;
  vacancy: {
    position_name: string;
    company_name: string;
  } | null;
}

export const useAnalyticsStats = () => {
  return useQuery({
    queryKey: ['analytics', 'stats'],
    queryFn: async () => {
      const { data } = await api.get<AnalyticsStats>('/analytics/stats');
      return data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useMatchesByScoreChart = () => {
  return useQuery({
    queryKey: ['analytics', 'matches-by-score'],
    queryFn: async () => {
      const { data } = await api.get<MatchesByScore[]>('/analytics/chart/matches-by-score');
      return data;
    },
    staleTime: 5 * 60 * 1000,
  });
};

export const useVacanciesByStatusChart = () => {
  return useQuery({
    queryKey: ['analytics', 'vacancies-by-status'],
    queryFn: async () => {
      const { data } = await api.get<VacancyByStatus[]>('/analytics/chart/vacancies-by-status');
      return data;
    },
    staleTime: 5 * 60 * 1000,
  });
};

export const useCandidatesByGradeChart = () => {
  return useQuery({
    queryKey: ['analytics', 'candidates-by-grade'],
    queryFn: async () => {
      const { data } = await api.get<CandidateByGrade[]>('/analytics/chart/candidates-by-grade');
      return data;
    },
    staleTime: 5 * 60 * 1000,
  });
};

export const useTopMatches = (limit: number = 10) => {
  return useQuery({
    queryKey: ['analytics', 'top-matches', limit],
    queryFn: async () => {
      const { data } = await api.get<TopMatch[]>('/analytics/top-matches', {
        params: { limit },
      });
      return data;
    },
    staleTime: 5 * 60 * 1000,
  });
};
