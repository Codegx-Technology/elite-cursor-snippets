'use client';

import React, { useState } from 'react';
import { FaEye, FaEyeSlash } from 'react-icons/fa';
import { UseFormRegister, FieldValues } from 'react-hook-form'; // Import types from react-hook-form

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Enterprise-grade form input with Kenya-first design system
// [GOAL]: Create beautiful, accessible form inputs with cultural authenticity
// [TASK]: Implement enhanced input with validation, icons, and proper styling

interface FormInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: { message?: string }; // Updated error prop to match react-hook-form's FieldError
  icon?: React.ReactNode;
  helperText?: string;
  variant?: 'default' | 'cultural' | 'elite';
  name: string; // Added name prop for react-hook-form registration
  register: UseFormRegister<FieldValues>; // Added register prop from react-hook-form
}

export default function FormInput({
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

  const variantClasses = {
    default: 'form-input',
    cultural: 'form-input border-yellow-300 focus:border-yellow-500 focus:ring-yellow-200',
    elite: 'form-input border-purple-300 focus:border-purple-500 focus:ring-purple-200'
  };

  const labelClasses = `block text-sm font-medium mb-2 transition-colors duration-200 ${
    error ? 'text-red-600' :
    isFocused ? 'text-green-600' :
    'text-gray-700'
  }`;

  const inputClasses = `${variantClasses[variant]} w-full ${
    error ? 'border-red-300 focus:border-red-500 focus:ring-red-200' : ''
  } ${props.disabled ? 'bg-gray-50 cursor-not-allowed' : ''} ${
    icon ? 'pl-10' : ''
  } ${isPassword ? 'pr-10' : ''} ${className}`;

  return (
    <div className="mb-6">
      {label && (
        <label htmlFor={props.id || name} className={labelClasses}> {/* Use name as fallback for htmlFor */}
          {label}
          {props.required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}

      <div className="relative">
        {icon && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <div className={`text-gray-400 ${isFocused ? 'text-green-500' : ''} transition-colors duration-200`}>
              {icon}
            </div>
          </div>
        )}

        <input
          type={inputType}
          className={inputClasses}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          {...register(name, { shouldUnregister: true })} // Register input with react-hook-form
          {...props}
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