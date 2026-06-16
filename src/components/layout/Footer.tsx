import './Footer.css';

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="container">
        <div className="footer__grid">
          <div className="footer__col footer__col--brand">
            <div className="footer__brand">
              <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
                <rect width="32" height="32" rx="8" fill="var(--color-primary)" />
                <path d="M8 16C8 11.58 11.58 8 16 8s8 3.58 8 8-3.58 8-8 8" stroke="#fff" strokeWidth="2.5" strokeLinecap="round" />
                <circle cx="16" cy="16" r="3" fill="#fff" />
              </svg>
              <span>UniPamplona</span>
            </div>
            <p className="footer__desc">
              Asistente virtual académico de la Universidad de Pamplona.
              Tu guía inteligente para información institucional.
            </p>
          </div>

          <div className="footer__col">
            <h4 className="footer__heading">Enlaces Rápidos</h4>
            <ul className="footer__list">
              <li><a href="https://www.unipamplona.edu.co" target="_blank" rel="noopener noreferrer">Portal Institucional</a></li>
              <li><a href="#categorias">Temas Frecuentes</a></li>
              <li><a href="#faq">FAQ</a></li>
              <li><a href="#chatbot">Consultar Chatbot</a></li>
              <li><a href="#contacto">Contacto</a></li>
            </ul>
          </div>

          <div className="footer__col">
            <h4 className="footer__heading">Servicios</h4>
            <ul className="footer__list">
              <li><a href="#categorias">Admisiones</a></li>
              <li><a href="#categorias">Matrícula</a></li>
              <li><a href="#categorias">Trámites</a></li>
              <li><a href="#categorias">Calendario Académico</a></li>
            </ul>
          </div>

          <div className="footer__col">
            <h4 className="footer__heading">Contacto</h4>
            <ul className="footer__list footer__list--contact">
              <li>📍 Pamplona, Norte de Santander</li>
              <li>📞 (607) 568 5303</li>
              <li>✉️ registro@unipamplona.edu.co</li>
              <li>🌐 www.unipamplona.edu.co</li>
            </ul>
          </div>
        </div>

        <div className="footer__bottom">
          <p>© {currentYear} Universidad de Pamplona. Todos los derechos reservados.</p>
          <p className="footer__credits">
            Asistente Virtual Académico — Proyecto Integrador
          </p>
        </div>
      </div>
    </footer>
  );
}
