import type { Meta, StoryObj } from '@storybook/react';
import { Welcome } from '../components/Welcome';
import LoadingStates from '../components/ui/LoadingStates';
import ErrorStates from '../components/ui/ErrorStates';

const meta: Meta = {
  title: 'Kenya-First/Enhanced Components',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Enhanced components with Kenya-first design elements and cultural authenticity'
      }
    }
  }
};

export default meta;

// Welcome Component with Animated Flag
export const WelcomeWithAnimatedFlag: StoryObj = {
  render: () => <Welcome />,
  parameters: {
    docs: {
      description: {
        story: 'Welcome page featuring animated Kenyan flag with wind effects and cultural elements'
      }
    }
  }
};

// Loading States with Cultural Elements
export const KenyaFirstLoadingStates: StoryObj = {
  render: () => (
    <div className="space-y-8 p-8">
      <div>
        <h2 className="text-2xl font-bold mb-4">Kenya-First Loading States</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Page Loading with Wildlife 🦒</h3>
            <LoadingStates.PageLoading />
          </div>
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Video Loading with Cultural Elements</h3>
            <LoadingStates.VideoLoading />
          </div>
        </div>
      </div>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Loading states enhanced with Kenyan wildlife emojis and cultural elements'
      }
    }
  }
};

// Error States with Kenya-First Design
export const KenyaFirstErrorStates: StoryObj = {
  render: () => (
    <div className="space-y-8 p-8">
      <div>
        <h2 className="text-2xl font-bold mb-4">Kenya-First Error States</h2>
        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold mb-2">Error Alert with Cultural Context</h3>
            <ErrorStates.Alert 
              type="error" 
              title="Connection Issue 🌍" 
              message="Unable to connect to Shujaa servers. Please check your internet connection." 
            />
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-2">Network Status with Kenya Context</h3>
            <ErrorStates.NetworkStatus 
              isOnline={false} 
              message="Offline - Your content will sync when connection is restored 📡" 
            />
          </div>
        </div>
      </div>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Error states with Kenya-first messaging and cultural context'
      }
    }
  }
};

// Cultural Design Showcase
export const CulturalDesignShowcase: StoryObj = {
  render: () => (
    <div className="space-y-8 p-8">
      <div className="text-center">
        <h2 className="text-3xl font-bold mb-4">Kenya-First Design Elements 🇰🇪</h2>
        <p className="text-lg text-gray-600 mb-8">
          Showcasing subtle cultural elements without overwhelming the UI
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-green-600 to-green-700 text-white p-6 rounded-lg">
          <h3 className="text-xl font-bold mb-2">Wildlife Elements 🦁</h3>
          <p>Subtle animal emojis in loading states and interactions</p>
        </div>
        
        <div className="bg-gradient-to-br from-red-600 to-red-700 text-white p-6 rounded-lg">
          <h3 className="text-xl font-bold mb-2">Cultural Colors 🎨</h3>
          <p>Kenya green (#00A651) and cultural gold (#FFD700)</p>
        </div>
        
        <div className="bg-gradient-to-br from-yellow-500 to-yellow-600 text-white p-6 rounded-lg">
          <h3 className="text-xl font-bold mb-2">Regional Data 🗺️</h3>
          <p>Nairobi, Mombasa, Kisumu examples in analytics</p>
        </div>
      </div>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Overview of Kenya-first design principles and cultural elements integration'
      }
    }
  }
};
