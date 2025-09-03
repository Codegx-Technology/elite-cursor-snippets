// [SNIPPET]: thinkwithai + surgicalfix + refactorintent + augmentsearch
// [CONTEXT]: API client for ShujaaStudio backend integration with proper error handling
// [GOAL]: Create robust API client with TypeScript support and error boundaries
// [TASK]: Implement API client with authentication, retry logic, and proper typing

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '';

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pages: number;
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

export interface BillingRecord {
  id: string;
  date: string;
  amount: number;
  currency: string;
  description: string;
  status: 'paid' | 'failed' | 'pending';
  invoice_url?: string;
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

export interface Tenant {
  id: number;
  name: string;
  is_active: boolean;
  plan: string;
}

export interface AuditLogEntry {
  id: string;
  timestamp: string;
  event_type: string;
  message: string;
  user_id?: string;
}

export interface CreateTenantData {
  name: string;
  is_active?: boolean;
  plan?: string;
}

export interface TenantBrandingData {
  logo_url?: string;
  primary_color?: string;
  secondary_color?: string;
  custom_css?: string;
  custom_domain?: string;
  tenant_id?: string;
  tls_status?: string;
  name?: string;
  // Add other branding fields as needed
}

export interface UserProfileData {
  id: string;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  phone_number?: string;
  address?: string;
  city?: string;
  country?: string;
  postal_code?: string;
  profile_picture_url?: string;
  bio?: string;
  website?: string;
  social_links?: Record<string, string>;
  created_at: string;
  updated_at: string;
}

export interface NotificationPreferences {
  email_notifications: boolean;
  sms_notifications: boolean;
  push_notifications: boolean;
  // Add other notification preferences as needed
}

export interface SecuritySettings {
  two_factor_enabled: boolean;
  last_password_change?: string;
  last_login_ip?: string;
  login_attempts_failed: number;
}

export interface LoginSession {
  id: string;
  ip_address: string;
  device_info: string;
  login_at: string;
  last_activity_at: string;
  is_current: boolean;
}

export interface StorageInfo {
  total_storage_gb: number;
  used_storage_gb: number;
  asset_count: number;
}

export interface LocalModel {
  id: string;
  name: string;
  version: string;
  size_gb: number;
  status: 'downloaded' | 'downloading' | 'pending' | 'error';
  progress?: number;
}

export interface CreateUserData {
  username: string;
  email: string;
  password?: string;
  role?: string;
  tenant_name?: string;
  is_active?: boolean;
}

export interface SuperAdminMetrics {
  total_users: number;
  active_users: number;
  total_tenants: number;
  active_tenants: number;
  total_videos_generated: number;
  total_storage_used: string;
  system_health: string;
  pending_approvals: number;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

class ApiClient {
  private getAuthHeaders(): HeadersInit {
    try {
      if (typeof window !== 'undefined') {
        const token = localStorage.getItem('access_token') || localStorage.getItem('jwt_token');
        if (token) return { Authorization: `Bearer ${token}` };
      }
    } catch (_) {}
    return {};
  }

  private async request<T>(path: string, init: RequestInit = {}): Promise<ApiResponse<T>> {
    const url = `${API_BASE_URL}${path}`;
    try {
      const res = await fetch(url, {
        ...init,
        headers: {
          'Content-Type': 'application/json',
          ...this.getAuthHeaders(),
          ...(init.headers || {})
        }
      });
      const status = res.status;
      const isJson = res.headers.get('content-type')?.includes('application/json');
      const data = isJson ? await res.json() : undefined;
      if (!res.ok) {
        return { status, error: (data && (data.detail || data.error)) || res.statusText };
      }
      return { status, data: data as T };
    } catch (e: unknown) {
      return { status: 0, error: (e as Error)?.message || 'Network error' };
    }
  }

  // Health/status
  async getStatus() {
    return this.request<{ status: string }>('/health');
  }

  // Dashboard
  async getDashboardStats() {
    return this.request<DashboardStats>('/api/dashboard/stats');
  }
  async getRecentActivity() {
    return this.request<RecentActivity[]>('/api/dashboard/recent');
  }

  // Projects
  async getProjects(page = 1, limit = 6) {
    const search = new URLSearchParams({ page: String(page), limit: String(limit) });
    return this.request<{ projects: Project[]; total: number; page: number; pages: number }>(`/api/projects?${search}`);
  }

