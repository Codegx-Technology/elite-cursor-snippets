// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Storybook stories for Loading and Error State components
// [GOAL]: Comprehensive documentation of state management UI with Kenya-first examples

import type { Meta, StoryObj } from '@storybook/react';
import { 
  LoadingSpinner, 
  LoadingCard, 
  VideoLoading, 
  Skeleton, 
  SkeletonCard, 
  SkeletonTable, 
  PageLoading, 
  LoadingButton 
} from '../components/ui/LoadingStates';
import { 
  Alert, 
  ErrorPage, 
  FormError, 
  EmptyState, 
  Toast, 
  NetworkStatus 
} from '../components/ui/ErrorStates';
import { useState } from 'react';

// Loading Spinner Stories
const LoadingSpinnerMeta: Meta<typeof LoadingSpinner> = {
  title: 'UI/LoadingStates/LoadingSpinner',
  component: LoadingSpinner,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Customizable loading spinner with Kenya-first design variants.',
      },
    },
  },
  argTypes: {
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg', 'xl'],
    },
    variant: {
      control: 'select',
      options: ['default', 'kenya', 'cultural', 'elite'],
    },
  },
};

export default LoadingSpinnerMeta;

export const SpinnerDefault: StoryObj<typeof LoadingSpinner> = {
  args: {
    size: 'md',
    variant: 'default',
  },
};

export const SpinnerKenya: StoryObj<typeof LoadingSpinner> = {
  args: {
    size: 'lg',
    variant: 'kenya',
  },
};

export const SpinnerSizes: StoryObj = {
  render: () => (
    <div className="flex items-center space-x-4">
      <LoadingSpinner size="sm" variant="kenya" />
      <LoadingSpinner size="md" variant="kenya" />
      <LoadingSpinner size="lg" variant="kenya" />
      <LoadingSpinner size="xl" variant="kenya" />
    </div>
  ),
};

// Video Loading Stories
const VideoLoadingMeta: Meta<typeof VideoLoading> = {
  title: 'UI/LoadingStates/VideoLoading',
  component: VideoLoading,
  parameters: {
    layout: 'centered',
  },
};

export const VideoLoadingUploading: StoryObj<typeof VideoLoading> = {
  args: {
    stage: 'uploading',
    variant: 'kenya',
    progress: 45,
  },
};

export const VideoLoadingProcessing: StoryObj<typeof VideoLoading> = {
  args: {
    stage: 'processing',
    variant: 'kenya',
    progress: 75,
  },
};

export const VideoLoadingGenerating: StoryObj<typeof VideoLoading> = {
  args: {
    stage: 'generating',
    variant: 'cultural',
    progress: 90,
  },
};

// Loading Card Stories
const LoadingCardMeta: Meta<typeof LoadingCard> = {
  title: 'UI/LoadingStates/LoadingCard',
  component: LoadingCard,
  parameters: {
    layout: 'centered',
  },
};

export const LoadingCardDefault: StoryObj<typeof LoadingCard> = {
  args: {
    title: 'Inapakia Maudhui...',
    subtitle: 'Tunapakia video na picha zako',
    variant: 'kenya',
    showProgress: true,
    progress: 65,
  },
};

// Skeleton Stories
const SkeletonMeta: Meta<typeof SkeletonCard> = {
  title: 'UI/LoadingStates/Skeleton',
  component: SkeletonCard,
  parameters: {
    layout: 'centered',
  },
};

export const SkeletonCardDefault: StoryObj<typeof SkeletonCard> = {
  args: {
    variant: 'kenya',
  },
};

export const SkeletonTableDefault: StoryObj<typeof SkeletonTable> = {
  args: {
    variant: 'kenya',
    rows: 5,
  },
};

// Loading Button Stories
const LoadingButtonMeta: Meta<typeof LoadingButton> = {
  title: 'UI/LoadingStates/LoadingButton',
  component: LoadingButton,
  parameters: {
    layout: 'centered',
  },
};

