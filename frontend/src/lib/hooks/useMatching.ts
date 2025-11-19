/**
 * React Query hooks for Matching API
 */
import { useQuery, useMutation } from '@tanstack/react-query';
import api from '../api';
import type { CandidateVacancyScore, MatchingListResponse } from '@/types';

export const useCalculateScore = () => {
  return useMutation({
    mutationFn: async ({ candidateId, vacancyId }: { candidateId: string; vacancyId: string }) => {
      const { data } = await api.post<CandidateVacancyScore>('/matching/score', null, {
        params: { candidate_id: candidateId, vacancy_id: vacancyId },
      });
      return data;
    },
  });
};

export const useFindVacanciesForCandidate = (
  candidateId: string,
  params?: {
    min_score?: number;
    match_quality?: string;
    page?: number;
    page_size?: number;
    sort_by?: string;
    sort_order?: string;
  }
) => {
  return useQuery({
    queryKey: ['candidate-vacancies', candidateId, params],
    queryFn: async () => {
      const { data } = await api.get<MatchingListResponse>(
        `/matching/candidates/${candidateId}/vacancies`,
        { params }
      );
      return data;
    },
    enabled: !!candidateId,
  });
};

export const useFindCandidatesForVacancy = (
  vacancyId: string,
  params?: {
    min_score?: number;
    match_quality?: string;
    page?: number;
    page_size?: number;
    sort_by?: string;
    sort_order?: string;
  }
) => {
  return useQuery({
    queryKey: ['vacancy-candidates', vacancyId, params],
    queryFn: async () => {
      const { data } = await api.get<MatchingListResponse>(
        `/matching/vacancies/${vacancyId}/candidates`,
        { params }
      );
      return data;
    },
    enabled: !!vacancyId,
  });
};
