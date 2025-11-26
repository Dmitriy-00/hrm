/**
 * Candidate creation/editing form
 */
'use client';

import { useState } from 'react';
import { useCreateCandidate, useUpdateCandidate } from '@/lib/hooks/useCandidates';
import { useToast } from '@/components/ui/Toast';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Textarea } from '@/components/ui/Textarea';
import { Button } from '@/components/ui/Button';
import type { Candidate } from '@/types';

interface CandidateFormProps {
  candidate?: Candidate;
  onSuccess?: () => void;
  onCancel?: () => void;
}

export function CandidateForm({ candidate, onSuccess, onCancel }: CandidateFormProps) {
  const isEdit = !!candidate;
  const { showToast } = useToast();
  const createMutation = useCreateCandidate();
  const updateMutation = useUpdateCandidate();

  const [formData, setFormData] = useState({
    full_name: candidate?.full_name || '',
    email: candidate?.email || '',
    phone: candidate?.phone || '',
    current_location: candidate?.current_location || '',
    grade: candidate?.grade || '',
    experience_months: candidate?.experience_months || 0,
    bio: candidate?.bio || '',
    skills: candidate?.skills?.join(', ') || '',
    salary_min: candidate?.salary_min || '',
    salary_max: candidate?.salary_max || '',
    salary_currency: candidate?.salary_currency || 'USD',
    salary_period: candidate?.salary_period || 'month',
    salary_type: candidate?.salary_type || 'gross',
    remote_work: candidate?.remote_work ?? true,
    relocation: candidate?.relocation ?? false,
    status: candidate?.status || 'active',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const validate = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.full_name.trim()) {
      newErrors.full_name = 'Имя обязательно';
    }
    if (!formData.email.trim()) {
      newErrors.email = 'Email обязателен';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Некорректный email';
    }
    if (formData.experience_months < 0) {
      newErrors.experience_months = 'Опыт не может быть отрицательным';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) {
      showToast('error', 'Пожалуйста, исправьте ошибки в форме');
      return;
    }

    try {
      const payload = {
        ...formData,
        experience_months: Number(formData.experience_months),
        salary_min: formData.salary_min ? Number(formData.salary_min) : null,
        salary_max: formData.salary_max ? Number(formData.salary_max) : null,
        skills: formData.skills
          ? formData.skills.split(',').map((s) => s.trim()).filter(Boolean)
          : [],
      };

      if (isEdit && candidate) {
        await updateMutation.mutateAsync({ id: candidate.id, updates: payload });
        showToast('success', 'Кандидат успешно обновлен');
      } else {
        await createMutation.mutateAsync(payload);
        showToast('success', 'Кандидат успешно создан');
      }

      onSuccess?.();
    } catch (error: any) {
      showToast('error', error.response?.data?.detail || 'Произошла ошибка');
    }
  };

  const handleChange = (field: string, value: any) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: '' }));
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Basic Info */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-gray-900">Основная информация</h3>

        <Input
          label="Полное имя"
          required
          value={formData.full_name}
          onChange={(e) => handleChange('full_name', e.target.value)}
          error={errors.full_name}
          placeholder="Иван Иванов"
        />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Email"
            type="email"
            required
            value={formData.email}
            onChange={(e) => handleChange('email', e.target.value)}
            error={errors.email}
            placeholder="ivan@example.com"
          />

          <Input
            label="Телефон"
            type="tel"
            value={formData.phone || ''}
            onChange={(e) => handleChange('phone', e.target.value)}
            placeholder="+7 (999) 123-45-67"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Локация"
            value={formData.current_location}
            onChange={(e) => handleChange('current_location', e.target.value)}
            placeholder="Москва, Россия"
          />

          <Select
            label="Грейд"
            value={formData.grade}
            onChange={(e) => handleChange('grade', e.target.value)}
            options={[
              { value: '', label: 'Выберите грейд' },
              { value: 'Intern', label: 'Intern' },
              { value: 'Junior', label: 'Junior' },
              { value: 'Middle', label: 'Middle' },
              { value: 'Senior', label: 'Senior' },
              { value: 'Lead', label: 'Lead' },
              { value: 'Principal', label: 'Principal' },
            ]}
          />
        </div>

        <Input
          label="Опыт работы (месяцев)"
          type="number"
          value={formData.experience_months}
          onChange={(e) => handleChange('experience_months', e.target.value)}
          error={errors.experience_months}
          min="0"
        />
      </div>

      {/* Bio & Skills */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-gray-900">О кандидате</h3>

        <Textarea
          label="Биография"
          value={formData.bio}
          onChange={(e) => handleChange('bio', e.target.value)}
          placeholder="Расскажите о кандидате..."
          rows={4}
        />

        <Input
          label="Навыки"
          value={formData.skills}
          onChange={(e) => handleChange('skills', e.target.value)}
          placeholder="JavaScript, React, Node.js (через запятую)"
          helperText="Перечислите навыки через запятую"
        />
      </div>

      {/* Salary */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-gray-900">Зарплатные ожидания</h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Минимум"
            type="number"
            value={formData.salary_min}
            onChange={(e) => handleChange('salary_min', e.target.value)}
            placeholder="100000"
          />

          <Input
            label="Максимум"
            type="number"
            value={formData.salary_max}
            onChange={(e) => handleChange('salary_max', e.target.value)}
            placeholder="150000"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Select
            label="Валюта"
            value={formData.salary_currency}
            onChange={(e) => handleChange('salary_currency', e.target.value)}
            options={[
              { value: 'USD', label: 'USD' },
              { value: 'EUR', label: 'EUR' },
              { value: 'RUB', label: 'RUB' },
            ]}
          />

          <Select
            label="Период"
            value={formData.salary_period}
            onChange={(e) => handleChange('salary_period', e.target.value)}
            options={[
              { value: 'hour', label: 'Час' },
              { value: 'month', label: 'Месяц' },
              { value: 'year', label: 'Год' },
            ]}
          />

          <Select
            label="Тип"
            value={formData.salary_type}
            onChange={(e) => handleChange('salary_type', e.target.value)}
            options={[
              { value: 'gross', label: 'Gross (до налогов)' },
              { value: 'net', label: 'Net (на руки)' },
            ]}
          />
        </div>
      </div>

      {/* Preferences */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-gray-900">Предпочтения</h3>

        <div className="space-y-3">
          <label className="flex items-center space-x-3">
            <input
              type="checkbox"
              checked={formData.remote_work}
              onChange={(e) => handleChange('remote_work', e.target.checked)}
              className="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span className="text-sm text-gray-700">Рассматривает удаленную работу</span>
          </label>

          <label className="flex items-center space-x-3">
            <input
              type="checkbox"
              checked={formData.relocation}
              onChange={(e) => handleChange('relocation', e.target.checked)}
              className="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span className="text-sm text-gray-700">Готов к релокации</span>
          </label>
        </div>

        <Select
          label="Статус"
          value={formData.status}
          onChange={(e) => handleChange('status', e.target.value)}
          options={[
            { value: 'active', label: 'Активен' },
            { value: 'inactive', label: 'Неактивен' },
            { value: 'hired', label: 'Нанят' },
          ]}
        />
      </div>

      {/* Actions */}
      <div className="flex items-center justify-end space-x-3 pt-6 border-t">
        {onCancel && (
          <Button
            type="button"
            variant="ghost"
            onClick={onCancel}
          >
            Отмена
          </Button>
        )}
        <Button
          type="submit"
          loading={createMutation.isPending || updateMutation.isPending}
        >
          {isEdit ? 'Сохранить изменения' : 'Создать кандидата'}
        </Button>
      </div>
    </form>
  );
}
