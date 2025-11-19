/**
 * Stats card component for displaying metrics
 */
'use client';

import { LucideIcon } from 'lucide-react';
import { Card } from './Card';

interface StatsCardProps {
  label: string;
  value: string | number;
  icon: LucideIcon;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  variant?: 'default' | 'primary' | 'success' | 'warning' | 'danger';
  className?: string;
}

export function StatsCard({
  label,
  value,
  icon: Icon,
  trend,
  variant = 'default',
  className = ''
}: StatsCardProps) {
  const variantStyles = {
    default: {
      iconBg: 'bg-gray-100',
      iconColor: 'text-gray-600',
    },
    primary: {
      iconBg: 'bg-blue-100',
      iconColor: 'text-blue-600',
    },
    success: {
      iconBg: 'bg-green-100',
      iconColor: 'text-green-600',
    },
    warning: {
      iconBg: 'bg-amber-100',
      iconColor: 'text-amber-600',
    },
    danger: {
      iconBg: 'bg-red-100',
      iconColor: 'text-red-600',
    },
  };

  const styles = variantStyles[variant];

  return (
    <Card variant="elevated" className={className}>
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600 mb-1">{label}</p>
          <p className="text-3xl font-bold text-gray-900">{value}</p>
          {trend && (
            <div className="mt-2 flex items-center space-x-1">
              <span
                className={`text-sm font-medium ${
                  trend.isPositive ? 'text-green-600' : 'text-red-600'
                }`}
              >
                {trend.isPositive ? '↑' : '↓'} {Math.abs(trend.value)}%
              </span>
              <span className="text-xs text-gray-500">vs последний месяц</span>
            </div>
          )}
        </div>
        <div className={`h-14 w-14 rounded-xl ${styles.iconBg} flex items-center justify-center`}>
          <Icon className={`h-7 w-7 ${styles.iconColor}`} />
        </div>
      </div>
    </Card>
  );
}