export const LoadingButtonExample: StoryObj = {
  render: () => {
    const InteractiveLoadingButtonExample = () => {
      const [loading, setLoading] = useState(false);
      
      const handleClick = () => {
        setLoading(true);
        setTimeout(() => setLoading(false), 3000);
      };

      return (
        <div className="space-y-4">
          <LoadingButton
            loading={loading}
            variant="kenya"
            onClick={handleClick}
          >
            {loading ? 'Inaunda Video...' : 'Unda Video'}
          </LoadingButton>
          
          <LoadingButton
            loading={false}
            variant="cultural"
            size="lg"
          >
            Anza Mradi
          </LoadingButton>
        </div>
      );
    };
    return <InteractiveLoadingButtonExample />;
  },
};

// Alert Stories
const AlertMeta: Meta<typeof Alert> = {
  title: 'UI/ErrorStates/Alert',
  component: Alert,
  parameters: {
    layout: 'centered',
  },
};

export const AlertSuccess: StoryObj<typeof Alert> = {
  args: {
    type: 'success',
    title: 'Umefanikiwa!',
    message: 'Video yako imeundwa kikamilifu na iko tayari kutumika.',
    variant: 'kenya',
  },
};

export const AlertError: StoryObj<typeof Alert> = {
  args: {
    type: 'error',
    title: 'Hitilafu Imetokea',
    message: 'Imeshindikana kuunda video. Tafadhali jaribu tena au wasiliana na msaada.',
    variant: 'kenya',
  },
};

export const AlertWarning: StoryObj<typeof Alert> = {
  args: {
    type: 'warning',
    title: 'Onyo',
    message: 'Faili lako ni kubwa sana. Inaweza kuchukua muda mrefu kuupakia.',
    variant: 'cultural',
  },
};

// Error Page Stories
const ErrorPageMeta: Meta<typeof ErrorPage> = {
  title: 'UI/ErrorStates/ErrorPage',
  component: ErrorPage,
  parameters: {
    layout: 'fullscreen',
  },
};

export const Error404: StoryObj<typeof ErrorPage> = {
  args: {
    type: 'not-found',
    variant: 'kenya',
    onRetry: () => console.log('Retry clicked'),
    onGoHome: () => console.log('Go home clicked'),
  },
};

export const Error500: StoryObj<typeof ErrorPage> = {
  args: {
    type: 'server-error',
    variant: 'kenya',
    onRetry: () => console.log('Retry clicked'),
    onGoHome: () => console.log('Go home clicked'),
  },
};

export const ErrorNetwork: StoryObj<typeof ErrorPage> = {
  args: {
    type: 'network-error',
    variant: 'cultural',
    onRetry: () => console.log('Retry clicked'),
  },
};

// Empty State Stories
const EmptyStateMeta: Meta<typeof EmptyState> = {
  title: 'UI/ErrorStates/EmptyState',
  component: EmptyState,
  parameters: {
    layout: 'centered',
  },
};

export const EmptyStateVideos: StoryObj<typeof EmptyState> = {
  args: {
    title: 'Hakuna Video',
    message: 'Bado hujatengeneza video yoyote. Anza kuunda maudhui yako ya kwanza!',
    variant: 'kenya',
    action: {
      label: 'Unda Video ya Kwanza',
      onClick: () => console.log('Create video clicked'),
    },
    icon: (
      <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-4">
        <span className="text-2xl">🎬</span>
      </div>
    ),
  },
};

export const EmptyStateProjects: StoryObj<typeof EmptyState> = {
  args: {
    title: 'Hakuna Miradi',
    message: 'Anza mradi wako wa kwanza wa kuunda maudhui ya kipekee.',
    variant: 'cultural',
    action: {
      label: 'Anza Mradi',
      onClick: () => console.log('Create project clicked'),
    },
    icon: (
      <div className="w-16 h-16 rounded-full bg-yellow-100 flex items-center justify-center mx-auto mb-4">
        <span className="text-2xl">📁</span>
      </div>
    ),
  },
};

// Toast Stories
const ToastMeta: Meta<typeof Toast> = {
  title: 'UI/ErrorStates/Toast',
  component: Toast,
  parameters: {
    layout: 'centered',
  },
};

export const ToastSuccess: StoryObj<typeof Toast> = {
  args: {
    type: 'success',
    title: 'Imehifadhiwa',
    message: 'Mabadiliko yako yamehifadhiwa kikamilifu.',
    variant: 'kenya',
  },
};

