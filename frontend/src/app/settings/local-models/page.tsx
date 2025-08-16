import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';

interface LocalModel {
  id: string;
  name: string;
  type: 'llm' | 'image_gen' | 'tts' | 'stt';
  version: string;
  size_gb: number;
  status: 'installed' | 'downloading' | 'available';
  download_progress?: number; // 0-100
}

const LocalModels: React.FC = () => {
  const [models, setModels] = useState<LocalModel[]>([]);
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
    const fetchModels = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const headers = getAuthHeaders();
        if (!headers.Authorization) return;

        // Conceptual API endpoint for fetching local models
        const response = await axios.get('http://localhost:8000/models/local', { headers });
        setModels(response.data);

      } catch (err: any) {
        if (err.response && err.response.data && err.response.data.detail) {
          setError(err.response.data.detail);
        } else {
          setError('Failed to load local models. Please try again.');
        }
        console.error('Local models fetch error:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchModels();
  }, []);

  const handleDownload = async (modelId: string) => {
    // Simulate download process
    setModels((prev) =>
      prev.map((m) => (m.id === modelId ? { ...m, status: 'downloading', download_progress: 0 } : m))
    );

    try {
      const headers = getAuthHeaders();
      if (!headers.Authorization) return;

      // Conceptual API endpoint to initiate model download
      await axios.post(`http://localhost:8000/models/local/${modelId}/download`, {}, { headers });

      // Simulate progress (in a real app, this would be via websockets or polling)
      let progress = 0;
      const interval = setInterval(() => {
        progress += 10;
        if (progress <= 100) {
          setModels((prev) =>
            prev.map((m) => (m.id === modelId ? { ...m, download_progress: progress } : m))
          );
        } else {
          clearInterval(interval);
          setModels((prev) =>
            prev.map((m) => (m.id === modelId ? { ...m, status: 'installed', download_progress: undefined } : m))
          );
        }
      }, 200);

    } catch (err: any) {
      setError('Failed to initiate download.');
      setModels((prev) =>
        prev.map((m) => (m.id === modelId ? { ...m, status: 'available', download_progress: undefined } : m))
      );
      console.error('Download initiation error:', err);
    }
  };

  const handleDelete = async (modelId: string) => {
    if (!confirm('Are you sure you want to delete this model?')) return;

    try {
      const headers = getAuthHeaders();
      if (!headers.Authorization) return;

      // Conceptual API endpoint to delete a local model
      await axios.delete(`http://localhost:8000/models/local/${modelId}`, { headers });
      setModels((prev) => prev.filter((m) => m.id !== modelId));
      alert('Model deleted successfully!');
    } catch (err: any) {
      setError('Failed to delete model.');
      console.error('Delete model error:', err);
    }
  };

  if (isLoading) {
    return (
      <div className="elite-container my-10 text-center">
        <div className="loading-spinner mx-auto mb-4"></div>
        <p className="text-soft-text">Loading local models...</p>
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
      <h1 className="section-title text-center mb-8">Local AI Models</h1>

      {models.length === 0 ? (
        <div className="text-center text-soft-text">
          <p>No local models found or configured.</p>
        </div>
      ) : (
        <div className="responsive-grid">
          {models.map((model) => (
            <div key={model.id} className="elite-card p-4 rounded-lg">
              <h3 className="section-subtitle mb-1 text-charcoal font-semibold">{model.name}</h3>
              <p className="text-soft-text text-sm">Type: {model.type.toUpperCase()}</p>
              <p className="text-soft-text text-sm">Version: {model.version}</p>
              <p className="text-soft-text text-sm">Size: {model.size_gb} GB</p>
              <p className="text-soft-text text-sm mb-3">Status: {model.status}</p>

              {model.status === 'downloading' && (
                <div className="w-full bg-gray-200 rounded-full h-2.5 mb-3">
                  <div 
                    className="bg-primary-gradient h-2.5 rounded-full" 
                    style={{ width: `${model.download_progress || 0}%` }} 
                  ></div>
                  <p className="text-xs text-soft-text text-right mt-1">{model.download_progress || 0}%</p>
                </div>
              )}

              <div className="flex justify-between items-center mt-4">
                {model.status === 'available' && (
                  <button 
                    onClick={() => handleDownload(model.id)} 
                    className="btn-primary px-4 py-2 rounded-lg text-white text-sm"
                  >
                    Download
                  </button>
                )}
                {model.status === 'installed' && (
                  <button 
                    onClick={() => handleDelete(model.id)} 
                    className="btn-secondary px-4 py-2 rounded-lg text-sm"
                  >
                    Delete
                  </button>
                )}
                {model.status === 'downloading' && (
                  <button 
                    className="btn-secondary px-4 py-2 rounded-lg text-sm" 
                    disabled
                  >
                    Downloading...
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default LocalModels;