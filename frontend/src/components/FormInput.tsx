'use client';

import React, { useState } from 'react';
import { FaEye, FaEyeSlash } from 'react-icons/fa';
import { UseFormRegister, FieldValues } from 'react-hook-form';
import { colors, spacing, typography, borderRadius } from '@/config/designTokens';
import { cn } from '@/lib/utils';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Enterprise-grade form input with Kenya-first design system integration
// [GOAL]: Standardize FormInput to use design tokens and maintain cultural authenticity
// [TASK]: Refactor to use centralized design system tokens

interface FormInputProps<TFieldValues extends FieldValues = FieldValues> extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: { message?: string }; // Updated error prop to match react-hook-form's FieldError
  icon?: React.ReactNode;
  helperText?: string;
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  name?: string; // Optional: for react-hook-form registration
  register?: UseFormRegister<TFieldValues>; // Optional: react-hook-form register
}

export default function FormInput<TFieldValues extends FieldValues = FieldValues>({
  label,
  className = '',
  type = 'text',
  error,
  icon,
  helperText,
  variant = 'default',
  name,
  register,
  ...props
}: FormInputProps) {
  const [showPassword, setShowPassword] = useState(false);
  const [isFocused, setIsFocused] = useState(false);

  const isPassword = type === 'password';
  const inputType = isPassword && showPassword ? 'text' : type;

  const baseClasses = 'w-full px-4 py-3 text-base border rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-1 font-medium';
  
  const variantClasses = {
    default: 'border-gray-300 focus:border-blue-500 focus:ring-blue-500 bg-white',
    kenya: `border-gray-300 focus:border-[${colors.kenya.green}] focus:ring-green-500 bg-white`,
    cultural: `border-gray-300 focus:border-[${colors.cultural.gold}] focus:ring-yellow-500 bg-white`,
    elite: 'border-purple-300 focus:border-purple-500 focus:ring-purple-500 bg-white'
  };

  const labelClasses = cn(
    'block font-medium mb-2 transition-colors duration-200',
    `text-[${typography.fontSizes.sm}]`,
    `font-[${typography.fontWeights.medium}]`,
    error ? 'text-red-600' :
    isFocused && variant === 'kenya' ? `text-[${colors.kenya.green}]` :
    isFocused && variant === 'cultural' ? `text-[${colors.cultural.gold}]` :
    isFocused ? 'text-blue-600' :
    'text-gray-700'
  );

  const inputClasses = cn(
    baseClasses,
    variantClasses[variant],
    error ? 'border-red-300 focus:border-red-500 focus:ring-red-500' : '',
    props.disabled ? 'bg-gray-50 cursor-not-allowed opacity-60' : '',
    icon ? 'pl-10' : '',
    isPassword ? 'pr-10' : '',
    'placeholder:text-gray-400',
    className
  );

  return (
    <div className="mb-6">
      {label && (
        <label htmlFor={(props.id as string) || (name as string)} className={labelClasses}>
          {label}
          {props.required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}

      <div className="relative">
        {icon && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <div className={cn(
            'text-gray-400 transition-colors duration-200',
            isFocused && variant === 'kenya' ? `text-[${colors.kenya.green}]` :
            isFocused && variant === 'cultural' ? `text-[${colors.cultural.gold}]` :
            isFocused ? 'text-blue-500' : ''
          )}>
              {icon}
            </div>
          </div>
        )}

        <input
          type={inputType}
          className={inputClasses}
          {...(register && name ? register(name, { shouldUnregister: true }) : {})}
          {...props}
          onFocus={(e) => {
            setIsFocused(true);
            props.onFocus?.(e);
          }}
          onBlur={(e) => {
            setIsFocused(false);
            props.onBlur?.(e);
          }}
        />

        {isPassword && (
          <button
            type="button"
            className="absolute inset-y-0 right-0 pr-3 flex items-center"
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? (
              <FaEyeSlash className="h-4 w-4 text-gray-400 hover:text-gray-600" />
            ) : (
              <FaEye className="h-4 w-4 text-gray-400 hover:text-gray-600" />
            )}
          </button>
        )}
      </div>

      {error?.message && (
        <p className={cn('mt-2 text-red-600 flex items-center', `text-[${typography.fontSizes.sm}]`)}>
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