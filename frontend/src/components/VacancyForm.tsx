/**
 * Vacancy creation/editing form
 */
'use client';

import { useState } from 'react';
import { useCreateVacancy, useUpdateVacancy } from '@/lib/hooks/useVacancies';
import { useToast } from '@/components/ui/Toast';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Textarea } from '@/components/ui/Textarea';
import { Button } from '@/components/ui/Button';
import { TagInput } from '@/components/ui/TagInput';
import type { Vacancy } from '@/types';

interface VacancyFormProps {
  vacancy?: Vacancy;
  onSuccess?: () => void;
  onCancel?: () => void;
}

export function VacancyForm({ vacancy, onSuccess, onCancel }: VacancyFormProps) {
  const isEdit = !!vacancy;
  const { showToast } = useToast();
  const createMutation = useCreateVacancy();
  const updateMutation = useUpdateVacancy();

  const [formData, setFormData] = useState({
    company_name: vacancy?.company_name || '',
    position_name: vacancy?.position_name || '',
    grade: vacancy?.grade || '',
    min_experience_years: vacancy?.min_experience_years || '',
    max_experience_years: vacancy?.max_experience_years || '',
    description: vacancy?.description || '',
    responsibilities: vacancy?.responsibilities || [],
    timezone_requirements: vacancy?.timezone_requirements || [],
    citizenship_allowed: vacancy?.citizenship_allowed || [],
    salary_min: vacancy?.salary_min || '',
    salary_max: vacancy?.salary_max || '',
    salary_currency: vacancy?.salary_currency || 'USD',
    salary_period: vacancy?.salary_period || 'month',
    salary_type: vacancy?.salary_type || 'gross',
    salary_negotiable: vacancy?.salary_negotiable ?? true,
    status: vacancy?.status || 'active',
    // Simplified location - just one for MVP
    location_city: vacancy?.locations?.[0]?.city || '',
    location_country: vacancy?.locations?.[0]?.country || '',
    location_remote: vacancy?.locations?.[0]?.remote ?? true,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const validate = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.company_name.trim()) {
      newErrors.company_name = 'Название компании обязательно';
    }
    if (!formData.position_name.trim()) {
      newErrors.position_name = 'Название должности обязательно';
    }
    if (formData.min_experience_years && formData.max_experience_years) {
      if (Number(formData.min_experience_years) > Number(formData.max_experience_years)) {
        newErrors.max_experience_years = 'Максимум должен быть больше минимума';
      }
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
        company_name: formData.company_name,
        position_name: formData.position_name,
        grade: formData.grade || null,
        min_experience_years: formData.min_experience_years ? Number(formData.min_experience_years) : null,
        max_experience_years: formData.max_experience_years ? Number(formData.max_experience_years) : null,
        description: formData.description || null,
        responsibilities: formData.responsibilities,
        timezone_requirements: formData.timezone_requirements,
        citizenship_allowed: formData.citizenship_allowed,
        salary_min: formData.salary_min ? Number(formData.salary_min) : null,
        salary_max: formData.salary_max ? Number(formData.salary_max) : null,
        salary_currency: formData.salary_currency,
        salary_period: formData.salary_period,
        salary_type: formData.salary_type,
        salary_negotiable: formData.salary_negotiable,
        status: formData.status,
        locations: [
          {
            city: formData.location_city || null,
            country: formData.location_country || null,
            remote: formData.location_remote,
          },
        ],
        language_requirements: [],
        citizenship_restricted: [],
        external_links: {},
        interview_process: {},
      };

      if (isEdit && vacancy) {
        await updateMutation.mutateAsync({ id: vacancy.id, updates: payload });
        showToast('success', 'Вакансия успешно обновлена');
      } else {
        await createMutation.mutateAsync(payload);
        showToast('success', 'Вакансия успешно создана');
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
          label="Название компании"
          required
          value={formData.company_name}
          onChange={(e) => handleChange('company_name', e.target.value)}
          error={errors.company_name}
          placeholder="Acme Corp"
        />

        <Input
          label="Название должности"
          required
          value={formData.position_name}
          onChange={(e) => handleChange('position_name', e.target.value)}
          error={errors.position_name}
          placeholder="Senior Frontend Developer"
        />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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

          <Select
            label="Статус"
            value={formData.status}
            onChange={(e) => handleChange('status', e.target.value)}
            options={[
              { value: 'active', label: 'Активна' },
              { value: 'inactive', label: 'Неактивна' },
              { value: 'filled', label: 'Закрыта' },
            ]}
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Минимальный опыт (лет)"
            type="number"
            value={formData.min_experience_years}
            onChange={(e) => handleChange('min_experience_years', e.target.value)}
            min="0"
            placeholder="2"
          />

          <Input
            label="Максимальный опыт (лет)"
            type="number"
            value={formData.max_experience_years}
            onChange={(e) => handleChange('max_experience_years', e.target.value)}
            error={errors.max_experience_years}
            min="0"
            placeholder="5"
          />
        </div>
      </div>

      {/* Description */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-gray-900">Описание вакансии</h3>

        <Textarea
          label="Описание"
          value={formData.description}
          onChange={(e) => handleChange('description', e.target.value)}
          placeholder="Расскажите о вакансии..."
          rows={4}
        />

        <TagInput
          label="Обязанности"
          value={formData.responsibilities}
          onChange={(value) => handleChange('responsibilities', value)}
          placeholder="Добавьте обязанность и нажмите Enter"
          helperText="Нажмите Enter после каждой обязанности"
        />
      </div>

      {/* Location */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-gray-900">Локация</h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Город"
            value={formData.location_city}
            onChange={(e) => handleChange('location_city', e.target.value)}
            placeholder="Москва"
          />

          <Input
            label="Страна"
            value={formData.location_country}
            onChange={(e) => handleChange('location_country', e.target.value)}
            placeholder="Россия"
          />
        </div>

        <label className="flex items-center space-x-3">
          <input
            type="checkbox"
            checked={formData.location_remote}
            onChange={(e) => handleChange('location_remote', e.target.checked)}
            className="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          />
          <span className="text-sm text-gray-700">Возможна удаленная работа</span>
        </label>
      </div>

      {/* Requirements */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-gray-900">Требования</h3>

        <TagInput
          label="Часовые пояса"
          value={formData.timezone_requirements}
          onChange={(value) => handleChange('timezone_requirements', value)}
          placeholder="Например: UTC+3, UTC+0"
          helperText="Добавьте допустимые часовые пояса"
        />

        <TagInput
          label="Гражданство"
          value={formData.citizenship_allowed}
          onChange={(value) => handleChange('citizenship_allowed', value)}
          placeholder="Например: RU, BY, KZ"
          helperText="Добавьте коды стран (ISO 3166-1 alpha-2)"
        />
      </div>

      {/* Salary */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-gray-900">Зарплатная вилка</h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Минимум"
            type="number"
            value={formData.salary_min}
            onChange={(e) => handleChange('salary_min', e.target.value)}
            placeholder="150000"
          />

          <Input
            label="Максимум"
            type="number"
            value={formData.salary_max}
            onChange={(e) => handleChange('salary_max', e.target.value)}
            placeholder="250000"
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

        <label className="flex items-center space-x-3">
          <input
            type="checkbox"
            checked={formData.salary_negotiable}
            onChange={(e) => handleChange('salary_negotiable', e.target.checked)}
            className="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          />
          <span className="text-sm text-gray-700">Зарплата обсуждаема</span>
        </label>
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
          {isEdit ? 'Сохранить изменения' : 'Создать вакансию'}
        </Button>
      </div>
    </form>
  );
}
