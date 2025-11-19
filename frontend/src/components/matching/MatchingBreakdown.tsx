/**
 * Detailed matching breakdown component
 */
'use client';

import React from 'react';
import {
  Code,
  Briefcase,
  Languages,
  MapPin,
  DollarSign,
  Users,
  FileText,
  CheckCircle,
  XCircle,
} from 'lucide-react';
import { Card } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { ScoreGauge } from './ScoreGauge';
import type { AdvancedMatchingResult } from '@/lib/hooks/useAdvancedMatching';

interface MatchingBreakdownProps {
  result: AdvancedMatchingResult;
}

export function MatchingBreakdown({ result }: MatchingBreakdownProps) {
  const { base_score, semantic_match, cultural_fit, final_score, recommendation } = result;

  const getRecommendationColor = () => {
    switch (recommendation) {
      case 'highly_recommend':
        return 'success';
      case 'recommend':
        return 'primary';
      case 'consider':
        return 'warning';
      default:
        return 'danger';
    }
  };

  const getRecommendationLabel = () => {
    switch (recommendation) {
      case 'highly_recommend':
        return 'Настоятельно рекомендуется';
      case 'recommend':
        return 'Рекомендуется';
      case 'consider':
        return 'Рассмотреть';
      default:
        return 'Не рекомендуется';
    }
  };

  const breakdownItems = [
    {
      icon: Code,
      label: 'Технологии',
      score: base_score.breakdown.technologies.score,
      color: 'from-blue-500 to-blue-600',
      details: `${base_score.breakdown.technologies.matched}/${base_score.breakdown.technologies.required} совпадений`,
    },
    {
      icon: Briefcase,
      label: 'Опыт',
      score: base_score.breakdown.experience.score,
      color: 'from-green-500 to-emerald-500',
      details: `${base_score.breakdown.experience.candidate_years} лет опыта`,
    },
    {
      icon: Languages,
      label: 'Языки',
      score: base_score.breakdown.languages.score,
      color: 'from-purple-500 to-purple-600',
      details: `${base_score.breakdown.languages.matched.length} языков`,
    },
    {
      icon: MapPin,
      label: 'Локация',
      score: base_score.breakdown.location.score,
      color: 'from-orange-500 to-orange-600',
      details: base_score.breakdown.location.compatible ? 'Совместима' : 'Не совместима',
    },
    {
      icon: DollarSign,
      label: 'Зарплата',
      score: base_score.breakdown.salary.score,
      color: 'from-emerald-500 to-green-600',
      details: base_score.breakdown.salary.overlap ? 'Совпадает' : 'Не совпадает',
    },
    {
      icon: Users,
      label: 'Культурный фит',
      score: cultural_fit.overall_fit,
      color: 'from-pink-500 to-rose-500',
      details: `${Math.round(cultural_fit.overall_fit)}% совпадение`,
    },
  ];

  return (
    <div className="space-y-6">
      {/* Overall Score */}
      <Card variant="gradient" className="animate-fade-in">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <h3 className="text-2xl font-bold text-white mb-2">Финальный скор</h3>
            <p className="text-white/90 text-lg">
              {result.match_explanation}
            </p>
            <Badge
              variant={getRecommendationColor() as any}
              size="lg"
              className="mt-4"
            >
              {getRecommendationLabel()}
            </Badge>
          </div>
          <div className="ml-6">
            <ScoreGauge score={final_score} size="lg" />
          </div>
        </div>
      </Card>

      {/* Breakdown Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {breakdownItems.map((item, index) => {
          const Icon = item.icon;
          return (
            <Card
              key={index}
              variant="elevated"
              hover
              className="animate-slide-up"
              style={{ animationDelay: `${index * 50}ms` }}
            >
              <div className="flex items-start space-x-4">
                <div className={`h-12 w-12 rounded-xl bg-gradient-to-br ${item.color} flex items-center justify-center flex-shrink-0`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
                <div className="flex-1 min-w-0">
                  <h4 className="text-sm font-semibold text-gray-700 mb-1">{item.label}</h4>
                  <div className="flex items-center space-x-2 mb-2">
                    <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div
                        className={`h-full bg-gradient-to-r ${item.color} transition-all duration-500`}
                        style={{ width: `${item.score}%` }}
                      />
                    </div>
                    <span className="text-sm font-bold text-gray-900 min-w-[3rem] text-right">
                      {Math.round(item.score)}%
                    </span>
                  </div>
                  <p className="text-xs text-gray-600">{item.details}</p>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Semantic Match */}
      <Card variant="elevated" className="animate-slide-up" style={{ animationDelay: '300ms' }}>
        <div className="flex items-center space-x-3 mb-4">
          <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-indigo-500 to-indigo-600 flex items-center justify-center">
            <FileText className="h-5 w-5 text-white" />
          </div>
          <h3 className="text-lg font-bold text-gray-900">Семантический анализ</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-xs text-gray-600 mb-1">Сходство текстов</p>
            <p className="text-2xl font-bold text-gray-900">
              {Math.round(semantic_match.bio_description_similarity)}%
            </p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-xs text-gray-600 mb-1">Совпадение навыков</p>
            <p className="text-2xl font-bold text-gray-900">
              {Math.round(semantic_match.skill_extraction_match)}%
            </p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-xs text-gray-600 mb-1">Перекрытие ключевых слов</p>
            <p className="text-2xl font-bold text-gray-900">
              {Math.round(semantic_match.keyword_overlap)}%
            </p>
          </div>
        </div>

        {semantic_match.missing_keywords.length > 0 && (
          <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
            <p className="text-sm font-semibold text-yellow-800 mb-2">
              Отсутствующие ключевые слова:
            </p>
            <div className="flex flex-wrap gap-2">
              {semantic_match.missing_keywords.slice(0, 10).map((keyword, i) => (
                <Badge key={i} variant="warning" size="sm">
                  {keyword}
                </Badge>
              ))}
            </div>
          </div>
        )}

        {semantic_match.key_phrases_match.length > 0 && (
          <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-sm font-semibold text-green-800 mb-2">
              Совпадающие ключевые фразы:
            </p>
            <div className="flex flex-wrap gap-2">
              {semantic_match.key_phrases_match.map((phrase, i) => (
                <Badge key={i} variant="success" size="sm">
                  {phrase}
                </Badge>
              ))}
            </div>
          </div>
        )}
      </Card>

      {/* Strengths & Concerns */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Strengths */}
        <Card variant="elevated" className="animate-slide-up" style={{ animationDelay: '400ms' }}>
          <div className="flex items-center space-x-2 mb-4">
            <CheckCircle className="h-5 w-5 text-green-600" />
            <h3 className="text-lg font-bold text-gray-900">Сильные стороны</h3>
          </div>
          <div className="space-y-2">
            {result.detailed_strengths.length > 0 ? (
              result.detailed_strengths.map((strength, i) => (
                <div key={i} className="flex items-start space-x-2 p-2 bg-green-50 rounded-lg">
                  <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                  <p className="text-sm text-gray-700">{strength}</p>
                </div>
              ))
            ) : (
              <p className="text-sm text-gray-500 italic">Нет выявленных сильных сторон</p>
            )}
          </div>
        </Card>

        {/* Concerns */}
        <Card variant="elevated" className="animate-slide-up" style={{ animationDelay: '450ms' }}>
          <div className="flex items-center space-x-2 mb-4">
            <XCircle className="h-5 w-5 text-red-600" />
            <h3 className="text-lg font-bold text-gray-900">Опасения</h3>
          </div>
          <div className="space-y-2">
            {result.detailed_concerns.length > 0 ? (
              result.detailed_concerns.map((concern, i) => (
                <div key={i} className="flex items-start space-x-2 p-2 bg-red-50 rounded-lg">
                  <XCircle className="h-4 w-4 text-red-600 mt-0.5 flex-shrink-0" />
                  <p className="text-sm text-gray-700">{concern}</p>
                </div>
              ))
            ) : (
              <p className="text-sm text-gray-500 italic">Нет выявленных опасений</p>
            )}
          </div>
        </Card>
      </div>

      {/* Cultural Fit Details */}
      <Card variant="elevated" className="animate-slide-up" style={{ animationDelay: '500ms' }}>
        <div className="flex items-center space-x-3 mb-4">
          <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-pink-500 to-rose-500 flex items-center justify-center">
            <Users className="h-5 w-5 text-white" />
          </div>
          <h3 className="text-lg font-bold text-gray-900">Культурное соответствие</h3>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div className="text-center">
            <p className="text-xs text-gray-600 mb-2">Размер компании</p>
            <div className="text-2xl font-bold text-gray-900">
              {Math.round(cultural_fit.company_size_fit)}%
            </div>
          </div>
          <div className="text-center">
            <p className="text-xs text-gray-600 mb-2">Стиль работы</p>
            <div className="text-2xl font-bold text-gray-900">
              {Math.round(cultural_fit.work_style_fit)}%
            </div>
          </div>
          <div className="text-center">
            <p className="text-xs text-gray-600 mb-2">Команда</p>
            <div className="text-2xl font-bold text-gray-900">
              {Math.round(cultural_fit.team_environment_fit)}%
            </div>
          </div>
          <div className="text-center">
            <p className="text-xs text-gray-600 mb-2">Ценности</p>
            <div className="text-2xl font-bold text-gray-900">
              {Math.round(cultural_fit.values_alignment)}%
            </div>
          </div>
        </div>

        <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <p className="text-sm text-gray-700">{cultural_fit.fit_explanation}</p>
        </div>
      </Card>
    </div>
  );
}
