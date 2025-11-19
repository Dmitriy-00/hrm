/**
 * Button component
 */
'use client';

import { ButtonHTMLAttributes, forwardRef } from 'react';
import { Loader2 } from 'lucide-react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  fullWidth?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      loading = false,
      fullWidth = false,
      className = '',
      children,
      disabled,
      ...props
    },
    ref
  ) => {
    const baseClasses = `
      inline-flex items-center justify-center font-medium rounded-lg
      transition-all duration-200
      focus:outline-none focus:ring-2 focus:ring-offset-2
      disabled:opacity-50 disabled:cursor-not-allowed
      ${fullWidth ? 'w-full' : ''}
    `;

    const variantClasses = {
      primary: `
        gradient-primary text-white
        hover:shadow-lg hover:scale-105
        focus:ring-blue-500
      `,
      secondary: `
        bg-gray-100 text-gray-900
        hover:bg-gray-200
        focus:ring-gray-500
      `,
      outline: `
        border-2 border-gray-300 text-gray-700 bg-white
        hover:border-blue-500 hover:text-blue-600
        focus:ring-blue-500
      `,
      ghost: `
        text-gray-700 bg-transparent
        hover:bg-gray-100
        focus:ring-gray-500
      `,
      danger: `
        bg-red-600 text-white
        hover:bg-red-700 hover:shadow-lg
        focus:ring-red-500
      `,
    };

    const sizeClasses = {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-4 py-2.5 text-base',
      lg: 'px-6 py-3 text-lg',
    };

    return (
      <button
        ref={ref}
        className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
        disabled={disabled || loading}
        {...props}
      >
        {loading && <Loader2 className="h-4 w-4 mr-2 animate-spin" />}
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';
