// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Complex multi-step form with validation and Kenya-first UX
// [GOAL]: Enterprise-grade form handling with cultural authenticity
// [TASK]: Phase 2.2 - Advanced form workflows with step validation

'use client';

import React, { useState } from 'react';
import { FormWizard, WizardStep, TextInputStep, SelectStep } from './FormWizard';
import { Button } from '@/components/ui/design-system';
import { colors } from '@/config/designTokens';
import { FaUser, FaVideo, FaCog, FaCheck } from 'react-icons/fa';

// Video Creation Form Steps
const VideoCreationStep: React.FC<any> = ({ data, updateData, variant }) => {
  const videoTypes = [
    { value: 'tourism', label: 'Utalii (Tourism)' },
    { value: 'cultural', label: 'Utamaduni (Cultural)' },
    { value: 'business', label: 'Biashara (Business)' },
    { value: 'educational', label: 'Elimu (Educational)' },
    { value: 'entertainment', label: 'Burudani (Entertainment)' }
  ];

  return (
    <div className="space-y-6">
      <SelectStep
        data={data}
        updateData={updateData}
        variant={variant}
        field={{
          name: 'videoType',
          label: 'Aina ya Video',
          options: videoTypes,
          required: true
        }}
        errors={{}}
      />
      
      <TextInputStep
        data={data}
        updateData={updateData}
        variant={variant}
        errors={{}}
        fields={[
          {
            name: 'title',
            label: 'Kichwa cha Video',
            placeholder: 'Ingiza kichwa cha video yako...',
            required: true
          },
          {
            name: 'description',
            label: 'Maelezo',
            placeholder: 'Eleza video yako kwa ufupi...',
            required: true
          }
        ]}
      />
    </div>
  );
};

const PersonalizationStep: React.FC<any> = ({ data, updateData, variant }) => {
  const languages = [
    { value: 'swahili', label: 'Kiswahili' },
    { value: 'english', label: 'English' },
    { value: 'kikuyu', label: 'Kikuyu' },
    { value: 'luo', label: 'Dholuo' },
    { value: 'kalenjin', label: 'Kalenjin' }
  ];

  const durations = [
    { value: '30', label: '30 sekunde' },
    { value: '60', label: '1 dakika' },
    { value: '120', label: '2 dakika' },
    { value: '300', label: '5 dakika' }
  ];

  return (
    <div className="space-y-6">
      <SelectStep
        data={data}
        updateData={updateData}
        variant={variant}
        field={{
          name: 'language',
          label: 'Lugha ya Video',
          options: languages,
          required: true
        }}
        errors={{}}
      />
      
      <SelectStep
        data={data}
        updateData={updateData}
        variant={variant}
        field={{
          name: 'duration',
          label: 'Muda wa Video',
          options: durations,
          required: true
        }}
        errors={{}}
      />

      <TextInputStep
        data={data}
        updateData={updateData}
        variant={variant}
        errors={{}}
        fields={[
          {
            name: 'targetAudience',
            label: 'Hadhira Lengwa',
            placeholder: 'Ni nani utakayewaona video hii?',
            required: false
          }
        ]}
      />
    </div>
  );
};

const ReviewStep: React.FC<any> = ({ data, variant }) => {
  const getVideoTypeLabel = (type: string) => {
    const types: Record<string, string> = {
      tourism: 'Utalii (Tourism)',
      cultural: 'Utamaduni (Cultural)',
      business: 'Biashara (Business)',
      educational: 'Elimu (Educational)',
      entertainment: 'Burudani (Entertainment)'
    };
    return types[type] || type;
  };

  const getLanguageLabel = (lang: string) => {
    const languages: Record<string, string> = {
      swahili: 'Kiswahili',
      english: 'English',
      kikuyu: 'Kikuyu',
      luo: 'Dholuo',
      kalenjin: 'Kalenjin'
    };
    return languages[lang] || lang;
  };

  return (
    <div className="space-y-6">
      <div className="bg-gray-50 rounded-lg p-6">
        <h4 className="font-semibold text-gray-900 mb-4">Muhtasari wa Video</h4>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <span className="text-sm font-medium text-gray-600">Aina ya Video:</span>
            <p className="text-gray-900">{getVideoTypeLabel(data.videoType)}</p>
          </div>
          
          <div>
            <span className="text-sm font-medium text-gray-600">Lugha:</span>
            <p className="text-gray-900">{getLanguageLabel(data.language)}</p>
          </div>
          
          <div>
            <span className="text-sm font-medium text-gray-600">Muda:</span>
            <p className="text-gray-900">{data.duration} sekunde</p>
          </div>
          
          {data.targetAudience && (
            <div>
              <span className="text-sm font-medium text-gray-600">Hadhira:</span>
              <p className="text-gray-900">{data.targetAudience}</p>
            </div>
          )}
        </div>
        
        <div className="mt-4">
          <span className="text-sm font-medium text-gray-600">Kichwa:</span>
          <p className="text-gray-900 font-medium">{data.title}</p>
        </div>
        
        <div className="mt-4">
          <span className="text-sm font-medium text-gray-600">Maelezo:</span>
          <p className="text-gray-900">{data.description}</p>
        </div>
      </div>
      
      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <div className="flex items-center space-x-2">
          <FaCheck className="text-green-600" />
          <span className="text-green-800 font-medium">Tayari kuanza uundaji wa video!</span>
        </div>
        <p className="text-green-700 text-sm mt-1">
          Video yako itaundwa kwa kutumia maelezo uliyotoa. Mchakato utachukua dakika 2-5.
        </p>
      </div>
    </div>
  );
};

