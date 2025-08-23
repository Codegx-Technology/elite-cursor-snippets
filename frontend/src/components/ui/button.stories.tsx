import type { Meta, StoryObj } from '@storybook/react';
import { Button } from '@/components/ui/button';
import { FiSend, FiLoader, FiCheckCircle } from 'react-icons/fi'; // Added FiLoader, FiCheckCircle

const meta: Meta<typeof Button> = {
  title: 'UI/Button',
  component: Button,
  tags: ['autodocs'],
  args: {
    children: 'Click me',
  },
};

export default meta;

type Story = StoryObj<typeof Button>;

export const Default: Story = {
  args: {},
};

export const Variants: Story = {
  render: () => (
    <div className="flex gap-2 flex-wrap">
      <Button variant="default">Default</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="destructive">Destructive</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="link">Link</Button>
    </div>
  ),
};

export const Sizes: Story = {
  render: () => (
    <div className="flex gap-2 items-center">
      <Button size="sm">Small</Button>
      <Button size="default">Default</Button>
      <Button size="lg">Large</Button>
      <Button size="icon" aria-label="Icon button">
        <FiSend />
      </Button>
    </div>
  ),
};

export const Loading: Story = {
  args: {
    loading: true,
    children: 'Loading...', // Explicitly show text that would be hidden
  },
};

export const WithIcons: Story = {
  render: () => (
    <div className="flex gap-2 flex-wrap">
      <Button leadingIcon={<FiSend />}>Send Message</Button>
      <Button trailingIcon={<FiCheckCircle />} variant="secondary">Done</Button>
      <Button leadingIcon={<FiLoader />} loading>Processing</Button>
      <Button leadingIcon={<FiSend />} trailingIcon={<FiCheckCircle />} variant="outline">Send & Confirm</Button>
    </div>
  ),
};
