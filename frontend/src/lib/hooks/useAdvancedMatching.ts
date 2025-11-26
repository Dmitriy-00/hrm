/**
 * React Query hooks for Advanced Matching API
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../api';

export interface AdvancedMatchingResult {
  base_score: any;
  semantic_match: SemanticMatchResult;
  career_analysis: CareerAnalysis;
  cultural_fit: CulturalFitScore;
  final_score: number;
  match_explanation: string;
  detailed_strengths: string[];
  detailed_concerns: string[];
  recommendation: 'highly_recommend' | 'recommend' | 'consider' | 'not_recommend';
  ml_features?: Record<string, number>;
}

export interface SemanticMatchResult {
  bio_description_similarity: number;
  skill_extraction_match: number;
  keyword_overlap: number;
  missing_keywords: string[];
  key_phrases_match: string[];
}

export interface CareerAnalysis {
  career_trend: CareerTrend;
  role_progression: RoleProgression;
  technical_growth: TechnicalGrowth;
  red_flags: string[];
  strengths: string[];
  career_stage: string;
  potential_score: number;
}

export interface CareerTrend {
  direction: 'upward' | 'stable' | 'lateral' | 'downward';
  growth_rate: number;
  consistency: number;
  specialization_level: number;
  leadership_progression: boolean;
  technical_depth_growth: boolean;
}

export interface RoleProgression {
  role_levels: string[];
  promotions_count: number;
  avg_tenure_months: number;
  job_hopping_score: number;
  role_diversity_score: number;
}

export interface TechnicalGrowth {
  technologies_learned: number;
  tech_stack_modernity: number;
  breadth_vs_depth: 'specialist' | 'balanced' | 'generalist';
  learning_velocity: number;
  tech_leadership: boolean;
}

export interface CulturalFitScore {
  company_size_fit: number;
  work_style_fit: number;
  team_environment_fit: number;
  values_alignment: number;
  overall_fit: number;
  fit_explanation: string;
}

export interface SkillExtraction {
  technical_skills: string[];
  soft_skills: string[];
  tools: string[];
  frameworks: string[];
  methodologies: string[];
}

export interface MatchRecommendation {
  candidate_id: string;
  candidate_name: string;
  score: number;
  recommendation: string;
  match_quality: string;
  highlights: string[];
  concerns: string[];
}

export const useAdvancedScore = (
  candidateId: string | null,
  vacancyId: string | null,
  includeMlFeatures: boolean = false
) => {
  return useQuery({
    queryKey: ['advanced-score', candidateId, vacancyId, includeMlFeatures],
    queryFn: async () => {
      if (!candidateId || !vacancyId) return null;

      const { data } = await api.post<AdvancedMatchingResult>(
        '/advanced-matching/advanced-score',
        null,
        {
          params: {
            candidate_id: candidateId,
            vacancy_id: vacancyId,
            include_ml_features: includeMlFeatures,
          },
        }
      );
      return data;
    },
    enabled: !!candidateId && !!vacancyId,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useCareerAnalysis = (candidateId: string | null) => {
  return useQuery({
    queryKey: ['career-analysis', candidateId],
    queryFn: async () => {
      if (!candidateId) return null;

      const { data } = await api.get<CareerAnalysis>(
        `/advanced-matching/career-analysis/${candidateId}`
      );
      return data;
    },
    enabled: !!candidateId,
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
};

export const useExtractSkills = () => {
  return useMutation({
    mutationFn: async (text: string) => {
      const { data } = await api.post<SkillExtraction>(
        '/advanced-matching/text-analysis/extract-skills',
        null,
        {
          params: { text },
        }
      );
      return data;
    },
  });
};

export const useTextSimilarity = () => {
  return useMutation({
    mutationFn: async ({ text1, text2 }: { text1: string; text2: string }) => {
      const { data } = await api.post<{ similarity_score: number; interpretation: string }>(
        '/advanced-matching/text-analysis/similarity',
        null,
        {
          params: { text1, text2 },
        }
      );
      return data;
    },
  });
};

export const useMatchingRecommendations = (
  vacancyId: string | null,
  minScore: number = 60,
  limit: number = 20
) => {
  return useQuery({
    queryKey: ['matching-recommendations', vacancyId, minScore, limit],
    queryFn: async () => {
      if (!vacancyId) return null;

      const { data } = await api.get<{
        vacancy_id: string;
        candidates: MatchRecommendation[];
        total_found: number;
        min_score_threshold: number;
      }>(`/advanced-matching/matching/recommendations/${vacancyId}`, {
        params: { min_score: minScore, limit },
      });
      return data;
    },
    enabled: !!vacancyId,
    staleTime: 3 * 60 * 1000, // 3 minutes
  });
};

export const useExplainMatch = (
  candidateId: string | null,
  vacancyId: string | null
) => {
  return useQuery({
    queryKey: ['explain-match', candidateId, vacancyId],
    queryFn: async () => {
      if (!candidateId || !vacancyId) return null;

      const { data } = await api.post<{
        candidate: { id: string; name: string; grade: string };
        vacancy: { id: string; position: string; company: string };
        final_score: number;
        recommendation: string;
        explanation: string;
        breakdown: Record<string, number>;
        strengths: string[];
        concerns: string[];
        career_insights: {
          stage: string;
          trajectory: string;
          growth_rate: number;
          red_flags: string[];
        };
        missing_requirements: string[];
      }>('/advanced-matching/explain-match', null, {
        params: {
          candidate_id: candidateId,
          vacancy_id: vacancyId,
        },
      });
      return data;
    },
    enabled: !!candidateId && !!vacancyId,
    staleTime: 5 * 60 * 1000,
  });
};

export const useBatchScore = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      vacancyId,
      candidateIds,
      useAdvancedScoring = true,
      includeMlFeatures = false,
    }: {
      vacancyId: string;
      candidateIds: string[];
      useAdvancedScoring?: boolean;
      includeMlFeatures?: boolean;
    }) => {
      const { data } = await api.post<{
        vacancy_id: string;
        results: AdvancedMatchingResult[];
        processing_time_seconds: number;
        total_candidates: number;
      }>('/advanced-matching/batch-score', {
        vacancy_id: vacancyId,
        candidate_ids: candidateIds,
        use_advanced_scoring: useAdvancedScoring,
        include_ml_features: includeMlFeatures,
      });
      return data;
    },
    onSuccess: (data) => {
      // Invalidate related queries
      queryClient.invalidateQueries({ queryKey: ['matching-recommendations'] });
    },
  });
};
