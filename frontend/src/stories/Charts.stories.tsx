// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Storybook stories for Chart components with Kenya-first examples
// [GOAL]: Comprehensive documentation of chart components with cultural data

import type { Meta, StoryObj } from '@storybook/react';
import { BarChart, LineChart, DonutChart } from '@/components/charts/Chart';

// Sample Kenya-first data
const kenyaVideoData = [
  { label: 'Nairobi', value: 1250, color: '#00A651' },
  { label: 'Mombasa', value: 890, color: '#FF6B35' },
  { label: 'Kisumu', value: 650, color: '#FFD700' },
  { label: 'Nakuru', value: 420, color: '#87CEEB' },
  { label: 'Eldoret', value: 380, color: '#F4A460' }
];

const monthlyGrowthData = [
  { label: 'Jan', value: 1200 },
  { label: 'Feb', value: 1450 },
  { label: 'Mar', value: 1800 },
  { label: 'Apr', value: 2100 },
  { label: 'May', value: 2650 },
  { label: 'Jun', value: 3200 }
];

const contentTypeData = [
  { label: 'Tourism Videos', value: 45, color: '#00A651' },
  { label: 'Cultural Stories', value: 30, color: '#FFD700' },
  { label: 'Business Content', value: 15, color: '#FF6B35' },
  { label: 'Educational', value: 10, color: '#87CEEB' }
];

// Bar Chart Stories
const BarChartMeta: Meta<typeof BarChart> = {
  title: 'Charts/BarChart',
  component: BarChart,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Enterprise-grade bar chart component with Kenya-first design variants and cultural data visualization.',
      },
    },
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'kenya', 'cultural', 'elite'],
    },
    showValues: {
      control: 'boolean',
    },
  },
};

export default BarChartMeta;

type BarChartStory = StoryObj<typeof BarChart>;

export const Default: BarChartStory = {
  args: {
    data: kenyaVideoData,
    title: 'Video Creation by City',
    subtitle: 'Monthly video generation statistics',
    variant: 'default',
    showValues: true,
  },
};

export const KenyaFirst: BarChartStory = {
  args: {
    data: kenyaVideoData,
    title: 'Uundaji wa Video kwa Mji',
    subtitle: 'Takwimu za kila mwezi za uundaji wa video',
    variant: 'kenya',
    showValues: true,
  },
  parameters: {
    docs: {
      description: {
        story: 'Kenya-first bar chart with Swahili labels and cultural green theming.',
      },
    },
  },
};

export const Cultural: BarChartStory = {
  args: {
    data: [
      { label: 'Maasai Heritage', value: 850 },
      { label: 'Kikuyu Traditions', value: 720 },
      { label: 'Luo Culture', value: 680 },
      { label: 'Kalenjin Stories', value: 540 },
      { label: 'Coastal Swahili', value: 490 }
    ],
    title: 'Cultural Content Creation',
    subtitle: 'Traditional stories and heritage videos',
    variant: 'cultural',
    showValues: true,
  },
};

// Line Chart Stories
const LineChartMeta: Meta<typeof LineChart> = {
  title: 'Charts/LineChart',
  component: LineChart,
  parameters: {
    layout: 'centered',
  },
};

export const LineChartDefault: StoryObj<typeof LineChart> = {
  args: {
    data: monthlyGrowthData,
    title: 'Monthly Growth Trend',
    subtitle: 'User engagement over time',
    variant: 'default',
    showDots: true,
  },
};

export const LineChartKenya: StoryObj<typeof LineChart> = {
  args: {
    data: monthlyGrowthData,
    title: 'Ukuaji wa Kila Mwezi',
    subtitle: 'Ushiriki wa watumiaji kwa muda',
    variant: 'kenya',
    showDots: true,
  },
};

// Donut Chart Stories
const DonutChartMeta: Meta<typeof DonutChart> = {
  title: 'Charts/DonutChart',
  component: DonutChart,
  parameters: {
    layout: 'centered',
  },
};

export const DonutChartDefault: StoryObj<typeof DonutChart> = {
  args: {
    data: contentTypeData,
    title: 'Content Distribution',
    subtitle: 'Types of content created',
    variant: 'default',
    centerText: '100%',
    showLegend: true,
  },
};

export const DonutChartKenya: StoryObj<typeof DonutChart> = {
  args: {
    data: contentTypeData,
    title: 'Mgawanyo wa Maudhui',
    subtitle: 'Aina za maudhui yaliyoundwa',
    variant: 'kenya',
    centerText: 'Jumla',
    showLegend: true,
  },
};

// Combined Dashboard Example
export const DashboardShowcase: StoryObj = {
  render: () => (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Shujaa Studio Analytics Dashboard
        </h1>
        <p className="text-gray-600">
          Kenya-first data visualization with cultural authenticity
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <BarChart
          data={kenyaVideoData}
          title="Video Creation by Region"
          subtitle="Regional content generation statistics"
          variant="kenya"
          showValues={true}
        />
        
        <DonutChart
          data={contentTypeData}
          title="Content Categories"
          subtitle="Distribution of content types"
          variant="cultural"
          centerText="Total"
          showLegend={true}
        />
      </div>

      <div className="w-full">
        <LineChart
          data={monthlyGrowthData}
          title="Platform Growth Trajectory"
          subtitle="Monthly active users and content creation"
          variant="kenya"
          width={800}
          height={300}
          showDots={true}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="text-2xl font-bold text-green-700">3,200+</div>
          <div className="text-green-600">Videos Created</div>
        </div>
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="text-2xl font-bold text-yellow-700">47</div>
          <div className="text-yellow-600">Counties Reached</div>
        </div>
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="text-2xl font-bold text-blue-700">12K+</div>
          <div className="text-blue-600">Active Users</div>
        </div>
      </div>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Complete dashboard showcase with Kenya-first charts and cultural data visualization.',
      },
    },
  },
};

// Export Line and Donut chart stories
export { LineChartDefault as LineChart, LineChartKenya };
export { DonutChartDefault as DonutChart, DonutChartKenya };
