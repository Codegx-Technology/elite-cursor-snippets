
import { useState } from 'react';
import { FaPlus, FaTimes } from 'react-icons/fa6';

interface CreateProjectModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreate: (project: { name: string; description: string; type: 'video' | 'image' | 'audio'; }) => void;
}

export default function CreateProjectModal({ isOpen, onClose, onCreate }: CreateProjectModalProps) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [type, setType] = useState<'video' | 'image' | 'audio'>('video');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onCreate({ name, description, type });
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-8 w-full max-w-md">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Create New Project</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <FaTimes />
          </button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="space-y-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700">Project Name</label>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="form-input w-full mt-1"
                required
              />
            </div>
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700">Description</label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="form-input w-full mt-1 h-24 resize-none"
              />
            </div>
            <div>
              <label htmlFor="type" className="block text-sm font-medium text-gray-700">Project Type</label>
              <select
                id="type"
                value={type}
                onChange={(e) => setType(e.target.value as 'video' | 'image' | 'audio')}
                className="form-input w-full mt-1"
              >
                <option value="video">Video</option>
                <option value="image">Image</option>
                <option value="audio">Audio</option>
              </select>
            </div>
          </div>
          <div className="flex justify-end space-x-4 mt-6">
            <button type="button" onClick={onClose} className="btn-secondary">
              Cancel
            </button>
            <button type="submit" className="btn-primary flex items-center space-x-2">
              <FaPlus />
              <span>Create Project</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
