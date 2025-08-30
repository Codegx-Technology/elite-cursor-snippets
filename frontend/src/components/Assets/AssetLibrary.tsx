
import { useState } from 'react';
import { FaUpload, FaTrash, FaDownload, FaImage, FaMusic, FaBox, FaSpinner, FaExclamationTriangle } from 'react-icons/fa6';
import { useAssetLibrary, Asset } from '@/hooks/useAssetLibrary';
import DeleteAssetModal from './DeleteAssetModal';
import Pagination from '@/components/Pagination';
import Card from '@/components/Card';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean + augmentsearch
// [CONTEXT]: Enterprise-grade asset library with Kenya-first design and real backend integration
// [GOAL]: Create comprehensive asset management interface with filtering, pagination, and CRUD operations
// [TASK]: Implement asset library with proper API integration, file uploads, and mobile responsiveness

export default function AssetLibrary() {
  const { assets, isLoading, error, currentPage, totalPages, totalItems, itemsPerPage, filterType, loadAssets, uploadAsset, deleteAsset, handlePageChange, handleFilterChange } = useAssetLibrary();
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedAsset, setSelectedAsset] = useState<Asset | null>(null);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    await uploadAsset(file);
  };

  const openDeleteModal = (asset: Asset) => {
    setSelectedAsset(asset);
    setShowDeleteModal(true);
  };

  const handleDeleteAsset = async (id: string) => {
    await deleteAsset(id);
    setShowDeleteModal(false);
  };

  const getAssetIcon = (type: string) => {
    switch (type) {
      case 'image': return <FaImage className="text-green-600" aria-label="Image Asset" />;
      case 'audio': return <FaMusic className="text-purple-600" aria-label="Audio Asset" />;
      case 'model': return <FaBox className="text-blue-600" aria-label="Model Asset" />;
      default: return <FaImage className="text-gray-600" aria-label="Asset" />;
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <FaSpinner className="w-8 h-8 text-green-600 animate-spin mx-auto mb-4" aria-label="Loading" />
          <span className="text-gray-600 font-medium">Loading assets...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <DeleteAssetModal isOpen={showDeleteModal} onClose={() => setShowDeleteModal(false)} onDelete={handleDeleteAsset} asset={selectedAsset} />

      <h1 className="section-title text-center mb-8">My Asset Library</h1>

      <Card className="p-6">
        <div className="flex justify-between items-center mb-6">
          <div>
            <label htmlFor="asset-filter" className="text-soft-text text-sm font-medium mr-2">Filter by Type:</label>
            <select
              id="asset-filter"
              className="form-input p-2 rounded-lg"
              value={filterType}
              onChange={(e) => handleFilterChange(e.target.value)}
            >
              <option value="all">All</option>
              <option value="image">Images</option>
              <option value="audio">Audio</option>
              <option value="model">Models</option>
            </select>
          </div>
          <div>
            <label htmlFor="file-upload" className="btn-primary px-4 py-2 rounded-lg cursor-pointer flex items-center space-x-2">
              <FaUpload />
              <span>Upload New Asset</span>
            </label>
            <input
              id="file-upload"
              type="file"
              className="hidden"
              onChange={handleFileUpload}
            />
          </div>
        </div>
      </Card>

      {error ? (
        <Card className="p-8 text-center">
          <div className="text-red-600 mb-4">
            <FaExclamationTriangle className="text-4xl mx-auto mb-2" aria-label="Error Icon" />
            <p className="font-medium">Unable to load assets</p>
            <p className="text-sm text-gray-600 mt-2">{error}</p>
          </div>
          <button
            onClick={loadAssets}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors duration-200"
          >
            Try Again
          </button>
        </Card>
      ) : assets.length === 0 ? (
        <Card className="p-8 text-center">
          <div className="text-gray-500 mb-4">
            <FaImage className="text-4xl mx-auto mb-2" />
            <p className="font-medium">No assets found</p>
            <p className="text-sm mt-2">Upload your first asset to get started.</p>
          </div>
        </Card>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {assets.map((asset) => (
              <Card key={asset.id} className="overflow-hidden hover:shadow-lg transition-shadow duration-200">
                <div className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className="bg-gray-100 p-2 rounded-lg">
                        {getAssetIcon(asset.type)}
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-800 line-clamp-1">{asset.name}</h3>
                        <p className="text-sm text-gray-500 capitalize">{asset.type} asset</p>
                      </div>
                    </div>
                    <div className="relative">
                      <button onClick={() => openDeleteModal(asset)} className="p-2 text-gray-400 hover:text-gray-600 transition-colors duration-200">
                        <FaTrash aria-label="Delete Asset" />
                      </button>
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-sm text-gray-500">
                    <p>Size: {(asset.size / 1024 / 1024).toFixed(2)} MB</p>
                    <p>Used: {asset.usage_count} times</p>
                  </div>

                  <div className="flex space-x-2 mt-4">
                    <a href={asset.url} target="_blank" rel="noopener noreferrer" className="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-lg text-sm transition-colors duration-200 flex items-center justify-center space-x-1">
                      <FaDownload aria-label="Download Asset" />
                      <span>Download</span>
                    </a>
                  </div>
                </div>
              </Card>
            ))}
          </div>

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
    </div>
  );
}

