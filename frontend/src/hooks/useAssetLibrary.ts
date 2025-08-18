
import { useState, useEffect } from 'react';
import { apiClient, handleApiResponse } from '@/lib/api';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Custom hook for managing enterprise-grade asset library state and logic
// [GOAL]: Encapsulate asset management complexity and provide a clean interface for UI components

export interface Asset {
  id: string;
  name: string;
  type: 'image' | 'audio' | 'model';
  url: string;
  thumbnail_url?: string;
  size: number;
  uploaded_at: string;
  usage_count: number;
}

export function useAssetLibrary() {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterType, setFilterType] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalItems, setTotalItems] = useState(0);
  const itemsPerPage = 10;

  useEffect(() => {
    loadAssets();
  }, [currentPage, filterType]);

  const loadAssets = async () => {
    setIsLoading(true);
    setError(null);

    const response = await apiClient.getAssets(currentPage, itemsPerPage, filterType === 'all' ? undefined : filterType);
    handleApiResponse(
      response,
      (data) => {
        setAssets(data.assets);
        setTotalPages(data.pages);
        setTotalItems(data.total);
      },
      (error) => setError(error)
    );

    setIsLoading(false);
  };

  const uploadAsset = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiClient.uploadAsset(formData);
    handleApiResponse(
      response,
      () => {
        loadAssets();
      },
      (error) => setError(error)
    );
  };

  const deleteAsset = async (id: string) => {
    const response = await apiClient.deleteAsset(id);
    handleApiResponse(
      response,
      () => {
        loadAssets();
      },
      (error) => setError(error)
    );
  };

  const handlePageChange = (page: number) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  const handleFilterChange = (type: string) => {
    setFilterType(type);
    setCurrentPage(1);
  };

  return {
    assets,
    isLoading,
    error,
    currentPage,
    totalPages,
    totalItems,
    itemsPerPage,
    filterType,
    loadAssets,
    uploadAsset,
    deleteAsset,
    handlePageChange,
    handleFilterChange
  };
}
