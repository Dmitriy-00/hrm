/**
 * Circular score visualization component
 */
'use client';

import { useEffect, useState } from 'react';

interface ScoreCircleProps {
  score: number;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showLabel?: boolean;
  label?: string;
  className?: string;
}

export function ScoreCircle({
  score,
  size = 'md',
  showLabel = true,
  label,
  className = ''
}: ScoreCircleProps) {
  const [animatedScore, setAnimatedScore] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => setAnimatedScore(score), 100);
    return () => clearTimeout(timer);
  }, [score]);

  const sizeClasses = {
    sm: 'w-16 h-16',
    md: 'w-24 h-24',
    lg: 'w-32 h-32',
    xl: 'w-40 h-40',
  };

  const textSizes = {
    sm: 'text-lg',
    md: 'text-2xl',
    lg: 'text-3xl',
    xl: 'text-4xl',
  };

  const strokeWidths = {
    sm: 4,
    md: 6,
    lg: 8,
    xl: 10,
  };

  const getColor = (score: number) => {
    if (score >= 80) return { stroke: '#10b981', text: 'text-green-600' };
    if (score >= 65) return { stroke: '#3b82f6', text: 'text-blue-600' };
    if (score >= 50) return { stroke: '#f59e0b', text: 'text-amber-600' };
    return { stroke: '#ef4444', text: 'text-red-600' };
  };

  const color = getColor(score);
  const radius = 45;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (animatedScore / 100) * circumference;
  const strokeWidth = strokeWidths[size];

  return (
    <div className={`inline-flex flex-col items-center ${className}`}>
      <div className={`relative ${sizeClasses[size]}`}>
        <svg className="transform -rotate-90" width="100%" height="100%" viewBox="0 0 100 100">
          {/* Background circle */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            stroke="currentColor"
            strokeWidth={strokeWidth}
            fill="none"
            className="text-gray-200"
          />
          {/* Progress circle */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            stroke={color.stroke}
            strokeWidth={strokeWidth}
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className={`font-bold ${textSizes[size]} ${color.text}`}>
            {Math.round(animatedScore)}
          </span>
        </div>
      </div>
      {showLabel && label && (
        <span className="mt-2 text-sm font-medium text-gray-600">{label}</span>
      )}
    </div>
  );
}
