'use client';

import React from 'react';

interface EditProjectModalProps {
  isOpen: boolean;
  onClose: () => void;
  onUpdate: (id: string, project: Partial<any>) => Promise<void>;
  project: any | null;
}

const EditProjectModal: React.FC<EditProjectModalProps> = ({ isOpen, onClose, onUpdate, project }) => {
  if (!isOpen) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex justify-center items-center">
      <div className="bg-white p-8 rounded-lg">
        <h2 className="text-2xl font-bold mb-4">Edit Project (Placeholder)</h2>
        <p>This feature is not yet implemented.</p>
        <button onClick={onClose} className="mt-4 bg-gray-500 text-white px-4 py-2 rounded">Close</button>
      </div>
    </div>
  );
};

export default EditProjectModal;