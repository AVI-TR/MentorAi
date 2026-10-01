import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Compass, Sparkles } from 'lucide-react';

export default function Navbar() {
  const location = useLocation();
  const isWelcome = location.pathname === '/';

  return (
    <header className="app-nav">
      <div className="nav-container">
        <Link to="/" className="nav-brand" aria-label="Mentor AI Home">
          <div className="nav-logo-icon">
            <Compass size={20} className="logo-svg" />
          </div>
          <div className="nav-brand-text">
            <span className="brand-name">Mentor AI</span>
            <span className="brand-tag">Career Navigator</span>
          </div>
        </Link>

        {!isWelcome && (
          <div className="nav-actions">
            <Link to="/" className="nav-subtle-link">
              Start Over
            </Link>
          </div>
        )}
      </div>
    </header>
  );
}
