// [SNIPPET]: thinkwithai + surgicalfix + refactorintent + augmentsearch
// [CONTEXT]: API client for ShujaaStudio backend integration with proper error handling
// [GOAL]: Create robust API client with TypeScript support and error boundaries
// [TASK]: Implement API client with authentication, retry logic, and proper typing

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '';

import { canUse, canDownload } from '@/core/planGuard'; // New import
import { useAuth } from '@/context/AuthContext'; // New import

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
  status: 'pending' | 'processing' | 'completed' | 'failed' | 'friendly_fallback';
  progress: number;
  created_at: string;
  completed_at?: string;
  result_url?: string;
  error_message?: string;
  metadata: Record<string, unknown>;
  // Optional friendly fallback fields when service returns a soft-fail UX path
  friendly_message?: string;
  retry_options?: string[];
  spinner_type?: string;
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

export interface ApiKey {
  id: string;
  key: string;
  created_at: string;
  last_used_at?: string;
  is_active: boolean;
}

export interface Integration {
  id: string;
  name: string;
  type: string;
  is_enabled: boolean;
  config: Record<string, unknown>;
}

export interface Project {
  id: string;
  name: string;
  description?: string;
  type: 'video' | 'image' | 'audio';
  status: string;
  created_at: string;
  updated_at: string;
  items_count: number;
}

export interface GalleryItem {
  id: string;
  title: string;
  type: 'video' | 'image' | 'audio';
  url: string;
  thumbnail_url?: string;
  created_at: string;
}

export interface UserData {
  id: number;
  username: string;
  email: string;
  role: string;
  tenant_name: string;
  is_active: boolean;
}

export interface CreateUserData extends Omit<UserData, 'id'> {
  password: string;
}

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

export interface LocalModel {
  id: string;
  name: string;
  type: 'llm' | 'image_gen' | 'tts' | 'stt';
  version: string;
  size_gb: number;
  status: 'installed' | 'downloading' | 'available';
  download_progress?: number;
}

export interface StorageInfo {
  total_space_gb: number;
  used_space_gb: number;
  free_space_gb: number;
  cache_size_gb: number;
  project_data_size_gb: number;
  log_data_size_gb: number;
}

export interface UserProfileData {
  username: string;
  email: string;
  full_name?: string;
  bio?: string;
}

export interface TenantBrandingData {
  id: string;
  tenant_id: string;
  name: string;
  logo_url: string;
  primary_color: string;
  secondary_color: string;
  custom_domain: string;
  tls_status: 'pending' | 'active' | 'failed';
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

  async login(username: string, password: string): Promise<ApiResponse<{ access_token: string }>> {
    return this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const url = `${this.baseUrl}${endpoint}`;
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
        ...(options.headers as Record<string, string> | undefined),
      };

      if (this.authToken) {
        headers.Authorization = `Bearer ${this.authToken}`;
      }

      const response = await fetch(url, {
        ...options,
        headers,
      });
      // Safely parse response body (JSON preferred, fallback to text)
      const contentType = response.headers.get('content-type') || '';
      let parsed: any = null;
      try {
        if (contentType.includes('application/json')) {
          parsed = await response.json();
        } else {
          const text = await response.text();
          // Attempt to parse JSON from text if it looks like JSON
          if (text && (text.startsWith('{') || text.startsWith('['))) {
            try {
              parsed = JSON.parse(text);
            } catch {
              parsed = { message: text };
            }
          } else {
            parsed = { message: text };
          }
        }
      } catch (e) {
        // Parsing failed; leave parsed null
        parsed = null;
      }

      if (!response.ok) {
        const errMsg = (parsed && (parsed.detail || parsed.error || parsed.message))
          || `HTTP ${response.status}: ${response.statusText}`;
        return {
          error: errMsg,
          status: response.status,
        };
      }

