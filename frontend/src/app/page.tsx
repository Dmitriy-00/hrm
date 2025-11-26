/**
 * Home page - Dashboard with modern design
 */
'use client';

import Link from 'next/link';
import { Users, Briefcase, Target, TrendingUp, Search, Award, Sparkles, ArrowRight, Zap } from 'lucide-react';
import { StatsCard } from '@/components/ui/StatsCard';
import { Card } from '@/components/ui/Card';
import { RadarChart } from '@/components/ui/RadarChart';
import { ProgressBar } from '@/components/ui/ProgressBar';

export default function HomePage() {
  const stats = [
    { label: 'Активных кандидатов', value: '3', icon: Users, variant: 'primary' as const },
    { label: 'Открытых вакансий', value: '3', icon: Briefcase, variant: 'success' as const },
    { label: 'В справочниках', value: '40+', icon: Target, variant: 'warning' as const },
    { label: 'Совпадений найдено', value: '9', icon: TrendingUp, variant: 'danger' as const },
  ];

  const features = [
    {
      icon: Target,
      title: 'Интеллектуальный скоринг',
      description: 'Многоуровневая оценка соответствия кандидатов вакансиям по 8 компонентам с весами',
      gradient: 'from-blue-500 to-cyan-500',
    },
    {
      icon: Search,
      title: 'Расширенный поиск',
      description: 'Поиск по технологиям, опыту, локации и зарплатным ожиданиям с фильтрацией',
      gradient: 'from-green-500 to-emerald-500',
    },
    {
      icon: TrendingUp,
      title: 'Real-time матчинг',
      description: 'Мгновенный подбор кандидатов для вакансий и наоборот с live-обновлениями',
      gradient: 'from-purple-500 to-pink-500',
    },
    {
      icon: Award,
      title: 'Аналитика и insights',
      description: 'Highlights, concerns и детальная разбивка скоров для каждого матча',
      gradient: 'from-orange-500 to-amber-500',
    },
  ];

  const scoringComponents = [
    { label: 'Tech', value: 40 },
    { label: 'Exp', value: 20 },
    { label: 'Skills', value: 15 },
    { label: 'Standards', value: 10 },
    { label: 'Industry', value: 5 },
    { label: 'Languages', value: 5 },
    { label: 'Location', value: 3 },
    { label: 'Salary', value: 2 },
  ];

  return (
    <div className="space-y-16">
      {/* Hero Section with Gradient */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 gradient-primary opacity-5 blur-3xl" />
        <div className="relative text-center space-y-6 py-12 animate-fade-in">
          <div className="inline-flex items-center space-x-2 px-4 py-2 glass rounded-full mb-4">
            <Sparkles className="h-4 w-4 text-blue-600" />
            <span className="text-sm font-medium text-gray-700">
              Powered by AI Scoring Engine
            </span>
          </div>
          <h1 className="text-5xl md:text-6xl font-bold gradient-text">
            HRM Platform
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Интеллектуальная система подбора IT-специалистов с автоматическим скорингом
            и семантическим анализом навыков
          </p>
          <div className="flex items-center justify-center space-x-4 pt-4">
            <Link
              href="/candidates"
              className="inline-flex items-center space-x-2 px-6 py-3 gradient-primary text-white rounded-lg font-medium hover:shadow-glow transition-all duration-300 hover:scale-105"
            >
              <Users className="h-5 w-5" />
              <span>Кандидаты</span>
              <ArrowRight className="h-4 w-4" />
            </Link>
            <Link
              href="/vacancies"
              className="inline-flex items-center space-x-2 px-6 py-3 glass border border-gray-200 rounded-lg font-medium hover:border-blue-300 transition-all duration-300"
            >
              <Briefcase className="h-5 w-5" />
              <span>Вакансии</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 animate-slide-up">
        {stats.map((stat) => (
          <StatsCard
            key={stat.label}
            label={stat.label}
            value={stat.value}
            icon={stat.icon}
            variant={stat.variant}
          />
        ))}
      </div>

      {/* Features Grid */}
      <div className="space-y-8">
        <div className="text-center space-y-2">
          <h2 className="text-3xl font-bold text-gray-900">
            Возможности платформы
          </h2>
          <p className="text-gray-600">
            Современные инструменты для эффективного подбора персонала
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <Card
                key={feature.title}
                variant="bordered"
                hover
                className={`animate-scale-in`}
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="flex items-start space-x-4">
                  <div className={`p-4 rounded-xl bg-gradient-to-br ${feature.gradient} text-white shadow-lg`}>
                    <Icon className="h-7 w-7" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600 leading-relaxed">
                      {feature.description}
                    </p>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      </div>

      {/* Scoring Visualization */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Radar Chart */}
        <Card variant="glass">
          <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">
            Компоненты скоринга
          </h3>
          <RadarChart data={scoringComponents} size={350} />
        </Card>

        {/* Score Breakdown */}
        <Card variant="bordered">
          <div className="flex items-center space-x-2 mb-6">
            <Zap className="h-6 w-6 text-blue-600" />
            <h3 className="text-2xl font-bold text-gray-900">
              Веса компонентов
            </h3>
          </div>
          <div className="space-y-4">
            {[
              { name: 'Technologies', weight: 40, color: 'info' },
              { name: 'Experience', weight: 20, color: 'success' },
              { name: 'Skills', weight: 15, color: 'default' },
              { name: 'Standards', weight: 10, color: 'warning' },
              { name: 'Industry', weight: 5, color: 'danger' },
              { name: 'Languages', weight: 5, color: 'info' },
              { name: 'Location', weight: 3, color: 'success' },
              { name: 'Salary', weight: 2, color: 'warning' },
            ].map((component) => (
              <div key={component.name}>
                <ProgressBar
                  value={component.weight}
                  max={40}
                  label={component.name}
                  variant={component.color as any}
                  size="md"
                />
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card variant="gradient" padding="lg">
        <div className="text-center space-y-6">
          <h2 className="text-3xl font-bold">
            Начните работу прямо сейчас
          </h2>
          <p className="text-white/90 text-lg max-w-2xl mx-auto">
            Выберите раздел для начала работы с платформой
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
            <Link
              href="/candidates"
              className="card-glass-dark group"
            >
              <Users className="h-10 w-10 mb-4 transition-transform group-hover:scale-110" />
              <h3 className="text-xl font-semibold mb-2">Кандидаты</h3>
              <p className="text-white/80 text-sm">
                Просмотр и управление базой кандидатов
              </p>
            </Link>

            <Link
              href="/vacancies"
              className="card-glass-dark group"
            >
              <Briefcase className="h-10 w-10 mb-4 transition-transform group-hover:scale-110" />
              <h3 className="text-xl font-semibold mb-2">Вакансии</h3>
              <p className="text-white/80 text-sm">
                Управление вакансиями и требованиями
              </p>
            </Link>

            <Link
              href="/ontology"
              className="card-glass-dark group"
            >
              <Target className="h-10 w-10 mb-4 transition-transform group-hover:scale-110" />
              <h3 className="text-xl font-semibold mb-2">Онтология</h3>
              <p className="text-white/80 text-sm">
                Справочники должностей и технологий
              </p>
            </Link>
          </div>
        </div>
      </Card>

      {/* Footer Link */}
      <div className="text-center text-sm text-gray-500 pb-8">
        <div className="inline-flex items-center space-x-2 px-4 py-2 bg-gray-50 rounded-lg">
          <span>API Documentation:</span>
          <a
            href="http://localhost:8000/docs"
            className="text-blue-600 hover:text-blue-700 font-medium transition-colors"
            target="_blank"
            rel="noopener noreferrer"
          >
            http://localhost:8000/docs
          </a>
        </div>
      </div>
    </div>
  );
}
