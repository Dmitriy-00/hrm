/**
 * React Query hooks for Vacancies API
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../api';
import type { Vacancy, PaginatedResponse } from '@/types';

export const useVacancies = (params?: {
  skip?: number;
  limit?: number;
  status?: string;
}) => {
  return useQuery({
    queryKey: ['vacancies', params],
    queryFn: async () => {
      const { data } = await api.get<PaginatedResponse<Vacancy>>('/vacancies', {
        params,
      });
      return data;
    },
  });
};

export const useVacancy = (id: string) => {
  return useQuery({
    queryKey: ['vacancy', id],
    queryFn: async () => {
      const { data } = await api.get<Vacancy>(`/vacancies/${id}`);
      return data;
    },
    enabled: !!id,
  });
};

export const useCreateVacancy = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (vacancy: Partial<Vacancy>) => {
      const { data } = await api.post<Vacancy>('/vacancies', vacancy);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['vacancies'] });
    },
  });
};

export const useUpdateVacancy = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, updates }: { id: string; updates: Partial<Vacancy> }) => {
      const { data } = await api.patch<Vacancy>(`/vacancies/${id}`, updates);
      return data;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['vacancies'] });
      queryClient.invalidateQueries({ queryKey: ['vacancy', data.id] });
    },
  });
};

export const useSearchVacancies = () => {
  return useMutation({
    mutationFn: async (searchParams: any) => {
      const { data } = await api.post<PaginatedResponse<Vacancy>>('/vacancies/search', searchParams);
      return data;
    },
  });
};
