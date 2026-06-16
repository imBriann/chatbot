import { motion } from 'framer-motion';
import './Contact.css';

const CONTACTS = [
  {
    icon: '📍',
    title: 'Dirección',
    detail: 'Km 1 Vía Bucaramanga, Pamplona, Norte de Santander, Colombia',
  },
  {
    icon: '📞',
    title: 'Teléfono',
    detail: '(607) 568 5303',
    href: 'tel:+576075685303',
  },
  {
    icon: '✉️',
    title: 'Correo Electrónico',
    detail: 'registro@unipamplona.edu.co',
    href: 'mailto:registro@unipamplona.edu.co',
  },
  {
    icon: '🌐',
    title: 'Portal Web',
    detail: 'www.unipamplona.edu.co',
    href: 'https://www.unipamplona.edu.co',
  },
];

export function Contact() {
  return (
    <section className="contact section" id="contacto">
      <div className="container">
        <motion.div
          className="contact__header"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-80px' }}
          transition={{ duration: 0.6 }}
        >
          <span className="contact__label">Soporte Institucional</span>
          <h2 className="contact__title">
            ¿Necesitas más <span className="text-gradient">ayuda</span>?
          </h2>
          <p className="contact__subtitle">
            Si no encontraste la respuesta que buscabas, contacta directamente con las dependencias de la universidad
          </p>
        </motion.div>

        <motion.div
          className="contact__grid"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.6, delay: 0.15 }}
        >
          {CONTACTS.map((c) => (
            <div key={c.title} className="contact-card">
              <div className="contact-card__icon">{c.icon}</div>
              <h3 className="contact-card__title">{c.title}</h3>
              {c.href ? (
                <a href={c.href} className="contact-card__detail" target="_blank" rel="noopener noreferrer">
                  {c.detail}
                </a>
              ) : (
                <p className="contact-card__detail">{c.detail}</p>
              )}
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
