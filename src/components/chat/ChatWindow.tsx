import { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useChatStore } from '../../stores/chatStore';
import { MessageBubble } from './MessageBubble';
import { ChatInput } from './ChatInput';
import { TypingIndicator } from './TypingIndicator';
import './ChatWindow.css';

const QUICK_QUESTIONS = [
  '¿Cuáles son los requisitos de admisión?',
  '¿Cómo me matriculo?',
  '¿Qué programas ofrece Ingenierías?',
  '¿Cuándo son las inscripciones?',
];


export function ChatWindow() {
  const { messages, isLoading, sendMessage, clearChat, loadHistory } = useChatStore();
  const messagesContainerRef = useRef<HTMLDivElement>(null);
  const didLoad = useRef(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('theme') || 'light';
  });

  useEffect(() => {
    if (!didLoad.current) {
      didLoad.current = true;
      loadHistory();
    }
  }, [loadHistory]);

  // Manejar cambio de tema a nivel global (document.documentElement)
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  // Manejar scroll interno del contenedor de mensajes
  useEffect(() => {
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  const handleSend = (content: string) => {
    sendMessage(content);
  };

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  const isEmpty = messages.length === 0;

  return (
    <div className={`chat-window ${isExpanded ? 'chat-window--expanded' : ''}`}>
      {/* Header */}
      <div className="chat-window__header">
        <div className="chat-window__header-info">
          <div className="chat-window__status">
            <span className="chat-window__status-dot" />
            En línea
          </div>
          <h3 className="chat-window__title">Asistente Virtual</h3>
        </div>
        
        <div className="chat-window__header-actions">
          {/* Botón de Modo Oscuro */}
          <button className="chat-window__action-btn" onClick={toggleTheme} title="Cambiar tema">
            {theme === 'light' ? (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
              </svg>
            ) : (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="5" />
                <line x1="12" y1="1" x2="12" y2="3" />
                <line x1="12" y1="21" x2="12" y2="23" />
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
                <line x1="1" y1="12" x2="3" y2="12" />
                <line x1="21" y1="12" x2="23" y2="12" />
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
              </svg>
            )}
          </button>
          
          {/* Botón de Expandir/Contraer */}
          <button className="chat-window__action-btn" onClick={() => setIsExpanded(!isExpanded)} title={isExpanded ? "Reducir pantalla" : "Pantalla completa"}>
            {isExpanded ? (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="4 14 10 14 10 20" />
                <polyline points="20 10 14 10 14 4" />
                <line x1="14" y1="10" x2="21" y2="3" />
                <line x1="10" y1="14" x2="3" y2="21" />
              </svg>
            ) : (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="15 3 21 3 21 9" />
                <polyline points="9 21 3 21 3 15" />
                <line x1="21" y1="3" x2="14" y2="10" />
                <line x1="3" y1="21" x2="10" y2="14" />
              </svg>
            )}
          </button>

          {/* Botón de Limpiar */}
          <button className="chat-window__action-btn chat-window__clear" onClick={clearChat} title="Limpiar conversación">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="3 6 5 6 21 6" />
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
            </svg>
          </button>
        </div>
      </div>

      {/* Messages Area */}
      <div className="chat-window__messages" ref={messagesContainerRef}>
        <AnimatePresence mode="popLayout">
          {isEmpty && !isLoading && (
            <motion.div
              className="chat-window__empty"
              key="empty"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.4 }}
            >
              <div className="chat-window__empty-icon">💬</div>
              <h4>¡Bienvenido!</h4>
              <p>Soy el asistente virtual de la Universidad de Pamplona. Puedes preguntarme sobre admisiones, matrícula, trámites y más.</p>
              <div className="chat-window__suggestions">
                <p className="chat-window__suggestions-label">Prueba preguntar:</p>
                {QUICK_QUESTIONS.map((q) => (
                  <button
                    key={q}
                    className="chat-window__suggestion-btn"
                    onClick={() => handleSend(q)}
                  >
                    {q}
                  </button>
                ))}
              </div>
            </motion.div>
          )}

          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} />
          ))}
        </AnimatePresence>

        {isLoading && <TypingIndicator />}
      </div>

      {/* Input */}
      <ChatInput onSend={handleSend} disabled={isLoading} />
    </div>
  );
}
