// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Storybook stories for design system components with Kenya-first examples
// [GOAL]: Comprehensive documentation of design system components

import type { Meta, StoryObj } from '@storybook/react';
import { Button, Card, Input, Typography } from '@/components/ui/design-system';
import { FaHeart, FaUser, FaVideo } from 'react-icons/fa';

// Button Stories
const ButtonMeta: Meta<typeof Button> = {
  title: 'Design System/Button',
  component: Button,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Enterprise-grade button component with Kenya-first design variants and cultural authenticity.',
      },
    },
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'kenya', 'cultural', 'danger', 'success'],
    },
    size: {
      control: 'select',
      options: ['xs', 'sm', 'md', 'lg', 'xl'],
    },
    loading: {
      control: 'boolean',
    },
  },
};

export default ButtonMeta;

type ButtonStory = StoryObj<typeof Button>;

export const Primary: ButtonStory = {
  args: {
    children: 'Create Video',
    variant: 'primary',
    size: 'md',
  },
};

export const KenyaFirst: ButtonStory = {
  args: {
    children: 'Unda Video',
    variant: 'kenya',
    size: 'md',
    icon: <FaVideo />,
  },
  parameters: {
    docs: {
      description: {
        story: 'Kenya-first button with Swahili text and cultural green color.',
      },
    },
  },
};

export const Cultural: ButtonStory = {
  args: {
    children: 'Harambee Spirit',
    variant: 'cultural',
    size: 'lg',
    icon: <FaHeart />,
  },
  parameters: {
    docs: {
      description: {
        story: 'Cultural variant with golden color representing African heritage.',
      },
    },
  },
};

export const Loading: ButtonStory = {
  args: {
    children: 'Generating...',
    variant: 'primary',
    size: 'md',
    loading: true,
  },
};

export const AllSizes: ButtonStory = {
  render: () => (
    <div className="flex flex-col gap-4 items-center">
      <Button size="xs" variant="kenya">Extra Small</Button>
      <Button size="sm" variant="kenya">Small</Button>
      <Button size="md" variant="kenya">Medium</Button>
      <Button size="lg" variant="kenya">Large</Button>
      <Button size="xl" variant="kenya">Extra Large</Button>
    </div>
  ),
};

// Card Stories
const CardMeta: Meta<typeof Card> = {
  title: 'Design System/Card',
  component: Card,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Flexible card component with Kenya-first design variants and cultural styling.',
      },
    },
  },
};

export const CardDefault: StoryObj<typeof Card> = {
  args: {
    children: (
      <div>
        <h3 className="text-lg font-semibold mb-2">Shujaa Studio</h3>
        <p className="text-gray-600">Create amazing videos with AI-powered tools designed for Kenya.</p>
      </div>
    ),
    variant: 'primary',
    padding: 'lg',
  },
};

export const CardKenya: StoryObj<typeof Card> = {
  args: {
    children: (
      <div>
        <h3 className="text-lg font-semibold mb-2 text-green-700">Umoja Project</h3>
        <p className="text-gray-600">Harness the power of unity in content creation.</p>
        <Button variant="kenya" size="sm" className="mt-3">
          Anza Sasa
        </Button>
      </div>
    ),
    variant: 'kenya',
    padding: 'xl',
  },
};

export const CardCultural: StoryObj<typeof Card> = {
  args: {
    children: (
      <div>
        <h3 className="text-lg font-semibold mb-2 text-yellow-700">Heritage Collection</h3>
        <p className="text-gray-600">Celebrate African culture through digital storytelling.</p>
        <Button variant="cultural" size="sm" className="mt-3">
          Explore
        </Button>
      </div>
    ),
    variant: 'cultural',
    padding: 'lg',
  },
};

// Input Stories
const InputMeta: Meta<typeof Input> = {
  title: 'Design System/Input',
  component: Input,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Form input component with Kenya-first styling and comprehensive validation states.',
      },
    },
  },
};

export const InputDefault: StoryObj<typeof Input> = {
  args: {
    label: 'Project Name',
    placeholder: 'Enter your project name',
    variant: 'primary',
    size: 'md',
  },
};

