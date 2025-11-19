/**
 * Home page - Dashboard
 */
'use client';

import Link from 'next/link';
import { Users, Briefcase, Target, TrendingUp, Search, Award } from 'lucide-react';

export default function HomePage() {
  const stats = [
    { label: 'Кандидатов', value: '3', icon: Users, color: 'text-blue-600' },
    { label: 'Вакансий', value: '3', icon: Briefcase, color: 'text-green-600' },
    { label: 'Технологий', value: '40+', icon: Target, color: 'text-purple-600' },
    { label: 'Матчей', value: '9', icon: TrendingUp, color: 'text-orange-600' },
  ];

  const features = [
    {
      icon: Target,
      title: 'Интеллектуальный скоринг',
      description: 'Многоуровневая оценка соответствия кандидатов вакансиям по 8 компонентам',
      color: 'bg-blue-50 text-blue-600',
    },
    {
      icon: Search,
      title: 'Расширенный поиск',
      description: 'Поиск по технологиям, опыту, локации и зарплатным ожиданиям',
      color: 'bg-green-50 text-green-600',
    },
    {
      icon: TrendingUp,
      title: 'Real-time матчинг',
      description: 'Мгновенный подбор кандидатов для вакансий и наоборот',
      color: 'bg-purple-50 text-purple-600',
    },
    {
      icon: Award,
      title: 'Аналитика и insights',
      description: 'Highlights, concerns и детальная разбивка скоров для каждого матча',
      color: 'bg-orange-50 text-orange-600',
    },
  ];

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold text-gray-900">
          HRM Platform
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Интеллектуальная система подбора IT-специалистов с автоматическим скорингом и семантическим анализом навыков
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.label} className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
                </div>
                <Icon className={`h-12 w-12 ${stat.color}`} />
              </div>
            </div>
          );
        })}
      </div>

      {/* Features */}
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-gray-900 text-center">
          Возможности платформы
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <div key={feature.title} className="bg-white rounded-lg shadow p-6">
                <div className="flex items-start space-x-4">
                  <div className={`p-3 rounded-lg ${feature.color}`}>
                    <Icon className="h-6 w-6" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600">
                      {feature.description}
                    </p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Quick Links */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg shadow-lg p-8 text-white">
        <h2 className="text-2xl font-bold mb-6 text-center">
          Начните работу
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link
            href="/candidates"
            className="bg-white/10 hover:bg-white/20 backdrop-blur rounded-lg p-6 transition-all hover:scale-105"
          >
            <Users className="h-8 w-8 mb-3" />
            <h3 className="text-lg font-semibold mb-2">Кандидаты</h3>
            <p className="text-sm text-white/80">
              Просмотр и управление кандидатами
            </p>
          </Link>

          <Link
            href="/vacancies"
            className="bg-white/10 hover:bg-white/20 backdrop-blur rounded-lg p-6 transition-all hover:scale-105"
          >
            <Briefcase className="h-8 w-8 mb-3" />
            <h3 className="text-lg font-semibold mb-2">Вакансии</h3>
            <p className="text-sm text-white/80">
              Управление вакансиями и требованиями
            </p>
          </Link>

          <Link
            href="/ontology"
            className="bg-white/10 hover:bg-white/20 backdrop-blur rounded-lg p-6 transition-all hover:scale-105"
          >
            <Target className="h-8 w-8 mb-3" />
            <h3 className="text-lg font-semibold mb-2">Онтология</h3>
            <p className="text-sm text-white/80">
              Справочники должностей и технологий
            </p>
          </Link>
        </div>
      </div>

      {/* Scoring Components */}
      <div className="bg-white rounded-lg shadow p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
          Компоненты скоринга
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { name: 'Technologies', weight: '40%', color: 'bg-blue-100 text-blue-700' },
            { name: 'Experience', weight: '20%', color: 'bg-green-100 text-green-700' },
            { name: 'Skills', weight: '15%', color: 'bg-purple-100 text-purple-700' },
            { name: 'Standards', weight: '10%', color: 'bg-orange-100 text-orange-700' },
            { name: 'Industry', weight: '5%', color: 'bg-pink-100 text-pink-700' },
            { name: 'Languages', weight: '5%', color: 'bg-indigo-100 text-indigo-700' },
            { name: 'Location', weight: '3%', color: 'bg-teal-100 text-teal-700' },
            { name: 'Salary', weight: '2%', color: 'bg-yellow-100 text-yellow-700' },
          ].map((component) => (
            <div
              key={component.name}
              className={`${component.color} rounded-lg p-4 text-center`}
            >
              <div className="text-2xl font-bold mb-1">{component.weight}</div>
              <div className="text-sm font-medium">{component.name}</div>
            </div>
          ))}
        </div>
      </div>

      {/* API Link */}
      <div className="text-center text-sm text-gray-500">
        API Documentation:{' '}
        <a
          href="http://localhost:8000/docs"
          className="text-blue-600 hover:underline"
          target="_blank"
          rel="noopener noreferrer"
        >
          http://localhost:8000/docs
        </a>
      </div>
    </div>
  );
}
