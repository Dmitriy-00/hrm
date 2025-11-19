/**
 * React Query hooks for Candidates API
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../api';
import type { Candidate, PaginatedResponse } from '@/types';

export const useCandidates = (params?: {
  skip?: number;
  limit?: number;
  status?: string;
}) => {
  return useQuery({
    queryKey: ['candidates', params],
    queryFn: async () => {
      const { data } = await api.get<PaginatedResponse<Candidate>>('/candidates', {
        params,
      });
      return data;
    },
  });
};

export const useCandidate = (id: string) => {
  return useQuery({
    queryKey: ['candidate', id],
    queryFn: async () => {
      const { data } = await api.get<Candidate>(`/candidates/${id}`);
      return data;
    },
    enabled: !!id,
  });
};

export const useCreateCandidate = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (candidate: Partial<Candidate>) => {
      const { data } = await api.post<Candidate>('/candidates', candidate);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['candidates'] });
    },
  });
};

export const useUpdateCandidate = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, updates }: { id: string; updates: Partial<Candidate> }) => {
      const { data} = await api.patch<Candidate>(`/candidates/${id}`, updates);
      return data;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['candidates'] });
      queryClient.invalidateQueries({ queryKey: ['candidate', data.id] });
    },
  });
};

export const useDeleteCandidate = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`/candidates/${id}`);
      return id;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['candidates'] });
    },
  });
};

export const useSearchCandidates = () => {
  return useMutation({
    mutationFn: async (searchParams: any) => {
      const { data } = await api.post<PaginatedResponse<Candidate>>('/candidates/search', searchParams);
      return data;
    },
  });
};
