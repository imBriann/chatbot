import type {
  ChatMessage,
  ChatResponse,
  Category,
  FAQ,
  AdminCategory,
  AdminFAQ,
  AdminMetrics,
  AdminLog,
} from '../types';

const API_BASE = import.meta.env.VITE_API_URL || '/api';

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Network error' }));
    throw new Error(error.message || `Request failed with status ${response.status}`);
  }

  return response.json();
}

function authRequest<T>(endpoint: string, token: string, options?: RequestInit): Promise<T> {
  return request<T>(endpoint, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
      ...(options?.headers || {}),
    },
  });
}

export const api = {
  adminLogin: (email: string, password: string) =>
    request<{ token: string }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),

  sendMessage: (sessionId: string, message: string, category?: string) =>
    request<ChatResponse>('/chat/message', {
      method: 'POST',
      body: JSON.stringify({ sessionId, message, category }),
    }),

  getHistory: (sessionId: string) =>
    request<{ messages: ChatMessage[] }>(`/chat/history/${sessionId}`),

  clearHistory: (sessionId: string) =>
    request<{ status: string }>(`/chat/history/${sessionId}`, { method: 'DELETE' }),

  getCategories: () =>
    request<{ categories: Category[] }>('/categories'),

  getFAQs: (slug: string) =>
    request<{ faqs: FAQ[] }>(`/categories/${slug}/faqs`),

  adminGetMetrics: (token: string) =>
    authRequest<{ metrics: AdminMetrics }>('/admin/metrics', token),

  adminGetLogs: (token: string, limit = 20) =>
    authRequest<{ logs: AdminLog[] }>(`/admin/logs?limit=${limit}`, token),

  adminGetCategories: (token: string) =>
    authRequest<{ categories: AdminCategory[] }>('/admin/categories', token),

  adminCreateCategory: (token: string, input: Omit<AdminCategory, 'id' | 'createdAt'>) =>
    authRequest<{ category: AdminCategory }>('/admin/categories', token, {
      method: 'POST',
      body: JSON.stringify(input),
    }),

  adminUpdateCategory: (token: string, id: string, input: Partial<Omit<AdminCategory, 'id' | 'createdAt'>>) =>
    authRequest<{ status: string }>(`/admin/categories/${id}`, token, {
      method: 'PUT',
      body: JSON.stringify(input),
    }),

  adminDeleteCategory: (token: string, id: string) =>
    authRequest<{ status: string }>(`/admin/categories/${id}`, token, {
      method: 'DELETE',
    }),

  adminGetFaqs: (token: string, categoryId: string) =>
    authRequest<{ faqs: AdminFAQ[] }>(`/admin/faqs?categoryId=${categoryId}`, token),

  adminCreateFaq: (token: string, input: Omit<AdminFAQ, 'id' | 'createdAt'>) =>
    authRequest<{ faq: AdminFAQ }>('/admin/faqs', token, {
      method: 'POST',
      body: JSON.stringify(input),
    }),

  adminUpdateFaq: (token: string, id: string, input: Partial<Omit<AdminFAQ, 'id' | 'createdAt'>>) =>
    authRequest<{ status: string }>(`/admin/faqs/${id}`, token, {
      method: 'PUT',
      body: JSON.stringify(input),
    }),

  adminDeleteFaq: (token: string, id: string) =>
    authRequest<{ status: string }>(`/admin/faqs/${id}`, token, {
      method: 'DELETE',
    }),
};
