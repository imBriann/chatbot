import { useEffect, useRef } from 'react';
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
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const didLoad = useRef(false);

  useEffect(() => {
    if (!didLoad.current) {
      didLoad.current = true;
      loadHistory();
    }
  }, [loadHistory]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSend = (content: string) => {
    sendMessage(content);
  };

  const isEmpty = messages.length === 0;

  return (
    <div className="chat-window">
      {/* Header */}
      <div className="chat-window__header">
        <div className="chat-window__header-info">
          <div className="chat-window__status">
            <span className="chat-window__status-dot" />
            En línea
          </div>
          <h3 className="chat-window__title">Asistente Virtual</h3>
        </div>
        <button className="chat-window__clear" onClick={clearChat} title="Limpiar conversación">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="3 6 5 6 21 6" />
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
          </svg>
        </button>
      </div>

      {/* Messages Area */}
      <div className="chat-window__messages">
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
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <ChatInput onSend={handleSend} disabled={isLoading} />
    </div>
  );
}
