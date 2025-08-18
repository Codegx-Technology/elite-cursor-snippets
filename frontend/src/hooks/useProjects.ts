
import { useState, useEffect } from 'react';
import { apiClient, handleApiResponse } from '@/lib/api';
import { device } from '@/lib/utils';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Custom hook for managing enterprise-grade project management state and logic
// [GOAL]: Encapsulate project CRUD complexity and provide a clean interface for UI components

export interface Project {
  id: string;
  name: string;
  description?: string;
  type: 'video' | 'image' | 'audio';
  status: string;
  created_at: string;
  updated_at: string;
  items_count: number;
}

export function useProjects() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalItems, setTotalItems] = useState(0);
  const [isMobile, setIsMobile] = useState(false);
  const itemsPerPage = isMobile ? 3 : 6;

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

  const createProject = async (project: Omit<Project, 'id' | 'created_at' | 'updated_at' | 'items_count'>) => {
    const response = await apiClient.createProject(project);
    handleApiResponse(
      response,
      () => {
        loadProjects();
      },
      (error) => setError(error)
    );
  };

  const updateProject = async (id: string, project: Partial<Project>) => {
    const response = await apiClient.updateProject(id, project);
    handleApiResponse(
      response,
      () => {
        loadProjects();
      },
      (error) => setError(error)
    );
  };

  const deleteProject = async (id: string) => {
    const response = await apiClient.deleteProject(id);
    handleApiResponse(
      response,
      () => {
        loadProjects();
      },
      (error) => setError(error)
    );
  };

  const handlePageChange = (page: number) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  return {
    projects,
    isLoading,
    error,
    currentPage,
    totalPages,
    totalItems,
    itemsPerPage,
    loadProjects,
    createProject,
    updateProject,
    deleteProject,
    handlePageChange
  };
}
