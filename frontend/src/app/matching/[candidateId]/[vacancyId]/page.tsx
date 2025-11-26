/**
 * Detailed matching analysis page
 * Shows comprehensive matching results between a candidate and vacancy
 */
'use client';

import { use } from 'react';
import { ArrowLeft, Download, Share2 } from 'lucide-react';
import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { SkeletonList } from '@/components/ui/Skeleton';
import { ScoreGauge } from '@/components/matching/ScoreGauge';
import { CareerTrajectoryChart } from '@/components/matching/CareerTrajectoryChart';
import { MatchingBreakdown } from '@/components/matching/MatchingBreakdown';
import { useAdvancedScore } from '@/lib/hooks/useAdvancedMatching';
import { useCandidates } from '@/lib/hooks/useCandidates';
import { useVacancies } from '@/lib/hooks/useVacancies';

interface PageProps {
  params: Promise<{
    candidateId: string;
    vacancyId: string;
  }>;
}

export default function MatchingDetailPage({ params }: PageProps) {
  const resolvedParams = use(params);
  const { candidateId, vacancyId } = resolvedParams;

  const { data: result, isLoading: matchLoading } = useAdvancedScore(
    candidateId,
    vacancyId,
    false
  );

  const { data: candidatesData } = useCandidates({ page: 1, limit: 100 });
  const { data: vacanciesData } = useVacancies({ page: 1, limit: 100 });

  const candidate = candidatesData?.items.find((c) => c.id === candidateId);
  const vacancy = vacanciesData?.items.find((v) => v.id === vacancyId);

  if (matchLoading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div className="h-8 w-48 bg-gray-200 rounded animate-pulse" />
          <div className="flex space-x-2">
            <div className="h-10 w-32 bg-gray-200 rounded animate-pulse" />
            <div className="h-10 w-32 bg-gray-200 rounded animate-pulse" />
          </div>
        </div>
        <SkeletonList count={3} />
      </div>
    );
  }

  if (!result || !candidate || !vacancy) {
    return (
      <div className="flex items-center justify-center h-96">
        <Card variant="elevated" className="text-center p-8">
          <p className="text-lg text-gray-600">Не удалось загрузить данные о совпадении</p>
          <Link href="/candidates">
            <Button variant="primary" className="mt-4">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Вернуться к кандидатам
            </Button>
          </Link>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between animate-fade-in">
        <div className="flex-1">
          <Link href="/candidates" className="inline-flex items-center text-blue-600 hover:text-blue-700 mb-2">
            <ArrowLeft className="h-4 w-4 mr-1" />
            Назад к кандидатам
          </Link>
          <h1 className="text-3xl font-bold gradient-text">Детальный анализ совпадения</h1>
          <div className="mt-2 space-y-1">
            <p className="text-lg text-gray-700">
              <span className="font-semibold">Кандидат:</span> {candidate.full_name}
              {candidate.grade && (
                <span className="ml-2 text-sm text-gray-600">({candidate.grade})</span>
              )}
            </p>
            <p className="text-lg text-gray-700">
              <span className="font-semibold">Вакансия:</span> {vacancy.position_name}
              <span className="mx-2 text-gray-400">•</span>
              <span className="text-gray-600">{vacancy.company_name}</span>
            </p>
          </div>
        </div>

        <div className="flex space-x-2 ml-4">
          <Button variant="outline" size="md">
            <Share2 className="h-4 w-4 mr-2" />
            Поделиться
          </Button>
          <Button variant="outline" size="md">
            <Download className="h-4 w-4 mr-2" />
            Экспорт
          </Button>
        </div>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Breakdown */}
        <div className="lg:col-span-2 space-y-6">
          <MatchingBreakdown result={result} />
        </div>

        {/* Right Column - Career & Summary */}
        <div className="space-y-6">
          {/* Quick Summary */}
          <Card variant="elevated" className="animate-slide-up sticky top-4">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Краткая сводка</h3>

            <div className="flex justify-center mb-6">
              <ScoreGauge score={result.final_score} size="lg" label="Финальный скор" />
            </div>

            <div className="space-y-3">
              <div className="p-3 bg-gray-50 rounded-lg">
                <p className="text-xs text-gray-600 mb-1">Рекомендация</p>
                <p className="text-sm font-semibold text-gray-900">
                  {result.recommendation === 'highly_recommend' && 'Настоятельно рекомендуется'}
                  {result.recommendation === 'recommend' && 'Рекомендуется'}
                  {result.recommendation === 'consider' && 'Рассмотреть'}
                  {result.recommendation === 'not_recommend' && 'Не рекомендуется'}
                </p>
              </div>

              <div className="p-3 bg-gray-50 rounded-lg">
                <p className="text-xs text-gray-600 mb-1">Карьерный этап</p>
                <p className="text-sm font-semibold text-gray-900 uppercase">
                  {result.career_analysis.career_stage}
                </p>
              </div>

              <div className="p-3 bg-gray-50 rounded-lg">
                <p className="text-xs text-gray-600 mb-1">Траектория</p>
                <p className="text-sm font-semibold text-gray-900 capitalize">
                  {result.career_analysis.career_trend.direction === 'upward' && 'Восходящая'}
                  {result.career_analysis.career_trend.direction === 'stable' && 'Стабильная'}
                  {result.career_analysis.career_trend.direction === 'lateral' && 'Горизонтальная'}
                  {result.career_analysis.career_trend.direction === 'downward' && 'Нисходящая'}
                </p>
              </div>

              <div className="p-3 bg-gray-50 rounded-lg">
                <p className="text-xs text-gray-600 mb-1">Потенциал роста</p>
                <p className="text-sm font-semibold text-gray-900">
                  {Math.round(result.career_analysis.potential_score)}%
                </p>
              </div>

              <div className="p-3 bg-gray-50 rounded-lg">
                <p className="text-xs text-gray-600 mb-1">Уверенность в оценке</p>
                <p className="text-sm font-semibold text-gray-900">
                  {Math.round(result.base_score.confidence_level)}%
                </p>
              </div>
            </div>

            {result.base_score.missing_critical_requirements.length > 0 && (
              <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-xs font-semibold text-red-800 mb-2">
                  Критические недостатки:
                </p>
                <ul className="space-y-1">
                  {result.base_score.missing_critical_requirements.map((req, i) => (
                    <li key={i} className="text-xs text-red-700">• {req}</li>
                  ))}
                </ul>
              </div>
            )}
          </Card>
        </div>
      </div>

      {/* Career Trajectory - Full Width */}
      <CareerTrajectoryChart careerAnalysis={result.career_analysis} />

      {/* Match Explanation */}
      <Card variant="elevated" className="animate-slide-up" style={{ animationDelay: '600ms' }}>
        <h3 className="text-xl font-bold text-gray-900 mb-4">Объяснение решения</h3>
        <div className="prose max-w-none">
          <p className="text-gray-700 leading-relaxed">{result.match_explanation}</p>
        </div>
      </Card>

      {/* Red Flags & Strengths Summary */}
      {(result.career_analysis.red_flags.length > 0 || result.career_analysis.strengths.length > 0) && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {result.career_analysis.strengths.length > 0 && (
            <Card variant="elevated" className="animate-slide-up" style={{ animationDelay: '700ms' }}>
              <h3 className="text-lg font-bold text-gray-900 mb-3">Карьерные сильные стороны</h3>
              <ul className="space-y-2">
                {result.career_analysis.strengths.map((strength, i) => (
                  <li key={i} className="text-sm text-gray-700 flex items-start">
                    <span className="text-green-600 mr-2">✓</span>
                    {strength}
                  </li>
                ))}
              </ul>
            </Card>
          )}

          {result.career_analysis.red_flags.length > 0 && (
            <Card variant="elevated" className="animate-slide-up" style={{ animationDelay: '750ms' }}>
              <h3 className="text-lg font-bold text-gray-900 mb-3">Красные флаги</h3>
              <ul className="space-y-2">
                {result.career_analysis.red_flags.map((flag, i) => (
                  <li key={i} className="text-sm text-gray-700 flex items-start">
                    <span className="text-red-600 mr-2">⚠</span>
                    {flag}
                  </li>
                ))}
              </ul>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
