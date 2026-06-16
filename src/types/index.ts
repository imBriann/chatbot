export interface ChatMessage {
  id: string;
  conversationId?: string;
  role: 'user' | 'bot';
  content: string;
  category?: string;
  confidence?: number;
  createdAt: string;
}

export interface ChatResponse {
  id: string;
  response: string;
  category: string;
  confidence: number;
  relatedTopics: string[];
  timestamp: string;
}

export interface Category {
  slug: string;
  name: string;
  description: string;
  icon: string;
  faqCount: number;
}

export interface FAQ {
  question: string;
  answer: string;
}

export interface AdminCategory {
  id: string;
  slug: string;
  name: string;
  description?: string;
  icon?: string;
  createdAt: string;
}

export interface AdminFAQ {
  id: string;
  categoryId: string;
  question: string;
  answer: string;
  keywords: string[];
  relatedTopics: string[];
  createdAt: string;
}

export interface AdminMetrics {
  categories: number;
  faqs: number;
  conversations: number;
  messages: number;
}

export interface AdminLog {
  id: string;
  method: string;
  url: string;
  status: number;
  durationMs: number;
  createdAt: string;
}
