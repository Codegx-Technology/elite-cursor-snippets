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
  style?: 'realistic' | 'cartoon' | 'anime' | 'documentary';
  duration?: number;
  voice_type?: 'male' | 'female' | 'child';
  background_music?: boolean;
  cultural_preset?: 'mount_kenya' | 'maasai_mara' | 'diani_beach' | 'nairobi_city';
}

export interface NewsVideoGenerationRequest {
  news_url?: string;
  news_query?: string;
  script_content?: string;
  lang?: string;
  scenes?: number;
  duration?: number;
  voice_type?: string;
  upload_youtube?: boolean;
}

export interface VideoGenerationResponse {
  status: string;
  video_id: string;
  video_path?: string;
  message: string;
  progress?: number;
  estimated_time?: number;
  thumbnail_url?: string;
}

export interface ContentGenerationJob {
  id: string;
  type: 'video' | 'image' | 'audio';
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress: number;
  created_at: string;
  completed_at?: string;
  result_url?: string;
  error_message?: string;
  metadata: Record<string, any>;
}

export interface PaymentPlan {
  id: string;
  name: string;
  price: number;
  currency: string;
  interval: 'monthly' | 'yearly';
  features: string[];
  video_credits: number;
  image_credits: number;
  audio_credits: number;
  is_popular?: boolean;
}

export interface PaymentSession {
  session_id: string;
  payment_url: string;
  status: 'pending' | 'completed' | 'failed';
  amount: number;
  currency: string;
}

export interface UserSubscription {
  id: string;
  plan_id: string;
  status: 'active' | 'cancelled' | 'expired';
  current_period_start: string;
  current_period_end: string;
  video_credits_remaining: number;
  image_credits_remaining: number;
  audio_credits_remaining: number;
}

export interface AnalyticsData {
  overview: {
    total_videos: number;
    total_images: number;
    total_audio: number;
    total_views: number;
    total_downloads: number;
  };
  usage_trends: Array<{
    date: string;
    videos: number;
    images: number;
    audio: number;
  }>;
  popular_content: Array<{
    id: string;
    title: string;
    type: 'video' | 'image' | 'audio';
    views: number;
    downloads: number;
  }>;
  performance_metrics: {
    avg_generation_time: number;
    success_rate: number;
    user_satisfaction: number;
  };
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
    return this.request('/api/dashboard/stats');
  }

  async getRecentActivity(): Promise<ApiResponse<RecentActivity[]>> {
    return this.request('/api/dashboard/activity');
  }

  // Content Generation
  async generateVideo(request: VideoGenerationRequest): Promise<ApiResponse<VideoGenerationResponse>> {
    return this.request('/api/generate/video', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async generateNewsVideo(request: NewsVideoGenerationRequest): Promise<ApiResponse<VideoGenerationResponse>> {
    return this.request('/api/generate/news-video', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async generateImage(request: {
    prompt: string;
    style?: string;
    size?: string;
    cultural_preset?: string;
  }): Promise<ApiResponse<VideoGenerationResponse>> {
    return this.request('/api/generate/image', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async generateAudio(request: {
    text: string;
    voice_type?: string;
    language?: string;
    speed?: number;
  }): Promise<ApiResponse<VideoGenerationResponse>> {
    return this.request('/api/generate/audio', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getGenerationJob(jobId: string): Promise<ApiResponse<ContentGenerationJob>> {
    return this.request(`/api/jobs/${jobId}`);
  }

  async getGenerationJobs(): Promise<ApiResponse<ContentGenerationJob[]>> {
    return this.request('/api/jobs');
  }

  // Payment System
  async getPaymentPlans(): Promise<ApiResponse<PaymentPlan[]>> {
    // Mock plans for now - will be replaced with real Paystack integration
    return {
      data: [
        {
          id: 'starter',
          name: 'Starter',
          price: 2500,
          currency: 'KES',
          interval: 'monthly',
          features: ['10 Videos/month', '50 Images/month', '20 Audio tracks/month', 'Basic support'],
          video_credits: 10,
          image_credits: 50,
          audio_credits: 20,
        },
        {
          id: 'professional',
          name: 'Professional',
          price: 7500,
          currency: 'KES',
          interval: 'monthly',
          features: ['50 Videos/month', '200 Images/month', '100 Audio tracks/month', 'Priority support', 'HD Quality'],
          video_credits: 50,
          image_credits: 200,
          audio_credits: 100,
          is_popular: true,
        },
        {
          id: 'enterprise',
          name: 'Enterprise',
          price: 15000,
          currency: 'KES',
          interval: 'monthly',
          features: ['Unlimited Videos', 'Unlimited Images', 'Unlimited Audio', '24/7 Support', '4K Quality', 'Custom branding'],
          video_credits: -1,
          image_credits: -1,
          audio_credits: -1,
        }
      ],
      status: 200
    };
  }

  async createPaymentSession(planId: string): Promise<ApiResponse<PaymentSession>> {
    return this.request('/api/payments/create-session', {
      method: 'POST',
      body: JSON.stringify({ plan_id: planId }),
    });
  }

  async getUserSubscription(): Promise<ApiResponse<UserSubscription>> {
    return this.request('/api/user/subscription');
  }

  async cancelSubscription(): Promise<ApiResponse<{ success: boolean }>> {
    return this.request('/api/user/subscription/cancel', {
      method: 'POST',
    });
  }

  // Analytics
  async getAnalytics(timeRange: '7d' | '30d' | '90d' = '30d'): Promise<ApiResponse<AnalyticsData>> {
    return this.request(`/api/analytics?range=${timeRange}`);
  }

  async getAnalyticsOverview(): Promise<ApiResponse<AnalyticsData['overview']>> {
    return this.request('/api/analytics/overview');
  }

  // Projects with pagination
  async getProjects(page: number = 1, limit: number = 6): Promise<ApiResponse<{
    projects: any[];
    total: number;
    page: number;
    pages: number;
  }>> {
    return this.request(`/api/projects?page=${page}&limit=${limit}`);
  }

  async getProject(projectId: string): Promise<ApiResponse<any>> {
    return this.request(`/api/projects/${projectId}`);
  }

  async createProject(project: {
    name: string;
    description?: string;
    type: 'video' | 'image' | 'audio';
  }): Promise<ApiResponse<any>> {
    return this.request('/api/projects', {
      method: 'POST',
      body: JSON.stringify(project),
    });
  }

  async updateProject(projectId: string, updates: any): Promise<ApiResponse<any>> {
    return this.request(`/api/projects/${projectId}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  async deleteProject(projectId: string): Promise<ApiResponse<{ success: boolean }>> {
    return this.request(`/api/projects/${projectId}`, {
      method: 'DELETE',
    });
  }

  // Gallery with pagination and filtering
  async getGalleryItems(
    page: number = 1,
    limit: number = 6,
    type?: 'video' | 'image' | 'audio',
    search?: string
  ): Promise<ApiResponse<{
    items: any[];
    total: number;
    page: number;
    pages: number;
  }>> {
    const params = new URLSearchParams({
      page: page.toString(),
      limit: limit.toString(),
    });

    if (type) params.append('type', type);
    if (search) params.append('search', search);

    return this.request(`/api/gallery?${params.toString()}`);
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
