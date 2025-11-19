/**
 * Vacancies list page
 */
'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useVacancies, useDeleteVacancy } from '@/lib/hooks/useVacancies';
import { Briefcase, Building2, MapPin, DollarSign, Search, Loader2, Calendar, Plus, Pencil, Trash2 } from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Modal } from '@/components/ui/Modal';
import { EmptyState } from '@/components/ui/EmptyState';
import { SkeletonList } from '@/components/ui/Skeleton';
import { VacancyForm } from '@/components/VacancyForm';
import { useToast } from '@/components/ui/Toast';
import type { Vacancy } from '@/types';

export default function VacanciesPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [editingVacancy, setEditingVacancy] = useState<Vacancy | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const { data, isLoading, error } = useVacancies({ limit: 100 });
  const deleteMutation = useDeleteVacancy();
  const { showToast } = useToast();

  const filteredVacancies = data?.items?.filter(vacancy =>
    vacancy.position_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    vacancy.company_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleDelete = async (id: string, name: string) => {
    if (!confirm(`Вы уверены, что хотите удалить вакансию "${name}"?`)) {
      return;
    }

    setDeletingId(id);
    try {
      await deleteMutation.mutateAsync(id);
      showToast('success', 'Вакансия успешно удалена');
    } catch (error: any) {
      showToast('error', error.response?.data?.detail || 'Ошибка при удалении');
    } finally {
      setDeletingId(null);
    }
  };

  const handleEdit = (vacancy: Vacancy, e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setEditingVacancy(vacancy);
  };

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 text-lg">Ошибка загрузки вакансий</div>
        <p className="text-gray-600 mt-2">{error.message}</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center space-y-4 animate-fade-in">
        <div>
          <h1 className="text-4xl font-bold gradient-text">Вакансии</h1>
          <p className="text-xl text-gray-600 mt-2">
            {data?.total || 0} открытых вакансий
          </p>
        </div>
        <Button
          onClick={() => setIsCreateModalOpen(true)}
          className="inline-flex items-center space-x-2"
        >
          <Plus className="h-5 w-5" />
          <span>Добавить вакансию</span>
        </Button>
      </div>

      {/* Search */}
      <Card variant="glass" className="animate-slide-up">
        <div className="relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
          <input
            type="text"
            placeholder="Поиск по должности или компании..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-12 pr-4 py-3 bg-transparent border-2 border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-gray-900 placeholder-gray-500"
          />
        </div>
      </Card>

      {/* Loading state */}
      {isLoading && <SkeletonList count={6} />}

      {/* Vacancies list */}
      {!isLoading && filteredVacancies && filteredVacancies.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredVacancies.map((vacancy, index) => (
            <div key={vacancy.id} className="relative group">
              <Link href={`/vacancies/${vacancy.id}`}>
                <Card
                  variant="elevated"
                  hover
                  className="h-full animate-scale-in"
                  style={{ animationDelay: `${index * 50}ms` }}
                >
                  {/* Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className="h-14 w-14 rounded-xl bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center shadow-md">
                        <Briefcase className="h-7 w-7 text-white" />
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                          {vacancy.position_name}
                        </h3>
                        <Badge variant="success" size="sm">
                          {vacancy.grade || 'Any level'}
                        </Badge>
                      </div>
                    </div>
                  </div>

                  {/* Company */}
                  <div className="flex items-center text-gray-700 mb-4">
                    <Building2 className="h-4 w-4 mr-2 text-gray-400" />
                    <span className="font-medium">{vacancy.company_name}</span>
                  </div>

                  {/* Info */}
                  <div className="space-y-2.5">
                    {vacancy.locations && vacancy.locations.length > 0 && (
                      <div className="flex items-center text-sm text-gray-600">
                        <MapPin className="h-4 w-4 mr-2 text-gray-400" />
                        {vacancy.locations[0].city || 'Remote'}
                        {vacancy.locations[0].remote && ' (Remote)'}
                        {vacancy.locations.length > 1 && ` +${vacancy.locations.length - 1}`}
                      </div>
                    )}

                    {vacancy.salary_min && vacancy.salary_max && (
                      <div className="flex items-center text-sm text-gray-600">
                        <DollarSign className="h-4 w-4 mr-2 text-gray-400" />
                        {vacancy.salary_min.toLocaleString()}-{vacancy.salary_max.toLocaleString()} {vacancy.salary_currency}
                        {vacancy.salary_negotiable && ' (обсуждаемо)'}
                      </div>
                    )}

                    {(vacancy.min_experience_years || vacancy.max_experience_years) && (
                      <div className="flex items-center text-sm text-gray-600">
                        <Calendar className="h-4 w-4 mr-2 text-gray-400" />
                        {vacancy.min_experience_years && `от ${vacancy.min_experience_years}`}
                        {vacancy.min_experience_years && vacancy.max_experience_years && ' до '}
                        {vacancy.max_experience_years && `${vacancy.max_experience_years}`} лет опыта
                      </div>
                    )}
                  </div>

                  {/* Requirements */}
                  {vacancy.requirements && vacancy.requirements.length > 0 && (
                    <div className="mt-4">
                      <p className="text-xs font-medium text-gray-500 mb-2">Требования:</p>
                      <div className="flex flex-wrap gap-2">
                        {vacancy.requirements.slice(0, 4).map((req) => {
                          const variant =
                            req.importance === 'required'
                              ? 'danger'
                              : req.importance === 'nice_to_have'
                              ? 'info'
                              : 'neutral';
                          return (
                            <Badge key={req.id} variant={variant as any} size="sm">
                              {req.technology?.name || req.technology_id}
                            </Badge>
                          );
                        })}
                        {vacancy.requirements.length > 4 && (
                          <Badge variant="neutral" size="sm">
                            +{vacancy.requirements.length - 4}
                          </Badge>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Status badge */}
                  <div className="mt-4 pt-4 border-t border-gray-100">
                    <Badge
                      variant={vacancy.status === 'active' ? 'success' : 'neutral'}
                      size="sm"
                    >
                      {vacancy.status === 'active' ? 'Активна' : vacancy.status}
                    </Badge>
                  </div>
                </Card>
              </Link>

              {/* Action buttons */}
              <div className="absolute top-4 right-4 flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-opacity z-10">
                <button
                  onClick={(e) => handleEdit(vacancy, e)}
                  className="p-2 bg-white rounded-lg shadow-lg hover:bg-blue-50 hover:text-blue-600 transition-colors"
                  title="Редактировать"
                >
                  <Pencil className="h-4 w-4" />
                </button>
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    handleDelete(vacancy.id, vacancy.position_name);
                  }}
                  disabled={deletingId === vacancy.id}
                  className="p-2 bg-white rounded-lg shadow-lg hover:bg-red-50 hover:text-red-600 transition-colors disabled:opacity-50"
                  title="Удалить"
                >
                  {deletingId === vacancy.id ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Trash2 className="h-4 w-4" />
                  )}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Empty state */}
      {!isLoading && (!filteredVacancies || filteredVacancies.length === 0) && (
        <Card variant="elevated">
          <EmptyState
            icon={Briefcase}
            title="Вакансии не найдены"
            description={
              searchTerm
                ? 'Попробуйте изменить параметры поиска или сбросить фильтры'
                : 'Начните с добавления первой вакансии в систему'
            }
          />
        </Card>
      )}

      {/* Create Modal */}
      <Modal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        title="Добавить вакансию"
        size="lg"
      >
        <VacancyForm
          onSuccess={() => {
            setIsCreateModalOpen(false);
          }}
          onCancel={() => setIsCreateModalOpen(false)}
        />
      </Modal>

      {/* Edit Modal */}
      {editingVacancy && (
        <Modal
          isOpen={true}
          onClose={() => setEditingVacancy(null)}
          title="Редактировать вакансию"
          size="lg"
        >
          <VacancyForm
            vacancy={editingVacancy}
            onSuccess={() => {
              setEditingVacancy(null);
            }}
            onCancel={() => setEditingVacancy(null)}
          />
        </Modal>
      )}
    </div>
  );
}
