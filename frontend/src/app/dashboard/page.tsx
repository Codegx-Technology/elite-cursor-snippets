// [TASK]: Create a new page component for the user dashboard.
// [GOAL]: Provide a central hub for users to view PlanGuard info, recent projects, and account settings.
// [CONSTRAINTS]: Integrate seamlessly with existing UI, use Tailwind CSS, apply Kenya-first principles.
// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Building out the enterprise-grade UI, starting with the user dashboard.

"use client";

import React, { useEffect, useState } from 'react';
import { usePlanGuard } from '@/context/PlanGuardContext';
import { useAuth } from '@/context/AuthContext';
import Link from 'next/link';
import { FaVideo, FaCreditCard, FaCog, FaChartLine, FaImage, FaMusic } from 'react-icons/fa6';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import type { PlanStatus } from '@/widgets/PlanGuardWidget/types';
import { apiClient, Project } from '@/lib/api';
// Phase 2 Enterprise Components
import LoadingStates from '@/components/ui/LoadingStates';
import ErrorStates from '@/components/ui/ErrorStates';
import { BarChart, LineChart } from '@/components/charts/Chart';

// [SNIPPET]: thinkwithai + kenyafirst + refactorclean
// [CONTEXT]: Dashboard page component for Shujaa Studio users.
// [GOAL]: Display user-specific information like plan status, usage, and quick links.
// [TASK]: Implement the main dashboard layout and integrate data from contexts.

