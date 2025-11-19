/**
 * Vacancies list page
 */
'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useVacancies } from '@/lib/hooks/useVacancies';
import { Briefcase, Building2, MapPin, DollarSign, Search, Loader2, Calendar } from 'lucide-react';

export default function VacanciesPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const { data, isLoading, error } = useVacancies({ limit: 100 });

  const filteredVacancies = data?.items?.filter(vacancy =>
    vacancy.position_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    vacancy.company_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 text-lg">Ошибка загрузки вакансий</div>
        <p className="text-gray-600 mt-2">{error.message}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Вакансии</h1>
          <p className="text-gray-600 mt-1">
            {data?.total || 0} открытых вакансий
          </p>
        </div>
      </div>

      {/* Search */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
          <input
            type="text"
            placeholder="Поиск по должности или компании..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* Loading state */}
      {isLoading && (
        <div className="flex justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
        </div>
      )}

      {/* Vacancies list */}
      {!isLoading && filteredVacancies && filteredVacancies.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredVacancies.map((vacancy) => (
            <Link
              key={vacancy.id}
              href={`/vacancies/${vacancy.id}`}
              className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6 group"
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="h-12 w-12 rounded-full bg-green-100 flex items-center justify-center">
                    <Briefcase className="h-6 w-6 text-green-600" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                      {vacancy.position_name}
                    </h3>
                    <p className="text-sm text-gray-600">{vacancy.grade || 'Any level'}</p>
                  </div>
                </div>
              </div>

              {/* Company */}
              <div className="flex items-center text-gray-600 mb-3">
                <Building2 className="h-4 w-4 mr-2" />
                <span className="font-medium">{vacancy.company_name}</span>
              </div>

              {/* Info */}
              <div className="space-y-2">
                {vacancy.locations && vacancy.locations.length > 0 && (
                  <div className="flex items-center text-sm text-gray-600">
                    <MapPin className="h-4 w-4 mr-2" />
                    {vacancy.locations[0].city || 'Remote'}
                    {vacancy.locations[0].remote && ' (Remote)'}
                    {vacancy.locations.length > 1 && ` +${vacancy.locations.length - 1}`}
                  </div>
                )}

                {vacancy.salary_min && vacancy.salary_max && (
                  <div className="flex items-center text-sm text-gray-600">
                    <DollarSign className="h-4 w-4 mr-2" />
                    {vacancy.salary_min.toLocaleString()}-{vacancy.salary_max.toLocaleString()} {vacancy.salary_currency}
                    {vacancy.salary_negotiable && ' (обсуждаемо)'}
                  </div>
                )}

                {(vacancy.min_experience_years || vacancy.max_experience_years) && (
                  <div className="flex items-center text-sm text-gray-600">
                    <Calendar className="h-4 w-4 mr-2" />
                    {vacancy.min_experience_years && `от ${vacancy.min_experience_years}`}
                    {vacancy.min_experience_years && vacancy.max_experience_years && ' до '}
                    {vacancy.max_experience_years && `${vacancy.max_experience_years}`} лет опыта
                  </div>
                )}
              </div>

              {/* Requirements */}
              {vacancy.requirements && vacancy.requirements.length > 0 && (
                <div className="mt-4">
                  <p className="text-xs text-gray-500 mb-2">Требования:</p>
                  <div className="flex flex-wrap gap-2">
                    {vacancy.requirements.slice(0, 4).map((req) => (
                      <span
                        key={req.id}
                        className={`px-2 py-1 text-xs rounded-md ${
                          req.importance === 'required'
                            ? 'bg-red-50 text-red-700'
                            : req.importance === 'nice_to_have'
                            ? 'bg-blue-50 text-blue-700'
                            : 'bg-gray-50 text-gray-700'
                        }`}
                      >
                        {req.technology?.name || req.technology_id}
                      </span>
                    ))}
                    {vacancy.requirements.length > 4 && (
                      <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-md">
                        +{vacancy.requirements.length - 4}
                      </span>
                    )}
                  </div>
                </div>
              )}

              {/* Status badge */}
              <div className="mt-4 pt-4 border-t">
                <span
                  className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    vacancy.status === 'active'
                      ? 'bg-green-100 text-green-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {vacancy.status === 'active' ? 'Активна' : vacancy.status}
                </span>
              </div>
            </Link>
          ))}
        </div>
      )}

      {/* Empty state */}
      {!isLoading && (!filteredVacancies || filteredVacancies.length === 0) && (
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <Briefcase className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Вакансии не найдены
          </h3>
          <p className="text-gray-600">
            {searchTerm
              ? 'Попробуйте изменить параметры поиска'
              : 'Начните с добавления первой вакансии'}
          </p>
        </div>
      )}
    </div>
  );
}
