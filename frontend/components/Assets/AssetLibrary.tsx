// frontend/components/Assets/AssetLibrary.tsx (Conceptual)

import React, { useState, useEffect } 'react';
import axios from 'axios';
import { useRouter } from 'next/router';

interface Asset {
  id: string;
  name: string;
  type: 'image' | 'audio' | 'model';
  url: string; // URL to the asset file
  thumbnail_url?: string; // URL to a thumbnail image
  size: number; // Size in bytes
  uploaded_at: string;
  usage_count: number; // How many times this asset has been used in videos
}

const AssetLibrary: React.FC = () => {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterType, setFilterType] = useState('all'); // 'all', 'image', 'audio', 'model'
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
    const fetchAssets = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const headers = getAuthHeaders();
        if (!headers.Authorization) return;

        // Conceptual API endpoint for fetching user assets
        const response = await axios.get('http://localhost:8000/assets/me', { 
          headers,
          params: { type: filterType === 'all' ? undefined : filterType } // Pass filter to API
        });
        setAssets(response.data);

      } catch (err: any) {
        if (err.response && err.response.data && err.response.data.detail) {
          setError(err.response.data.detail);
        } else {
          setError('Failed to load assets. Please try again.');
        }
        console.error('Asset fetch error:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchAssets();
  }, [filterType]); // Refetch when filterType changes

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);
    // You might also append asset type, name, etc.

    try {
      const headers = getAuthHeaders();
      if (!headers.Authorization) return;

      // Conceptual API endpoint for uploading assets
      const response = await axios.post('http://localhost:8000/assets/upload', formData, {
        headers: {
          ...headers,
          'Content-Type': 'multipart/form-data', // Important for file uploads
        },
      });

      if (response.status === 200) {
        // Assuming API returns the new asset data
        setAssets((prevAssets) => [...prevAssets, response.data]);
        alert('Asset uploaded successfully!');
      }

    } catch (err: any) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('An unexpected error occurred during upload. Please try again.');
      }
      console.error('Asset upload error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="elite-container my-10 text-center">
        <div className="loading-spinner mx-auto mb-4"></div>
        <p className="text-soft-text">Loading assets...</p>
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
      <h1 className="section-title text-center mb-8">My Asset Library</h1>

      <div className="flex justify-between items-center mb-6">
        <div>
          <label htmlFor="asset-filter" className="text-soft-text text-sm font-medium mr-2">Filter by Type:</label>
          <select 
            id="asset-filter" 
            className="form-input p-2 rounded-lg" 
            value={filterType} 
            onChange={(e) => setFilterType(e.target.value)}
          >
            <option value="all">All</option>
            <option value="image">Images</option>
            <option value="audio">Audio</option>
            <option value="model">Models</option>
          </select>
        </div>
        <div>
          <label htmlFor="file-upload" className="btn-primary px-4 py-2 rounded-lg cursor-pointer">
            Upload New Asset
          </label>
          <input 
            id="file-upload" 
            type="file" 
            className="hidden" 
            onChange={handleFileUpload} 
          />
        </div>
      </div>

      {assets.length === 0 ? (
        <div className="text-center text-soft-text">
          <p>No assets found in your library. Upload one to get started!</p>
        </div>
      ) : (
        <div className="responsive-grid">
          {assets.map((asset) => (
            <div key={asset.id} className="elite-card p-4 rounded-lg">
              {asset.type === 'image' && (
                <img src={asset.thumbnail_url || asset.url} alt={asset.name} className="w-full h-32 object-cover rounded-md mb-3" />
              )}
              {asset.type === 'audio' && (
                <div className="w-full h-32 flex items-center justify-center bg-gray-100 rounded-md mb-3">
                  <span className="text-soft-text text-4xl">🎵</span>
                </div>
              )}
              {asset.type === 'model' && (
                <div className="w-full h-32 flex items-center justify-center bg-gray-100 rounded-md mb-3">
                  <span className="text-soft-text text-4xl">📦</span>
                </div>
              )}
              <h3 className="section-subtitle mb-1 text-charcoal font-semibold">{asset.name}</h3>
              <p className="text-soft-text text-sm">Type: {asset.type}</p>
              <p className="text-soft-text text-sm">Size: {(asset.size / 1024 / 1024).toFixed(2)} MB</p>
              <p className="text-soft-text text-sm mb-3">Used: {asset.usage_count} times</p>
              <div className="flex justify-between items-center">
                <a 
                  href={asset.url} 
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
      {assets.length > 0 && (
        <div className="pagination-container mt-8">
          <p className="pagination-info">Showing 1-10 of {assets.length} assets</p>
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

export default AssetLibrary;