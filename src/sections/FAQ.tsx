import { useEffect, useMemo, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import type { Category, FAQ } from '../types';
import { api } from '../services/api';
import { Input } from '../components/ui/Input';
import { Spinner } from '../components/ui/Spinner';
import { Badge } from '../components/ui/Badge';
import { Card } from '../components/ui/Card';
import './FAQ.css';

export function FAQSection() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [activeCategory, setActiveCategory] = useState<string>('');
  const [faqs, setFaqs] = useState<FAQ[]>([]);
  const [query, setQuery] = useState('');
  const [openIndex, setOpenIndex] = useState<number | null>(0);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    api.getCategories()
      .then((res) => {
        const list = res.categories || [];
        setCategories(list);
        if (list.length > 0) {
          setActiveCategory(list[0].slug);
        }
      })
      .catch(() => {
        setCategories([]);
      });
  }, []);

  useEffect(() => {
    if (!activeCategory) return;
    setIsLoading(true);
    api.getFAQs(activeCategory)
      .then((res) => {
        setFaqs(res.faqs || []);
        setOpenIndex(0);
      })
      .catch(() => setFaqs([]))
      .finally(() => setIsLoading(false));
  }, [activeCategory]);

  const filteredFaqs = useMemo(() => {
    const term = query.trim().toLowerCase();
    if (!term) return faqs;
    return faqs.filter((f) =>
      f.question.toLowerCase().includes(term) || f.answer.toLowerCase().includes(term)
    );
  }, [faqs, query]);

  return (
    <section className="faq section" id="faq">
      <div className="container">
        <motion.div
          className="faq__header"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-80px' }}
          transition={{ duration: 0.6 }}
        >
          <span className="faq__label">Preguntas Frecuentes</span>
          <h2 className="faq__title">
            Respuestas rápidas para tus <span className="text-gradient">dudas</span>
          </h2>
          <p className="faq__subtitle">
            Explora las preguntas más consultadas por categoría o busca una respuesta específica
          </p>
        </motion.div>

        <motion.div
          className="faq__controls"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.6, delay: 0.1 }}
        >
          <div className="faq__categories">
            {categories.map((cat) => {
              const isActive = cat.slug === activeCategory;
              return (
                <button
                  key={cat.slug}
                  className={`faq__category ${isActive ? 'faq__category--active' : ''}`}
                  onClick={() => setActiveCategory(cat.slug)}
                >
                  <Badge variant={isActive ? 'primary' : 'outline'} size="sm">
                    {cat.icon} {cat.name}
                  </Badge>
                </button>
              );
            })}
          </div>

          <div className="faq__search">
            <Input
              placeholder="Buscar en preguntas frecuentes"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              aria-label="Buscar preguntas frecuentes"
            />
          </div>
        </motion.div>

        <motion.div
          className="faq__content"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.6, delay: 0.15 }}
        >
          <Card className="faq__card" padding="lg">
            {isLoading ? (
              <div className="faq__loading">
                <Spinner size="md" />
                <p>Cargando preguntas...</p>
              </div>
            ) : filteredFaqs.length === 0 ? (
              <div className="faq__empty">
                <div className="faq__empty-icon">🔍</div>
                <p>No encontramos resultados. Intenta con otra palabra o categoría.</p>
              </div>
            ) : (
              <div className="faq__list">
                {filteredFaqs.map((faq, index) => {
                  const isOpen = openIndex === index;
                  return (
                    <div key={faq.question} className={`faq-item ${isOpen ? 'is-open' : ''}`}>
                      <button
                        className="faq-item__question"
                        onClick={() => setOpenIndex(isOpen ? null : index)}
                      >
                        <span>{faq.question}</span>
                        <span className="faq-item__icon">{isOpen ? '−' : '+'}</span>
                      </button>
                      <AnimatePresence initial={false}>
                        {isOpen && (
                          <motion.div
                            className="faq-item__answer"
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: 'auto', opacity: 1 }}
                            exit={{ height: 0, opacity: 0 }}
                            transition={{ duration: 0.3 }}
                          >
                            <p>{faq.answer}</p>
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>
                  );
                })}
              </div>
            )}
          </Card>
        </motion.div>
      </div>
    </section>
  );
}