export const ToastError: StoryObj<typeof Toast> = {
  args: {
    type: 'error',
    title: 'Hitilafu',
    message: 'Imeshindikana kuhifadhi mabadiliko. Jaribu tena.',
    variant: 'kenya',
  },
};

// Form Error Stories
const FormErrorMeta: Meta<typeof FormError> = {
  title: 'UI/ErrorStates/FormError',
  component: FormError,
  parameters: {
    layout: 'centered',
  },
};

export const FormErrorExample: StoryObj<typeof FormError> = {
  args: {
    errors: {
      title: 'Kichwa cha video ni lazima',
      description: 'Maelezo ya video ni lazima',
      duration: 'Chagua muda wa video',
    },
    variant: 'kenya',
  },
};

// Complete Showcase
export const StateManagementShowcase: StoryObj = {
  render: () => (
    <div className="max-w-6xl mx-auto p-6 space-y-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Shujaa Studio State Management
        </h1>
        <p className="text-gray-600">
          Enterprise-grade loading and error states with Kenya-first design
        </p>
      </div>

      {/* Loading States Section */}
      <div className="space-y-6">
        <h2 className="text-2xl font-semibold text-green-700">Loading States</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <LoadingCard
            title="Inapakia Maudhui..."
            subtitle="Tunapakia video zako"
            variant="kenya"
            showProgress={true}
            progress={75}
          />
          
          <VideoLoading
            stage="processing"
            variant="kenya"
            progress={60}
          />
          
          <SkeletonCard variant="kenya" />
        </div>
      </div>

      {/* Error States Section */}
      <div className="space-y-6">
        <h2 className="text-2xl font-semibold text-red-700">Error States</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Alert
            type="error"
            title="Hitilafu Imetokea"
            message="Imeshindikana kuunda video. Tafadhali jaribu tena."
            variant="kenya"
          />
          
          <Alert
            type="warning"
            title="Onyo"
            message="Faili lako ni kubwa sana. Inaweza kuchukua muda mrefu."
            variant="cultural"
          />
        </div>
      </div>

      {/* Empty States Section */}
      <div className="space-y-6">
        <h2 className="text-2xl font-semibold text-yellow-700">Empty States</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <EmptyState
            title="Hakuna Video"
            message="Anza kuunda maudhui yako ya kwanza!"
            variant="kenya"
            action={{
              label: 'Unda Video',
              onClick: () => console.log('Create video')
            }}
            icon={
              <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🎬</span>
              </div>
            }
          />
          
          <EmptyState
            title="Hakuna Miradi"
            message="Anza mradi wako wa kwanza wa kuunda maudhui."
            variant="cultural"
            action={{
              label: 'Anza Mradi',
              onClick: () => console.log('Create project')
            }}
            icon={
              <div className="w-16 h-16 rounded-full bg-yellow-100 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">📁</span>
              </div>
            }
          />
        </div>
      </div>

      {/* Interactive Examples */}
      <div className="space-y-6">
        <h2 className="text-2xl font-semibold text-blue-700">Interactive Examples</h2>
        
        <div className="bg-gray-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Loading Button States</h3>
          <div className="flex space-x-4">
            <LoadingButton variant="kenya" loading={false}>
              Unda Video
            </LoadingButton>
            <LoadingButton variant="cultural" loading={true}>
              Inaunda...
            </LoadingButton>
            <LoadingButton variant="elite" loading={false} size="lg">
              Anza Mradi
            </LoadingButton>
          </div>
        </div>
      </div>

      <div className="bg-green-50 border border-green-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-green-800 mb-2">Kenya-First Features</h3>
        <ul className="text-green-700 space-y-1">
          <li>• Swahili localization for all user messages</li>
          <li>• Cultural color schemes and design patterns</li>
          <li>• Mobile-first responsive design</li>
          <li>• Contextual error messages with helpful guidance</li>
          <li>• Accessible design with proper ARIA attributes</li>
        </ul>
      </div>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Complete showcase of loading and error state components with Kenya-first design.',
      },
    },
  },
};
