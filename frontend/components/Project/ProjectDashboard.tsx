// frontend/components/Project/ProjectDashboard.tsx (Conceptual)

import React, { useState, useEffect } 'react';
import axios from 'axios';
import { useRouter } from 'next/router';

interface Project {
  id: string;
  title: string;
  thumbnail_url: string;
  created_at: string;
  duration: string;
  status: string;
  rendered_output_path: string; // Link to the actual video file
}

const ProjectDashboard: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const getAuthHeaders = () => {
    const token = localStorage.getItem('jwt_token');
    if (!token) {
      router.push('/login');
      return {};
    }
    return { Authorization: `Bearer ${token}` };
  };

  useEffect(() => {
    const fetchProjects = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const headers = getAuthHeaders();
        if (!headers.Authorization) return;

        // Conceptual API endpoint for fetching user projects
        const response = await axios.get('http://localhost:8000/projects/me', { headers });
        setProjects(response.data);

      } catch (err: any) {
        if (err.response && err.response.data && err.response.data.detail) {
          setError(err.response.data.detail);
        } else {
          setError('Failed to load projects. Please try again.');
        }
        console.error('Project fetch error:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProjects();
  }, []);

  if (isLoading) {
    return (
      <div className="elite-container my-10 text-center">
        <div className="loading-spinner mx-auto mb-4"></div>
        <p className="text-soft-text">Loading projects...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="elite-container my-10 text-center text-red-500">
        <p>Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="elite-container my-10">
      <h1 className="section-title text-center mb-8">My Video Projects</h1>

      {projects.length === 0 ? (
        <div className="text-center text-soft-text">
          <p className="mb-4">You haven't generated any videos yet.</p>
          <button onClick={() => router.push('/create-video')} className="btn-primary px-6 py-3 rounded-lg">
            Create Your First Video
          </button>
        </div>
      ) : (
        <div className="responsive-grid">
          {projects.map((project) => (
            <div key={project.id} className="elite-card p-4 rounded-lg">
              <img src={project.thumbnail_url || '/placeholder-thumbnail.png'} alt={project.title} className="w-full h-40 object-cover rounded-md mb-3" />
              <h3 className="section-subtitle mb-1 text-charcoal font-semibold">{project.title}</h3>
              <p className="text-soft-text text-sm mb-2">Status: {project.status}</p>
              <p className="text-soft-text text-sm mb-3">Created: {new Date(project.created_at).toLocaleDateString()}</p>
              <div className="flex justify-between items-center">
                <a 
                  href={project.rendered_output_path} 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="btn-primary px-4 py-2 rounded-lg text-white text-sm"
                >
                  View
                </a>
                {/* Add more actions like Download, Delete */}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Conceptual Pagination */}
      {projects.length > 0 && (
        <div className="pagination-container mt-8">
          <p className="pagination-info">Showing 1-10 of {projects.length} projects</p>
          <div className="pagination-controls">
            <button className="pagination-btn" disabled>Previous</button>
            <button className="pagination-btn">1</button>
            <button className="pagination-btn">2</button>
            <button className="pagination-btn">Next</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProjectDashboard;