import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';

interface StorageInfo {
  total_space_gb: number;
  used_space_gb: number;
  free_space_gb: number;
  cache_size_gb: number;
  project_data_size_gb: number;
  log_data_size_gb: number;
}

const StorageManagementPage: React.FC = () => { // Renamed to StorageManagementPage
  const [storageInfo, setStorageInfo] = useState<StorageInfo | null>(null);
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
    const fetchStorageInfo = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const headers = getAuthHeaders();
        if (!headers.Authorization) return;

        // Conceptual API endpoint for fetching storage information
        const response = await axios.get('http://localhost:8000/storage/info', { headers });
        setStorageInfo(response.data);

      } catch (err: any) {
        if (err.response && err.response.data && err.response.data.detail) {
          setError(err.response.data.detail);
        } else {
          setError('Failed to load storage information. Please try again.');
        }
        console.error('Storage info fetch error:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchStorageInfo();
  }, []);

  const handleClearCache = async () => {
    if (!confirm('Are you sure you want to clear the cache? This cannot be undone.')) return;

    setIsLoading(true);
    setError(null);
    try {
      const headers = getAuthHeaders();
      if (!headers.Authorization) return;

      // Conceptual API endpoint to clear cache
      await axios.post('http://localhost:8000/storage/clear-cache', {}, { headers });
      alert('Cache cleared successfully!');
      // Refetch storage info to update display
      await fetchStorageInfo();
    } catch (err: any) {
      setError('Failed to clear cache.');
      console.error('Clear cache error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="elite-container my-10 text-center">
        <div className="loading-spinner mx-auto mb-4"></div>
        <p className="text-soft-text">Loading storage information...</p>
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

  if (!storageInfo) {
    return <div className="elite-container my-10 text-center text-soft-text">No storage information available.</div>;
  }

  const usedPercentage = (storageInfo.used_space_gb / storageInfo.total_space_gb) * 100;

  return (
    <div className="elite-container my-10">
      <h1 className="section-title text-center mb-8">Storage Management</h1>

      <div className="elite-card p-8 max-w-2xl mx-auto my-10 rounded-xl shadow-lg">
        <h3 className="section-subtitle mb-4">Storage Overview</h3>
        
        <div className="mb-4">
          <p className="text-soft-text text-sm mb-2">Total Space: <span className="font-semibold text-charcoal">{storageInfo.total_space_gb.toFixed(2)} GB</span></p>
          <p className="text-soft-text text-sm mb-2">Used Space: <span className="font-semibold text-charcoal">{storageInfo.used_space_gb.toFixed(2)} GB</span></p>
          <p className="text-soft-text text-sm mb-2">Free Space: <span className="font-semibold text-charcoal">{storageInfo.free_space_gb.toFixed(2)} GB</span></p>
        </div>

        <div className="w-full bg-gray-200 rounded-full h-4 mb-4">
          <div 
            className="bg-primary-gradient h-4 rounded-full" 
            style={{ width: `${usedPercentage}%` }} 
          ></div>
        </div>
        <p className="text-soft-text text-sm text-right mb-6">{usedPercentage.toFixed(1)}% Used</p>

        <h3 className="section-subtitle mb-4">Breakdown</h3>
        <ul className="list-disc pl-5 text-soft-text mb-6">
          <li>Cache Size: {storageInfo.cache_size_gb.toFixed(2)} GB</li>
          <li>Project Data Size: {storageInfo.project_data_size_gb.toFixed(2)} GB</li>
          <li>Log Data Size: {storageInfo.log_data_size_gb.toFixed(2)} GB</li>
        </ul>

        <div className="flex justify-center">
          <button 
            onClick={handleClearCache} 
            className="btn-primary px-6 py-3 rounded-lg text-white font-semibold"
          >
            Clear Cache
          </button>
        </div>
      </div>
    </div>
  );
};

export default StorageManagementPage; // Export as default for page component