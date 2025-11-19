/**
 * React Query hooks for Ontology APIs (Job Titles, Technologies, Standards, Industries)
 */
import { useQuery } from '@tanstack/react-query';
import api from '../api';
import type { JobTitle, Technology, Standard, Industry } from '@/types';

export const useJobTitles = () => {
  return useQuery({
    queryKey: ['job-titles'],
    queryFn: async () => {
      const { data } = await api.get<JobTitle[]>('/job-titles');
      return data;
    },
  });
};

export const useTechnologies = (params?: { category?: string }) => {
  return useQuery({
    queryKey: ['technologies', params],
    queryFn: async () => {
      const { data } = await api.get<Technology[]>('/technologies', { params });
      return data;
    },
  });
};

export const useStandards = () => {
  return useQuery({
    queryKey: ['standards'],
    queryFn: async () => {
      const { data } = await api.get<Standard[]>('/standards');
      return data;
    },
  });
};

export const useIndustries = () => {
  return useQuery({
    queryKey: ['industries'],
    queryFn: async () => {
      const { data } = await api.get<Industry[]>('/industries');
      return data;
    },
  });
};
