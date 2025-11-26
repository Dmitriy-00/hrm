/**
 * Match card component for displaying candidate-vacancy matches
 */
'use client';

import Link from 'next/link';
import { Card } from './Card';
import { ScoreCircle } from './ScoreCircle';
import { MatchQualityBadge } from './Badge';
import { ScoreBreakdown } from './ScoreBreakdown';
import { Building2, User, TrendingUp } from 'lucide-react';

interface MatchScore {
  total_score: number;
  match_quality: string;
  confidence_level: number;
  breakdown: {
    technologies: { score: number; weight: number };
    experience: { score: number; weight: number };
    skills: { score: number; weight: number };
    [key: string]: { score: number; weight: number };
  };
}

interface MatchCardProps {
  type: 'candidate' | 'vacancy';
  id: string;
  title: string;
  subtitle: string;
  score: MatchScore;
  highlights?: string[];
  concerns?: string[];
  showBreakdown?: boolean;
  className?: string;
}

export function MatchCard({
  type,
  id,
  title,
  subtitle,
  score,
  highlights = [],
  concerns = [],
  showBreakdown = false,
  className = ''
}: MatchCardProps) {
  const Icon = type === 'candidate' ? User : Building2;
  const href = type === 'candidate' ? `/candidates/${id}` : `/vacancies/${id}`;

  const breakdownComponents = Object.entries(score.breakdown).map(([key, value]) => ({
    label: getLabelForKey(key),
    score: value.score,
    weight: value.weight,
  }));

  return (
    <Card variant="elevated" hover className={className}>
      <div className="space-y-4">
        {/* Header */}
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-3 flex-1">
            <div className={`h-12 w-12 rounded-full ${
              type === 'candidate' ? 'bg-blue-100' : 'bg-green-100'
            } flex items-center justify-center`}>
              <Icon className={`h-6 w-6 ${
                type === 'candidate' ? 'text-blue-600' : 'text-green-600'
              }`} />
            </div>
            <div className="flex-1">
              <Link
                href={href}
                className="text-lg font-semibold text-gray-900 hover:text-blue-600 transition-colors"
              >
                {title}
              </Link>
              <p className="text-sm text-gray-600">{subtitle}</p>
            </div>
          </div>

          <div className="flex flex-col items-center space-y-2">
            <ScoreCircle score={score.total_score} size="md" showLabel={false} />
            <MatchQualityBadge quality={score.match_quality} />
          </div>
        </div>

        {/* Quick stats */}
        <div className="grid grid-cols-4 gap-3 pt-3 border-t border-gray-100">
          {Object.entries(score.breakdown).slice(0, 4).map(([key, value]) => (
            <div key={key} className="text-center">
              <div className="text-lg font-bold text-gray-900">
                {Math.round(value.score)}%
              </div>
              <div className="text-xs text-gray-600">
                {getShortLabel(key)}
              </div>
            </div>
          ))}
        </div>

        {/* Detailed breakdown */}
        {showBreakdown && (
          <div className="pt-3 border-t border-gray-100">
            <ScoreBreakdown components={breakdownComponents} showWeights />
          </div>
        )}

        {/* Highlights */}
        {highlights.length > 0 && (
          <div className="pt-3 border-t border-gray-100">
            <div className="flex items-center space-x-2 mb-2">
              <TrendingUp className="h-4 w-4 text-green-600" />
              <span className="text-sm font-semibold text-green-700">
                Сильные стороны
              </span>
            </div>
            <ul className="space-y-1">
              {highlights.slice(0, 3).map((highlight, index) => (
                <li key={index} className="text-sm text-gray-600 pl-4">
                  • {highlight}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Concerns */}
        {concerns.length > 0 && (
          <div className="pt-3 border-t border-gray-100">
            <div className="flex items-center space-x-2 mb-2">
              <span className="text-sm font-semibold text-amber-700">
                ⚠ Зоны внимания
              </span>
            </div>
            <ul className="space-y-1">
              {concerns.slice(0, 2).map((concern, index) => (
                <li key={index} className="text-sm text-gray-600 pl-4">
                  • {concern}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </Card>
  );
}

function getLabelForKey(key: string): string {
  const labels: Record<string, string> = {
    technologies: 'Технологии',
    experience: 'Опыт',
    skills: 'Навыки',
    languages: 'Языки',
    education: 'Образование',
    culture_fit: 'Культурное соответствие',
    salary: 'Зарплата',
    location: 'Локация',
  };
  return labels[key] || key;
}

function getShortLabel(key: string): string {
  const labels: Record<string, string> = {
    technologies: 'Tech',
    experience: 'Exp',
    skills: 'Skills',
    languages: 'Lang',
    education: 'Edu',
    culture_fit: 'Culture',
    salary: 'Salary',
    location: 'Location',
  };
  return labels[key] || key;
}