// Main Multi-Step Form Component
export interface MultiStepFormProps {
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  onComplete?: (data: any) => void;
  onCancel?: () => void;
  className?: string;
}

export const VideoCreationForm: React.FC<MultiStepFormProps> = ({
  variant = 'kenya',
  onComplete,
  onCancel,
  className
}) => {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const steps: WizardStep[] = [
    {
      id: 'video-details',
      title: 'Maelezo ya Video',
      subtitle: 'Tuambie kuhusu video unayotaka kuunda',
      component: VideoCreationStep,
      validation: (data) => {
        if (!data.videoType) return 'Chagua aina ya video';
        if (!data.title?.trim()) return 'Ingiza kichwa cha video';
        if (!data.description?.trim()) return 'Ingiza maelezo ya video';
        return true;
      }
    },
    {
      id: 'personalization',
      title: 'Upangaji',
      subtitle: 'Panga video yako kulingana na mahitaji yako',
      component: PersonalizationStep,
      validation: (data) => {
        if (!data.language) return 'Chagua lugha ya video';
        if (!data.duration) return 'Chagua muda wa video';
        return true;
      }
    },
    {
      id: 'review',
      title: 'Kagua na Thibitisha',
      subtitle: 'Kagua maelezo yako kabla ya kuanza uundaji',
      component: ReviewStep,
      validation: () => true
    }
  ];

  const handleComplete = async (data: any) => {
    setIsSubmitting(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      onComplete?.(data);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isSubmitting) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Inaunda Video...</h3>
          <p className="text-gray-600">Tafadhali subiri, tunaunda video yako.</p>
        </div>
      </div>
    );
  }

  return (
    <FormWizard
      steps={steps}
      onComplete={handleComplete}
      onCancel={onCancel}
      variant={variant}
      className={className}
      showProgress={true}
      allowSkip={false}
    />
  );
};

// Project Setup Form
export const ProjectSetupForm: React.FC<MultiStepFormProps> = ({
  variant = 'cultural',
  onComplete,
  onCancel,
  className
}) => {
  const ProjectDetailsStep: React.FC<any> = ({ data, updateData, variant }) => (
    <TextInputStep
      data={data}
      updateData={updateData}
      variant={variant}
      errors={{}}
      fields={[
        {
          name: 'projectName',
          label: 'Jina la Mradi',
          placeholder: 'Ingiza jina la mradi wako...',
          required: true
        },
        {
          name: 'description',
          label: 'Maelezo ya Mradi',
          placeholder: 'Eleza mradi wako...',
          required: true
        }
      ]}
    />
  );

  const TeamSetupStep: React.FC<any> = ({ data, updateData, variant }) => (
    <div className="space-y-6">
      <TextInputStep
        data={data}
        updateData={updateData}
        variant={variant}
        errors={{}}
        fields={[
          {
            name: 'teamSize',
            label: 'Idadi ya Timu',
            placeholder: '5',
            type: 'number',
            required: true
          },
          {
            name: 'budget',
            label: 'Bajeti (KSh)',
            placeholder: '100000',
            type: 'number',
            required: false
          }
        ]}
      />
    </div>
  );

  const steps: WizardStep[] = [
    {
      id: 'project-details',
      title: 'Maelezo ya Mradi',
      subtitle: 'Anza kwa kutueleza kuhusu mradi wako',
      component: ProjectDetailsStep,
      validation: (data) => {
        if (!data.projectName?.trim()) return 'Ingiza jina la mradi';
        if (!data.description?.trim()) return 'Ingiza maelezo ya mradi';
        return true;
      }
    },
    {
      id: 'team-setup',
      title: 'Mpangilio wa Timu',
      subtitle: 'Panga timu yako na rasilimali',
      component: TeamSetupStep,
      validation: (data) => {
        if (!data.teamSize || data.teamSize < 1) return 'Ingiza idadi sahihi ya timu';
        return true;
      }
    }
  ];

  return (
    <FormWizard
      steps={steps}
      onComplete={onComplete}
      onCancel={onCancel}
      variant={variant}
      className={className}
      showProgress={true}
      allowSkip={true}
    />
  );
};

export default VideoCreationForm;
