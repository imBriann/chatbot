import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import type { Category } from '../types';
import { api } from '../services/api';
import './Categories.css';

export function Categories() {
  const [categories, setCategories] = useState<Category[]>([]);

  useEffect(() => {
    api.getCategories()
      .then((res) => setCategories(res.categories || []))
      .catch(() => {});
  }, []);

  const container = {
    hidden: {},
    show: { transition: { staggerChildren: 0.08 } },
  };

  const item = {
    hidden: { opacity: 0, y: 24 },
    show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] as any } },
  };

  return (
    <section className="categories section" id="categorias">
      <div className="container">
        <motion.div
          className="categories__header"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-80px' }}
          transition={{ duration: 0.6 }}
        >
          <span className="categories__label">Temas de Consulta</span>
          <h2 className="categories__title">
            ¿Sobre qué necesitas <span className="text-gradient">información</span>?
          </h2>
          <p className="categories__subtitle">
            Explora las categorías más consultadas por los estudiantes de la Universidad de Pamplona
          </p>
        </motion.div>

        <motion.div
          className="categories__grid"
          variants={container}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, margin: '-60px' }}
        >
          {categories.map((cat) => (
            <motion.a
              key={cat.slug}
              href="#chatbot"
              className="category-card"
              variants={item}
              whileHover={{ y: -4, scale: 1.02 }}
              transition={{ type: 'spring', stiffness: 300, damping: 20 }}
            >
              <div className="category-card__icon">{cat.icon}</div>
              <h3 className="category-card__name">{cat.name}</h3>
              <p className="category-card__desc">{cat.description}</p>
              <span className="category-card__count">{cat.faqCount} preguntas frecuentes</span>
            </motion.a>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
