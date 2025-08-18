'use client';

import { useState, useEffect } from 'react';
import Card from '@/components/Card';
import Pagination from '@/components/Pagination';
import { FaPlus, FaVideo, FaImages, FaMusic, FaEllipsisV, FaEdit, FaTrash, FaEye, FaFlag, FaMountain, FaFolder, FaClock, FaExclamationTriangle, FaSpinner } from 'react-icons/fa';
import { apiClient, handleApiResponse } from '@/lib/api';
import { device } from '@/lib/utils';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean + augmentsearch
// [CONTEXT]: Enterprise-grade projects page with Kenya-first design and real backend integration
// [GOAL]: Create comprehensive project management interface with pagination and real data
// [TASK]: Implement projects with proper CRUD operations, pagination, and mobile responsiveness

interface Project {
  id: string;
  name: string;
  description?: string;
  type: 'video' | 'image' | 'audio';
  status: string;
  created_at: string;
  updated_at: string;
  items_count: number;
}

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalItems, setTotalItems] = useState(0);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  // Mobile detection
  const [isMobile, setIsMobile] = useState(false);
  const itemsPerPage = isMobile ? 3 : 6; // 3 on mobile, 6 on desktop

  useEffect(() => {
    setIsMobile(device.isMobile());
  }, []);

  useEffect(() => {
    loadProjects();
  }, [currentPage, itemsPerPage]);

  const loadProjects = async () => {
    setIsLoading(true);
    setError(null);

    const response = await apiClient.getProjects(currentPage, itemsPerPage);
    handleApiResponse(
      response,
      (data) => {
        setProjects(data.projects);
        setTotalPages(data.pages);
        setTotalItems(data.total);
      },
      (error) => setError(error)
    );

    setIsLoading(false);
  };

  const handlePageChange = (page: number) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  const getProjectIcon = (type: string) => {
    switch (type) {
      case 'video': return <FaVideo className="text-blue-600" />;
      case 'image': return <FaImages className="text-green-600" />;
      case 'audio': return <FaMusic className="text-purple-600" />;
      default: return <FaFolder className="text-gray-600" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'completed': return 'bg-blue-100 text-blue-800';
      case 'archived': return 'bg-gray-100 text-gray-800';
      default: return 'bg-yellow-100 text-yellow-800';
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <FaSpinner className="w-8 h-8 text-green-600 animate-spin mx-auto mb-4" />
          <span className="text-gray-600 font-medium">Loading projects...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Kenya-First Header */}
      <div className="bg-gradient-to-r from-green-600 via-red-600 to-black p-6 rounded-xl text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <FaFolder className="text-3xl" />
            <div>
              <h1 className="text-2xl font-bold">Projects 🇰🇪</h1>
              <p className="text-green-100">Manage your Kenya-first creative projects</p>
            </div>
          </div>
          <div className="hidden md:block">
            <FaMountain className="text-4xl text-yellow-300" />
          </div>
        </div>
      </div>

      {/* Action Bar */}
      <Card className="p-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between space-y-4 sm:space-y-0">
          <div>
            <h2 className="text-xl font-bold text-gray-800">Your Projects</h2>
            <p className="text-gray-600">Create and manage your content projects</p>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors duration-200"
          >
            <FaPlus />
            <span>New Project</span>
          </button>
        </div>
      </Card>

      {/* Projects Grid */}
      {error ? (
        <Card className="p-8 text-center">
          <div className="text-red-600 mb-4">
            <FaExclamationTriangle className="text-4xl mx-auto mb-2" />
            <p className="font-medium">Unable to load projects</p>
            <p className="text-sm text-gray-600 mt-2">{error}</p>
          </div>
          <button
            onClick={loadProjects}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors duration-200"
          >
            Try Again
          </button>
        </Card>
      ) : projects.length === 0 ? (
        <Card className="p-8 text-center">
          <div className="text-gray-500 mb-4">
            <FaFolder className="text-4xl mx-auto mb-2" />
            <p className="font-medium">No projects yet</p>
            <p className="text-sm mt-2">Create your first Kenya-first content project!</p>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors duration-200"
          >
            Create Project
          </button>
        </Card>
      ) : (
        <>
          <div className={`grid gap-6 ${
            isMobile
              ? 'grid-cols-1'
              : 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3'
          }`}>
            {projects.map((project) => (
              <Card key={project.id} className="overflow-hidden hover:shadow-lg transition-shadow duration-200">
                <div className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className="bg-gray-100 p-2 rounded-lg">
                        {getProjectIcon(project.type)}
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-800 line-clamp-1">{project.name}</h3>
                        <p className="text-sm text-gray-500 capitalize">{project.type} project</p>
                      </div>
                    </div>
                    <div className="relative">
                      <button className="p-2 text-gray-400 hover:text-gray-600 transition-colors duration-200">
                        <FaEllipsisV />
                      </button>
                    </div>
                  </div>

                  {project.description && (
                    <p className="text-gray-600 text-sm mb-4 line-clamp-2">{project.description}</p>
                  )}

                  <div className="flex items-center justify-between mb-4">
                    <span className={`px-2 py-1 text-xs rounded-full font-medium ${getStatusColor(project.status)}`}>
                      {project.status}
                    </span>
                    <span className="text-sm text-gray-500">
                      {project.items_count} items
                    </span>
                  </div>

                  <div className="flex items-center justify-between text-sm text-gray-500">
                    <div className="flex items-center space-x-1">
                      <FaClock className="text-xs" />
                      <span>Updated {new Date(project.updated_at).toLocaleDateString()}</span>
                    </div>
                  </div>

                  <div className="flex space-x-2 mt-4">
                    <button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-lg text-sm transition-colors duration-200 flex items-center justify-center space-x-1">
                      <FaEye className="text-xs" />
                      <span>View</span>
                    </button>
                    <button className="flex-1 bg-gray-600 hover:bg-gray-700 text-white px-3 py-2 rounded-lg text-sm transition-colors duration-200 flex items-center justify-center space-x-1">
                      <FaEdit className="text-xs" />
                      <span>Edit</span>
                    </button>
                  </div>
                </div>
              </Card>
            ))}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <Card className="p-6">
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                totalItems={totalItems}
                itemsPerPage={itemsPerPage}
                onPageChange={handlePageChange}
              />
            </Card>
          )}
        </>
      )}

      {/* Cultural Footer */}
      <div className="bg-gradient-to-r from-yellow-400 via-red-500 to-green-600 p-4 rounded-lg text-white text-center">
        <div className="flex items-center justify-center space-x-2">
          <FaFlag className="text-lg" />
          <span className="font-medium">Building Kenya-first content projects • Harambee spirit</span>
          <FaFolder className="text-lg" />
        </div>
      </div>
    </div>
  );
}