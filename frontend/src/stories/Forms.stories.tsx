// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Storybook stories for Form Wizard and Multi-Step Form components
// [GOAL]: Comprehensive documentation of form workflows with Kenya-first examples

import type { Meta, StoryObj } from '@storybook/react';
import { VideoCreationForm, ProjectSetupForm } from '../components/forms/MultiStepForm';
import { FormWizard, TextInputStep, SelectStep } from '../components/forms/FormWizard';

// Video Creation Form Stories
const VideoCreationMeta: Meta<typeof VideoCreationForm> = {
  title: 'Forms/VideoCreationForm',
  component: VideoCreationForm,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Enterprise-grade multi-step video creation form with Kenya-first UX and Swahili localization.',
      },
    },
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'kenya', 'cultural', 'elite'],
    },
  },
};

export default VideoCreationMeta;

type VideoCreationStory = StoryObj<typeof VideoCreationForm>;

export const Default: VideoCreationStory = {
  args: {
    variant: 'kenya',
    onComplete: (data) => {
      console.log('Video creation completed:', data);
      alert('Video creation started! Check console for data.');
    },
    onCancel: () => {
      console.log('Video creation cancelled');
      alert('Video creation cancelled');
    },
  },
};

export const Cultural: VideoCreationStory = {
  args: {
    variant: 'cultural',
    onComplete: (data) => {
      console.log('Cultural video creation completed:', data);
    },
  },
  parameters: {
    docs: {
      description: {
        story: 'Cultural variant with gold theming for heritage and traditional content creation.',
      },
    },
  },
};

export const Elite: VideoCreationStory = {
  args: {
    variant: 'elite',
    onComplete: (data) => {
      console.log('Elite video creation completed:', data);
    },
  },
};

// Project Setup Form Stories
const ProjectSetupMeta: Meta<typeof ProjectSetupForm> = {
  title: 'Forms/ProjectSetupForm',
  component: ProjectSetupForm,
  parameters: {
    layout: 'centered',
  },
};

export const ProjectSetupDefault: StoryObj<typeof ProjectSetupForm> = {
  args: {
    variant: 'cultural',
    onComplete: (data) => {
      console.log('Project setup completed:', data);
      alert('Project created successfully! Check console for data.');
    },
    onCancel: () => {
      console.log('Project setup cancelled');
    },
  },
};

export const ProjectSetupKenya: StoryObj<typeof ProjectSetupForm> = {
  args: {
    variant: 'kenya',
    onComplete: (data) => {
      console.log('Kenya project setup completed:', data);
    },
  },
};

// Custom Form Wizard Example
const CustomWizardMeta: Meta<typeof FormWizard> = {
  title: 'Forms/FormWizard',
  component: FormWizard,
  parameters: {
    layout: 'centered',
  },
};

interface BusinessFormData {
  businessName: string;
  registrationNumber: string;
}

// Custom Business Registration Form
const BusinessInfoStep: React.FC<WizardStepProps<BusinessFormData>> = ({ data, updateData, variant }) => (
  <div className="space-y-6">
    <TextInputStep
      data={data}
      updateData={updateData}
      variant={variant}
      errors={{}}
      fields={[
        {
          name: 'businessName',
          label: 'Jina la Biashara',
          placeholder: 'Ingiza jina la biashara yako...',
          required: true
        },
        {
          name: 'registrationNumber',
          label: 'Nambari ya Usajili',
          placeholder: 'KE123456789',
          required: true
        }
      ]}
    />
  </div>
);

interface LocationFormData {
  county: string;
  town: string;
  address?: string;
}

const LocationStep: React.FC<WizardStepProps<LocationFormData>> = ({ data, updateData, variant }) => {
  const counties = [
    { value: 'nairobi', label: 'Nairobi' },
    { value: 'mombasa', label: 'Mombasa' },
    { value: 'kisumu', label: 'Kisumu' },
    { value: 'nakuru', label: 'Nakuru' },
    { value: 'eldoret', label: 'Eldoret' },
    { value: 'thika', label: 'Thika' },
    { value: 'malindi', label: 'Malindi' }
  ];

  return (
    <div className="space-y-6">
      <SelectStep
        data={data}
        updateData={updateData}
        variant={variant}
        field={{
          name: 'county',
          label: 'Kaunti',
          options: counties,
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
            name: 'town',
            label: 'Mji/Mtaa',
            placeholder: 'Ingiza mji au mtaa...',
            required: true
          },
          {
            name: 'address',
            label: 'Anwani Kamili',
            placeholder: 'P.O Box 123, Nairobi',
            required: false
          }
        ]}
      />
    </div>
  );
};

