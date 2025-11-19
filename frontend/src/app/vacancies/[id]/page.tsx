/**
 * Vacancy detail page with matching candidates
 */
'use client';

import { useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { useVacancy } from '@/lib/hooks/useVacancies';
import { useFindCandidatesForVacancy } from '@/lib/hooks/useMatching';
import {
  Briefcase,
  Building2,
  MapPin,
  DollarSign,
  Calendar,
  Globe,
  Users,
  Target,
  Loader2,
  ArrowLeft,
  TrendingUp,
} from 'lucide-react';

export default function VacancyDetailPage() {
  const params = useParams();
  const vacancyId = params.id as string;
  const [minScore, setMinScore] = useState(50);

  const { data: vacancy, isLoading, error } = useVacancy(vacancyId);
  const { data: matches, isLoading: matchesLoading } = useFindCandidatesForVacancy(
    vacancyId,
    { min_score: minScore, page_size: 10 }
  );

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 text-lg">Ошибка загрузки вакансии</div>
        <p className="text-gray-600 mt-2">{error.message}</p>
      </div>
    );
  }

  if (isLoading || !vacancy) {
    return (
      <div className="flex justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  const getMatchQualityColor = (quality: string) => {
    switch (quality) {
      case 'excellent':
        return 'bg-green-100 text-green-800';
      case 'good':
        return 'bg-blue-100 text-blue-800';
      case 'fair':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getMatchQualityLabel = (quality: string) => {
    switch (quality) {
      case 'excellent':
        return 'Отлично';
      case 'good':
        return 'Хорошо';
      case 'fair':
        return 'Приемлемо';
      case 'poor':
        return 'Слабо';
      default:
        return quality;
    }
  };

  return (
    <div className="space-y-6">
      {/* Back button */}
      <Link
        href="/vacancies"
        className="inline-flex items-center text-blue-600 hover:text-blue-700"
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Назад к списку
      </Link>

      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-4">
            <div className="h-16 w-16 rounded-full bg-green-100 flex items-center justify-center">
              <Briefcase className="h-8 w-8 text-green-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{vacancy.position_name}</h1>
              <p className="text-lg text-gray-600 mt-1 flex items-center">
                <Building2 className="h-4 w-4 mr-2" />
                {vacancy.company_name}
              </p>
            </div>
          </div>
          <span
            className={`px-3 py-1 rounded-full text-sm font-medium ${
              vacancy.status === 'active'
                ? 'bg-green-100 text-green-800'
                : 'bg-gray-100 text-gray-800'
            }`}
          >
            {vacancy.status === 'active' ? 'Активна' : vacancy.status}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left column - Main info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Description */}
          {vacancy.description && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Описание</h2>
              <p className="text-gray-700 whitespace-pre-wrap">{vacancy.description}</p>
            </div>
          )}

          {/* Responsibilities */}
          {vacancy.responsibilities && vacancy.responsibilities.length > 0 && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Обязанности</h2>
              <ul className="space-y-2">
                {vacancy.responsibilities.map((resp, index) => (
                  <li key={index} className="flex items-start text-gray-700">
                    <span className="text-blue-600 mr-2">•</span>
                    {resp}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Requirements */}
          {vacancy.requirements && vacancy.requirements.length > 0 && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Требования</h2>
              <div className="space-y-4">
                {/* Required */}
                {vacancy.requirements.filter(r => r.importance === 'required').length > 0 && (
                  <div>
                    <h3 className="text-sm font-medium text-red-700 mb-2">Обязательные:</h3>
                    <div className="flex flex-wrap gap-2">
                      {vacancy.requirements
                        .filter(r => r.importance === 'required')
                        .map((req) => (
                          <span
                            key={req.id}
                            className="px-3 py-1.5 bg-red-50 text-red-700 rounded-md text-sm"
                          >
                            {req.technology?.name || req.technology_id}
                            {req.min_experience_years && ` (${req.min_experience_years}+ лет)`}
                          </span>
                        ))}
                    </div>
                  </div>
                )}

                {/* Nice to have */}
                {vacancy.requirements.filter(r => r.importance === 'nice_to_have').length > 0 && (
                  <div>
                    <h3 className="text-sm font-medium text-blue-700 mb-2">Желательно:</h3>
                    <div className="flex flex-wrap gap-2">
                      {vacancy.requirements
                        .filter(r => r.importance === 'nice_to_have')
                        .map((req) => (
                          <span
                            key={req.id}
                            className="px-3 py-1.5 bg-blue-50 text-blue-700 rounded-md text-sm"
                          >
                            {req.technology?.name || req.technology_id}
                          </span>
                        ))}
                    </div>
                  </div>
                )}

                {/* Plus */}
                {vacancy.requirements.filter(r => r.importance === 'plus').length > 0 && (
                  <div>
                    <h3 className="text-sm font-medium text-gray-700 mb-2">Будет плюсом:</h3>
                    <div className="flex flex-wrap gap-2">
                      {vacancy.requirements
                        .filter(r => r.importance === 'plus')
                        .map((req) => (
                          <span
                            key={req.id}
                            className="px-3 py-1.5 bg-gray-100 text-gray-700 rounded-md text-sm"
                          >
                            {req.technology?.name || req.technology_id}
                          </span>
                        ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Languages */}
          {vacancy.language_requirements && vacancy.language_requirements.length > 0 && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Требования к языкам</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {vacancy.language_requirements.map((lang, index) => (
                  <div key={index} className="flex items-center space-x-2">
                    <Globe className="h-4 w-4 text-gray-400" />
                    <span className="text-gray-700">
                      {lang.language} - <span className="font-medium">{lang.min_level}+</span>
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right column - Details */}
        <div className="space-y-6">
          {/* Salary */}
          {vacancy.salary_min && vacancy.salary_max && (
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center space-x-3 mb-4">
                <DollarSign className="h-5 w-5 text-gray-400" />
                <h2 className="text-lg font-semibold text-gray-900">Зарплата</h2>
              </div>
              <div className="text-2xl font-bold text-gray-900">
                {vacancy.salary_min.toLocaleString()} - {vacancy.salary_max.toLocaleString()}
              </div>
              <p className="text-sm text-gray-600 mt-1">
                {vacancy.salary_currency} / {vacancy.salary_period === 'month' ? 'месяц' : vacancy.salary_period}
              </p>
              <p className="text-sm text-gray-600">
                {vacancy.salary_type === 'gross' ? 'До вычета налогов' : 'На руки'}
              </p>
              {vacancy.salary_negotiable && (
                <p className="text-sm text-blue-600 mt-2">Обсуждаемо</p>
              )}
            </div>
          )}

          {/* Experience */}
          {(vacancy.min_experience_years || vacancy.max_experience_years) && (
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center space-x-3 mb-4">
                <Calendar className="h-5 w-5 text-gray-400" />
                <h2 className="text-lg font-semibold text-gray-900">Опыт работы</h2>
              </div>
              <div className="text-gray-900">
                {vacancy.min_experience_years && `От ${vacancy.min_experience_years}`}
                {vacancy.min_experience_years && vacancy.max_experience_years && ' до '}
                {vacancy.max_experience_years && `${vacancy.max_experience_years}`} лет
              </div>
            </div>
          )}

          {/* Locations */}
          {vacancy.locations && vacancy.locations.length > 0 && (
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center space-x-3 mb-4">
                <MapPin className="h-5 w-5 text-gray-400" />
                <h2 className="text-lg font-semibold text-gray-900">Локации</h2>
              </div>
              <div className="space-y-2">
                {vacancy.locations.map((location, index) => (
                  <div key={index} className="text-gray-700">
                    <div className="font-medium">
                      {location.city || location.country || 'Remote'}
                    </div>
                    {location.remote && (
                      <div className="text-sm text-blue-600">Возможна удаленная работа</div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Grade */}
          {vacancy.grade && (
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center space-x-3 mb-4">
                <Target className="h-5 w-5 text-gray-400" />
                <h2 className="text-lg font-semibold text-gray-900">Уровень</h2>
              </div>
              <div className="text-lg font-medium text-gray-900">{vacancy.grade}</div>
            </div>
          )}
        </div>
      </div>

      {/* Matching Candidates */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <Users className="h-6 w-6 text-green-600" />
            <h2 className="text-2xl font-semibold text-gray-900">Подходящие кандидаты</h2>
          </div>
          <div className="flex items-center space-x-2">
            <label className="text-sm text-gray-600">Минимальный скор:</label>
            <select
              value={minScore}
              onChange={(e) => setMinScore(Number(e.target.value))}
              className="px-3 py-1 border border-gray-300 rounded-md text-sm"
            >
              <option value="0">Все</option>
              <option value="50">50+</option>
              <option value="65">65+</option>
              <option value="80">80+</option>
            </select>
          </div>
        </div>

        {matchesLoading ? (
          <div className="flex justify-center py-8">
            <Loader2 className="h-6 w-6 animate-spin text-blue-600" />
          </div>
        ) : matches && matches.items.length > 0 ? (
          <div className="space-y-4">
            {matches.items.map((match) => (
              <div
                key={match.candidate_id}
                className="border border-gray-200 rounded-lg p-4 hover:border-blue-500 transition-colors"
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <Link
                      href={`/candidates/${match.candidate_id}`}
                      className="text-lg font-semibold text-gray-900 hover:text-blue-600"
                    >
                      {match.candidate?.full_name}
                    </Link>
                    <p className="text-gray-600">
                      {match.candidate?.grade} • {match.candidate?.experience_months && Math.floor(match.candidate.experience_months / 12)} лет опыта
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="text-3xl font-bold text-blue-600">
                      {match.score.total_score.toFixed(1)}
                    </div>
                    <span
                      className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${getMatchQualityColor(
                        match.score.match_quality
                      )}`}
                    >
                      {getMatchQualityLabel(match.score.match_quality)}
                    </span>
                  </div>
                </div>

                {/* Score breakdown */}
                <div className="grid grid-cols-4 gap-2 mb-3">
                  <div className="text-center">
                    <div className="text-sm font-semibold text-gray-900">
                      {match.score.breakdown.technologies.score.toFixed(0)}%
                    </div>
                    <div className="text-xs text-gray-600">Tech</div>
                  </div>
                  <div className="text-center">
                    <div className="text-sm font-semibold text-gray-900">
                      {match.score.breakdown.experience.score.toFixed(0)}%
                    </div>
                    <div className="text-xs text-gray-600">Exp</div>
                  </div>
                  <div className="text-center">
                    <div className="text-sm font-semibold text-gray-900">
                      {match.score.breakdown.skills.score.toFixed(0)}%
                    </div>
                    <div className="text-xs text-gray-600">Skills</div>
                  </div>
                  <div className="text-center">
                    <div className="text-sm font-semibold text-gray-900">
                      {match.score.confidence_level.toFixed(0)}%
                    </div>
                    <div className="text-xs text-gray-600">Conf</div>
                  </div>
                </div>

                {/* Highlights */}
                {match.highlights && match.highlights.length > 0 && (
                  <div className="mb-2">
                    <div className="text-sm font-medium text-green-700 mb-1">✓ Сильные стороны:</div>
                    <ul className="space-y-1">
                      {match.highlights.slice(0, 3).map((highlight, index) => (
                        <li key={index} className="text-sm text-gray-600 pl-4">
                          • {highlight}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Concerns */}
                {match.concerns && match.concerns.length > 0 && (
                  <div>
                    <div className="text-sm font-medium text-orange-700 mb-1">⚠ Зоны внимания:</div>
                    <ul className="space-y-1">
                      {match.concerns.slice(0, 2).map((concern, index) => (
                        <li key={index} className="text-sm text-gray-600 pl-4">
                          • {concern}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <TrendingUp className="h-12 w-12 text-gray-400 mx-auto mb-2" />
            <p className="text-gray-600">
              Подходящие кандидаты не найдены со скором выше {minScore}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
