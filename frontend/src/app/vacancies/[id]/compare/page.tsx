/**
 * Candidate comparison page with side-by-side analysis
 */
'use client';

import { use, useState, useEffect } from 'react';
import { ArrowLeft, Download, Share2, Plus, X, Loader2 } from 'lucide-react';
import Link from 'next/link';
import { useSearchParams, useRouter } from 'next/navigation';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { CandidateComparison } from '@/components/matching/CandidateComparison';
import { useBatchScore } from '@/lib/hooks/useAdvancedMatching';
import { useVacancy } from '@/lib/hooks/useVacancies';
import { useCandidates } from '@/lib/hooks/useCandidates';

interface PageProps {
  params: Promise<{
    id: string;
  }>;
}

export default function ComparisonPage({ params }: PageProps) {
  const resolvedParams = use(params);
  const { id: vacancyId } = resolvedParams;
  const searchParams = useSearchParams();
  const router = useRouter();

  // Get candidate IDs from URL params
  const candidateIdsParam = searchParams?.get('candidates');
  const [selectedCandidates, setSelectedCandidates] = useState<string[]>([]);

  useEffect(() => {
    if (candidateIdsParam) {
      setSelectedCandidates(candidateIdsParam.split(','));
    }
  }, [candidateIdsParam]);

  const { data: vacancy, isLoading: vacancyLoading } = useVacancy(vacancyId);
  const { data: candidatesData } = useCandidates({ skip: 0, limit: 100 });

  const batchScoreMutation = useBatchScore();

  // Trigger batch scoring when candidates are selected
  useEffect(() => {
    if (selectedCandidates.length > 0 && vacancyId) {
      batchScoreMutation.mutate({
        vacancyId,
        candidateIds: selectedCandidates,
        useAdvancedScoring: true,
        includeMlFeatures: false,
      });
    }
  }, [selectedCandidates, vacancyId]);

  const handleRemoveCandidate = (candidateId: string) => {
    const updated = selectedCandidates.filter((id) => id !== candidateId);
    setSelectedCandidates(updated);

    // Update URL
    if (updated.length > 0) {
      router.push(`/vacancies/${vacancyId}/compare?candidates=${updated.join(',')}`);
    } else {
      router.push(`/vacancies/${vacancyId}/candidates`);
    }
  };

  const handleAddCandidate = () => {
    router.push(`/vacancies/${vacancyId}/candidates?select=true`);
  };

  const handleExport = () => {
    // Implement export to PDF/Excel
    alert('Экспорт в разработке');
  };

  const handleShare = () => {
    // Copy link to clipboard
    navigator.clipboard.writeText(window.location.href);
    alert('Ссылка скопирована в буфер обмена');
  };

  if (vacancyLoading) {
    return (
      <div className="flex justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  if (!vacancy) {
    return (
      <Card variant="elevated" className="text-center p-8">
        <p className="text-lg text-gray-600">Вакансия не найдена</p>
      </Card>
    );
  }

  // Build candidate names map
  const candidateNames: Record<string, string> = {};
  if (candidatesData) {
    candidatesData.items.forEach((c) => {
      candidateNames[c.id] = c.full_name;
    });
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="animate-fade-in">
        <Link
          href={`/vacancies/${vacancyId}/candidates`}
          className="inline-flex items-center text-blue-600 hover:text-blue-700 mb-2"
        >
          <ArrowLeft className="h-4 w-4 mr-1" />
          Назад к списку кандидатов
        </Link>
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold gradient-text">Сравнение кандидатов</h1>
            <p className="text-lg text-gray-700 mt-2">
              <span className="font-semibold">{vacancy.position_name}</span>
              <span className="mx-2 text-gray-400">•</span>
              <span className="text-gray-600">{vacancy.company_name}</span>
            </p>
          </div>

          <div className="flex space-x-2">
            <Button variant="outline" size="md" onClick={handleShare}>
              <Share2 className="h-4 w-4 mr-2" />
              Поделиться
            </Button>
            <Button variant="outline" size="md" onClick={handleExport}>
              <Download className="h-4 w-4 mr-2" />
              Экспорт
            </Button>
          </div>
        </div>
      </div>

      {/* Selected Candidates Pills */}
      {selectedCandidates.length > 0 && (
        <Card variant="elevated" className="animate-slide-up">
          <div className="flex items-center justify-between">
            <div className="flex flex-wrap gap-2">
              {selectedCandidates.map((candidateId) => (
                <div
                  key={candidateId}
                  className="flex items-center space-x-2 px-3 py-2 bg-blue-50 border border-blue-200 rounded-lg"
                >
                  <span className="text-sm font-medium text-blue-900">
                    {candidateNames[candidateId] || candidateId}
                  </span>
                  <button
                    onClick={() => handleRemoveCandidate(candidateId)}
                    className="text-blue-600 hover:text-blue-800"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
            <Button variant="outline" size="sm" onClick={handleAddCandidate}>
              <Plus className="h-4 w-4 mr-2" />
              Добавить кандидата
            </Button>
          </div>
        </Card>
      )}

      {/* Info Card */}
      {selectedCandidates.length === 0 && (
        <Card variant="elevated" className="text-center p-12">
          <h3 className="text-xl font-bold text-gray-900 mb-2">
            Не выбраны кандидаты для сравнения
          </h3>
          <p className="text-gray-600 mb-6">
            Выберите минимум 2 кандидатов для начала сравнения
          </p>
          <Link href={`/vacancies/${vacancyId}/candidates`}>
            <Button variant="primary" size="lg">
              Выбрать кандидатов
            </Button>
          </Link>
        </Card>
      )}

      {selectedCandidates.length === 1 && (
        <Card variant="elevated" className="text-center p-12 bg-yellow-50 border-yellow-200">
          <h3 className="text-xl font-bold text-yellow-900 mb-2">
            Выбран только один кандидат
          </h3>
          <p className="text-yellow-700 mb-6">
            Добавьте хотя бы еще одного кандидата для сравнения
          </p>
          <Button variant="outline" size="lg" onClick={handleAddCandidate}>
            <Plus className="h-4 w-4 mr-2" />
            Добавить кандидата
          </Button>
        </Card>
      )}

      {/* Loading State */}
      {batchScoreMutation.isPending && selectedCandidates.length > 1 && (
        <Card variant="elevated" className="text-center p-12">
          <Loader2 className="h-12 w-12 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-lg font-semibold text-gray-900 mb-2">
            Анализируем кандидатов...
          </p>
          <p className="text-gray-600">
            Это может занять несколько секунд
          </p>
        </Card>
      )}

      {/* Comparison Results */}
      {batchScoreMutation.data && selectedCandidates.length >= 2 && (
        <>
          <CandidateComparison
            results={batchScoreMutation.data.results}
            candidateNames={candidateNames}
            vacancyName={vacancy.position_name}
          />

          {/* Processing Time */}
          <Card variant="elevated" className="text-center">
            <p className="text-sm text-gray-600">
              Анализ выполнен за{' '}
              <span className="font-semibold text-gray-900">
                {batchScoreMutation.data.processing_time_seconds}с
              </span>
              {' '}для{' '}
              <span className="font-semibold text-gray-900">
                {batchScoreMutation.data.total_candidates}
              </span>
              {' '}кандидатов
            </p>
          </Card>
        </>
      )}

      {/* Error State */}
      {batchScoreMutation.isError && (
        <Card variant="elevated" className="text-center p-12 bg-red-50 border-red-200">
          <h3 className="text-xl font-bold text-red-900 mb-2">
            Ошибка при анализе
          </h3>
          <p className="text-red-700 mb-6">
            {batchScoreMutation.error?.message || 'Произошла неизвестная ошибка'}
          </p>
          <Button
            variant="danger"
            size="lg"
            onClick={() => {
              if (selectedCandidates.length > 0) {
                batchScoreMutation.mutate({
                  vacancyId,
                  candidateIds: selectedCandidates,
                  useAdvancedScoring: true,
                  includeMlFeatures: false,
                });
              }
            }}
          >
            Попробовать снова
          </Button>
        </Card>
      )}
    </div>
  );
}
