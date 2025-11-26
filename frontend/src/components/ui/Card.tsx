/**
 * Card component with multiple variants
 */
'use client';

import { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  variant?: 'elevated' | 'bordered' | 'glass' | 'gradient';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  hover?: boolean;
  className?: string;
  onClick?: () => void;
}

export function Card({
  children,
  variant = 'elevated',
  padding = 'md',
  hover = false,
  className = '',
  onClick
}: CardProps) {
  const variantClasses = {
    elevated: 'bg-white shadow-md',
    bordered: 'bg-white border-2 border-gray-200',
    glass: 'glass shadow-lg',
    gradient: 'gradient-primary text-white shadow-glow',
  };

  const paddingClasses = {
    none: 'p-0',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  };

  const hoverClass = hover
    ? 'transition-all duration-300 hover:shadow-xl hover:scale-[1.02] cursor-pointer'
    : '';

  return (
    <div
      className={`rounded-xl ${variantClasses[variant]} ${paddingClasses[padding]} ${hoverClass} ${className}`}
      onClick={onClick}
    >
      {children}
    </div>
  );
}
