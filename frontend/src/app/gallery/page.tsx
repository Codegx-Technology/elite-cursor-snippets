'use client';

import { useState, useEffect } from 'react';
import Card from '@/components/Card';
import LazyImage from '@/components/LazyImage';
import LoadingStates from '@/components/ui/LoadingStates';
import ErrorStates from '@/components/ui/ErrorStates';
import { FaImages, FaVideo, FaMusic, FaDownload, FaPlay, FaEye, FaHeart, FaFlag, FaMountain } from 'react-icons/fa6';
import { apiClient, handleApiResponse } from '@/lib/api';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorintent
// [CONTEXT]: Gallery page for browsing generated content with Kenya-first design
// [GOAL]: Create responsive gallery with proper loading states and mobile-first approach
// [TASK]: Implement gallery with real backend integration and cultural authenticity

interface GalleryItem {
  id: string;
  type: 'video' | 'image' | 'audio';
  title: string;
  thumbnail: string;
  createdAt: string;
  duration?: string;
  size: string;
  tags: string[];
}

export default function GalleryPage() {
  const [items, setItems] = useState<GalleryItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'video' | 'image' | 'audio'>('all');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadGalleryItems();
  }, []);

  const loadGalleryItems = async () => {
    setIsLoading(true);
    setError(null);

    const response = await apiClient.getGalleryItems();
    handleApiResponse(
      response,
      (data) => {
        // data is expected to be a paginated object: { items: any[]; total: number; page: number; pages: number }
        const arr: GalleryItem[] = Array.isArray((data as { items: GalleryItem[] }).items)
          ? (data as { items: GalleryItem[] }).items
          : Array.isArray(data)
          ? (data as GalleryItem[])
          : [];
        if (arr.length === 0) {
          // Show sample Kenya-first content when no real data is available
          setItems([
            {
              id: '1',
              type: 'video',
              title: 'Mount Kenya Sunrise',
              thumbnail: '/api/placeholder/400/300',
              createdAt: '2024-01-15',
              duration: '2:30',
              size: '45 MB',
              tags: ['Kenya', 'Nature', 'Tourism']
            },
            {
              id: '2',
              type: 'image',
              title: 'Maasai Mara Wildlife',
              thumbnail: '/api/placeholder/400/300',
              createdAt: '2024-01-14',
              size: '2.1 MB',
              tags: ['Wildlife', 'Safari', 'Kenya']
            },
            {
              id: '3',
              type: 'audio',
              title: 'Swahili Narration',
              thumbnail: '/api/placeholder/400/300',
              createdAt: '2024-01-13',
              duration: '1:45',
              size: '8.5 MB',
              tags: ['Swahili', 'Voice', 'Culture']
            }
          ]);
        } else {
          setItems(arr);
        }
      },
      (error) => setError(error)
    );

    setIsLoading(false);
  };

  const filteredItems = items.filter(item => 
    filter === 'all' || item.type === filter
  );

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'video': return <FaVideo className="text-blue-600" />;
      case 'image': return <FaImages className="text-green-600" />;
      case 'audio': return <FaMusic className="text-purple-600" />;
      default: return <FaImages className="text-gray-600" />;
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-green-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <span className="text-gray-600 font-medium">Loading gallery...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Kenya-First Header */}
      <div className="bg-gradient-to-r from-green-600 via-red-600 to-black p-6 rounded-xl text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <FaImages className="text-3xl" />
            <div>
              <h1 className="text-2xl font-bold">Content Gallery 🇰🇪</h1>
              <p className="text-green-100">Browse your Kenya-first generated content</p>
            </div>
          </div>
          <div className="hidden md:block">
            <FaMountain className="text-4xl text-yellow-300" />
          </div>
        </div>
      </div>

      {/* Filter Tabs */}
      <Card className="p-6">
        <div className="flex flex-wrap gap-2">
          {[
            { key: 'all', label: 'All Content', icon: FaImages },
            { key: 'video', label: 'Videos', icon: FaVideo },
            { key: 'image', label: 'Images', icon: FaImages },
            { key: 'audio', label: 'Audio', icon: FaMusic }
          ].map(({ key, label, icon: Icon }) => (
            <button
              key={key}
              onClick={() => setFilter(key as 'all' | 'video' | 'image' | 'audio')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors duration-200 ${
                filter === key
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <Icon className="text-sm" />
              <span className="font-medium">{label}</span>
            </button>
          ))}
        </div>
      </Card>

      {/* Gallery Grid */}
      {error ? (
        <Card className="p-8 text-center">
          <div className="text-red-600 mb-4">
            <FaImages className="text-4xl mx-auto mb-2" />
            <p className="font-medium">Unable to load gallery</p>
            <p className="text-sm text-gray-600 mt-2">{error}</p>
          </div>
          <button
            onClick={loadGalleryItems}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors duration-200"
          >
            Try Again
          </button>
        </Card>
      ) : filteredItems.length === 0 ? (
        <Card className="p-8 text-center">
          <div className="text-gray-500 mb-4">
            <FaImages className="text-4xl mx-auto mb-2" />
            <p className="font-medium">No content available</p>
            <p className="text-sm mt-2">Start creating amazing Kenya-first content!</p>
          </div>
          <button className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors duration-200">
            Generate Content
          </button>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredItems.map((item) => (
            <Card key={item.id} className="overflow-hidden hover:shadow-lg transition-shadow duration-200">
              <div className="relative">
                <LazyImage
                  src={item.thumbnail}
                  alt={item.title}
                  placeholder={
                    <div className="aspect-video bg-gray-200 flex items-center justify-center">
                      {getTypeIcon(item.type)}
                      <span className="ml-2 text-gray-600 font-medium">{item.type.toUpperCase()}</span>
                    </div>
                  }
                  className="aspect-video"
                />
                <div className="absolute top-2 right-2">
                  <span className="bg-black bg-opacity-50 text-white text-xs px-2 py-1 rounded">
                    {item.duration || item.size}
                  </span>
                </div>
              </div>
              
              <div className="p-4">
                <h3 className="font-semibold text-gray-800 mb-2 line-clamp-2">{item.title}</h3>
                <p className="text-sm text-gray-500 mb-3">{item.createdAt}</p>
                
                <div className="flex flex-wrap gap-1 mb-3">
                  {item.tags.map((tag) => (
                    <span key={tag} className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
                      {tag}
                    </span>
                  ))}
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex space-x-2">
                    <button className="p-2 text-gray-600 hover:text-green-600 transition-colors duration-200">
                      <FaPlay className="text-sm" />
                    </button>
                    <button className="p-2 text-gray-600 hover:text-blue-600 transition-colors duration-200">
                      <FaEye className="text-sm" />
                    </button>
                    <button className="p-2 text-gray-600 hover:text-red-600 transition-colors duration-200">
                      <FaHeart className="text-sm" />
                    </button>
                  </div>
                  <button className="p-2 text-gray-600 hover:text-green-600 transition-colors duration-200">
                    <FaDownload className="text-sm" />
                  </button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Cultural Footer */}
      <div className="bg-gradient-to-r from-yellow-400 via-red-500 to-green-600 p-4 rounded-lg text-white text-center">
        <div className="flex items-center justify-center space-x-2">
          <FaFlag className="text-lg" />
          <span className="font-medium">Celebrating Kenyan creativity through AI</span>
          <FaHeart className="text-lg" />
        </div>
      </div>
    </div>
  );
}
