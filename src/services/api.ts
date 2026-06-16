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
const DEFAULT_TIMEOUT = 30000; // 30 segundos

async function request<T>(
  endpoint: string,
  options?: RequestInit,
  timeout: number = DEFAULT_TIMEOUT
): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      headers: { 'Content-Type': 'application/json' },
      ...options,
      signal: controller.signal,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: 'Network error' }));
      throw new Error(error.message || `Request failed with status ${response.status}`);
    }

    return response.json();
  } catch (error) {
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error(`Request timeout after ${timeout}ms`);
    }
    throw error;
  } finally {
    clearTimeout(timeoutId);
  }
}

function authRequest<T>(
  endpoint: string,
  token: string,
  options?: RequestInit,
  timeout?: number
): Promise<T> {
  return request<T>(
    endpoint,
    {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
        ...(options?.headers || {}),
      },
    },
    timeout
  );
}

export const api = {
  adminLogin: (email: string, password: string) =>
    request<{ token: string }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }, 10000),

  sendMessage: (sessionId: string, message: string, category?: string) =>
    request<ChatResponse>('/chat/message', {
      method: 'POST',
      body: JSON.stringify({ sessionId, message, category }),
    }, 60000), // 60 segundos para procesamiento de IA

  getHistory: (sessionId: string) =>
    request<{ messages: ChatMessage[] }>(`/chat/history/${sessionId}`, undefined, 15000),

  clearHistory: (sessionId: string) =>
    request<{ status: string }>(`/chat/history/${sessionId}`, { method: 'DELETE' }, 10000),

  getCategories: () =>
    request<{ categories: Category[] }>('/categories', undefined, 10000),

  getFAQs: (slug: string) =>
    request<{ faqs: FAQ[] }>(`/categories/${slug}/faqs`, undefined, 10000),

  adminGetMetrics: (token: string) =>
    authRequest<{ metrics: AdminMetrics }>('/admin/metrics', token, undefined, 15000),

  adminGetLogs: (token: string, limit = 20) =>
    authRequest<{ logs: AdminLog[] }>(`/admin/logs?limit=${limit}`, token, undefined, 15000),

  adminGetCategories: (token: string) =>
    authRequest<{ categories: AdminCategory[] }>('/admin/categories', token, undefined, 15000),

  adminCreateCategory: (token: string, input: Omit<AdminCategory, 'id' | 'createdAt'>) =>
    authRequest<{ category: AdminCategory }>('/admin/categories', token, {
      method: 'POST',
      body: JSON.stringify(input),
    }, 15000),

  adminUpdateCategory: (token: string, id: string, input: Partial<Omit<AdminCategory, 'id' | 'createdAt'>>) =>
    authRequest<{ status: string }>(`/admin/categories/${id}`, token, {
      method: 'PUT',
      body: JSON.stringify(input),
    }, 15000),

  adminDeleteCategory: (token: string, id: string) =>
    authRequest<{ status: string }>(`/admin/categories/${id}`, token, {
      method: 'DELETE',
    }, 15000),

  adminGetFaqs: (token: string, categoryId: string) =>
    authRequest<{ faqs: AdminFAQ[] }>(`/admin/faqs?categoryId=${categoryId}`, token, undefined, 15000),

  adminCreateFaq: (token: string, input: Omit<AdminFAQ, 'id' | 'createdAt'>) =>
    authRequest<{ faq: AdminFAQ }>('/admin/faqs', token, {
      method: 'POST',
      body: JSON.stringify(input),
    }, 15000),

  adminUpdateFaq: (token: string, id: string, input: Partial<Omit<AdminFAQ, 'id' | 'createdAt'>>) =>
    authRequest<{ status: string }>(`/admin/faqs/${id}`, token, {
      method: 'PUT',
      body: JSON.stringify(input),
    }, 15000),

  adminDeleteFaq: (token: string, id: string) =>
    authRequest<{ status: string }>(`/admin/faqs/${id}`, token, {
      method: 'DELETE',
    }, 15000),
};
