'use client';

import { useState } from 'react';
import Card from '@/components/Card';
import Pagination from '@/components/Pagination';
import LoadingStates from '@/components/ui/LoadingStates';
import ErrorStates from '@/components/ui/ErrorStates';
import { FaPlus, FaVideo, FaImages, FaMusic, FaEdit, FaTrash, FaEye, FaFlag, FaMountain, FaFolder, FaClock, FaExclamationTriangle, FaSpinner } from 'react-icons/fa6';
import { useProjects, Project } from '@/hooks/useProjects';
import CreateProjectModal from '@/components/Project/CreateProjectModal';
import EditProjectModal from '@/components/Project/EditProjectModal';
import DeleteProjectModal from '@/components/Project/DeleteProjectModal';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean + augmentsearch
// [CONTEXT]: Enterprise-grade projects page with Kenya-first design and real backend integration
// [GOAL]: Create comprehensive project management interface with pagination and real data
// [TASK]: Implement projects with proper CRUD operations, pagination, and mobile responsiveness

export default function ProjectsPage() {
  const { projects, isLoading, error, currentPage, totalPages, totalItems, itemsPerPage, loadProjects, createProject, updateProject, deleteProject, handlePageChange } = useProjects();
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);

  const handleCreateProject = async (project: { name: string; description: string; type: 'video' | 'image' | 'audio'; }) => {
    await createProject({ ...project, status: 'active' });
    setShowCreateModal(false);
  };

  const handleUpdateProject = async (id: string, project: Partial<Project>) => {
    await updateProject(id, project);
    setShowEditModal(false);
  };

  const handleDeleteProject = async (id: string) => {
    await deleteProject(id);
    setShowDeleteModal(false);
  };

  const openEditModal = (project: Project) => {
    setSelectedProject(project);
    setShowEditModal(true);
  };

  const openDeleteModal = (project: Project) => {
    setSelectedProject(project);
    setShowDeleteModal(true);
  };

  const getProjectIcon = (type: string) => {
    switch (type) {
      case 'video': return <FaVideo className="text-blue-600" aria-label="Video Project" />;
      case 'image': return <FaImages className="text-green-600" aria-label="Image Project" />;
      case 'audio': return <FaMusic className="text-purple-600" aria-label="Audio Project" />;
      default: return <FaFolder className="text-gray-600" aria-label="Folder Icon" />;
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
    return <LoadingStates.PageLoading message="Loading your Kenya-first projects... 🦒" />;
  }

  if (error) {
    return (
      <ErrorStates.ErrorPage
        type="network-error"
        variant="kenya"
        customTitle="Projects Unavailable 🦁"
        customMessage="Unable to load your projects. Please check your connection and try again."
        onRetry={() => loadProjects()}
      />
    );
  }

  return (
    <div className="space-y-6">
      {/* Modals */}
      <CreateProjectModal isOpen={showCreateModal} onClose={() => setShowCreateModal(false)} onCreate={handleCreateProject} />
      <EditProjectModal isOpen={showEditModal} onClose={() => setShowEditModal(false)} onUpdate={handleUpdateProject} project={selectedProject} />
      <DeleteProjectModal isOpen={showDeleteModal} onClose={() => setShowDeleteModal(false)} onDelete={handleDeleteProject} project={selectedProject} />

      {/* Kenya-First Header */}
      <div className="bg-gradient-to-r from-green-600 via-red-600 to-black p-6 rounded-xl text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <FaFolder className="text-3xl" aria-label="Folder Icon" />
            <div>
              <h1 className="text-2xl font-bold">Projects 🇰🇪</h1>
              <p className="text-green-100">Manage your Kenya-first creative projects</p>
            </div>
          </div>
          <div className="hidden md:block">
            <FaMountain className="text-4xl text-yellow-300" aria-label="Mount Kenya" />
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
            <FaPlus aria-label="Add Icon" />
            <span>New Project</span>
          </button>
        </div>
      </Card>

      {/* Projects Grid */}
      {error ? (
        <Card className="p-8 text-center">
          <div className="text-red-600 mb-4">
            <FaExclamationTriangle className="text-4xl mx-auto mb-2" aria-label="Error Icon" />
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
            <FaFolder className="text-4xl mx-auto mb-2" aria-label="Folder Icon" />
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
          <div className={`grid gap-6 grid-cols-1 md:grid-cols-2 lg:grid-cols-3`}>
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
                      <button onClick={() => openDeleteModal(project)} className="p-2 text-gray-400 hover:text-gray-600 transition-colors duration-200">
                        <FaTrash aria-label="Delete Project" />
                      </button>
                      <button onClick={() => openEditModal(project)} className="p-2 text-gray-400 hover:text-gray-600 transition-colors duration-200">
                        <FaEdit aria-label="Edit Project" />
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
                      <FaClock className="text-xs" aria-label="Clock Icon" />
                      <span>Updated {new Date(project.updated_at).toLocaleDateString()}</span>
                    </div>
                  </div>

                  <div className="flex space-x-2 mt-4">
                    <button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-lg text-sm transition-colors duration-200 flex items-center justify-center space-x-1">
                      <FaEye className="text-xs" aria-label="View Project" />
                      <span>View</span>
                    </button>
                    <button onClick={() => openEditModal(project)} className="flex-1 bg-gray-600 hover:bg-gray-700 text-white px-3 py-2 rounded-lg text-sm transition-colors duration-200 flex items-center justify-center space-x-1">
                      <FaEdit className="text-xs" aria-label="Edit Project" />
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
          <FaFlag className="text-lg" aria-label="Kenyan Flag" />
          <span className="font-medium">Building Kenya-first content projects • Harambee spirit</span>
          <FaFolder className="text-lg" aria-label="Folder Icon" />
        </div>
      </div>
    </div>
  );
}
