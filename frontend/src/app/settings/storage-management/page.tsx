
import { useStorageManagement } from '@/hooks/useStorageManagement';
import { FaSpinner } from 'react-icons/fa';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Reusable storage management component
// [GOAL]: Provide a clean and reusable component for managing storage

export default function StorageManagementPage() {
  const { storageInfo, isLoading, error, clearCache } = useStorageManagement();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <FaSpinner className="w-8 h-8 text-green-600 animate-spin mx-auto mb-4" />
          <span className="text-gray-600 font-medium">Loading storage information...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-500 text-center">
        <p>Error: {error}</p>
      </div>
    );
  }

  if (!storageInfo) {
    return <div className="text-center text-soft-text">No storage information available.</div>;
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
            onClick={clearCache}
            className="btn-danger px-6 py-3 rounded-lg text-white font-semibold"
          >
            Clear Cache
          </button>
        </div>
      </div>
    </div>
  );
}