      return {
        data: parsed as T,
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
    const { user } = useAuth(); // Get user from context
    const check = canUse('tts:generation', { userId: user?.id || '', userRole: user?.role });
    if (!check.ok) {
      return { error: check.reason || 'TTS generation denied by PlanGuard', status: 403 };
    }
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

  // API Keys
  async getApiKeys(): Promise<ApiResponse<ApiKey[]>> {
    return this.request('/api/keys');
  }

  async generateApiKey(): Promise<ApiResponse<ApiKey>> {
    return this.request('/api/keys', {
      method: 'POST',
    });
  }

  async revokeApiKey(id: string): Promise<ApiResponse<{ success: boolean }>> {
    return this.request(`/api/keys/${id}`, {
      method: 'DELETE',
    });
  }

  // Integrations
  async getIntegrations(): Promise<ApiResponse<Integration[]>> {
    return this.request('/api/integrations');
  }

  async updateIntegration(id: string, config: Partial<Integration>): Promise<ApiResponse<Integration>> {
    return this.request(`/api/integrations/${id}`, {
      method: 'PUT',
      body: JSON.stringify(config),
    });
  }

  // Projects with pagination
  async getProjects(page: number = 1, limit: number = 6): Promise<ApiResponse<{
    projects: Project[];
    total: number;
    page: number;
    pages: number;
  }>> {
    return this.request(`/api/projects?page=${page}&limit=${limit}`);
  }

  async getProject(projectId: string): Promise<ApiResponse<Project>> {
    return this.request(`/api/projects/${projectId}`);
  }

  async createProject(project: {
    name: string;
    description?: string;
    type: 'video' | 'image' | 'audio';
  }): Promise<ApiResponse<Project>> {
    return this.request('/api/projects', {
      method: 'POST',
      body: JSON.stringify(project),
    });
  }

  async updateProject(projectId: string, updates: Partial<Project>): Promise<ApiResponse<Project>> {
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

  // User Management
  async getUsers(): Promise<ApiResponse<UserData[]>> {
    return this.request('/api/users');
  }

  async getUser(id: number): Promise<ApiResponse<UserData>> {
    return this.request(`/api/users/${id}`);
  }

  async createUser(data: CreateUserData): Promise<ApiResponse<UserData>> {
    return this.request('/api/users', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateUser(id: number, data: Partial<UserData>): Promise<ApiResponse<UserData>> {
    return this.request(`/api/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteUser(id: number): Promise<ApiResponse<{ success: boolean }>> {
    return this.request(`/api/users/${id}`, {
      method: 'DELETE',
    });
  }

  // Assets
  async getAssets(page: number, limit: number, type?: string): Promise<ApiResponse<{ assets: Asset[], pages: number, total: number }>> {
    const params = new URLSearchParams({
      page: page.toString(),
      limit: limit.toString(),
    });
    if (type) {
      params.append('type', type);
    }
    return this.request(`/api/assets?${params.toString()}`);
  }

  async uploadAsset(formData: FormData): Promise<ApiResponse<Asset>> {
    return this.request('/api/assets', {
      method: 'POST',
      body: formData,
    });
  }

  async deleteAsset(id: string): Promise<ApiResponse<{ success: boolean }>> {
    return this.request(`/api/assets/${id}`, {
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
        items: GalleryItem[];
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

  // Local Models
  async getLocalModels(): Promise<ApiResponse<LocalModel[]>> {
    const { user } = useAuth(); // Get user from context
    const check = canUse('models:local', { userId: user?.id || '', userRole: user?.role });
    if (!check.ok) {
      return { error: check.reason || 'Access denied by PlanGuard', status: 403 };
    }
    return this.request('/api/models/local');
  }

  async downloadLocalModel(modelId: string): Promise<ApiResponse<{ success: boolean }>> {
    const { user } = useAuth(); // Get user from context
    const check = canDownload(`model:${modelId}`, { userId: user?.id || '', userRole: user?.role });
    if (!check.ok) {
      return { error: check.reason || 'Download denied by PlanGuard', status: 403 };
    }
    return this.request(`/api/models/local/${modelId}/download`, {
      method: 'POST',
    });
  }

  async deleteLocalModel(modelId: string): Promise<ApiResponse<{ success: boolean }>> {
    return this.request(`/api/models/local/${modelId}`, {
      method: 'DELETE',
    });
  }

  async getPromptSuggestions(prompt: string): Promise<ApiResponse<{ suggestions: string[] }>> {
    return this.request(`/api/prompts/suggestions?q=${encodeURIComponent(prompt)}`);
  }

  // Storage Management
  async getStorageInfo(): Promise<ApiResponse<StorageInfo>> {
    return this.request('/api/storage/info');
  }

  async clearCache(): Promise<ApiResponse<{ success: boolean }>> {
    return this.request('/api/storage/clear-cache', {
      method: 'POST',
    });
  }

  // User Profile
  async getProfile(): Promise<ApiResponse<UserProfileData>> {
    return this.request('/api/user/profile');
  }

  async updateProfile(data: Partial<UserProfileData>): Promise<ApiResponse<UserProfileData>> {
    return this.request('/api/user/profile', {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // Super Admin
  async getSuperAdminMetrics(): Promise<ApiResponse<any>> { // Define a proper type for SuperAdminMetrics later
    return this.request('/api/superadmin/metrics');
  }

  async getSuperAdminUsers(): Promise<ApiResponse<UserData[]>> {
    return this.request('/api/superadmin/users');
  }

  async getSuperAdminTenants(): Promise<ApiResponse<any[]>> { // Define a proper type for TenantData later
    return this.request('/api/superadmin/tenants');
  }

  // Tenant Branding
  async getTenantBranding(tenantId: string): Promise<ApiResponse<TenantBrandingData>> {
    return this.request(`/api/superadmin/tenants/${tenantId}/branding`);
  }

  async updateTenantBranding(tenantId: string, brandingData: Partial<TenantBrandingData>): Promise<ApiResponse<TenantBrandingData>> {
    return this.request(`/api/superadmin/tenants/${tenantId}/branding`, {
      method: 'PUT',
      body: JSON.stringify(brandingData),
    });
  }

  // Widget Management
  async installWidget(widgetName: string, widgetVersion: string, dependencies: string[]): Promise<ApiResponse<{ success: boolean; message: string }>> {
    const { user } = useAuth();
    const check = canDownload(`widget:${widgetName}`, { userId: user?.id || '', userRole: user?.role });
    if (!check.ok) {
      return { error: check.reason || 'Widget installation denied by PlanGuard', status: 403 };
    }
    return this.request('/api/widgets/install', {
      method: 'POST',
      body: JSON.stringify({ widget_name: widgetName, widget_version: widgetVersion, dependencies }),
    });
  }

  async updateWidget(widgetName: string, newWidgetVersion: string, newDependencies: string[]): Promise<ApiResponse<{ success: boolean; message: string }>> {
    const { user } = useAuth();
    const check = canDownload(`widget:${widgetName}`, { userId: user?.id || '', userRole: user?.role });
    if (!check.ok) {
      return { error: check.reason || 'Widget update denied by PlanGuard', status: 403 };
    }
    return this.request('/api/widgets/update', {
      method: 'POST',
      body: JSON.stringify({ widget_name: widgetName, new_widget_version: newWidgetVersion, new_dependencies: newDependencies }),
    });
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




