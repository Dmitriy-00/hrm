/**
 * Side-by-side candidate comparison component
 */
'use client';

import React from 'react';
import {
  CheckCircle,
  XCircle,
  TrendingUp,
  Award,
  Code,
  Briefcase,
  Languages,
  MapPin,
  DollarSign,
  Users,
  ChevronRight,
} from 'lucide-react';
import { Card } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { ScoreGauge } from './ScoreGauge';
import type { AdvancedMatchingResult } from '@/lib/hooks/useAdvancedMatching';

interface CandidateComparisonProps {
  results: AdvancedMatchingResult[];
  candidateNames: Record<string, string>;
  vacancyName?: string;
}

export function CandidateComparison({ results, candidateNames, vacancyName }: CandidateComparisonProps) {
  if (results.length === 0) {
    return (
      <Card variant="elevated" className="text-center p-8">
        <p className="text-gray-600">Нет кандидатов для сравнения</p>
      </Card>
    );
  }

  const getRecommendationLabel = (rec: string) => {
    switch (rec) {
      case 'highly_recommend': return 'Настоятельно';
      case 'recommend': return 'Рекомендуется';
      case 'consider': return 'Рассмотреть';
      default: return 'Не рекомендуется';
    }
  };

  const getRecommendationColor = (rec: string) => {
    switch (rec) {
      case 'highly_recommend': return 'success';
      case 'recommend': return 'primary';
      case 'consider': return 'warning';
      default: return 'danger';
    }
  };

  const getDirectionLabel = (direction: string) => {
    switch (direction) {
      case 'upward': return 'Восходящая';
      case 'downward': return 'Нисходящая';
      case 'lateral': return 'Горизонтальная';
      default: return 'Стабильная';
    }
  };

  return (
    <div className="space-y-6">
      {/* Vacancy Header */}
      {vacancyName && (
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">Сравнение кандидатов</h2>
          <p className="text-gray-600 mt-1">для вакансии: {vacancyName}</p>
        </div>
      )}

      {/* Overall Scores Comparison */}
      <Card variant="gradient" className="overflow-hidden">
        <div className="grid gap-4" style={{ gridTemplateColumns: `repeat(${results.length}, 1fr)` }}>
          {results.map((result, index) => (
            <div key={index} className="text-center">
              <h3 className="text-lg font-bold text-white mb-4 truncate">
                {candidateNames[result.base_score.candidate_id] || 'Unknown'}
              </h3>
              <div className="flex justify-center mb-3">
                <ScoreGauge score={result.final_score} size="md" showValue />
              </div>
              <Badge
                variant={getRecommendationColor(result.recommendation) as any}
                size="sm"
              >
                {getRecommendationLabel(result.recommendation)}
              </Badge>
            </div>
          ))}
        </div>
      </Card>

      {/* Detailed Comparison Table */}
      <Card variant="elevated">
        <div className="overflow-x-auto">
          <table className="w-full">
            <tbody className="divide-y divide-gray-200">
              {/* Candidate Names Row */}
              <tr className="bg-gray-50">
                <td className="py-3 px-4 font-semibold text-gray-700 sticky left-0 bg-gray-50 z-10">
                  Кандидат
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center font-medium text-gray-900">
                    {candidateNames[result.base_score.candidate_id] || 'Unknown'}
                  </td>
                ))}
              </tr>

              {/* Final Score */}
              <tr>
                <td className="py-3 px-4 font-semibold text-gray-700 sticky left-0 bg-white z-10">
                  Финальный скор
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center">
                    <span className="text-2xl font-bold text-gray-900">
                      {Math.round(result.final_score)}
                    </span>
                  </td>
                ))}
              </tr>

              {/* Technologies */}
              <tr className="bg-gray-50">
                <td colSpan={results.length + 1} className="py-2 px-4 font-bold text-gray-900 flex items-center">
                  <Code className="h-5 w-5 mr-2 text-blue-600" />
                  Технологии
                </td>
              </tr>
              <tr>
                <td className="py-3 px-4 text-sm text-gray-600 pl-8 sticky left-0 bg-white z-10">
                  Скор
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center">
                    <div className="flex items-center justify-center space-x-2">
                      <div className="flex-1 h-2 bg-gray-200 rounded-full max-w-[100px]">
                        <div
                          className="h-full bg-gradient-to-r from-blue-500 to-blue-600 rounded-full"
                          style={{ width: `${result.base_score.breakdown.technologies.score}%` }}
                        />
                      </div>
                      <span className="text-sm font-semibold">
                        {Math.round(result.base_score.breakdown.technologies.score)}%
                      </span>
                    </div>
                  </td>
                ))}
              </tr>
              <tr>
                <td className="py-3 px-4 text-sm text-gray-600 pl-8 sticky left-0 bg-white z-10">
                  Совпадений
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center text-sm">
                    {result.base_score.breakdown.technologies.matched}/{result.base_score.breakdown.technologies.required}
                  </td>
                ))}
              </tr>

              {/* Experience */}
              <tr className="bg-gray-50">
                <td colSpan={results.length + 1} className="py-2 px-4 font-bold text-gray-900 flex items-center">
                  <Briefcase className="h-5 w-5 mr-2 text-green-600" />
                  Опыт
                </td>
              </tr>
              <tr>
                <td className="py-3 px-4 text-sm text-gray-600 pl-8 sticky left-0 bg-white z-10">
                  Скор
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center">
                    <div className="flex items-center justify-center space-x-2">
                      <div className="flex-1 h-2 bg-gray-200 rounded-full max-w-[100px]">
                        <div
                          className="h-full bg-gradient-to-r from-green-500 to-emerald-500 rounded-full"
                          style={{ width: `${result.base_score.breakdown.experience.score}%` }}
                        />
                      </div>
                      <span className="text-sm font-semibold">
                        {Math.round(result.base_score.breakdown.experience.score)}%
                      </span>
                    </div>
                  </td>
                ))}
              </tr>
              <tr>
                <td className="py-3 px-4 text-sm text-gray-600 pl-8 sticky left-0 bg-white z-10">
                  Годы опыта
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center text-sm">
                    {result.base_score.breakdown.experience.candidate_years} лет
                  </td>
                ))}
              </tr>

              {/* Semantic Match */}
              <tr className="bg-gray-50">
                <td colSpan={results.length + 1} className="py-2 px-4 font-bold text-gray-900 flex items-center">
                  <Award className="h-5 w-5 mr-2 text-indigo-600" />
                  Семантическое совпадение
                </td>
              </tr>
              <tr>
                <td className="py-3 px-4 text-sm text-gray-600 pl-8 sticky left-0 bg-white z-10">
                  Сходство текстов
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center text-sm font-semibold">
                    {Math.round(result.semantic_match.bio_description_similarity)}%
                  </td>
                ))}
              </tr>
              <tr>
                <td className="py-3 px-4 text-sm text-gray-600 pl-8 sticky left-0 bg-white z-10">
                  Совпадение навыков
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center text-sm font-semibold">
                    {Math.round(result.semantic_match.skill_extraction_match)}%
                  </td>
                ))}
              </tr>

              {/* Career Analysis */}
              <tr className="bg-gray-50">
                <td colSpan={results.length + 1} className="py-2 px-4 font-bold text-gray-900 flex items-center">
                  <TrendingUp className="h-5 w-5 mr-2 text-purple-600" />
                  Карьерный анализ
                </td>
              </tr>
              <tr>
                <td className="py-3 px-4 text-sm text-gray-600 pl-8 sticky left-0 bg-white z-10">
                  Карьерный этап
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center">
                    <Badge variant="secondary" size="sm">
                      {result.career_analysis.career_stage.toUpperCase()}
                    </Badge>
                  </td>
                ))}
              </tr>
              <tr>
                <td className="py-3 px-4 text-sm text-gray-600 pl-8 sticky left-0 bg-white z-10">
                  Траектория
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center text-sm">
                    {getDirectionLabel(result.career_analysis.career_trend.direction)}
                  </td>
                ))}
              </tr>
              <tr>
                <td className="py-3 px-4 text-sm text-gray-600 pl-8 sticky left-0 bg-white z-10">
                  Потенциал
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center text-sm font-semibold">
                    {Math.round(result.career_analysis.potential_score)}%
                  </td>
                ))}
              </tr>
              <tr>
                <td className="py-3 px-4 text-sm text-gray-600 pl-8 sticky left-0 bg-white z-10">
                  Продвижения
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center text-sm">
                    {result.career_analysis.role_progression.promotions_count}
                  </td>
                ))}
              </tr>
              <tr>
                <td className="py-3 px-4 text-sm text-gray-600 pl-8 sticky left-0 bg-white z-10">
                  Стабильность работы
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center text-sm font-semibold">
                    {Math.round(result.career_analysis.role_progression.job_hopping_score)}%
                  </td>
                ))}
              </tr>
              <tr>
                <td className="py-3 px-4 text-sm text-gray-600 pl-8 sticky left-0 bg-white z-10">
                  Изучено технологий
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center text-sm">
                    {result.career_analysis.technical_growth.technologies_learned}
                  </td>
                ))}
              </tr>

              {/* Cultural Fit */}
              <tr className="bg-gray-50">
                <td colSpan={results.length + 1} className="py-2 px-4 font-bold text-gray-900 flex items-center">
                  <Users className="h-5 w-5 mr-2 text-pink-600" />
                  Культурное соответствие
                </td>
              </tr>
              <tr>
                <td className="py-3 px-4 text-sm text-gray-600 pl-8 sticky left-0 bg-white z-10">
                  Общий фит
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center text-sm font-semibold">
                    {Math.round(result.cultural_fit.overall_fit)}%
                  </td>
                ))}
              </tr>
              <tr>
                <td className="py-3 px-4 text-sm text-gray-600 pl-8 sticky left-0 bg-white z-10">
                  Стиль работы
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center text-sm">
                    {Math.round(result.cultural_fit.work_style_fit)}%
                  </td>
                ))}
              </tr>

              {/* Other Metrics */}
              <tr className="bg-gray-50">
                <td colSpan={results.length + 1} className="py-2 px-4 font-bold text-gray-900">
                  Дополнительные метрики
                </td>
              </tr>
              <tr>
                <td className="py-3 px-4 text-sm text-gray-600 pl-8 sticky left-0 bg-white z-10 flex items-center">
                  <Languages className="h-4 w-4 mr-2 text-gray-400" />
                  Языки
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center text-sm">
                    {Math.round(result.base_score.breakdown.languages.score)}%
                  </td>
                ))}
              </tr>
              <tr>
                <td className="py-3 px-4 text-sm text-gray-600 pl-8 sticky left-0 bg-white z-10 flex items-center">
                  <MapPin className="h-4 w-4 mr-2 text-gray-400" />
                  Локация
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center">
                    {result.base_score.breakdown.location.compatible ? (
                      <CheckCircle className="h-5 w-5 text-green-600 mx-auto" />
                    ) : (
                      <XCircle className="h-5 w-5 text-red-600 mx-auto" />
                    )}
                  </td>
                ))}
              </tr>
              <tr>
                <td className="py-3 px-4 text-sm text-gray-600 pl-8 sticky left-0 bg-white z-10 flex items-center">
                  <DollarSign className="h-4 w-4 mr-2 text-gray-400" />
                  Зарплата
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center">
                    {result.base_score.breakdown.salary.overlap ? (
                      <CheckCircle className="h-5 w-5 text-green-600 mx-auto" />
                    ) : (
                      <XCircle className="h-5 w-5 text-red-600 mx-auto" />
                    )}
                  </td>
                ))}
              </tr>

              {/* Red Flags */}
              <tr className="bg-red-50">
                <td className="py-3 px-4 text-sm font-semibold text-red-900 pl-8 sticky left-0 bg-red-50 z-10">
                  Красные флаги
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center">
                    <Badge variant="danger" size="sm">
                      {result.career_analysis.red_flags.length}
                    </Badge>
                  </td>
                ))}
              </tr>

              {/* Missing Critical Requirements */}
              <tr className="bg-red-50">
                <td className="py-3 px-4 text-sm font-semibold text-red-900 pl-8 sticky left-0 bg-red-50 z-10">
                  Критические недостатки
                </td>
                {results.map((result, index) => (
                  <td key={index} className="py-3 px-4 text-center">
                    <Badge variant="danger" size="sm">
                      {result.base_score.missing_critical_requirements.length}
                    </Badge>
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
      </Card>

      {/* Detailed Strengths & Concerns */}
      <div className="grid grid-cols-1 gap-6" style={{ gridTemplateColumns: `repeat(${Math.min(results.length, 3)}, 1fr)` }}>
        {results.map((result, index) => (
          <Card key={index} variant="elevated" className="animate-slide-up" style={{ animationDelay: `${index * 100}ms` }}>
            <h3 className="text-lg font-bold text-gray-900 mb-4 truncate">
              {candidateNames[result.base_score.candidate_id] || 'Unknown'}
            </h3>

            {/* Strengths */}
            <div className="mb-4">
              <p className="text-sm font-semibold text-green-700 mb-2 flex items-center">
                <CheckCircle className="h-4 w-4 mr-1" />
                Сильные стороны ({result.detailed_strengths.length})
              </p>
              <div className="space-y-1">
                {result.detailed_strengths.slice(0, 3).map((strength, i) => (
                  <div key={i} className="flex items-start text-xs text-gray-700">
                    <ChevronRight className="h-3 w-3 text-green-600 mt-0.5 mr-1 flex-shrink-0" />
                    <span className="line-clamp-2">{strength}</span>
                  </div>
                ))}
                {result.detailed_strengths.length > 3 && (
                  <p className="text-xs text-gray-500 italic pl-4">
                    +{result.detailed_strengths.length - 3} еще
                  </p>
                )}
              </div>
            </div>

            {/* Concerns */}
            <div>
              <p className="text-sm font-semibold text-red-700 mb-2 flex items-center">
                <XCircle className="h-4 w-4 mr-1" />
                Опасения ({result.detailed_concerns.length})
              </p>
              <div className="space-y-1">
                {result.detailed_concerns.slice(0, 3).map((concern, i) => (
                  <div key={i} className="flex items-start text-xs text-gray-700">
                    <ChevronRight className="h-3 w-3 text-red-600 mt-0.5 mr-1 flex-shrink-0" />
                    <span className="line-clamp-2">{concern}</span>
                  </div>
                ))}
                {result.detailed_concerns.length > 3 && (
                  <p className="text-xs text-gray-500 italic pl-4">
                    +{result.detailed_concerns.length - 3} еще
                  </p>
                )}
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
