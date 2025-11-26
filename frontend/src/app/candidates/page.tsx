/**
 * Candidates list page
 */
'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useCandidates, useDeleteCandidate } from '@/lib/hooks/useCandidates';
import { Users, Mail, MapPin, Briefcase, DollarSign, Search, Loader2, Plus, Pencil, Trash2 } from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Modal } from '@/components/ui/Modal';
import { EmptyState } from '@/components/ui/EmptyState';
import { SkeletonList } from '@/components/ui/Skeleton';
import { CandidateForm } from '@/components/CandidateForm';
import { useToast } from '@/components/ui/Toast';
import type { Candidate } from '@/types';

export default function CandidatesPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [editingCandidate, setEditingCandidate] = useState<Candidate | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const { data, isLoading, error } = useCandidates({ limit: 100 });
  const deleteMutation = useDeleteCandidate();
  const { showToast } = useToast();

  const filteredCandidates = data?.items?.filter(candidate =>
    candidate.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    candidate.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleDelete = async (id: string, name: string) => {
    if (!confirm(`Вы уверены, что хотите удалить кандидата "${name}"?`)) {
      return;
    }

    setDeletingId(id);
    try {
      await deleteMutation.mutateAsync(id);
      showToast('success', 'Кандидат успешно удален');
    } catch (error: any) {
      showToast('error', error.response?.data?.detail || 'Ошибка при удалении');
    } finally {
      setDeletingId(null);
    }
  };

  const handleEdit = (candidate: Candidate, e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setEditingCandidate(candidate);
  };

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 text-lg">Ошибка загрузки кандидатов</div>
        <p className="text-gray-600 mt-2">{error.message}</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center space-y-4 animate-fade-in">
        <div>
          <h1 className="text-4xl font-bold gradient-text">Кандидаты</h1>
          <p className="text-xl text-gray-600 mt-2">
            {data?.total || 0} кандидатов в базе
          </p>
        </div>
        <Button
          onClick={() => setIsCreateModalOpen(true)}
          className="inline-flex items-center space-x-2"
        >
          <Plus className="h-5 w-5" />
          <span>Добавить кандидата</span>
        </Button>
      </div>

      {/* Search */}
      <Card variant="glass" className="animate-slide-up">
        <div className="relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
          <input
            type="text"
            placeholder="Поиск по имени или email..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-12 pr-4 py-3 bg-transparent border-2 border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-gray-900 placeholder-gray-500"
          />
        </div>
      </Card>

      {/* Loading state */}
      {isLoading && <SkeletonList count={6} />}

      {/* Candidates list */}
      {!isLoading && filteredCandidates && filteredCandidates.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredCandidates.map((candidate, index) => (
            <div key={candidate.id} className="relative group">
              <Link href={`/candidates/${candidate.id}`}>
                <Card
                  variant="elevated"
                  hover
                  className="h-full animate-scale-in"
                  style={{ animationDelay: `${index * 50}ms` }}
                >
                  {/* Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className="h-14 w-14 rounded-xl bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center shadow-md">
                        <Users className="h-7 w-7 text-white" />
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                          {candidate.full_name}
                        </h3>
                        <Badge variant="info" size="sm">
                          {candidate.grade || 'N/A'}
                        </Badge>
                      </div>
                    </div>
                  </div>

                  {/* Info */}
                  <div className="space-y-2.5">
                    <div className="flex items-center text-sm text-gray-600">
                      <Mail className="h-4 w-4 mr-2 text-gray-400" />
                      <span className="truncate">{candidate.email}</span>
                    </div>

                    {candidate.current_location && (
                      <div className="flex items-center text-sm text-gray-600">
                        <MapPin className="h-4 w-4 mr-2 text-gray-400" />
                        {candidate.current_location}
                      </div>
                    )}

                    <div className="flex items-center text-sm text-gray-600">
                      <Briefcase className="h-4 w-4 mr-2 text-gray-400" />
                      {Math.floor(candidate.experience_months / 12)} лет опыта
                    </div>

                    {candidate.salary_min && candidate.salary_max && (
                      <div className="flex items-center text-sm text-gray-600">
                        <DollarSign className="h-4 w-4 mr-2 text-gray-400" />
                        {candidate.salary_min.toLocaleString()}-{candidate.salary_max.toLocaleString()} {candidate.salary_currency}
                      </div>
                    )}
                  </div>

                  {/* Skills */}
                  {candidate.skills && candidate.skills.length > 0 && (
                    <div className="mt-4 flex flex-wrap gap-2">
                      {candidate.skills.slice(0, 3).map((skill, index) => (
                        <Badge key={index} variant="default" size="sm">
                          {skill}
                        </Badge>
                      ))}
                      {candidate.skills.length > 3 && (
                        <Badge variant="neutral" size="sm">
                          +{candidate.skills.length - 3}
                        </Badge>
                      )}
                    </div>
                  )}

                  {/* Status badge */}
                  <div className="mt-4 pt-4 border-t border-gray-100">
                    <Badge
                      variant={candidate.status === 'active' ? 'success' : 'neutral'}
                      size="sm"
                    >
                      {candidate.status === 'active' ? 'Активен' : candidate.status}
                    </Badge>
                  </div>
                </Card>
              </Link>

              {/* Action buttons */}
              <div className="absolute top-4 right-4 flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-opacity z-10">
                <button
                  onClick={(e) => handleEdit(candidate, e)}
                  className="p-2 bg-white rounded-lg shadow-lg hover:bg-blue-50 hover:text-blue-600 transition-colors"
                  title="Редактировать"
                >
                  <Pencil className="h-4 w-4" />
                </button>
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    handleDelete(candidate.id, candidate.full_name);
                  }}
                  disabled={deletingId === candidate.id}
                  className="p-2 bg-white rounded-lg shadow-lg hover:bg-red-50 hover:text-red-600 transition-colors disabled:opacity-50"
                  title="Удалить"
                >
                  {deletingId === candidate.id ? (
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
      {!isLoading && (!filteredCandidates || filteredCandidates.length === 0) && (
        <Card variant="elevated">
          <EmptyState
            icon={Users}
            title="Кандидаты не найдены"
            description={
              searchTerm
                ? 'Попробуйте изменить параметры поиска или сбросить фильтры'
                : 'Начните с добавления первого кандидата в систему'
            }
          />
        </Card>
      )}

      {/* Create Modal */}
      <Modal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        title="Добавить кандидата"
        size="lg"
      >
        <CandidateForm
          onSuccess={() => {
            setIsCreateModalOpen(false);
          }}
          onCancel={() => setIsCreateModalOpen(false)}
        />
      </Modal>

      {/* Edit Modal */}
      {editingCandidate && (
        <Modal
          isOpen={true}
          onClose={() => setEditingCandidate(null)}
          title="Редактировать кандидата"
          size="lg"
        >
          <CandidateForm
            candidate={editingCandidate}
            onSuccess={() => {
              setEditingCandidate(null);
            }}
            onCancel={() => setEditingCandidate(null)}
          />
        </Modal>
      )}
    </div>
  );
}
