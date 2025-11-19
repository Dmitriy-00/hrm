/**
 * Candidates list page
 */
'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useCandidates } from '@/lib/hooks/useCandidates';
import { Users, Mail, MapPin, Briefcase, DollarSign, Search, Loader2 } from 'lucide-react';

export default function CandidatesPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const { data, isLoading, error } = useCandidates({ limit: 100 });

  const filteredCandidates = data?.items?.filter(candidate =>
    candidate.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    candidate.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 text-lg">Ошибка загрузки кандидатов</div>
        <p className="text-gray-600 mt-2">{error.message}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Кандидаты</h1>
          <p className="text-gray-600 mt-1">
            {data?.total || 0} кандидатов в базе
          </p>
        </div>
      </div>

      {/* Search */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
          <input
            type="text"
            placeholder="Поиск по имени или email..."
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

      {/* Candidates list */}
      {!isLoading && filteredCandidates && filteredCandidates.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredCandidates.map((candidate) => (
            <Link
              key={candidate.id}
              href={`/candidates/${candidate.id}`}
              className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6 group"
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="h-12 w-12 rounded-full bg-blue-100 flex items-center justify-center">
                    <Users className="h-6 w-6 text-blue-600" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                      {candidate.full_name}
                    </h3>
                    <p className="text-sm text-gray-600">{candidate.grade || 'N/A'}</p>
                  </div>
                </div>
              </div>

              {/* Info */}
              <div className="space-y-2">
                <div className="flex items-center text-sm text-gray-600">
                  <Mail className="h-4 w-4 mr-2" />
                  {candidate.email}
                </div>

                {candidate.current_location && (
                  <div className="flex items-center text-sm text-gray-600">
                    <MapPin className="h-4 w-4 mr-2" />
                    {candidate.current_location}
                  </div>
                )}

                <div className="flex items-center text-sm text-gray-600">
                  <Briefcase className="h-4 w-4 mr-2" />
                  {Math.floor(candidate.experience_months / 12)} лет опыта
                </div>

                {candidate.salary_min && candidate.salary_max && (
                  <div className="flex items-center text-sm text-gray-600">
                    <DollarSign className="h-4 w-4 mr-2" />
                    {candidate.salary_min.toLocaleString()}-{candidate.salary_max.toLocaleString()} {candidate.salary_currency}
                  </div>
                )}
              </div>

              {/* Skills */}
              {candidate.skills && candidate.skills.length > 0 && (
                <div className="mt-4 flex flex-wrap gap-2">
                  {candidate.skills.slice(0, 3).map((skill, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded-md"
                    >
                      {skill}
                    </span>
                  ))}
                  {candidate.skills.length > 3 && (
                    <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-md">
                      +{candidate.skills.length - 3}
                    </span>
                  )}
                </div>
              )}

              {/* Status badge */}
              <div className="mt-4 pt-4 border-t">
                <span
                  className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    candidate.status === 'active'
                      ? 'bg-green-100 text-green-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {candidate.status === 'active' ? 'Активен' : candidate.status}
                </span>
              </div>
            </Link>
          ))}
        </div>
      )}

      {/* Empty state */}
      {!isLoading && (!filteredCandidates || filteredCandidates.length === 0) && (
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Кандидаты не найдены
          </h3>
          <p className="text-gray-600">
            {searchTerm
              ? 'Попробуйте изменить параметры поиска'
              : 'Начните с добавления первого кандидата'}
          </p>
        </div>
      )}
    </div>
  );
}
