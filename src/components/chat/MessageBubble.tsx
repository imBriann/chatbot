import { motion } from 'framer-motion';
import type { ChatMessage } from '../../types';
import './MessageBubble.css';

interface MessageBubbleProps {
  message: ChatMessage;
}

function formatTime(dateStr: string): string {
  try {
    const d = new Date(dateStr);
    return d.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' });
  } catch {
    return '';
  }
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';

  return (
    <motion.div
      className={`message ${isUser ? 'message--user' : 'message--bot'}`}
      initial={{ opacity: 0, y: 12, scale: 0.97 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
    >
      {!isUser && <div className="message__avatar">🤖</div>}
      <div className="message__content">
        <div className="message__bubble">
          <p className="message__text">{message.content}</p>
        </div>
        <span className="message__time">{formatTime(message.createdAt)}</span>
      </div>
    </motion.div>
  );
}
