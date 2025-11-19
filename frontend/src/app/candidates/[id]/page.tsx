/**
 * Candidate detail page with matching vacancies
 */
'use client';

import { useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { useCandidate } from '@/lib/hooks/useCandidates';
import { useFindVacanciesForCandidate } from '@/lib/hooks/useMatching';
import {
  Users,
  Mail,
  Phone,
  MapPin,
  Briefcase,
  DollarSign,
  Globe,
  Github,
  Linkedin,
  Award,
  Target,
  Loader2,
  ArrowLeft,
  TrendingUp,
} from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { MatchCard } from '@/components/ui/MatchCard';
import { EmptyState } from '@/components/ui/EmptyState';
import { SkeletonMatchCard } from '@/components/ui/Skeleton';

export default function CandidateDetailPage() {
  const params = useParams();
  const candidateId = params.id as string;
  const [minScore, setMinScore] = useState(50);

  const { data: candidate, isLoading, error } = useCandidate(candidateId);
  const { data: matches, isLoading: matchesLoading } = useFindVacanciesForCandidate(
    candidateId,
    { min_score: minScore, page_size: 10 }
  );

  if (error) {
    return (
      <Card variant="elevated" className="text-center">
        <div className="text-red-600 text-lg font-semibold">Ошибка загрузки кандидата</div>
        <p className="text-gray-600 mt-2">{error.message}</p>
      </Card>
    );
  }

  if (isLoading || !candidate) {
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
        href="/candidates"
        className="inline-flex items-center text-blue-600 hover:text-blue-700"
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Назад к списку
      </Link>

      {/* Header */}
      <Card variant="glass" className="animate-fade-in">
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-4">
            <div className="h-20 w-20 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center shadow-lg">
              <Users className="h-10 w-10 text-white" />
            </div>
            <div>
              <h1 className="text-4xl font-bold gradient-text">{candidate.full_name}</h1>
              <p className="text-xl text-gray-600 mt-2">{candidate.grade || 'N/A'}</p>
            </div>
          </div>
          <Badge variant={candidate.status === 'active' ? 'success' : 'neutral'} size="lg">
            {candidate.status === 'active' ? 'Активен' : candidate.status}
          </Badge>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left column - Main info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Contact info */}
          <Card variant="elevated" hover className="animate-slide-up">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Контактная информация</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-center text-gray-700">
                <Mail className="h-5 w-5 mr-3 text-gray-400" />
                <a href={`mailto:${candidate.email}`} className="hover:text-blue-600">
                  {candidate.email}
                </a>
              </div>
              {candidate.phone && (
                <div className="flex items-center text-gray-700">
                  <Phone className="h-5 w-5 mr-3 text-gray-400" />
                  <a href={`tel:${candidate.phone}`} className="hover:text-blue-600">
                    {candidate.phone}
                  </a>
                </div>
              )}
              {candidate.current_location && (
                <div className="flex items-center text-gray-700">
                  <MapPin className="h-5 w-5 mr-3 text-gray-400" />
                  {candidate.current_location}
                </div>
              )}
              {candidate.github && (
                <div className="flex items-center text-gray-700">
                  <Github className="h-5 w-5 mr-3 text-gray-400" />
                  <a
                    href={candidate.github}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-blue-600"
                  >
                    GitHub
                  </a>
                </div>
              )}
              {candidate.linkedin && (
                <div className="flex items-center text-gray-700">
                  <Linkedin className="h-5 w-5 mr-3 text-gray-400" />
                  <a
                    href={candidate.linkedin}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-blue-600"
                  >
                    LinkedIn
                  </a>
                </div>
              )}
              {candidate.portfolio && (
                <div className="flex items-center text-gray-700">
                  <Globe className="h-5 w-5 mr-3 text-gray-400" />
                  <a
                    href={candidate.portfolio}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-blue-600"
                  >
                    Portfolio
                  </a>
                </div>
              )}
            </div>
          </Card>

          {/* Bio */}
          {candidate.bio && (
            <Card variant="elevated" hover className="animate-slide-up" style={{ animationDelay: '100ms' }}>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">О себе</h2>
              <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">{candidate.bio}</p>
            </Card>
          )}

          {/* Skills */}
          {candidate.skills && candidate.skills.length > 0 && (
            <Card variant="elevated" hover className="animate-slide-up" style={{ animationDelay: '200ms' }}>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Навыки</h2>
              <div className="flex flex-wrap gap-2">
                {candidate.skills.map((skill, index) => (
                  <Badge key={index} variant="info" size="md">
                    {skill}
                  </Badge>
                ))}
              </div>
            </Card>
          )}

          {/* Languages */}
          {candidate.languages && candidate.languages.length > 0 && (
            <Card variant="elevated" hover className="animate-slide-up" style={{ animationDelay: '300ms' }}>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Языки</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {candidate.languages.map((lang, index) => (
                  <div key={index} className="flex items-center space-x-2">
                    <Globe className="h-4 w-4 text-gray-400" />
                    <span className="text-gray-700">
                      {lang.language} - <span className="font-medium">{lang.level}</span>
                    </span>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </div>

        {/* Right column - Stats & Preferences */}
        <div className="space-y-6">
          {/* Experience */}
          <Card variant="gradient" className="animate-slide-up">
            <div className="flex items-center space-x-3 mb-4">
              <Briefcase className="h-5 w-5 text-blue-600" />
              <h2 className="text-lg font-semibold text-gray-900">Опыт работы</h2>
            </div>
            <div className="text-4xl font-bold text-blue-600">
              {Math.floor(candidate.experience_months / 12)} лет
            </div>
            <p className="text-sm text-gray-600 mt-1">
              {candidate.experience_months % 12} месяцев
            </p>
          </Card>

          {/* Salary expectations */}
          {candidate.salary_min && candidate.salary_max && (
            <Card variant="elevated" hover className="animate-slide-up" style={{ animationDelay: '100ms' }}>
              <div className="flex items-center space-x-3 mb-4">
                <DollarSign className="h-5 w-5 text-green-600" />
                <h2 className="text-lg font-semibold text-gray-900">Зарплатные ожидания</h2>
              </div>
              <div className="text-2xl font-bold text-gray-900">
                {candidate.salary_min.toLocaleString()} - {candidate.salary_max.toLocaleString()}
              </div>
              <p className="text-sm text-gray-600 mt-1">
                {candidate.salary_currency} / {candidate.salary_period === 'month' ? 'месяц' : candidate.salary_period}
              </p>
              <p className="text-sm text-gray-600">
                {candidate.salary_type === 'gross' ? 'До вычета налогов' : 'На руки'}
              </p>
            </Card>
          )}

          {/* Work preferences */}
          <Card variant="elevated" hover className="animate-slide-up" style={{ animationDelay: '200ms' }}>
            <div className="flex items-center space-x-3 mb-4">
              <Award className="h-5 w-5 text-purple-600" />
              <h2 className="text-lg font-semibold text-gray-900">Предпочтения</h2>
            </div>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Удаленная работа</span>
                <Badge variant={candidate.remote_work ? 'success' : 'neutral'} size="sm">
                  {candidate.remote_work ? 'Да' : 'Нет'}
                </Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Релокация</span>
                <Badge variant={candidate.relocation ? 'success' : 'neutral'} size="sm">
                  {candidate.relocation ? 'Да' : 'Нет'}
                </Badge>
              </div>
            </div>
          </Card>
        </div>
      </div>

      {/* Matching Vacancies */}
      <Card variant="elevated" className="animate-scale-in" style={{ animationDelay: '400ms' }}>
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
              <Target className="h-6 w-6 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Подходящие вакансии</h2>
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
                key={match.vacancy_id}
                type="vacancy"
                id={match.vacancy_id}
                title={match.vacancy?.position_name || 'Вакансия'}
                subtitle={match.vacancy?.company_name || 'Компания'}
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
            description={`Подходящие вакансии не найдены со скором выше ${minScore}. Попробуйте снизить порог или обновите профиль кандидата.`}
          />
        )}
      </Card>
    </div>
  );
}
