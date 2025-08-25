'use client';

import React, { useState } from 'react';
import { FaChevronDown } from 'react-icons/fa';
import { UseFormRegister, FieldValues } from 'react-hook-form'; // Import types from react-hook-form

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Enterprise-grade form select with Kenya-first design system
// [GOAL]: Create beautiful, accessible select inputs with cultural authenticity
// [TASK]: Implement enhanced select with proper styling and Kenya-first options

interface FormSelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: { value: string; label: string }[];
  error?: { message?: string }; // Updated error prop to match react-hook-form's FieldError
  helperText?: string;
  variant?: 'default' | 'cultural' | 'elite';
  placeholder?: string;
  labelClassName?: string;
  name: string; // Added name prop for react-hook-form registration
  register?: UseFormRegister<FieldValues>; // Optional register prop from react-hook-form
}

export default function FormSelect({
  label,
  options,
  className = '',
  error,
  helperText,
  variant = 'default',
  placeholder = 'Select an option...',
  labelClassName,
  name,
  register,
  onChange,
  onBlur,
  onFocus,
  id,
  ...props
}: FormSelectProps) {
  const [isFocused, setIsFocused] = useState(false);

  const variantClasses = {
    default: 'form-select',
    cultural: 'form-select border-yellow-300 focus:border-yellow-500 focus:ring-yellow-200',
    elite: 'form-select border-purple-300 focus:border-purple-500 focus:ring-purple-200'
  };

  const defaultLabelColor = error?.message ? 'text-red-600' : isFocused ? 'text-green-600' : 'text-gray-700';
  const labelClasses = `${labelClassName ? labelClassName : defaultLabelColor} block text-sm font-medium mb-2 transition-colors duration-200`;

  const selectClasses = `${variantClasses[variant]} w-full appearance-none ${
    error?.message ? 'border-red-300 focus:border-red-500 focus:ring-red-200' : ''
  } ${props.disabled ? 'bg-gray-50 cursor-not-allowed' : ''} ${className}`;

  // Prepare react-hook-form registration (if provided)
  const registration = register ? register(name, { shouldUnregister: true }) : undefined;

  // Compose handlers to avoid duplicate prop keys and ensure all callbacks fire
  const handleFocus: React.FocusEventHandler<HTMLSelectElement> = (e) => {
    setIsFocused(true);
    onFocus?.(e);
  };

  const handleBlur: React.FocusEventHandler<HTMLSelectElement> = (e) => {
    setIsFocused(false);
    registration?.onBlur?.(e);
    onBlur?.(e);
  };

  const handleChange: React.ChangeEventHandler<HTMLSelectElement> = (e) => {
    registration?.onChange?.(e);
    onChange?.(e);
  };

  return (
    <div className="mb-6">
      {label && (
        <label htmlFor={id || name} className={labelClasses}> {/* Use name as fallback for htmlFor */}
          {label}
          {props.required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}

      <div className="relative">
        <select
          id={id || name}
          name={name}
          ref={registration?.ref}
          className={selectClasses}
          onFocus={handleFocus}
          onBlur={handleBlur}
          onChange={handleChange}
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

      {error?.message && ( // Display error message from react-hook-form
        <p className="mt-2 text-sm text-red-600 flex items-center">
          <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          {error.message}
        </p>
      )}

      {helperText && !error?.message && ( // Only show helper text if no error
        <p className="mt-2 text-sm text-gray-500">
          {helperText}
        </p>
      )}
    </div>
  );
}

