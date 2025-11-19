/**
 * Candidate comparison page for a vacancy
 * Shows all recommended candidates with their matching scores
 */
'use client';

import { use, useState } from 'react';
import { ArrowLeft, ArrowRight, Filter, SortDesc, Eye } from 'lucide-react';
import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { ScoreGauge } from '@/components/matching/ScoreGauge';
import { SkeletonList } from '@/components/ui/Skeleton';
import { useMatchingRecommendations } from '@/lib/hooks/useAdvancedMatching';
import { useVacancy } from '@/lib/hooks/useVacancies';

interface PageProps {
  params: Promise<{
    id: string;
  }>;
}

export default function VacancyCandidatesPage({ params }: PageProps) {
  const resolvedParams = use(params);
  const { id: vacancyId } = resolvedParams;

  const [minScore, setMinScore] = useState(60);
  const [limit, setLimit] = useState(20);

  const { data: vacancy, isLoading: vacancyLoading } = useVacancy(vacancyId);
  const { data: recommendations, isLoading: recsLoading } = useMatchingRecommendations(
    vacancyId,
    minScore,
    limit
  );

  if (vacancyLoading || recsLoading) {
    return (
      <div className="space-y-6">
        <div className="h-8 w-64 bg-gray-200 rounded animate-pulse" />
        <SkeletonList count={5} />
      </div>
    );
  }

  if (!vacancy) {
    return (
      <div className="flex items-center justify-center h-96">
        <Card variant="elevated" className="text-center p-8">
          <p className="text-lg text-gray-600">Вакансия не найдена</p>
        </Card>
      </div>
    );
  }

  const getRecommendationBadge = (recommendation: string) => {
    switch (recommendation) {
      case 'highly_recommend':
        return <Badge variant="success">Настоятельно рекомендуется</Badge>;
      case 'recommend':
        return <Badge variant="primary">Рекомендуется</Badge>;
      case 'consider':
        return <Badge variant="warning">Рассмотреть</Badge>;
      default:
        return <Badge variant="danger">Не рекомендуется</Badge>;
    }
  };

  const getMatchQualityBadge = (quality: string) => {
    switch (quality) {
      case 'excellent':
        return <Badge variant="success" size="sm">Отлично</Badge>;
      case 'good':
        return <Badge variant="primary" size="sm">Хорошо</Badge>;
      case 'fair':
        return <Badge variant="warning" size="sm">Удовлетворительно</Badge>;
      default:
        return <Badge variant="danger" size="sm">Плохо</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="animate-fade-in">
        <Link href={`/vacancies/${vacancyId}`} className="inline-flex items-center text-blue-600 hover:text-blue-700 mb-2">
          <ArrowLeft className="h-4 w-4 mr-1" />
          Назад к вакансии
        </Link>
        <h1 className="text-3xl font-bold gradient-text">Рекомендованные кандидаты</h1>
        <div className="mt-2">
          <p className="text-lg text-gray-700">
            <span className="font-semibold">{vacancy.position_name}</span>
            <span className="mx-2 text-gray-400">•</span>
            <span className="text-gray-600">{vacancy.company_name}</span>
          </p>
        </div>
      </div>

      {/* Filters & Controls */}
      <Card variant="elevated" className="animate-slide-up">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center space-x-4">
            <div>
              <label className="text-sm font-medium text-gray-700 mb-1 block">
                Минимальный скор
              </label>
              <select
                value={minScore}
                onChange={(e) => setMinScore(Number(e.target.value))}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value={50}>50+</option>
                <option value={60}>60+</option>
                <option value={70}>70+</option>
                <option value={80}>80+</option>
              </select>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-700 mb-1 block">
                Показать
              </label>
              <select
                value={limit}
                onChange={(e) => setLimit(Number(e.target.value))}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value={10}>10</option>
                <option value={20}>20</option>
                <option value={50}>50</option>
                <option value={100}>100</option>
              </select>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <Button variant="outline" size="sm">
              <Filter className="h-4 w-4 mr-2" />
              Фильтры
            </Button>
            <Button variant="outline" size="sm">
              <SortDesc className="h-4 w-4 mr-2" />
              Сортировка
            </Button>
          </div>
        </div>
      </Card>

      {/* Results Summary */}
      {recommendations && (
        <div className="flex items-center justify-between px-4">
          <p className="text-sm text-gray-600">
            Найдено <span className="font-semibold text-gray-900">{recommendations.total_found}</span> кандидатов
            с минимальным скором {recommendations.min_score_threshold}%
          </p>
        </div>
      )}

      {/* Candidates List */}
      {recommendations && recommendations.candidates.length > 0 ? (
        <div className="space-y-4">
          {recommendations.candidates.map((candidate, index) => (
            <Card
              key={candidate.candidate_id}
              variant="elevated"
              hover
              className="animate-slide-up"
              style={{ animationDelay: `${index * 50}ms` }}
            >
              <div className="flex items-start space-x-6">
                {/* Score Gauge */}
                <div className="flex-shrink-0">
                  <ScoreGauge score={candidate.score} size="md" showValue />
                </div>

                {/* Candidate Info */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <h3 className="text-xl font-bold text-gray-900 mb-1">
                        {candidate.candidate_name}
                      </h3>
                      <div className="flex items-center space-x-2">
                        {getRecommendationBadge(candidate.recommendation)}
                        {getMatchQualityBadge(candidate.match_quality)}
                      </div>
                    </div>
                    <Link href={`/matching/${candidate.candidate_id}/${vacancyId}`}>
                      <Button variant="primary" size="sm">
                        <Eye className="h-4 w-4 mr-2" />
                        Подробнее
                      </Button>
                    </Link>
                  </div>

                  {/* Highlights */}
                  {candidate.highlights.length > 0 && (
                    <div className="mb-3">
                      <p className="text-sm font-semibold text-gray-700 mb-2">
                        Сильные стороны:
                      </p>
                      <div className="space-y-1">
                        {candidate.highlights.map((highlight, i) => (
                          <div key={i} className="flex items-start text-sm text-gray-700">
                            <span className="text-green-600 mr-2">✓</span>
                            <span>{highlight}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Concerns */}
                  {candidate.concerns.length > 0 && (
                    <div>
                      <p className="text-sm font-semibold text-gray-700 mb-2">
                        Опасения:
                      </p>
                      <div className="space-y-1">
                        {candidate.concerns.map((concern, i) => (
                          <div key={i} className="flex items-start text-sm text-gray-700">
                            <span className="text-red-600 mr-2">⚠</span>
                            <span>{concern}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <Card variant="elevated" className="text-center p-12">
          <p className="text-lg text-gray-600 mb-2">
            Нет кандидатов, соответствующих критериям
          </p>
          <p className="text-sm text-gray-500">
            Попробуйте снизить минимальный скор или увеличить лимит результатов
          </p>
        </Card>
      )}

      {/* Compare Button */}
      {recommendations && recommendations.candidates.length > 1 && (
        <Card variant="gradient" className="animate-scale-in">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-white mb-1">
                Сравнить кандидатов
              </h3>
              <p className="text-white/90 text-sm">
                Выберите несколько кандидатов для детального сравнения
              </p>
            </div>
            <Button variant="secondary" size="lg">
              Выбрать для сравнения
              <ArrowRight className="h-4 w-4 ml-2" />
            </Button>
          </div>
        </Card>
      )}
    </div>
  );
}
