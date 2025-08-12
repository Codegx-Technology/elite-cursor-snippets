'use client';

import React, { useState } from 'react';
import { FaChevronDown } from 'react-icons/fa';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Enterprise-grade form select with Kenya-first design system
// [GOAL]: Create beautiful, accessible select inputs with cultural authenticity
// [TASK]: Implement enhanced select with proper styling and Kenya-first options

interface FormSelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: { value: string; label: string }[];
  error?: string;
  helperText?: string;
  variant?: 'default' | 'cultural' | 'elite';
  placeholder?: string;
}

export default function FormSelect({
  label,
  options,
  className = '',
  error,
  helperText,
  variant = 'default',
  placeholder = 'Select an option...',
  ...props
}: FormSelectProps) {
  const [isFocused, setIsFocused] = useState(false);

  const variantClasses = {
    default: 'form-select',
    cultural: 'form-select border-yellow-300 focus:border-yellow-500 focus:ring-yellow-200',
    elite: 'form-select border-purple-300 focus:border-purple-500 focus:ring-purple-200'
  };

  const labelClasses = `block text-sm font-medium mb-2 transition-colors duration-200 ${
    error ? 'text-red-600' :
    isFocused ? 'text-green-600' :
    'text-gray-700'
  }`;

  const selectClasses = `${variantClasses[variant]} w-full appearance-none ${
    error ? 'border-red-300 focus:border-red-500 focus:ring-red-200' : ''
  } ${props.disabled ? 'bg-gray-50 cursor-not-allowed' : ''} ${className}`;

  return (
    <div className="mb-6">
      {label && (
        <label htmlFor={props.id} className={labelClasses}>
          {label}
          {props.required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}

      <div className="relative">
        <select
          className={selectClasses}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          {...props}
        >
          {placeholder && (
            <option value="" disabled>
              {placeholder}
            </option>
          )}
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>

        <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
          <FaChevronDown className={`h-4 w-4 transition-colors duration-200 ${
            isFocused ? 'text-green-500' : 'text-gray-400'
          }`} />
        </div>
      </div>

      {error && (
        <p className="mt-2 text-sm text-red-600 flex items-center">
          <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          {error}
        </p>
      )}

      {helperText && !error && (
        <p className="mt-2 text-sm text-gray-500">
          {helperText}
        </p>
      )}
    </div>
  );
}
