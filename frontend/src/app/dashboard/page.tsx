/**
 * Dashboard page with analytics, charts, and statistics
 */
'use client';

import {
  Users,
  Briefcase,
  CheckCircle,
  TrendingUp,
  Award,
  BarChart3,
  PieChart,
  Activity
} from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { StatCard } from '@/components/ui/StatCard';
import { Badge } from '@/components/ui/Badge';
import { SkeletonList } from '@/components/ui/Skeleton';
import {
  useAnalyticsStats,
  useMatchesByScoreChart,
  useVacanciesByStatusChart,
  useCandidatesByGradeChart,
  useTopMatches,
} from '@/lib/hooks/useAnalytics';
import {
  BarChart,
  Bar,
  PieChart as RechartsPieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import Link from 'next/link';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];
const STATUS_COLORS: Record<string, string> = {
  active: '#10b981',
  inactive: '#6b7280',
  filled: '#3b82f6',
};

export default function DashboardPage() {
  const { data: stats, isLoading: statsLoading } = useAnalyticsStats();
  const { data: matchesByScore, isLoading: matchesLoading } = useMatchesByScoreChart();
  const { data: vacanciesByStatus, isLoading: vacanciesLoading } = useVacanciesByStatusChart();
  const { data: candidatesByGrade, isLoading: gradesLoading } = useCandidatesByGradeChart();
  const { data: topMatches, isLoading: topMatchesLoading } = useTopMatches(5);

  if (statsLoading) {
    return (
      <div className="space-y-8">
        <div className="text-center animate-fade-in">
          <h1 className="text-4xl font-bold gradient-text">Аналитика</h1>
          <p className="text-xl text-gray-600 mt-2">Обзор метрик и статистики</p>
        </div>
        <SkeletonList count={4} />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center animate-fade-in">
        <h1 className="text-4xl font-bold gradient-text">Аналитика</h1>
        <p className="text-xl text-gray-600 mt-2">Обзор метрик и статистики</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Всего кандидатов"
          value={stats?.total_candidates || 0}
          icon={Users}
          iconColor="text-blue-600"
          iconBgColor="from-blue-500 to-blue-600"
          trend={{
            value: stats?.trends.candidates || 0,
            label: 'за 30 дней'
          }}
        />
        <StatCard
          title="Всего вакансий"
          value={stats?.total_vacancies || 0}
          icon={Briefcase}
          iconColor="text-green-600"
          iconBgColor="from-green-500 to-emerald-500"
          trend={{
            value: stats?.trends.vacancies || 0,
            label: 'за 30 дней'
          }}
        />
        <StatCard
          title="Активные вакансии"
          value={stats?.active_vacancies || 0}
          icon={CheckCircle}
          iconColor="text-purple-600"
          iconBgColor="from-purple-500 to-purple-600"
        />
        <StatCard
          title="Средний скор"
          value={`${stats?.avg_match_score || 0}%`}
          icon={TrendingUp}
          iconColor="text-orange-600"
          iconBgColor="from-orange-500 to-orange-600"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Matches by Score Distribution */}
        <Card variant="elevated" className="animate-slide-up">
          <div className="flex items-center space-x-3 mb-6">
            <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center">
              <BarChart3 className="h-5 w-5 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900">Распределение совпадений</h2>
              <p className="text-sm text-gray-600">По диапазонам скоров</p>
            </div>
          </div>

          {matchesLoading ? (
            <div className="h-64 flex items-center justify-center">
              <Activity className="h-8 w-8 animate-spin text-blue-600" />
            </div>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={matchesByScore}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis
                  dataKey="range"
                  stroke="#6b7280"
                  style={{ fontSize: '12px' }}
                />
                <YAxis
                  stroke="#6b7280"
                  style={{ fontSize: '12px' }}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#ffffff',
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
                  }}
                />
                <Bar
                  dataKey="count"
                  fill="#3b82f6"
                  radius={[8, 8, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          )}
        </Card>

        {/* Vacancies by Status */}
        <Card variant="elevated" className="animate-slide-up" style={{ animationDelay: '100ms' }}>
          <div className="flex items-center space-x-3 mb-6">
            <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center">
              <PieChart className="h-5 w-5 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900">Вакансии по статусу</h2>
              <p className="text-sm text-gray-600">Распределение по статусам</p>
            </div>
          </div>

          {vacanciesLoading ? (
            <div className="h-64 flex items-center justify-center">
              <Activity className="h-8 w-8 animate-spin text-green-600" />
            </div>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <RechartsPieChart>
                <Pie
                  data={vacanciesByStatus}
                  dataKey="count"
                  nameKey="status"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label={({ status, count }) => `${status}: ${count}`}
                  labelLine={false}
                >
                  {vacanciesByStatus?.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={STATUS_COLORS[entry.status] || COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#ffffff',
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
                  }}
                />
              </RechartsPieChart>
            </ResponsiveContainer>
          )}
        </Card>
      </div>

      {/* Second Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Candidates by Grade */}
        <Card variant="elevated" className="animate-slide-up" style={{ animationDelay: '200ms' }}>
          <div className="flex items-center space-x-3 mb-6">
            <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-purple-500 to-purple-600 flex items-center justify-center">
              <Award className="h-5 w-5 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900">Кандидаты по уровню</h2>
              <p className="text-sm text-gray-600">Распределение по грейдам</p>
            </div>
          </div>

          {gradesLoading ? (
            <div className="h-64 flex items-center justify-center">
              <Activity className="h-8 w-8 animate-spin text-purple-600" />
            </div>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={candidatesByGrade}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis
                  dataKey="grade"
                  stroke="#6b7280"
                  style={{ fontSize: '12px' }}
                />
                <YAxis
                  stroke="#6b7280"
                  style={{ fontSize: '12px' }}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#ffffff',
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
                  }}
                />
                <Bar
                  dataKey="count"
                  fill="#8b5cf6"
                  radius={[8, 8, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          )}
        </Card>

        {/* Top Matches */}
        <Card variant="elevated" className="animate-slide-up" style={{ animationDelay: '300ms' }}>
          <div className="flex items-center space-x-3 mb-6">
            <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-orange-500 to-orange-600 flex items-center justify-center">
              <TrendingUp className="h-5 w-5 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900">Топ совпадений</h2>
              <p className="text-sm text-gray-600">Лучшие пары кандидат-вакансия</p>
            </div>
          </div>

          {topMatchesLoading ? (
            <div className="space-y-3">
              {[1, 2, 3, 4, 5].map((i) => (
                <div key={i} className="h-16 bg-gray-100 rounded-lg animate-pulse" />
              ))}
            </div>
          ) : topMatches && topMatches.length > 0 ? (
            <div className="space-y-3">
              {topMatches.map((match, index) => (
                <div
                  key={`${match.candidate_id}-${match.vacancy_id}`}
                  className="flex items-center justify-between p-4 bg-gradient-to-r from-gray-50 to-white rounded-lg border border-gray-100 hover:border-blue-200 transition-colors"
                >
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className="text-sm font-semibold text-gray-900">
                        #{index + 1}
                      </span>
                      <Link
                        href={`/candidates/${match.candidate_id}`}
                        className="text-sm font-medium text-blue-600 hover:text-blue-700 hover:underline"
                      >
                        {match.candidate?.full_name || 'Unknown'}
                      </Link>
                      <span className="text-sm text-gray-400">→</span>
                      <Link
                        href={`/vacancies/${match.vacancy_id}`}
                        className="text-sm font-medium text-green-600 hover:text-green-700 hover:underline"
                      >
                        {match.vacancy?.position_name || 'Unknown'}
                      </Link>
                    </div>
                    <p className="text-xs text-gray-600">
                      {match.vacancy?.company_name || 'Unknown company'}
                    </p>
                  </div>
                  <Badge
                    variant={match.score >= 90 ? 'success' : match.score >= 80 ? 'primary' : 'info'}
                    size="md"
                  >
                    {match.score}%
                  </Badge>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <p>Нет данных о совпадениях</p>
              <p className="text-sm mt-2">Создайте кандидатов и вакансии для анализа</p>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
