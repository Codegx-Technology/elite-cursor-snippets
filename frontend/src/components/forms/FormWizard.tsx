// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Enterprise-grade Form Wizard with Kenya-first design system integration
// [GOAL]: Create multi-step form wizard with cultural authenticity and mobile-first design
// [TASK]: Phase 2.2 - User Workflow Components with complex forms and wizards

'use client';

import React, { useState, useCallback } from 'react';
import { Button } from '@/components/ui/design-system';
import { colors, spacing, typography } from '@/config/designTokens';
import { cn } from '@/lib/utils';
import { FaCheck, FaChevronLeft, FaChevronRight } from 'react-icons/fa';

// Form Wizard Step Interface
export interface WizardStep {
  id: string;
  title: string;
  subtitle?: string;
  component: React.ComponentType<WizardStepProps>;
  validation?: (data: any) => boolean | string;
  optional?: boolean;
}

// Step Component Props
export interface WizardStepProps {
  data: any;
  updateData: (data: any) => void;
  errors: Record<string, string>;
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
}

// Main Form Wizard Props
export interface FormWizardProps {
  steps: WizardStep[];
  onComplete: (data: any) => void;
  onCancel?: () => void;
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  className?: string;
  initialData?: any;
  showProgress?: boolean;
  allowSkip?: boolean;
}

