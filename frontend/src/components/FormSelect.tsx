import React from 'react';

interface FormSelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: { value: string; label: string }[];
}

export default function FormSelect({ label, options, className, ...props }: FormSelectProps) {
  return (
    <div className="mb-4">
      {label && <label className="block text-charcoal-text text-sm font-bold mb-2">{label}</label>}
      <select
        className={`form-input w-full ${className || ''}`}
        {...props}
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
}
