import { motion } from 'framer-motion';
import { ChatWindow } from '../components/chat/ChatWindow';
import './ChatSection.css';

export function ChatSection() {
  return (
    <section className="chat-section section" id="chatbot">
      <div className="container">
        <motion.div
          className="chat-section__header"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-80px' }}
          transition={{ duration: 0.6 }}
        >
          <span className="chat-section__label">Chatbot Académico</span>
          <h2 className="chat-section__title">
            Haz tu <span className="text-gradient">consulta</span>
          </h2>
          <p className="chat-section__subtitle">
            Escribe tu pregunta y obtén respuestas inmediatas sobre información académica institucional
          </p>
        </motion.div>

        <motion.div
          className="chat-section__window"
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.7, delay: 0.15 }}
        >
          <ChatWindow />
        </motion.div>
      </div>
    </section>
  );
}