export const FormWizard: React.FC<FormWizardProps> = ({
  steps,
  onComplete,
  onCancel,
  variant = 'default',
  className,
  initialData = {},
  showProgress = true,
  allowSkip = false
}) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState(initialData);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set());

  const variantClasses = {
    default: 'border-gray-200 bg-white',
    kenya: `border-[${colors.kenya.green}] border-opacity-20 bg-white`,
    cultural: `border-[${colors.cultural.gold}] border-opacity-30 bg-gradient-to-br from-white to-yellow-50`,
    elite: 'border-purple-200 bg-gradient-to-br from-white to-purple-50'
  };

  const progressColors = {
    default: 'bg-blue-500',
    kenya: `bg-[${colors.kenya.green}]`,
    cultural: `bg-[${colors.cultural.gold}]`,
    elite: 'bg-purple-500'
  };

  const updateData = useCallback((newData: any) => {
    setFormData(prev => ({ ...prev, ...newData }));
    setErrors({});
  }, []);

  const validateCurrentStep = useCallback(() => {
    const step = steps[currentStep];
    if (!step.validation) return true;

    const result = step.validation(formData);
    if (typeof result === 'string') {
      setErrors({ [step.id]: result });
      return false;
    }
    return result;
  }, [currentStep, formData, steps]);

  const handleNext = useCallback(() => {
    if (validateCurrentStep()) {
      setCompletedSteps(prev => new Set([...prev, currentStep]));
      if (currentStep < steps.length - 1) {
        setCurrentStep(currentStep + 1);
      } else {
        onComplete(formData);
      }
    }
  }, [currentStep, formData, onComplete, steps.length, validateCurrentStep]);

  const handlePrevious = useCallback(() => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  }, [currentStep]);

  const handleStepClick = useCallback((stepIndex: number) => {
    if (stepIndex < currentStep || completedSteps.has(stepIndex)) {
      setCurrentStep(stepIndex);
    }
  }, [currentStep, completedSteps]);

  const currentStepData = steps[currentStep];
  const StepComponent = currentStepData.component;
  const progress = ((currentStep + 1) / steps.length) * 100;

  return (
    <div className={cn(
      'max-w-4xl mx-auto rounded-lg border shadow-sm',
      variantClasses[variant],
      className
    )}>
      {/* Progress Header */}
      {showProgress && (
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between mb-4">
            <h2 className={cn(
              'font-semibold',
              `text-[${typography.fontSizes.xl}]`,
              variant === 'kenya' && `text-[${colors.kenya.green}]`,
              variant === 'cultural' && `text-[${colors.cultural.gold}]`
            )}>
              Hatua {currentStep + 1} ya {steps.length}
            </h2>
            <span className={cn(
              'text-gray-500',
              `text-[${typography.fontSizes.sm}]`
            )}>
              {Math.round(progress)}% Imekamilika
            </span>
          </div>

          {/* Progress Bar */}
          <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
            <div
              className={cn('h-2 rounded-full transition-all duration-300', progressColors[variant])}
              style={{ width: `${progress}%` }}
            />
          </div>

          {/* Step Indicators */}
          <div className="flex items-center justify-between">
            {steps.map((step, index) => (
              <div
                key={step.id}
                className="flex flex-col items-center cursor-pointer"
                onClick={() => handleStepClick(index)}
              >
                <div className={cn(
                  'w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-all duration-200',
                  index < currentStep || completedSteps.has(index)
                    ? cn('text-white', progressColors[variant])
                    : index === currentStep
                    ? cn('border-2 text-gray-700', 
                        variant === 'kenya' ? `border-[${colors.kenya.green}]` :
                        variant === 'cultural' ? `border-[${colors.cultural.gold}]` :
                        'border-blue-500')
                    : 'bg-gray-200 text-gray-500'
                )}>
                  {completedSteps.has(index) ? (
                    <FaCheck className="w-3 h-3" />
                  ) : (
                    index + 1
                  )}
                </div>
                <span className={cn(
                  'mt-2 text-center max-w-20 truncate',
                  `text-[${typography.fontSizes.xs}]`,
                  index === currentStep ? 'text-gray-900 font-medium' : 'text-gray-500'
                )}>
                  {step.title}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Step Content */}
      <div className="px-6 py-8">
        <div className="mb-6">
          <h3 className={cn(
            'font-semibold text-gray-900 mb-2',
            `text-[${typography.fontSizes['2xl']}]`
          )}>
            {currentStepData.title}
          </h3>
          {currentStepData.subtitle && (
            <p className={cn(
              'text-gray-600',
              `text-[${typography.fontSizes.base}]`
            )}>
              {currentStepData.subtitle}
            </p>
          )}
        </div>

        {/* Error Display */}
        {errors[currentStepData.id] && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-700 text-sm">{errors[currentStepData.id]}</p>
          </div>
        )}

        {/* Step Component */}
        <div className="mb-8">
          <StepComponent
            data={formData}
            updateData={updateData}
            errors={errors}
            variant={variant}
          />
        </div>
      </div>

      {/* Navigation Footer */}
      <div className="px-6 py-4 border-t border-gray-200 bg-gray-50 rounded-b-lg">
        <div className="flex items-center justify-between">
          <div className="flex space-x-3">
            {onCancel && (
              <Button
                variant="secondary"
                size="md"
                onClick={onCancel}
              >
                Ghairi
              </Button>
            )}
            {currentStep > 0 && (
              <Button
                variant="secondary"
                size="md"
                onClick={handlePrevious}
                icon={<FaChevronLeft />}
              >
                Nyuma
              </Button>
            )}
          </div>

          <div className="flex space-x-3">
            {allowSkip && !currentStepData.optional === false && currentStep < steps.length - 1 && (
              <Button
                variant="secondary"
                size="md"
                onClick={() => setCurrentStep(currentStep + 1)}
              >
                Ruka
              </Button>
            )}
            <Button
              variant={variant === 'kenya' ? 'kenya' : variant === 'cultural' ? 'cultural' : 'primary'}
              size="md"
              onClick={handleNext}
              icon={currentStep === steps.length - 1 ? <FaCheck /> : <FaChevronRight />}
            >
              {currentStep === steps.length - 1 ? 'Maliza' : 'Endelea'}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Pre-built Step Components
export const TextInputStep: React.FC<WizardStepProps & {
  fields: Array<{
    name: string;
    label: string;
    placeholder?: string;
    required?: boolean;
    type?: string;
  }>;
}> = ({ data, updateData, fields, variant }) => {
  return (
    <div className="space-y-6">
      {fields.map((field) => (
        <div key={field.name}>
          <label className={cn(
            'block font-medium text-gray-700 mb-2',
            `text-[${typography.fontSizes.sm}]`
          )}>
            {field.label}
            {field.required && <span className="text-red-500 ml-1">*</span>}
          </label>
          <input
            type={field.type || 'text'}
            value={data[field.name] || ''}
            onChange={(e) => updateData({ [field.name]: e.target.value })}
            placeholder={field.placeholder}
            className={cn(
              'w-full px-4 py-3 border rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-1',
              variant === 'kenya' ? `border-gray-300 focus:border-[${colors.kenya.green}] focus:ring-green-500` :
              variant === 'cultural' ? `border-gray-300 focus:border-[${colors.cultural.gold}] focus:ring-yellow-500` :
              'border-gray-300 focus:border-blue-500 focus:ring-blue-500',
              'bg-white placeholder:text-gray-400'
            )}
          />
        </div>
      ))}
    </div>
  );
};

export const SelectStep: React.FC<WizardStepProps & {
  field: {
    name: string;
    label: string;
    options: Array<{ value: string; label: string }>;
    required?: boolean;
  };
}> = ({ data, updateData, field, variant }) => {
  return (
    <div>
      <label className={cn(
        'block font-medium text-gray-700 mb-2',
        `text-[${typography.fontSizes.sm}]`
      )}>
        {field.label}
        {field.required && <span className="text-red-500 ml-1">*</span>}
      </label>
      <select
        value={data[field.name] || ''}
        onChange={(e) => updateData({ [field.name]: e.target.value })}
        className={cn(
          'w-full px-4 py-3 border rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-1',
          variant === 'kenya' ? `border-gray-300 focus:border-[${colors.kenya.green}] focus:ring-green-500` :
          variant === 'cultural' ? `border-gray-300 focus:border-[${colors.cultural.gold}] focus:ring-yellow-500` :
          'border-gray-300 focus:border-blue-500 focus:ring-blue-500',
          'bg-white'
        )}
      >
        <option value="">Chagua chaguo...</option>
        {field.options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
};
