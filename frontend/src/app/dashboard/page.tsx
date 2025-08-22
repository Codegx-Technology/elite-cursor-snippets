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
import { FaVideo, FaCreditCard, FaCog, FaChartLine } from 'react-icons/fa';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import type { PlanStatus } from '@/widgets/PlanGuardWidget/types';
import { apiClient, Project } from '@/lib/api'; // New imports

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
      } catch (err: any) {
        setProjectsError(err.message || 'Failed to fetch projects.');
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
        <p className="text-gray-600">Loading dashboard data...</p>
      </div>
    );
  }

  if (planError) {
    return (
      <div className="flex justify-center items-center min-h-screen-content">
        <p className="text-red-600">Error loading plan information: {planError}</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 sm:p-6 lg:p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">
        Welcome, {user?.username || 'Shujaa'}!
      </h1>

      {/* PlanGuard Overview */}
      <section className="bg-white shadow-lg rounded-lg p-6 mb-8">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center">
          <FaCreditCard className="mr-3 text-green-600" /> Your Plan Overview
        </h2>
        {planStatus ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-gray-700 text-lg">
                Current Plan: <span className="font-bold text-green-700">{planStatus.planName}</span>
              </p>
              <p className="text-gray-600">
                Status: <Badge variant={getPlanStateVariant(planStatus.state)}>{planStatus.state}</Badge>
              </p>
              <p className="text-gray-600">
                Expires: <span className="font-medium">{planStatus.expiresAt ? new Date(planStatus.expiresAt).toLocaleDateString() : 'N/A'}</span>
              </p>
            </div>
            <div>
              <p className="text-gray-700 text-lg mb-2">
                Video Minutes Used: <span className="font-bold">{planStatus.usage.videoMins} / {planStatus.quota.videoMins}</span>
              </p>
              <Progress value={(planStatus.usage.videoMins / planStatus.quota.videoMins) * 100} className="h-2 mb-4" />
              <Button asChild className="mt-2">
                <Link href="/pricing">
                  Upgrade Your Plan
                </Link>
              </Button>
            </div>
          </div>
        ) : (
          <p className="text-gray-600">No plan information available. Please check your subscription.</p>
        )}
      </section>

      {/* Recent Projects */}
      <section className="bg-white shadow-lg rounded-lg p-6 mb-8">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center">
          <FaVideo className="mr-3 text-blue-600" /> Your Recent Projects
        </h2>
        {projectsLoading ? (
          <p className="text-gray-600">Loading recent projects...</p>
        ) : projectsError ? (
          <p className="text-red-600">Error loading projects: {projectsError}</p>
        ) : projects.length === 0 ? (
          <div className="border border-gray-200 rounded-lg p-4 text-center">
            <FaVideo className="text-5xl text-gray-300 mx-auto mb-3" />
            <p className="text-gray-500">No recent projects yet.</p>
            <Link href="/video-generate" className="text-green-600 hover:underline mt-2 inline-block">
              Start Creating Now!
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {projects.map((project) => (
              <div key={project.id} className="border border-gray-200 rounded-lg p-4">
                <h3 className="font-semibold text-gray-800 mb-2">{project.name}</h3>
                <p className="text-sm text-gray-600 mb-2">Type: {project.type}</p>
                <p className="text-sm text-gray-600 mb-2">Status: {project.status}</p>
                <p className="text-xs text-gray-500">Created: {new Date(project.created_at).toLocaleDateString()}</p>
                <Link href={`/projects/${project.id}`} className="text-blue-600 hover:underline mt-2 inline-block">
                  View Project
                </Link>
              </div>
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
        <div className="bg-white shadow-lg rounded-lg p-6 flex flex-col items-center text-center">
          <FaCog className="text-5xl text-purple-600 mb-4" />
          <h3 className="text-xl font-semibold text-gray-800 mb-2">Account Settings</h3>
          <p className="text-gray-600 mb-4">Manage your profile, security, and preferences.</p>
          <Link href="/profile" className="btn-primary">
            Go to Settings
          </Link>
        </div>

        <div className="bg-white shadow-lg rounded-lg p-6 flex flex-col items-center text-center">
          <FaChartLine className="text-5xl text-teal-600 mb-4" />
          <h3 className="text-xl font-semibold text-gray-800 mb-2">Usage & Analytics</h3>
          <p className="text-gray-600 mb-4">Monitor your resource consumption and performance.</p>
          <Link href="/usage" className="btn-primary">
            View Analytics
          </Link>
        </div>

        <div className="bg-white shadow-lg rounded-lg p-6 flex flex-col items-center text-center">
          <FaVideo className="text-5xl text-orange-600 mb-4" />
          <h3 className="text-xl font-semibold text-gray-800 mb-2">Start New Video</h3>
          <p className="text-gray-600 mb-4">Jump directly into creating your next masterpiece.</p>
          <Link href="/video-generate" className="btn-primary">
            Create Video
          </Link>
        </div>
      </section>
    </div>
  );
}