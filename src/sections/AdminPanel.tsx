import { useEffect, useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { api } from '../services/api';
import type { AdminCategory, AdminFAQ, AdminLog, AdminMetrics } from '../types';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import './AdminPanel.css';

const TOKEN_KEY = 'unipamplona_admin_token';
const ACCESS_KEY = 'unipamplona_admin_access';

export function AdminPanel() {
  const accessCodeEnv = import.meta.env.VITE_ADMIN_ACCESS_CODE || '';
  const [hasAccess, setHasAccess] = useState<boolean>(localStorage.getItem(ACCESS_KEY) === 'ok');
  const [accessCode, setAccessCode] = useState('');
  const [accessError, setAccessError] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem(TOKEN_KEY));
  const [email, setEmail] = useState('admin@unipamplona.edu.co');
  const [password, setPassword] = useState('');
  const [authError, setAuthError] = useState<string | null>(null);
  const [authLoading, setAuthLoading] = useState(false);

  const [categories, setCategories] = useState<AdminCategory[]>([]);
  const [selectedCategoryId, setSelectedCategoryId] = useState<string>('');
  const [faqs, setFaqs] = useState<AdminFAQ[]>([]);
  const [metrics, setMetrics] = useState<AdminMetrics | null>(null);
  const [logs, setLogs] = useState<AdminLog[]>([]);
  const [loadingDashboard, setLoadingDashboard] = useState(false);
  const [loadingFaqs, setLoadingFaqs] = useState(false);

  const [catForm, setCatForm] = useState({ slug: '', name: '', description: '', icon: '' });
  const [editingCategoryId, setEditingCategoryId] = useState<string | null>(null);

  const [faqForm, setFaqForm] = useState({
    question: '',
    answer: '',
    keywords: '',
    relatedTopics: '',
  });
  const [editingFaqId, setEditingFaqId] = useState<string | null>(null);

  const parsedKeywords = useMemo(
    () => faqForm.keywords.split(',').map((k) => k.trim()).filter(Boolean),
    [faqForm.keywords]
  );
  const parsedRelated = useMemo(
    () => faqForm.relatedTopics.split(',').map((k) => k.trim()).filter(Boolean),
    [faqForm.relatedTopics]
  );

  const loadDashboard = async (tokenValue: string) => {
    setLoadingDashboard(true);
    try {
      const [cats, metricsRes, logsRes] = await Promise.all([
        api.adminGetCategories(tokenValue),
        api.adminGetMetrics(tokenValue),
        api.adminGetLogs(tokenValue, 20),
      ]);
      setCategories(cats.categories);
      setMetrics(metricsRes.metrics);
      setLogs(logsRes.logs);

      if (cats.categories.length > 0 && !selectedCategoryId) {
        setSelectedCategoryId(cats.categories[0].id);
      }
    } finally {
      setLoadingDashboard(false);
    }
  };

  const loadFaqs = async (tokenValue: string, categoryId: string) => {
    if (!categoryId) return;
    setLoadingFaqs(true);
    try {
      const res = await api.adminGetFaqs(tokenValue, categoryId);
      setFaqs(res.faqs);
    } finally {
      setLoadingFaqs(false);
    }
  };

  useEffect(() => {
    if (token) {
      loadDashboard(token);
    }
  }, [token]);

  useEffect(() => {
    if (token && selectedCategoryId) {
      loadFaqs(token, selectedCategoryId);
    }
  }, [token, selectedCategoryId]);

  const handleLogin = async () => {
    setAuthLoading(true);
    setAuthError(null);
    try {
      const res = await api.adminLogin(email, password);
      localStorage.setItem(TOKEN_KEY, res.token);
      setToken(res.token);
    } catch (error) {
      setAuthError(error instanceof Error ? error.message : 'Error al iniciar sesión');
    } finally {
      setAuthLoading(false);
    }
  };

  const handleAccess = () => {
    if (!accessCodeEnv) {
      setAccessError('Falta configurar el código de acceso.');
      return;
    }

    if (accessCode.trim() !== accessCodeEnv) {
      setAccessError('Código de acceso inválido.');
      return;
    }

    localStorage.setItem(ACCESS_KEY, 'ok');
    setHasAccess(true);
    setAccessError(null);
  };

  const handleLogout = () => {
    localStorage.removeItem(TOKEN_KEY);
    setToken(null);
    setCategories([]);
    setFaqs([]);
    setMetrics(null);
    setLogs([]);
  };

  const handleSaveCategory = async () => {
    if (!token) return;
    if (!catForm.slug || !catForm.name) return;

    if (editingCategoryId) {
      await api.adminUpdateCategory(token, editingCategoryId, catForm);
    } else {
      await api.adminCreateCategory(token, catForm);
    }

    setCatForm({ slug: '', name: '', description: '', icon: '' });
    setEditingCategoryId(null);
    await loadDashboard(token);
  };

  const handleEditCategory = (category: AdminCategory) => {
    setEditingCategoryId(category.id);
    setCatForm({
      slug: category.slug,
      name: category.name,
      description: category.description || '',
      icon: category.icon || '',
    });
  };

  const handleDeleteCategory = async (id: string) => {
    if (!token) return;
    await api.adminDeleteCategory(token, id);
    if (selectedCategoryId === id) {
      setSelectedCategoryId('');
      setFaqs([]);
    }
    await loadDashboard(token);
  };

  const handleSaveFaq = async () => {
    if (!token || !selectedCategoryId) return;
    if (!faqForm.question || !faqForm.answer) return;

    const payload = {
      categoryId: selectedCategoryId,
      question: faqForm.question,
      answer: faqForm.answer,
      keywords: parsedKeywords,
      relatedTopics: parsedRelated,
    };

    if (editingFaqId) {
      await api.adminUpdateFaq(token, editingFaqId, payload);
    } else {
      await api.adminCreateFaq(token, payload);
    }

    setFaqForm({ question: '', answer: '', keywords: '', relatedTopics: '' });
    setEditingFaqId(null);
    await loadFaqs(token, selectedCategoryId);
  };

  const handleEditFaq = (faq: AdminFAQ) => {
    setEditingFaqId(faq.id);
    setFaqForm({
      question: faq.question,
      answer: faq.answer,
      keywords: faq.keywords.join(', '),
      relatedTopics: faq.relatedTopics.join(', '),
    });
  };

  const handleDeleteFaq = async (id: string) => {
    if (!token) return;
    await api.adminDeleteFaq(token, id);
    await loadFaqs(token, selectedCategoryId);
  };

  const activeCategory = categories.find((cat) => cat.id === selectedCategoryId);

  return (
    <section className="admin section" id="admin">
      <div className="container">
        <motion.div
          className="admin__header"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-80px' }}
          transition={{ duration: 0.6 }}
        >
          <span className="admin__label">Panel Administrativo</span>
          <h2 className="admin__title">Gestión de contenido y métricas</h2>
          <p className="admin__subtitle">
            Administra categorías, preguntas frecuentes y monitorea la actividad del chatbot.
          </p>
        </motion.div>

        {!hasAccess ? (
          <Card className="admin__login" padding="lg">
            <h3>Acceso restringido</h3>
            <p className="admin__hint">Ingresa el código de acceso para habilitar el panel.</p>
            <Input
              label="Código de acceso"
              type="password"
              value={accessCode}
              onChange={(e) => setAccessCode(e.target.value)}
            />
            {accessError && <p className="admin__error">{accessError}</p>}
            <Button variant="primary" onClick={handleAccess}>
              Validar acceso
            </Button>
          </Card>
        ) : !token ? (
          <Card className="admin__login" padding="lg">
            <h3>Acceso de administrador</h3>
            <div className="admin__login-grid">
              <Input label="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
              <Input
                label="Contraseña"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            {authError && <p className="admin__error">{authError}</p>}
            <Button variant="primary" onClick={handleLogin} isLoading={authLoading}>
              Ingresar
            </Button>
          </Card>
        ) : (
          <div className="admin__content">
            <div className="admin__toolbar">
              <div className="admin__badges">
                <Badge variant="primary">Acceso admin activo</Badge>
                {metrics && (
                  <Badge variant="outline">
                    {metrics.categories} categorías · {metrics.faqs} FAQs
                  </Badge>
                )}
              </div>
              <Button variant="ghost" onClick={handleLogout}>Cerrar sesión</Button>
            </div>

            {metrics && (
              <div className="admin__metrics">
                <Card className="admin__metric" padding="md">
                  <p>Categorías</p>
                  <h3>{metrics.categories}</h3>
                </Card>
                <Card className="admin__metric" padding="md">
                  <p>FAQs</p>
                  <h3>{metrics.faqs}</h3>
                </Card>
                <Card className="admin__metric" padding="md">
                  <p>Conversaciones</p>
                  <h3>{metrics.conversations}</h3>
                </Card>
                <Card className="admin__metric" padding="md">
                  <p>Mensajes</p>
                  <h3>{metrics.messages}</h3>
                </Card>
              </div>
            )}

            <div className="admin__grid">
              <Card className="admin__panel" padding="lg">
                <h3>Categorías</h3>
                <div className="admin__form">
                  <Input label="Slug" value={catForm.slug} onChange={(e) => setCatForm({ ...catForm, slug: e.target.value })} />
                  <Input label="Nombre" value={catForm.name} onChange={(e) => setCatForm({ ...catForm, name: e.target.value })} />
                  <Input label="Descripción" value={catForm.description} onChange={(e) => setCatForm({ ...catForm, description: e.target.value })} />
                  <Input label="Icono" value={catForm.icon} onChange={(e) => setCatForm({ ...catForm, icon: e.target.value })} />
                </div>
                <div className="admin__actions">
                  <Button variant="primary" onClick={handleSaveCategory}>
                    {editingCategoryId ? 'Actualizar categoría' : 'Crear categoría'}
                  </Button>
                  {editingCategoryId && (
                    <Button variant="ghost" onClick={() => {
                      setEditingCategoryId(null);
                      setCatForm({ slug: '', name: '', description: '', icon: '' });
                    }}>
                      Cancelar
                    </Button>
                  )}
                </div>

                <div className="admin__list">
                  {loadingDashboard && <p className="admin__loading">Cargando categorías...</p>}
                  {!loadingDashboard && categories.length === 0 && (
                    <p className="admin__empty">Aún no hay categorías. Crea la primera para empezar.</p>
                  )}
                  {categories.map((cat) => (
                    <div key={cat.id} className={`admin__list-item ${selectedCategoryId === cat.id ? 'is-active' : ''}`}>
                      <button onClick={() => setSelectedCategoryId(cat.id)}>
                        <span>{cat.icon || '📚'}</span>
                        <div>
                          <strong>{cat.name}</strong>
                          <small>{cat.slug}</small>
                        </div>
                      </button>
                      <div className="admin__list-actions">
                        <Button variant="ghost" onClick={() => handleEditCategory(cat)}>Editar</Button>
                        <Button variant="ghost" onClick={() => handleDeleteCategory(cat.id)}>Eliminar</Button>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>

              <Card className="admin__panel" padding="lg">
                <h3>FAQs</h3>
                {activeCategory && (
                  <p className="admin__hint">
                    Editando: <strong>{activeCategory.name}</strong>
                  </p>
                )}
                <div className="admin__form">
                  <Input label="Pregunta" value={faqForm.question} onChange={(e) => setFaqForm({ ...faqForm, question: e.target.value })} />
                  <Input label="Respuesta" value={faqForm.answer} onChange={(e) => setFaqForm({ ...faqForm, answer: e.target.value })} />
                  <Input label="Keywords (separadas por coma)" value={faqForm.keywords} onChange={(e) => setFaqForm({ ...faqForm, keywords: e.target.value })} />
                  <Input label="Related topics (separadas por coma)" value={faqForm.relatedTopics} onChange={(e) => setFaqForm({ ...faqForm, relatedTopics: e.target.value })} />
                </div>
                <div className="admin__actions">
                  <Button variant="primary" onClick={handleSaveFaq}>
                    {editingFaqId ? 'Actualizar FAQ' : 'Crear FAQ'}
                  </Button>
                  {editingFaqId && (
                    <Button variant="ghost" onClick={() => {
                      setEditingFaqId(null);
                      setFaqForm({ question: '', answer: '', keywords: '', relatedTopics: '' });
                    }}>
                      Cancelar
                    </Button>
                  )}
                </div>

                <div className="admin__list">
                  {loadingFaqs && <p className="admin__loading">Cargando FAQs...</p>}
                  {!loadingFaqs && faqs.length === 0 && (
                    <p className="admin__empty">No hay FAQs en esta categoría.</p>
                  )}
                  {faqs.map((faq) => (
                    <div key={faq.id} className="admin__faq-item">
                      <div>
                        <strong>{faq.question}</strong>
                        <p>{faq.answer}</p>
                        <div className="admin__tags">
                          {faq.keywords.map((k) => (
                            <span key={k}>{k}</span>
                          ))}
                        </div>
                      </div>
                      <div className="admin__list-actions">
                        <Button variant="ghost" onClick={() => handleEditFaq(faq)}>Editar</Button>
                        <Button variant="ghost" onClick={() => handleDeleteFaq(faq.id)}>Eliminar</Button>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            </div>

            <Card className="admin__panel admin__logs" padding="lg">
              <h3>Logs recientes</h3>
              <div className="admin__logs-grid">
                {loadingDashboard && <p className="admin__loading">Cargando logs...</p>}
                {!loadingDashboard && logs.length === 0 && (
                  <p className="admin__empty">No hay logs recientes.</p>
                )}
                {logs.map((log) => (
                  <div key={log.id} className="admin__log">
                    <span>{log.method} {log.url}</span>
                    <span>{log.status} · {log.durationMs}ms</span>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        )}
      </div>
    </section>
  );
}
