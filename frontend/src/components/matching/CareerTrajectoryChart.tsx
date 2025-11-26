/**
 * Career trajectory visualization component
 */
'use client';

import React from 'react';
import { TrendingUp, TrendingDown, Minus, ArrowRight } from 'lucide-react';
import { Card } from '../ui/Card';
import { Badge } from '../ui/Badge';
import type { CareerAnalysis } from '@/lib/hooks/useAdvancedMatching';

interface CareerTrajectoryChartProps {
  careerAnalysis: CareerAnalysis;
}

export function CareerTrajectoryChart({ careerAnalysis }: CareerTrajectoryChartProps) {
  const { career_trend, role_progression, technical_growth } = careerAnalysis;

  const getDirectionIcon = () => {
    switch (career_trend.direction) {
      case 'upward':
        return <TrendingUp className="h-6 w-6 text-green-600" />;
      case 'downward':
        return <TrendingDown className="h-6 w-6 text-red-600" />;
      case 'lateral':
        return <ArrowRight className="h-6 w-6 text-blue-600" />;
      default:
        return <Minus className="h-6 w-6 text-gray-600" />;
    }
  };

  const getDirectionColor = () => {
    switch (career_trend.direction) {
      case 'upward':
        return 'text-green-700 bg-green-50 border-green-200';
      case 'downward':
        return 'text-red-700 bg-red-50 border-red-200';
      case 'lateral':
        return 'text-blue-700 bg-blue-50 border-blue-200';
      default:
        return 'text-gray-700 bg-gray-50 border-gray-200';
    }
  };

  const getDirectionLabel = () => {
    switch (career_trend.direction) {
      case 'upward':
        return 'Восходящая';
      case 'downward':
        return 'Нисходящая';
      case 'lateral':
        return 'Горизонтальная';
      default:
        return 'Стабильная';
    }
  };

  return (
    <Card variant="elevated" className="animate-slide-up">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-bold text-gray-900">Карьерная траектория</h3>
          <div className={`flex items-center space-x-2 px-3 py-1 rounded-lg border ${getDirectionColor()}`}>
            {getDirectionIcon()}
            <span className="font-semibold">{getDirectionLabel()}</span>
          </div>
        </div>

        {/* Role Progression Timeline */}
        <div>
          <h4 className="text-sm font-semibold text-gray-700 mb-3">Прогресс позиций</h4>
          <div className="flex items-center space-x-2 overflow-x-auto pb-2">
            {role_progression.role_levels.map((role, index) => (
              <React.Fragment key={index}>
                <Badge variant="secondary" size="lg">
                  {role}
                </Badge>
                {index < role_progression.role_levels.length - 1 && (
                  <ArrowRight className="h-4 w-4 text-gray-400 flex-shrink-0" />
                )}
              </React.Fragment>
            ))}
          </div>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-gradient-to-br from-green-50 to-emerald-50 p-4 rounded-lg border border-green-100">
            <p className="text-xs text-gray-600 mb-1">Темп роста</p>
            <p className="text-2xl font-bold text-green-700">{Math.round(career_trend.growth_rate)}%</p>
          </div>

          <div className="bg-gradient-to-br from-blue-50 to-blue-50 p-4 rounded-lg border border-blue-100">
            <p className="text-xs text-gray-600 mb-1">Стабильность</p>
            <p className="text-2xl font-bold text-blue-700">{Math.round(career_trend.consistency)}%</p>
          </div>

          <div className="bg-gradient-to-br from-purple-50 to-purple-50 p-4 rounded-lg border border-purple-100">
            <p className="text-xs text-gray-600 mb-1">Продвижения</p>
            <p className="text-2xl font-bold text-purple-700">{role_progression.promotions_count}</p>
          </div>

          <div className="bg-gradient-to-br from-orange-50 to-orange-50 p-4 rounded-lg border border-orange-100">
            <p className="text-xs text-gray-600 mb-1">Потенциал</p>
            <p className="text-2xl font-bold text-orange-700">{Math.round(careerAnalysis.potential_score)}%</p>
          </div>
        </div>

        {/* Technical Growth */}
        <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
          <h4 className="text-sm font-semibold text-gray-700 mb-3">Технический рост</h4>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Изучено технологий:</span>
              <Badge variant="primary">{technical_growth.technologies_learned}</Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Современность стека:</span>
              <Badge variant={technical_growth.tech_stack_modernity >= 70 ? 'success' : 'warning'}>
                {Math.round(technical_growth.tech_stack_modernity)}%
              </Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Тип специализации:</span>
              <Badge variant="secondary">
                {technical_growth.breadth_vs_depth === 'specialist' && 'Специалист'}
                {technical_growth.breadth_vs_depth === 'balanced' && 'Сбалансированный'}
                {technical_growth.breadth_vs_depth === 'generalist' && 'Универсал'}
              </Badge>
            </div>
            {technical_growth.tech_leadership && (
              <div className="flex items-center space-x-2 mt-2">
                <Badge variant="success" size="sm">Опыт тех. лидерства</Badge>
              </div>
            )}
          </div>
        </div>

        {/* Career Stage */}
        <div className="flex items-center justify-between p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
          <span className="font-medium text-gray-700">Карьерный этап:</span>
          <Badge variant="primary" size="lg">
            {careerAnalysis.career_stage.toUpperCase()}
          </Badge>
        </div>
      </div>
    </Card>
  );
}