export default function DashboardPage() {
  const { planStatus, loading: planLoading, error: planError } = usePlanGuard();
  const { user, isLoading: authLoading } = useAuth();

  const [projects, setProjects] = useState<Project[]>([]);
  const [projectsLoading, setProjectsLoading] = useState(true);
  const [projectsError, setProjectsError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProjects = async () => {
      setProjectsLoading(true);
      setProjectsError(null);
      try {
        const response = await apiClient.getProjects(1, 3); // Fetch first 3 projects
        if (response.data) {
          setProjects(response.data.projects);
        } else if (response.error) {
          setProjectsError(response.error);
        }
      } catch (err: unknown) {
        const message = err instanceof Error ? err.message : 'Failed to fetch projects.';
        setProjectsError(message);
      } finally {
        setProjectsLoading(false);
      }
    };

    fetchProjects();
  }, []);

  const getPlanStateVariant = (state: PlanStatus['state']) => {
    switch (state) {
      case 'healthy':
        return 'success'; // Assuming a 'success' variant for Badge
      case 'grace':
        return 'warning';
      case 'view_only':
      case 'locked':
        return 'destructive';
      default:
        return 'default';
    }
  };

  if (planLoading || authLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen-content">
        <LoadingStates.PageLoading message="Loading dashboard data... 🦒" />
      </div>
    );
  }

  if (planError) {
    return (
      <div className="flex justify-center items-center min-h-screen-content">
        <ErrorStates.ErrorPage 
          type="server-error"
          customTitle="Plan Error"
          customMessage={`Failed to load plan information: ${planError}`}
          onRetry={() => window.location.reload()}
        />
      </div>
    );
  }

  // Sample analytics data for charts
  const usageData = [
    { label: 'Video', value: planStatus?.usage.videoMins || 0, color: '#00A651' },
    { label: 'Miradi', value: projects.length, color: '#3B82F6' },
    { label: 'Matumizi', value: Math.round((planStatus?.usage.videoMins || 0) / (planStatus?.quota.videoMins || 100) * 100), color: '#8B5CF6' }
  ];

  const monthlyData = [
    { label: 'Jan', value: 12 },
    { label: 'Feb', value: 19 },
    { label: 'Mar', value: 15 },
    { label: 'Apr', value: 22 },
    { label: 'May', value: 18 },
    { label: 'Jun', value: 25 }
  ];

  return (
    <div className="container mx-auto p-4 sm:p-6 lg:p-8">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">
          Welcome, {user?.username || 'Shujaa'}! 🇰🇪
        </h1>
        <p className="text-lg text-gray-600">Your Shujaa Studio Dashboard</p>
      </div>

      {/* Enterprise Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card className="p-6 bg-gradient-to-br from-kenya-green/10 to-cultural-gold/10 border-kenya-green/20">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Your Plan</p>
              <p className="text-2xl font-bold text-gray-900">{planStatus?.planName || 'None'}</p>
              <p className="text-xs text-gray-500">Status: {planStatus?.state || 'Unknown'}</p>
            </div>
            <FaCreditCard className="text-3xl text-kenya-green" />
          </div>
        </Card>
        
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Video Minutes</p>
              <p className="text-2xl font-bold text-gray-900">{planStatus?.usage.videoMins || 0}/{planStatus?.quota.videoMins || 0}</p>
              <p className="text-xs text-gray-500">{Math.round(((planStatus?.usage.videoMins || 0) / (planStatus?.quota.videoMins || 1)) * 100)}% used</p>
            </div>
            <FaVideo className="text-3xl text-blue-600" />
          </div>
        </Card>
        
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Projects</p>
              <p className="text-2xl font-bold text-gray-900">{projects.length}</p>
              <p className="text-xs text-gray-500">Recent projects</p>
            </div>
            <FaChartLine className="text-3xl text-purple-600" />
          </div>
        </Card>
        
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Account Status</p>
              <p className="text-2xl font-bold text-gray-900">{planStatus?.state === 'healthy' ? 'Healthy' : 'Check Required'}</p>
              <p className="text-xs text-gray-500">{planStatus?.expiresAt ? `Expires: ${new Date(planStatus.expiresAt).toLocaleDateString()}` : 'No expiry date'}</p>
            </div>
            <FaCog className="text-3xl text-teal-600" />
          </div>
        </Card>
      </div>

      {/* Analytics Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
            <FaChartLine className="mr-2 text-kenya-green" /> Resource Usage 🦁
          </h3>
          <BarChart 
            data={usageData}
            className="h-64"
            variant="kenya"
          />
        </Card>
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
            <FaVideo className="mr-2 text-blue-600" /> Monthly Growth 🏃‍♂️
          </h3>
          <LineChart 
            data={monthlyData}
            className="h-64"
            variant="kenya"
          />
        </Card>
      </div>

      {/* Recent Projects */}
      <section className="bg-white shadow-lg rounded-lg p-6 mb-8">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center">
          <FaVideo className="mr-3 text-blue-600" /> Your Recent Projects
        </h2>
        {projectsLoading ? (
          <LoadingStates.LoadingCard />
        ) : projectsError ? (
          <ErrorStates.Alert 
            title="Projects Error"
            message={`Failed to load projects: ${projectsError}`}
            variant="default"
          />
        ) : projects.length === 0 ? (
          <ErrorStates.EmptyState 
            title="No Projects Yet"
            message="You haven't created any projects yet. 🎬"
            action={{
              label: "Start Creating Now!",
              onClick: () => window.location.href = '/video-generate'
            }}
            icon={<FaVideo className="text-5xl text-gray-300" />}
          />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {projects.map((project) => (
              <Card key={project.id} className="p-4 flex flex-col justify-between">
                <div>
                  <div className="flex items-center mb-2">
                    {project.type === 'video' && <FaVideo className="text-blue-500 mr-2" />}
                    {project.type === 'image' && <FaImage className="text-purple-500 mr-2" />}
                    {project.type === 'audio' && <FaMusic className="text-orange-500 mr-2" />}
                    <h3 className="font-semibold text-gray-800">{project.name}</h3>
                  </div>
                  <p className="text-sm text-gray-600 mb-1">Status: {project.status}</p>
                  <p className="text-xs text-gray-500">Created: {new Date(project.created_at).toLocaleDateString()}</p>
                </div>
                <Link href={`/projects/${project.id}`} className="text-blue-600 hover:underline mt-3 inline-block self-end">
                  View Details
                </Link>
              </Card>
            ))}
          </div>
        )}
        <div className="text-right mt-4">
          <Link href="/projects" className="text-blue-600 hover:underline inline-block">
            View All Projects
          </Link>
        </div>
      </section>

      {/* Quick Links */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card className="p-6 flex flex-col items-center text-center">
          <FaCog className="text-5xl text-purple-600 mb-4" />
          <h3 className="text-xl font-semibold text-gray-800 mb-2">Account Settings</h3>
          <p className="text-gray-600 mb-4">Manage your profile, security, and preferences.</p>
          <Link href="/profile" className="btn-primary">
            Go to Settings
          </Link>
        </Card>

        <Card className="p-6 flex flex-col items-center text-center">
          <FaChartLine className="text-5xl text-teal-600 mb-4" />
          <h3 className="text-xl font-semibold text-gray-800 mb-2">Usage & Analytics</h3>
          <p className="text-gray-600 mb-4">Monitor your resource consumption and performance.</p>
          <Link href="/usage" className="btn-primary">
            View Analytics
          </Link>
        </Card>

        <Card className="p-6 flex flex-col items-center text-center">
          <FaVideo className="text-5xl text-orange-600 mb-4" />
          <h3 className="text-xl font-semibold text-gray-800 mb-2">Start New Video</h3>
          <p className="text-gray-600 mb-4">Jump directly into creating your next masterpiece.</p>
          <Link href="/video-generate" className="btn-primary">
            Create Video
          </Link>
        </Card>
      </section>
    </div>
  );
}

