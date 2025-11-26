/**
 * Score breakdown visualization component
 */
'use client';

import { ProgressBar } from './ProgressBar';

interface ScoreComponent {
  label: string;
  score: number;
  weight?: number;
  description?: string;
}

interface ScoreBreakdownProps {
  components: ScoreComponent[];
  showWeights?: boolean;
  className?: string;
}

export function ScoreBreakdown({
  components,
  showWeights = false,
  className = ''
}: ScoreBreakdownProps) {
  const getVariant = (score: number) => {
    if (score >= 80) return 'success';
    if (score >= 65) return 'info';
    if (score >= 50) return 'warning';
    return 'danger';
  };

  return (
    <div className={`space-y-4 ${className}`}>
      {components.map((component, index) => (
        <div key={index} className="space-y-1.5">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <span className="text-sm font-medium text-gray-700">
                {component.label}
              </span>
              {showWeights && component.weight !== undefined && (
                <span className="text-xs text-gray-500">
                  (вес: {component.weight}%)
                </span>
              )}
            </div>
            <span className="text-sm font-bold text-gray-900">
              {Math.round(component.score)}%
            </span>
          </div>
          <ProgressBar
            value={component.score}
            max={100}
            variant={getVariant(component.score)}
            size="sm"
            showValue={false}
          />
          {component.description && (
            <p className="text-xs text-gray-600 italic">
              {component.description}
            </p>
          )}
        </div>
      ))}
    </div>
  );
}
