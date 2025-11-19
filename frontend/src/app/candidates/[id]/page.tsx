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
      <div className="text-center py-12">
        <div className="text-red-600 text-lg">Ошибка загрузки кандидата</div>
        <p className="text-gray-600 mt-2">{error.message}</p>
      </div>
    );
  }

  if (isLoading || !candidate) {
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
        href="/candidates"
        className="inline-flex items-center text-blue-600 hover:text-blue-700"
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Назад к списку
      </Link>

      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-4">
            <div className="h-16 w-16 rounded-full bg-blue-100 flex items-center justify-center">
              <Users className="h-8 w-8 text-blue-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{candidate.full_name}</h1>
              <p className="text-lg text-gray-600 mt-1">{candidate.grade || 'N/A'}</p>
            </div>
          </div>
          <span
            className={`px-3 py-1 rounded-full text-sm font-medium ${
              candidate.status === 'active'
                ? 'bg-green-100 text-green-800'
                : 'bg-gray-100 text-gray-800'
            }`}
          >
            {candidate.status === 'active' ? 'Активен' : candidate.status}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left column - Main info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Contact info */}
          <div className="bg-white rounded-lg shadow p-6">
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
          </div>

          {/* Bio */}
          {candidate.bio && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">О себе</h2>
              <p className="text-gray-700 whitespace-pre-wrap">{candidate.bio}</p>
            </div>
          )}

          {/* Skills */}
          {candidate.skills && candidate.skills.length > 0 && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Навыки</h2>
              <div className="flex flex-wrap gap-2">
                {candidate.skills.map((skill, index) => (
                  <span
                    key={index}
                    className="px-3 py-1.5 bg-blue-50 text-blue-700 rounded-md text-sm font-medium"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Languages */}
          {candidate.languages && candidate.languages.length > 0 && (
            <div className="bg-white rounded-lg shadow p-6">
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
            </div>
          )}
        </div>

        {/* Right column - Stats & Preferences */}
        <div className="space-y-6">
          {/* Experience */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center space-x-3 mb-4">
              <Briefcase className="h-5 w-5 text-gray-400" />
              <h2 className="text-lg font-semibold text-gray-900">Опыт работы</h2>
            </div>
            <div className="text-3xl font-bold text-blue-600">
              {Math.floor(candidate.experience_months / 12)} лет
            </div>
            <p className="text-sm text-gray-600 mt-1">
              {candidate.experience_months % 12} месяцев
            </p>
          </div>

          {/* Salary expectations */}
          {candidate.salary_min && candidate.salary_max && (
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center space-x-3 mb-4">
                <DollarSign className="h-5 w-5 text-gray-400" />
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
            </div>
          )}

          {/* Work preferences */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center space-x-3 mb-4">
              <Award className="h-5 w-5 text-gray-400" />
              <h2 className="text-lg font-semibold text-gray-900">Предпочтения</h2>
            </div>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Удаленная работа</span>
                <span className={`px-2 py-1 rounded text-xs font-medium ${
                  candidate.remote_work ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
                }`}>
                  {candidate.remote_work ? 'Да' : 'Нет'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Релокация</span>
                <span className={`px-2 py-1 rounded text-xs font-medium ${
                  candidate.relocation ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
                }`}>
                  {candidate.relocation ? 'Да' : 'Нет'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Matching Vacancies */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <Target className="h-6 w-6 text-blue-600" />
            <h2 className="text-2xl font-semibold text-gray-900">Подходящие вакансии</h2>
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
                key={match.vacancy_id}
                className="border border-gray-200 rounded-lg p-4 hover:border-blue-500 transition-colors"
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <Link
                      href={`/vacancies/${match.vacancy_id}`}
                      className="text-lg font-semibold text-gray-900 hover:text-blue-600"
                    >
                      {match.vacancy?.position_name}
                    </Link>
                    <p className="text-gray-600">{match.vacancy?.company_name}</p>
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
              Подходящие вакансии не найдены со скором выше {minScore}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
