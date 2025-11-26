/**
 * Tag input component for managing arrays of strings
 */
'use client';

import { useState, KeyboardEvent } from 'react';
import { X } from 'lucide-react';

interface TagInputProps {
  label?: string;
  value: string[];
  onChange: (value: string[]) => void;
  placeholder?: string;
  error?: string;
  helperText?: string;
}

export function TagInput({
  label,
  value,
  onChange,
  placeholder = 'Введите и нажмите Enter',
  error,
  helperText,
}: TagInputProps) {
  const [inputValue, setInputValue] = useState('');

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && inputValue.trim()) {
      e.preventDefault();
      if (!value.includes(inputValue.trim())) {
        onChange([...value, inputValue.trim()]);
      }
      setInputValue('');
    } else if (e.key === 'Backspace' && !inputValue && value.length > 0) {
      onChange(value.slice(0, -1));
    }
  };

  const removeTag = (indexToRemove: number) => {
    onChange(value.filter((_, index) => index !== indexToRemove));
  };

  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-1.5">
          {label}
        </label>
      )}
      <div
        className={`
          w-full min-h-[42px] px-3 py-2 rounded-lg border-2
          ${error ? 'border-red-300' : 'border-gray-200'}
          focus-within:outline-none focus-within:ring-2
          ${error ? 'focus-within:ring-red-200 focus-within:border-red-500' : 'focus-within:ring-blue-200 focus-within:border-blue-500'}
          transition-all duration-200
          flex flex-wrap gap-2 items-center
        `}
      >
        {value.map((tag, index) => (
          <span
            key={index}
            className="inline-flex items-center space-x-1 px-2.5 py-1 bg-blue-100 text-blue-800 rounded-md text-sm font-medium"
          >
            <span>{tag}</span>
            <button
              type="button"
              onClick={() => removeTag(index)}
              className="hover:bg-blue-200 rounded transition-colors p-0.5"
            >
              <X className="h-3 w-3" />
            </button>
          </span>
        ))}
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={value.length === 0 ? placeholder : ''}
          className="flex-1 min-w-[120px] outline-none bg-transparent"
        />
      </div>
      {error && (
        <p className="mt-1.5 text-sm text-red-600">{error}</p>
      )}
      {helperText && !error && (
        <p className="mt-1.5 text-sm text-gray-500">{helperText}</p>
      )}
    </div>
  );
}
