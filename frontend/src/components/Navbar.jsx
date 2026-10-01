import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Compass } from 'lucide-react';
import { useMentor } from '../context/MentorContext';

export default function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { resetSession } = useMentor();
  const isWelcome = location.pathname === '/';

  const startOver = () => {
    resetSession();
    navigate('/');
  };

  return (
    <header className="app-nav">
      <div className="nav-container">
        <Link to="/" className="nav-brand" aria-label="Mentor AI Home">
          <div className="nav-logo-icon"><Compass size={20} /></div>
          <div className="nav-brand-text">
            <span className="brand-name">Mentor AI</span>
            <span className="brand-tag">Career Navigator</span>
          </div>
        </Link>
        {!isWelcome && (
          <button type="button" className="nav-subtle-link" onClick={startOver}>Start Over</button>
        )}
      </div>
    </header>
  );
}
