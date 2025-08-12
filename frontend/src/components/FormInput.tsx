import React from 'react';

interface FormInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}

export default function FormInput({ label, className, ...props }: FormInputProps) {
  return (
    <div className="mb-4">
      {label && <label className="block text-charcoal-text text-sm font-bold mb-2">{label}</label>}
      <input
        className={`form-input w-full ${className || ''}`}
        {...props}
      />
    </div>
  );
}