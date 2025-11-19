/**
 * Badge component for status and labels
 */
'use client';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'info' | 'neutral';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export function Badge({
  children,
  variant = 'default',
  size = 'md',
  className = ''
}: BadgeProps) {
  const variantClasses = {
    default: 'bg-blue-100 text-blue-800',
    success: 'bg-green-100 text-green-800',
    warning: 'bg-amber-100 text-amber-800',
    danger: 'bg-red-100 text-red-800',
    info: 'bg-cyan-100 text-cyan-800',
    neutral: 'bg-gray-100 text-gray-800',
  };

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-sm',
    lg: 'px-3 py-1.5 text-base',
  };

  return (
    <span
      className={`inline-flex items-center rounded-full font-medium ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
    >
      {children}
    </span>
  );
}

interface MatchQualityBadgeProps {
  quality: string;
  className?: string;
}

export function MatchQualityBadge({ quality, className = '' }: MatchQualityBadgeProps) {
  const qualityConfig = {
    excellent: { label: 'Отлично', variant: 'success' as const },
    good: { label: 'Хорошо', variant: 'info' as const },
    fair: { label: 'Приемлемо', variant: 'warning' as const },
    poor: { label: 'Слабо', variant: 'danger' as const },
  };

  const config = qualityConfig[quality as keyof typeof qualityConfig] || {
    label: quality,
    variant: 'neutral' as const,
  };

  return (
    <Badge variant={config.variant} className={className}>
      {config.label}
    </Badge>
  );
}
