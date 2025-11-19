/**
 * Circular gauge component for displaying scores
 */
'use client';

import React from 'react';

interface ScoreGaugeProps {
  score: number;
  size?: 'sm' | 'md' | 'lg';
  label?: string;
  showValue?: boolean;
}

export function ScoreGauge({ score, size = 'md', label, showValue = true }: ScoreGaugeProps) {
  const sizeClasses = {
    sm: 'w-20 h-20',
    md: 'w-32 h-32',
    lg: 'w-48 h-48',
  };

  const textSizes = {
    sm: 'text-xl',
    md: 'text-3xl',
    lg: 'text-5xl',
  };

  const labelSizes = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base',
  };

  // Determine color based on score
  const getColor = () => {
    if (score >= 85) return '#10b981'; // green
    if (score >= 70) return '#3b82f6'; // blue
    if (score >= 55) return '#f59e0b'; // orange
    return '#ef4444'; // red
  };

  const color = getColor();
  const radius = size === 'sm' ? 35 : size === 'md' ? 55 : 85;
  const strokeWidth = size === 'sm' ? 6 : size === 'md' ? 8 : 12;
  const normalizedRadius = radius - strokeWidth / 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="flex flex-col items-center">
      <div className={`relative ${sizeClasses[size]}`}>
        <svg className="transform -rotate-90" width="100%" height="100%">
          {/* Background circle */}
          <circle
            stroke="#e5e7eb"
            fill="transparent"
            strokeWidth={strokeWidth}
            r={normalizedRadius}
            cx="50%"
            cy="50%"
          />
          {/* Progress circle */}
          <circle
            stroke={color}
            fill="transparent"
            strokeWidth={strokeWidth}
            strokeDasharray={circumference + ' ' + circumference}
            style={{
              strokeDashoffset,
              transition: 'stroke-dashoffset 1s ease-in-out',
            }}
            strokeLinecap="round"
            r={normalizedRadius}
            cx="50%"
            cy="50%"
          />
        </svg>
        {showValue && (
          <div className="absolute inset-0 flex items-center justify-center">
            <span className={`font-bold ${textSizes[size]}`} style={{ color }}>
              {Math.round(score)}
            </span>
          </div>
        )}
      </div>
      {label && (
        <p className={`mt-2 font-medium text-gray-700 text-center ${labelSizes[size]}`}>
          {label}
        </p>
      )}
    </div>
  );
}
