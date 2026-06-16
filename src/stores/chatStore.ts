import { create } from 'zustand';
import { v4 as uuidv4 } from 'uuid';
import type { ChatMessage } from '../types';
import { api } from '../services/api';

interface ChatState {
  sessionId: string;
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  isChatOpen: boolean;

  openChat: () => void;
  closeChat: () => void;
  toggleChat: () => void;
  sendMessage: (content: string, category?: string) => Promise<void>;
  clearChat: () => void;
  loadHistory: () => Promise<void>;
}

function getOrCreateSessionId(): string {
  const KEY = 'unipamplona_chat_session';
  let id = localStorage.getItem(KEY);
  if (!id) {
    id = uuidv4();
    localStorage.setItem(KEY, id);
  }
  return id;
}

export const useChatStore = create<ChatState>((set, get) => ({
  sessionId: getOrCreateSessionId(),
  messages: [],
  isLoading: false,
  error: null,
  isChatOpen: false,

  openChat: () => set({ isChatOpen: true }),
  closeChat: () => set({ isChatOpen: false }),
  toggleChat: () => set((s) => ({ isChatOpen: !s.isChatOpen })),

  sendMessage: async (content: string, category?: string) => {
    const { sessionId } = get();

    const userMessage: ChatMessage = {
      id: uuidv4(),
      role: 'user',
      content,
      createdAt: new Date().toISOString(),
    };

    set((s) => ({
      messages: [...s.messages, userMessage],
      isLoading: true,
      error: null,
    }));

    try {
      const response = await api.sendMessage(sessionId, content, category);

      const botMessage: ChatMessage = {
        id: response.id,
        role: 'bot',
        content: response.response,
        category: response.category,
        confidence: response.confidence,
        createdAt: response.timestamp,
      };

      set((s) => ({
        messages: [...s.messages, botMessage],
        isLoading: false,
      }));
    } catch (error) {
      set({
        isLoading: false,
        error: error instanceof Error ? error.message : 'Error al conectar con el servidor',
      });

      const errorMessage: ChatMessage = {
        id: uuidv4(),
        role: 'bot',
        content: 'Lo siento, hubo un error al procesar tu consulta. Por favor intenta de nuevo.',
        createdAt: new Date().toISOString(),
      };

      set((s) => ({ messages: [...s.messages, errorMessage] }));
    }
  },

  clearChat: () => {
    const { sessionId } = get();
    api.clearHistory(sessionId).catch(() => {});
    const newSessionId = uuidv4();
    localStorage.setItem('unipamplona_chat_session', newSessionId);
    set({ messages: [], sessionId: newSessionId, error: null });
  },

  loadHistory: async () => {
    const { sessionId } = get();
    try {
      const { messages } = await api.getHistory(sessionId);
      if (messages.length > 0) {
        set({ messages });
      }
    } catch {
      // Silent fail - fresh session
    }
  },
}));
