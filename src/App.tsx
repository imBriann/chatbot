import { useEffect, useState } from 'react';
import { Navbar } from './components/layout/Navbar';
import { Footer } from './components/layout/Footer';
import { Hero } from './sections/Hero';
import { ChatSection } from './sections/ChatSection';
import { Categories } from './sections/Categories';
import { FAQSection } from './sections/FAQ';
import { Contact } from './sections/Contact';
import { AdminPanel } from './sections/AdminPanel';

function App() {
  const [showAdmin, setShowAdmin] = useState(false);

  useEffect(() => {
    const update = () => setShowAdmin(window.location.hash === '#admin');
    update();
    window.addEventListener('hashchange', update);
    return () => window.removeEventListener('hashchange', update);
  }, []);

  if (showAdmin) {
    return (
      <main>
        <AdminPanel />
      </main>
    );
  }

  return (
    <>
      <Navbar />
      <main>
        <Hero />
        <ChatSection />
        <Categories />
        <FAQSection />
        <Contact />
      </main>
      <Footer />
    </>
  );
}

export default App;
