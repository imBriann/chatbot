import { motion } from 'framer-motion';
import { Button } from '../components/ui/Button';
import './Hero.css';

export function Hero() {
  return (
    <section className="hero" id="inicio">
      <div className="hero__bg">
        <div className="hero__orb hero__orb--1" />
        <div className="hero__orb hero__orb--2" />
        <div className="hero__orb hero__orb--3" />
        <div className="hero__grid-pattern" />
      </div>

      <div className="container hero__content">
        <motion.div
          className="hero__text"
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
        >
          <motion.div
            className="hero__badge"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
          >
            <span className="hero__badge-dot" />
            Asistente Virtual Activo
          </motion.div>

          <h1 className="hero__title">
            Tu guía académica
            <br />
            <span className="text-gradient">inteligente</span>
          </h1>

          <p className="hero__subtitle">
            Resuelve tus dudas sobre admisiones, matrícula, trámites y más.
            Información institucional precisa y al instante.
          </p>

          <div className="hero__actions">
            <Button
              variant="primary"
              size="lg"
              onClick={() => document.getElementById('chatbot')?.scrollIntoView({ behavior: 'smooth' })}
            >
              Iniciar Consulta
            </Button>
            <Button
              variant="outline"
              size="lg"
              onClick={() => document.getElementById('categorias')?.scrollIntoView({ behavior: 'smooth' })}
            >
              Ver Temas
            </Button>
          </div>

          <div className="hero__stats">
            <div className="hero__stat">
              <span className="hero__stat-value">27+</span>
              <span className="hero__stat-label">Temas disponibles</span>
            </div>
            <div className="hero__stat-divider" />
            <div className="hero__stat">
              <span className="hero__stat-value">6</span>
              <span className="hero__stat-label">Categorías</span>
            </div>
            <div className="hero__stat-divider" />
            <div className="hero__stat">
              <span className="hero__stat-value">24/7</span>
              <span className="hero__stat-label">Disponible</span>
            </div>
          </div>
        </motion.div>

        <motion.div
          className="hero__visual"
          initial={{ opacity: 0, x: 60 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.9, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
        >
          <div className="hero__card">
            <div className="hero__card-header">
              <div className="hero__card-dots">
                <span /><span /><span />
              </div>
              <span className="hero__card-title">Asistente UniPamplona</span>
            </div>
            <div className="hero__card-body">
              <div className="hero__card-msg hero__card-msg--bot">
                <p>¡Hola! 👋 Soy el asistente virtual. ¿En qué puedo ayudarte?</p>
              </div>
              <div className="hero__card-msg hero__card-msg--user">
                <p>¿Cuáles son los requisitos de admisión?</p>
              </div>
              <div className="hero__card-msg hero__card-msg--bot">
                <p>Para ingresar necesitas: título de bachiller, resultados ICFES, documento de identidad...</p>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