export const InputKenya: StoryObj<typeof Input> = {
  args: {
    label: 'Jina la Mradi',
    placeholder: 'Ingiza jina la mradi wako',
    variant: 'kenya',
    size: 'md',
    helperText: 'Tumia jina rahisi kukumbuka',
  },
};

export const InputWithError: StoryObj<typeof Input> = {
  args: {
    label: 'Email Address',
    placeholder: 'Enter your email',
    variant: 'primary',
    size: 'md',
    error: 'Please enter a valid email address',
    value: 'invalid-email',
  },
};

// Typography Stories
const TypographyMeta: Meta<typeof Typography> = {
  title: 'Design System/Typography',
  component: Typography,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Typography system with Kenya-first color variants and cultural authenticity.',
      },
    },
  },
};

export const TypographyHeadings: StoryObj<typeof Typography> = {
  render: () => (
    <div className="space-y-4 max-w-2xl">
      <Typography variant="h1" color="kenya">Karibu Shujaa Studio</Typography>
      <Typography variant="h2" color="primary">Create Amazing Content</Typography>
      <Typography variant="h3" color="cultural">Heritage & Innovation</Typography>
      <Typography variant="h4" color="secondary">Powered by AI</Typography>
      <Typography variant="body" color="primary">
        Shujaa Studio combines the power of artificial intelligence with the rich cultural heritage 
        of Kenya to create stunning video content that resonates with African audiences.
      </Typography>
      <Typography variant="caption" color="muted">
        Built with love in Nairobi, Kenya 🇰🇪
      </Typography>
    </div>
  ),
};

export const TypographyColors: StoryObj<typeof Typography> = {
  render: () => (
    <div className="space-y-2">
      <Typography variant="body" color="primary">Primary text color</Typography>
      <Typography variant="body" color="secondary">Secondary text color</Typography>
      <Typography variant="body" color="kenya">Kenya green color</Typography>
      <Typography variant="body" color="cultural">Cultural gold color</Typography>
      <Typography variant="body" color="muted">Muted text color</Typography>
    </div>
  ),
};

// Combined Design System Showcase
export const DesignSystemShowcase: StoryObj = {
  render: () => (
    <div className="max-w-4xl mx-auto p-6 space-y-8">
      <div className="text-center">
        <Typography variant="h1" color="kenya" className="mb-2">
          Shujaa Studio Design System
        </Typography>
        <Typography variant="body" color="secondary">
          Enterprise-grade components with Kenya-first cultural authenticity
        </Typography>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card variant="kenya" padding="lg">
          <Typography variant="h3" color="kenya" className="mb-3">
            Video Creation
          </Typography>
          <Typography variant="body" color="secondary" className="mb-4">
            Create professional videos with AI-powered tools designed for African storytelling.
          </Typography>
          <Button variant="kenya" size="sm" icon={<FaVideo />}>
            Unda Video
          </Button>
        </Card>

        <Card variant="cultural" padding="lg">
          <Typography variant="h3" color="cultural" className="mb-3">
            Heritage Library
          </Typography>
          <Typography variant="body" color="secondary" className="mb-4">
            Access a curated collection of African cultural elements and templates.
          </Typography>
          <Button variant="cultural" size="sm" icon={<FaHeart />}>
            Explore
          </Button>
        </Card>

        <Card variant="primary" padding="lg">
          <Typography variant="h3" color="primary" className="mb-3">
            User Dashboard
          </Typography>
          <Typography variant="body" color="secondary" className="mb-4">
            Manage your projects and track your creative journey.
          </Typography>
          <Button variant="primary" size="sm" icon={<FaUser />}>
            Dashboard
          </Button>
        </Card>
      </div>

      <div className="space-y-4">
        <Typography variant="h2" color="primary">
          Form Elements
        </Typography>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Project Name"
            placeholder="Enter project name"
            variant="primary"
            size="md"
          />
          <Input
            label="Jina la Mradi"
            placeholder="Ingiza jina la mradi"
            variant="kenya"
            size="md"
            helperText="Swahili input example"
          />
        </div>
      </div>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Complete showcase of the Shujaa Studio design system with Kenya-first components.',
      },
    },
  },
};

// Export all stories with unique names
export { CardDefault as Card };
export { InputDefault as Input };
export { TypographyHeadings as Typography };
