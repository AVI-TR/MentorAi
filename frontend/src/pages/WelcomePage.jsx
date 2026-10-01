import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, Compass } from 'lucide-react';
import { motion, useReducedMotion } from 'framer-motion';
import AnimatedPage from '../components/AnimatedPage';
import { useMentor } from '../context/MentorContext';

export default function WelcomePage() {
  const navigate = useNavigate();
  const reduceMotion = useReducedMotion();
  const { resetSession } = useMentor();

  const start = () => {
    resetSession();
    navigate('/profile');
  };

  return (
    <AnimatedPage className="welcome-page">
      <motion.div
        className="welcome-card"
        initial={{ opacity: 0, y: reduceMotion ? 0 : 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: reduceMotion ? 0 : 0.24 }}
      >
        <div className="welcome-badge"><Compass size={16} /> AI Career Mentorship</div>
        <h1 className="welcome-title">Welcome to <span className="highlight-gradient">Mentor AI</span></h1>
        <p className="welcome-tagline">Your personalized path from where you are now to where you want to be.</p>
        <button type="button" className="btn btn-primary btn-large" onClick={start} id="get-started-button">
          Get Started <ArrowRight size={18} />
        </button>
      </motion.div>
    </AnimatedPage>
  );
}
