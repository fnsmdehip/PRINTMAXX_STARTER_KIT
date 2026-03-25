const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

type ToastFn = ((title: string, message?: string) => void) | null;

let _toastError: ToastFn = null;
let _toastSuccess: ToastFn = null;

export function bindToast(error: ToastFn, success: ToastFn) {
  _toastError = error;
  _toastSuccess = success;
}

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

class ApiClient {
  private apiKey: string | null = null;

  setApiKey(key: string) {
    this.apiKey = key;
    if (typeof window !== 'undefined') {
      localStorage.setItem('arai_api_key', key);
    }
  }

  getApiKey(): string | null {
    if (this.apiKey) return this.apiKey;
    if (typeof window !== 'undefined') {
      this.apiKey = localStorage.getItem('arai_api_key');
    }
    return this.apiKey;
  }

  clearApiKey() {
    this.apiKey = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('arai_api_key');
    }
  }

  private async request<T = any>(
    path: string,
    options: RequestInit = {},
    opts?: { silent?: boolean }
  ): Promise<T> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...((options.headers as Record<string, string>) || {}),
    };

    const key = this.getApiKey();
    if (key) {
      headers['x-api-key'] = key;
    }

    let res: Response;
    try {
      res = await fetch(`${API_URL}${path}`, { ...options, headers });
    } catch (networkErr) {
      const msg = 'Network error. Please check your connection.';
      if (!opts?.silent && _toastError) _toastError('Connection Failed', msg);
      throw new ApiError(msg, 0);
    }

    let data: any;
    try {
      data = await res.json();
    } catch {
      data = {};
    }

    if (!res.ok) {
      const msg = data.error || `Request failed (${res.status})`;

      if (res.status === 401) {
        this.clearApiKey();
        if (typeof window !== 'undefined' && !window.location.pathname.startsWith('/login')) {
          window.location.href = '/login';
        }
      }

      if (!opts?.silent && _toastError) {
        _toastError('Error', msg);
      }

      throw new ApiError(msg, res.status);
    }

    return data as T;
  }

  // ─── Auth ────────────────────────────────────────────────────────────
  async register(name: string, url: string, email: string) {
    const data = await this.request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ name, url, email }),
    });
    if (_toastSuccess) _toastSuccess('Account Created', 'Your API key has been generated.');
    return data;
  }

  async login(apiKey: string) {
    const data = await this.request(
      '/api/auth/login',
      { method: 'POST', body: JSON.stringify({ apiKey }) },
      { silent: true }
    );
    this.setApiKey(apiKey);
    return data;
  }

  async getMe() {
    return this.request('/api/auth/me', {}, { silent: true });
  }

  async updateSettings(settings: {
    primaryColor?: string;
    position?: string;
    greeting?: string;
  }) {
    const data = await this.request('/api/auth/settings', {
      method: 'PUT',
      body: JSON.stringify(settings),
    });
    if (_toastSuccess) _toastSuccess('Settings Saved', 'Widget appearance updated.');
    return data;
  }

  // ─── Knowledge Base ──────────────────────────────────────────────────
  async getKnowledgeBase() {
    return this.request('/api/knowledge');
  }

  async createKnowledgeItem(item: {
    title: string;
    content: string;
    type?: string;
  }) {
    const data = await this.request('/api/knowledge', {
      method: 'POST',
      body: JSON.stringify(item),
    });
    if (_toastSuccess) _toastSuccess('Item Created', 'Knowledge base updated.');
    return data;
  }

  async bulkCreateKnowledgeItems(items: { title: string; content: string; type?: string }[]) {
    const data = await this.request('/api/knowledge/bulk', {
      method: 'POST',
      body: JSON.stringify({ items }),
    });
    if (_toastSuccess) _toastSuccess('Bulk Import Complete', `${data.created} items added.`);
    return data;
  }

  async updateKnowledgeItem(
    id: string,
    item: { title?: string; content?: string; type?: string }
  ) {
    const data = await this.request(`/api/knowledge/${id}`, {
      method: 'PUT',
      body: JSON.stringify(item),
    });
    if (_toastSuccess) _toastSuccess('Item Updated');
    return data;
  }

  async deleteKnowledgeItem(id: string) {
    const data = await this.request(`/api/knowledge/${id}`, {
      method: 'DELETE',
    });
    if (_toastSuccess) _toastSuccess('Item Deleted');
    return data;
  }

  // ─── Analytics ───────────────────────────────────────────────────────
  async getAnalyticsOverview() {
    return this.request('/api/analytics/overview', {}, { silent: true });
  }

  async getMessagesPerDay(days?: number) {
    return this.request(
      `/api/analytics/messages-per-day${days ? `?days=${days}` : ''}`,
      {},
      { silent: true }
    );
  }

  async getConversations(page?: number, search?: string) {
    const params = new URLSearchParams();
    if (page) params.set('page', String(page));
    if (search) params.set('search', search);
    return this.request(`/api/analytics/conversations?${params.toString()}`, {}, { silent: true });
  }

  async getConversation(id: string) {
    return this.request(`/api/analytics/conversations/${id}`, {}, { silent: true });
  }

  // ─── Billing ─────────────────────────────────────────────────────────
  async getPlans() {
    return this.request('/api/billing/plans', {}, { silent: true });
  }

  async createCheckout(plan: string) {
    return this.request('/api/billing/checkout', {
      method: 'POST',
      body: JSON.stringify({ plan }),
    });
  }

  async getBillingPortal() {
    return this.request('/api/billing/portal', { method: 'POST' });
  }

  async getBillingStatus() {
    return this.request('/api/billing/status', {}, { silent: true });
  }
}

export const api = new ApiClient();
export default api;