export const BusinessRegistration: StoryObj<typeof FormWizard> = {
  args: {
    variant: 'kenya',
    showProgress: true,
    allowSkip: false,
    steps: [
      {
        id: 'business-info',
        title: 'Maelezo ya Biashara',
        subtitle: 'Tueleze kuhusu biashara yako',
        component: BusinessInfoStep,
        validation: (data) => {
          if (!data.businessName?.trim()) return 'Ingiza jina la biashara';
          if (!data.registrationNumber?.trim()) return 'Ingiza nambari ya usajili';
          return true;
        }
      },
      {
        id: 'location',
        title: 'Mahali',
        subtitle: 'Biashara yako iko wapi?',
        component: LocationStep,
        validation: (data) => {
          if (!data.county) return 'Chagua kaunti';
          if (!data.town?.trim()) return 'Ingiza mji au mtaa';
          return true;
        }
      }
    ],
    onComplete: (data) => {
      console.log('Business registration completed:', data);
      alert('Biashara imesajiliwa! Business registered successfully!');
    },
    onCancel: () => {
      console.log('Business registration cancelled');
    },
  },
  parameters: {
    docs: {
      description: {
        story: 'Custom business registration wizard with Kenya-specific fields and validation.',
      },
    },
  },
};

// Tourism Package Creation Form
interface PackageFormData {
  packageType: string;
  packageName: string;
  duration: number;
  price: number;
}

const PackageDetailsStep: React.FC<WizardStepProps<PackageFormData>> = ({ data, updateData, variant }) => {
  const packageTypes = [
    { value: 'safari', label: 'Safari ya Wanyamapori' },
    { value: 'cultural', label: 'Ziara za Kitamaduni' },
    { value: 'beach', label: 'Mapumziko ya Pwani' },
    { value: 'adventure', label: 'Michezo ya Hatari' },
    { value: 'business', label: 'Safari za Biashara' }
  ];

  return (
    <div className="space-y-6">
      <SelectStep
        data={data}
        updateData={updateData}
        variant={variant}
        field={{
          name: 'packageType',
          label: 'Aina ya Kifurushi',
          options: packageTypes,
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
            name: 'packageName',
            label: 'Jina la Kifurushi',
            placeholder: 'Safari Nzuri ya Maasai Mara...',
            required: true
          },
          {
            name: 'duration',
            label: 'Muda (Siku)',
            placeholder: '3',
            type: 'number',
            required: true
          },
          {
            name: 'price',
            label: 'Bei (KSh)',
            placeholder: '25000',
            type: 'number',
            required: true
          }
        ]}
      />
    </div>
  );
};

export const TourismPackage: StoryObj<typeof FormWizard> = {
  args: {
    variant: 'cultural',
    showProgress: true,
    allowSkip: true,
    steps: [
      {
        id: 'package-details',
        title: 'Maelezo ya Kifurushi',
        subtitle: 'Unda kifurushi chako cha utalii',
        component: PackageDetailsStep,
        validation: (data) => {
          if (!data.packageType) return 'Chagua aina ya kifurushi';
          if (!data.packageName?.trim()) return 'Ingiza jina la kifurushi';
          if (!data.duration || data.duration < 1) return 'Ingiza muda sahihi';
          if (!data.price || data.price < 1) return 'Ingiza bei sahihi';
          return true;
        }
      }
    ],
    onComplete: (data) => {
      console.log('Tourism package created:', data);
      alert('Kifurushi cha utalii kimeundwa! Tourism package created!');
    },
  },
  parameters: {
    docs: {
      description: {
        story: 'Tourism package creation form with cultural theming and Swahili localization.',
      },
    },
  },
};

// Form Showcase
export const FormShowcase: StoryObj = {
  render: () => (
    <div className="max-w-6xl mx-auto p-6 space-y-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Shujaa Studio Form Workflows
        </h1>
        <p className="text-gray-600">
          Enterprise-grade multi-step forms with Kenya-first design and cultural authenticity
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-green-700">Video Creation Workflow</h2>
          <div className="bg-green-50 border border-green-200 rounded-lg p-6">
            <VideoCreationForm
              variant="kenya"
              onComplete={(data) => console.log('Video:', data)}
            />
          </div>
        </div>

        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-yellow-700">Project Setup Workflow</h2>
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <ProjectSetupForm
              variant="cultural"
              onComplete={(data) => console.log('Project:', data)}
            />
          </div>
        </div>
      </div>

      <div className="bg-gray-50 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Key Features</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-2xl mb-2">🇰🇪</div>
            <h4 className="font-medium text-gray-900">Kenya-First Design</h4>
            <p className="text-sm text-gray-600">Swahili localization and cultural authenticity</p>
          </div>
          <div className="text-center">
            <div className="text-2xl mb-2">📱</div>
            <h4 className="font-medium text-gray-900">Mobile-First</h4>
            <p className="text-sm text-gray-600">Responsive design for all screen sizes</p>
          </div>
          <div className="text-center">
            <div className="text-2xl mb-2">✅</div>
            <h4 className="font-medium text-gray-900">Smart Validation</h4>
            <p className="text-sm text-gray-600">Real-time validation with helpful error messages</p>
          </div>
        </div>
      </div>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Complete showcase of form workflows with Kenya-first design and cultural authenticity.',
      },
    },
  },
};
