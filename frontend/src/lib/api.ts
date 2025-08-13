// [SNIPPET]: thinkwithai + surgicalfix + refactorintent + augmentsearch
// [CONTEXT]: API client for ShujaaStudio backend integration with proper error handling
// [GOAL]: Create robust API client with TypeScript support and error boundaries
// [TASK]: Implement API client with authentication, retry logic, and proper typing

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
}

export interface DashboardStats {
  videosGenerated: number;
  imagesCreated: number;
  audioTracks: number;
  activeUsers: number;
  systemStatus: 'online' | 'offline' | 'maintenance';
  lastGeneration: string;
}

export interface VideoGenerationRequest {
  prompt: string;
  lang?: string;
  scenes?: number;
  vertical?: boolean;
}

export interface VideoGenerationResponse {
  status: string;
  video_id: string;
  video_path: string;
  message: string;
}

export interface RecentActivity {
  id: string;
  type: 'video' | 'image' | 'audio';
  title: string;
  timestamp: string;
  status: 'completed' | 'processing' | 'failed';
}

class ApiClient {
  private baseUrl: string;
  private authToken: string | null = null;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  setAuthToken(token: string) {
    this.authToken = token;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const url = `${this.baseUrl}${endpoint}`;
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
        ...options.headers,
      };

      if (this.authToken) {
        headers.Authorization = `Bearer ${this.authToken}`;
      }

      const response = await fetch(url, {
        ...options,
        headers,
      });

      const data = await response.json();

      if (!response.ok) {
        return {
          error: data.detail || `HTTP ${response.status}: ${response.statusText}`,
          status: response.status,
        };
      }

      return {
        data,
        status: response.status,
      };
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Network error occurred',
        status: 0,
      };
    }
  }

  // Health check
  async getStatus(): Promise<ApiResponse<{ status: string; message: string }>> {
    return this.request('/api/status');
  }

  // Dashboard data
  async getDashboardStats(): Promise<ApiResponse<DashboardStats>> {
    // For now, return mock data with a note that real data isn't available
    // This will be replaced when backend endpoints are available
    return {
      data: {
        videosGenerated: 0,
        imagesCreated: 0,
        audioTracks: 0,
        activeUsers: 0,
        systemStatus: 'online',
        lastGeneration: 'No data available'
      },
      status: 200
    };
  }

  async getRecentActivity(): Promise<ApiResponse<RecentActivity[]>> {
    // Mock data with friendly message
    return {
      data: [],
      status: 200
    };
  }

  // Video generation
  async generateVideo(request: VideoGenerationRequest): Promise<ApiResponse<VideoGenerationResponse>> {
    return this.request('/generate-video', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // Analytics data
  async getAnalytics(): Promise<ApiResponse<any>> {
    return this.request('/metrics');
  }

  // Projects
  async getProjects(): Promise<ApiResponse<any[]>> {
    // Mock empty projects for now
    return {
      data: [],
      status: 200
    };
  }

  // Gallery
  async getGalleryItems(): Promise<ApiResponse<any[]>> {
    // Mock empty gallery for now
    return {
      data: [],
      status: 200
    };
  }
}

export const apiClient = new ApiClient();

// Utility function for handling API responses in components
export function handleApiResponse<T>(
  response: ApiResponse<T>,
  onSuccess: (data: T) => void,
  onError?: (error: string) => void
) {
  if (response.error) {
    if (onError) {
      onError(response.error);
    } else {
      console.error('API Error:', response.error);
    }
  } else if (response.data) {
    onSuccess(response.data);
  }
}

export default apiClient;