  // Gallery
  async getGalleryItems(page = 1, limit = 12, filter = 'all') {
    const search = new URLSearchParams({ 
      page: String(page), 
      limit: String(limit),
      type: filter 
    });
    return this.request<PaginatedResponse<GalleryItem>>(`/api/assets?${search}`);
  }
  async createProject(project: Partial<Project>) {
    return this.request<Project>('/api/projects', {
      method: 'POST',
      body: JSON.stringify(project)
    });
  }
  async updateProject(id: string, project: Partial<Project>) {
    return this.request<Project>(`/api/projects/${id}`, {
      method: 'PUT',
      body: JSON.stringify(project)
    });
  }
  async deleteProject(id: string) {
    return this.request<{ success: boolean }>(`/api/projects/${id}`, { method: 'DELETE' });
  }

  // Local models
  async getLocalModels() {
    return this.request<LocalModel[]>('/api/local-models');
  }
  async downloadLocalModel(modelId: string) {
    return this.request<{ status: string }>(`/api/local-models/${modelId}/download`, { method: 'POST' });
  }
  async deleteLocalModel(modelId: string) {
    return this.request<{ success: boolean }>(`/api/local-models/${modelId}`, { method: 'DELETE' });
  }

  // Billing
  async getBillingHistory() {
    return this.request<BillingRecord[]>('/api/billing/history');
  }

  // SuperAdmin
  async getSuperAdminUsers() {
    return this.request<UserData[]>('/superadmin/users');
  }

  async getSuperAdminTenants() {
    return this.request<Tenant[]>('/superadmin/tenants');
  }

  async getSuperAdminAuditLogs() {
    return this.request<AuditLogEntry[]>('/superadmin/audit-logs');
  }

  // Tenant Branding
  async getTenantBranding(tenantId: string) {
    return this.request<TenantBrandingData>(`/superadmin/tenants/${tenantId}/branding`);
  }

  // Auth
  async login(username: string, password: string): Promise<ApiResponse<LoginResponse>> {
    const body = new URLSearchParams({ username, password });
    // OAuth2PasswordRequestForm expects x-www-form-urlencoded
    try {
      const res = await fetch(`${API_BASE_URL}/token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: body.toString()
      });
      const status = res.status;
      const data = await res.json().catch(() => undefined);
      if (!res.ok) {
        return { status, error: (data && (data.detail || data.error)) || res.statusText };
      }
      return { status, data };
    } catch (e: unknown) {
      return { status: 0, error: (e as Error)?.message || 'Network error' };
    }
  }

  // User Management
  async getUsers() {
    return this.request<UserData[]>('/api/users');
  }

  async getUser(id: number) {
    return this.request<UserData>(`/api/users/${id}`);
  }

  async createUser(data: CreateUserData) {
    return this.request<UserData>('/api/users', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateUser(id: number, data: Partial<UserData>) {
    return this.request<UserData>(`/api/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteUser(id: number) {
    return this.request<{ success: boolean }>(`/api/users/${id}`, {
      method: 'DELETE',
    });
  }

  // Tenant Management
  async getTenants() {
    return this.request<Tenant[]>('/api/tenants');
  }

  async getTenant(id: number) {
    return this.request<Tenant>(`/api/tenants/${id}`);
  }

  async createTenant(data: CreateTenantData) {
    return this.request<Tenant>('/api/tenants', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateTenant(id: number, data: Partial<Tenant>) {
    return this.request<Tenant>(`/api/tenants/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // SuperAdmin Methods
  async getSuperAdminMetrics() {
    return this.request<SuperAdminMetrics>('/api/superadmin/metrics');
  }

  async deleteTenant(id: number) {
    return this.request<{ success: boolean }>(`/api/tenants/${id}`, {
      method: 'DELETE',
    });
  }

  // Audit Log Management
  async getAuditLogs() {
    return this.request<AuditLogEntry[]>('/api/audit-logs');
  }

  // Prompt Suggestions
  async getPromptSuggestions(prompt: string) {
    return this.request<{ suggestions: string[] }>(`/api/prompt-suggestions?prompt=${encodeURIComponent(prompt)}`);
  }
}

export function handleApiResponse<T>(
  response: ApiResponse<T>,
  onSuccess: (data: T) => void,
  onError: (error: string) => void
) {
  if (response.data !== undefined) {
    onSuccess(response.data);
  } else {
    onError(response.error || 'Unknown error');
  }
}

export const apiClient = new ApiClient();
