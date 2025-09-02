
import { FaTrashCan, FaXmark } from 'react-icons/fa6';
import { Asset } from '@/hooks/useAssetLibrary';

interface DeleteAssetModalProps {
  isOpen: boolean;
  onClose: () => void;
  onDelete: (id: string) => void;
  asset: Asset | null;
}

export default function DeleteAssetModal({ isOpen, onClose, onDelete, asset }: DeleteAssetModalProps) {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (asset) {
      onDelete(asset.id);
    }
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-8 w-full max-w-md">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Delete Asset</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <FaTimes />
          </button>
        </div>
        <form onSubmit={handleSubmit}>
          <p>Are you sure you want to delete the asset &quot;{asset?.name}&quot;?</p>
          <div className="flex justify-end space-x-4 mt-6">
            <button type="button" onClick={onClose} className="btn-secondary">
              Cancel
            </button>
            <button type="submit" className="btn-danger flex items-center space-x-2">
              <FaTrash />
              <span>Delete</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

