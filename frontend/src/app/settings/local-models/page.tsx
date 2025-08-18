'use client';

import { useLocalModels } from '@/hooks/useLocalModels';
import { FaSpinner, FaDownload, FaTrash } from 'react-icons/fa';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Reusable local models component
// [GOAL]: Provide a clean and reusable component for managing local AI models

export default function LocalModels() {
  const { models, isLoading, error, downloadModel, deleteModel } = useLocalModels();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <FaSpinner className="w-8 h-8 text-green-600 animate-spin mx-auto mb-4" />
          <span className="text-gray-600 font-medium">Loading local models...</span>
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
                    onClick={() => downloadModel(model.id)}
                    className="btn-primary px-4 py-2 rounded-lg text-white text-sm flex items-center space-x-2"
                  >
                    <FaDownload />
                    <span>Download</span>
                  </button>
                )}
                {model.status === 'installed' && (
                  <button
                    onClick={() => deleteModel(model.id)}
                    className="btn-danger px-4 py-2 rounded-lg text-sm flex items-center space-x-2"
                  >
                    <FaTrash />
                    <span>Delete</span>
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
}