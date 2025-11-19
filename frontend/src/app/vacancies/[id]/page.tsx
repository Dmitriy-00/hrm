/**
 * Vacancy detail page with matching candidates - Modern redesign
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
  Award,
  Sparkles,
} from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { MatchCard } from '@/components/ui/MatchCard';
import { EmptyState } from '@/components/ui/EmptyState';
import { SkeletonMatchCard } from '@/components/ui/Skeleton';

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
      <Card variant="elevated" className="text-center">
        <div className="text-red-600 text-lg font-semibold">Ошибка загрузки вакансии</div>
        <p className="text-gray-600 mt-2">{error.message}</p>
      </Card>
    );
  }

  if (isLoading || !vacancy) {
    return (
      <div className="flex justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Back button */}
      <Link
        href="/vacancies"
        className="inline-flex items-center text-blue-600 hover:text-blue-700 font-medium transition-colors"
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Назад к списку
      </Link>

      {/* Header */}
      <Card variant="glass" className="animate-fade-in">
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-4">
            <div className="h-20 w-20 rounded-full bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center shadow-lg">
              <Briefcase className="h-10 w-10 text-white" />
            </div>
            <div>
              <h1 className="text-4xl font-bold gradient-text">{vacancy.position_name}</h1>
              <p className="text-xl text-gray-600 mt-2 flex items-center">
                <Building2 className="h-5 w-5 mr-2" />
                {vacancy.company_name}
              </p>
            </div>
          </div>
          <div className="flex flex-col items-end space-y-2">
            <Badge variant={vacancy.status === 'active' ? 'success' : 'neutral'} size="lg">
              {vacancy.status === 'active' ? 'Активна' : vacancy.status}
            </Badge>
            <Link href={`/vacancies/${vacancyId}/candidates`}>
              <button className="flex items-center px-4 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-lg hover:from-purple-700 hover:to-indigo-700 transition-all shadow-lg hover:shadow-xl">
                <Sparkles className="h-4 w-4 mr-2" />
                AI Подбор
              </button>
            </Link>
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left column - Main info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Description */}
          {vacancy.description && (
            <Card variant="elevated" hover className="animate-slide-up">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Описание</h2>
              <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">{vacancy.description}</p>
            </Card>
          )}

          {/* Responsibilities */}
          {vacancy.responsibilities && vacancy.responsibilities.length > 0 && (
            <Card variant="elevated" hover className="animate-slide-up" style={{ animationDelay: '100ms' }}>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Обязанности</h2>
              <ul className="space-y-2.5">
                {vacancy.responsibilities.map((resp, index) => (
                  <li key={index} className="flex items-start text-gray-700">
                    <span className="text-blue-600 mr-3 font-bold">•</span>
                    <span>{resp}</span>
                  </li>
                ))}
              </ul>
            </Card>
          )}

          {/* Requirements */}
          {vacancy.requirements && vacancy.requirements.length > 0 && (
            <Card variant="elevated" hover className="animate-slide-up" style={{ animationDelay: '200ms' }}>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Требования</h2>
              <div className="space-y-4">
                {/* Required */}
                {vacancy.requirements.filter(r => r.importance === 'required').length > 0 && (
                  <div>
                    <h3 className="text-sm font-semibold text-red-700 mb-3 flex items-center">
                      <Award className="h-4 w-4 mr-2" />
                      Обязательные:
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {vacancy.requirements
                        .filter(r => r.importance === 'required')
                        .map((req) => (
                          <Badge key={req.id} variant="danger" size="md">
                            {req.technology?.name || req.technology_id}
                            {req.min_experience_years && ` (${req.min_experience_years}+ лет)`}
                          </Badge>
                        ))}
                    </div>
                  </div>
                )}

                {/* Nice to have */}
                {vacancy.requirements.filter(r => r.importance === 'nice_to_have').length > 0 && (
                  <div>
                    <h3 className="text-sm font-semibold text-blue-700 mb-3">Желательно:</h3>
                    <div className="flex flex-wrap gap-2">
                      {vacancy.requirements
                        .filter(r => r.importance === 'nice_to_have')
                        .map((req) => (
                          <Badge key={req.id} variant="info" size="md">
                            {req.technology?.name || req.technology_id}
                          </Badge>
                        ))}
                    </div>
                  </div>
                )}

                {/* Plus */}
                {vacancy.requirements.filter(r => r.importance === 'plus').length > 0 && (
                  <div>
                    <h3 className="text-sm font-semibold text-gray-700 mb-3">Будет плюсом:</h3>
                    <div className="flex flex-wrap gap-2">
                      {vacancy.requirements
                        .filter(r => r.importance === 'plus')
                        .map((req) => (
                          <Badge key={req.id} variant="neutral" size="md">
                            {req.technology?.name || req.technology_id}
                          </Badge>
                        ))}
                    </div>
                  </div>
                )}
              </div>
            </Card>
          )}

          {/* Languages */}
          {vacancy.language_requirements && vacancy.language_requirements.length > 0 && (
            <Card variant="elevated" hover className="animate-slide-up" style={{ animationDelay: '300ms' }}>
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
            </Card>
          )}
        </div>

        {/* Right column - Details */}
        <div className="space-y-6">
          {/* Salary */}
          {vacancy.salary_min && vacancy.salary_max && (
            <Card variant="gradient" className="animate-slide-up">
              <div className="flex items-center space-x-3 mb-4">
                <DollarSign className="h-5 w-5 text-green-600" />
                <h2 className="text-lg font-semibold text-gray-900">Зарплата</h2>
              </div>
              <div className="text-3xl font-bold text-green-600">
                {vacancy.salary_min.toLocaleString()} - {vacancy.salary_max.toLocaleString()}
              </div>
              <p className="text-sm text-gray-600 mt-2">
                {vacancy.salary_currency} / {vacancy.salary_period === 'month' ? 'месяц' : vacancy.salary_period}
              </p>
              <p className="text-sm text-gray-600">
                {vacancy.salary_type === 'gross' ? 'До вычета налогов' : 'На руки'}
              </p>
              {vacancy.salary_negotiable && (
                <Badge variant="info" size="sm" className="mt-3">
                  Обсуждаемо
                </Badge>
              )}
            </Card>
          )}

          {/* Experience */}
          {(vacancy.min_experience_years || vacancy.max_experience_years) && (
            <Card variant="elevated" hover className="animate-slide-up" style={{ animationDelay: '100ms' }}>
              <div className="flex items-center space-x-3 mb-4">
                <Calendar className="h-5 w-5 text-purple-600" />
                <h2 className="text-lg font-semibold text-gray-900">Опыт работы</h2>
              </div>
              <div className="text-2xl font-bold text-purple-600">
                {vacancy.min_experience_years && `${vacancy.min_experience_years}`}
                {vacancy.min_experience_years && vacancy.max_experience_years && ' - '}
                {vacancy.max_experience_years && `${vacancy.max_experience_years}`} лет
              </div>
            </Card>
          )}

          {/* Locations */}
          {vacancy.locations && vacancy.locations.length > 0 && (
            <Card variant="elevated" hover className="animate-slide-up" style={{ animationDelay: '200ms' }}>
              <div className="flex items-center space-x-3 mb-4">
                <MapPin className="h-5 w-5 text-orange-600" />
                <h2 className="text-lg font-semibold text-gray-900">Локации</h2>
              </div>
              <div className="space-y-3">
                {vacancy.locations.map((location, index) => (
                  <div key={index}>
                    <div className="font-medium text-gray-900">
                      {location.city || location.country || 'Remote'}
                    </div>
                    {location.remote && (
                      <Badge variant="success" size="sm" className="mt-1">
                        Возможна удаленная работа
                      </Badge>
                    )}
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Grade */}
          {vacancy.grade && (
            <Card variant="elevated" hover className="animate-slide-up" style={{ animationDelay: '300ms' }}>
              <div className="flex items-center space-x-3 mb-4">
                <Target className="h-5 w-5 text-blue-600" />
                <h2 className="text-lg font-semibold text-gray-900">Уровень</h2>
              </div>
              <Badge variant="primary" size="lg">
                {vacancy.grade}
              </Badge>
            </Card>
          )}
        </div>
      </div>

      {/* Matching Candidates */}
      <Card variant="elevated" className="animate-scale-in" style={{ animationDelay: '400ms' }}>
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center">
              <Users className="h-6 w-6 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Подходящие кандидаты</h2>
              <p className="text-sm text-gray-600">
                Найдено {matches?.total || 0} совпадений
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <label className="text-sm font-medium text-gray-600">Минимальный скор:</label>
            <select
              value={minScore}
              onChange={(e) => setMinScore(Number(e.target.value))}
              className="px-4 py-2 border-2 border-gray-200 rounded-lg text-sm font-medium focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            >
              <option value="0">Все</option>
              <option value="50">50+</option>
              <option value="65">65+</option>
              <option value="80">80+</option>
            </select>
          </div>
        </div>

        {matchesLoading ? (
          <div className="space-y-4">
            <SkeletonMatchCard />
            <SkeletonMatchCard />
          </div>
        ) : matches && matches.items.length > 0 ? (
          <div className="space-y-4">
            {matches.items.map((match) => (
              <MatchCard
                key={match.candidate_id}
                type="candidate"
                id={match.candidate_id}
                title={match.candidate?.full_name || 'Кандидат'}
                subtitle={`${match.candidate?.grade || 'N/A'} • ${match.candidate?.experience_months ? Math.floor(match.candidate.experience_months / 12) : 0} лет опыта`}
                score={match.score}
                highlights={match.highlights}
                concerns={match.concerns}
                showBreakdown={false}
              />
            ))}
          </div>
        ) : (
          <EmptyState
            icon={TrendingUp}
            title="Совпадения не найдены"
            description={`Подходящие кандидаты не найдены со скором выше ${minScore}. Попробуйте снизить порог или обновите требования вакансии.`}
          />
        )}
      </Card>
    </div>
  );
}
