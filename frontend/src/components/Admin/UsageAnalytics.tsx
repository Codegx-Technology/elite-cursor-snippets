'use client';

import { useUsageAnalytics } from '@/hooks/useUsageAnalytics';
import { FaSpinner } from 'react-icons/fa';
import Card from '@/components/Card';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Reusable usage analytics component
// [GOAL]: Provide a clean and reusable component for displaying usage analytics

export default function UsageAnalytics() {
  const { analytics, isLoading, error } = useUsageAnalytics();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <FaSpinner className="w-8 h-8 text-green-600 animate-spin mx-auto mb-4" />
          <span className="text-gray-600 font-medium">Loading usage analytics...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-500 text-center">
        <p>Error: {error}</p>
      </div>
    );
  }

  if (!analytics) {
    return <div className="text-center text-soft-text">No usage analytics available.</div>;
  }

  return (
    <div className="elite-container my-10">
      <h1 className="section-title text-center mb-8">Usage Analytics</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="p-6">
          <h3 className="section-subtitle mb-2">Total Videos Generated</h3>
          <p className="text-2xl font-bold">{analytics.total_videos_generated}</p>
        </Card>
        <Card className="p-6">
          <h3 className="section-subtitle mb-2">Total Images Generated</h3>
          <p className="text-2xl font-bold">{analytics.total_images_generated}</p>
        </Card>
        <Card className="p-6">
          <h3 className="section-subtitle mb-2">Total Audio Generated</h3>
          <p className="text-2xl font-bold">{analytics.total_audio_generated}</p>
        </Card>
      </div>

      <Card className="p-6 mt-6">
        <h3 className="section-subtitle mb-4">Daily Usage</h3>
        {/* Charts will go here */}
      </Card>
    </div>
  );
}
