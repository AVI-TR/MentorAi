import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { motion, useReducedMotion } from 'framer-motion';
import { Check } from 'lucide-react';

const STEPS = [
  { id: 'profile', label: 'Profile', path: '/profile' },
  { id: 'goal', label: 'Goal', path: '/goal' },
  { id: 'skills', label: 'Skills', path: '/skills' },
  { id: 'analysis', label: 'Analysis', path: '/analysis' },
  { id: 'roadmap', label: 'Roadmap', path: '/roadmap' },
];

export default function ProgressIndicator() {
  const location = useLocation();
  const navigate = useNavigate();
  const reduceMotion = useReducedMotion();
  const currentIndex = STEPS.findIndex((step) => step.path === location.pathname);
  if (currentIndex < 0) return null;

  return (
    <nav className="progress-container" aria-label="Onboarding progress">
      <div className="progress-track">
        <div className="progress-track-bg" />
        <motion.div
          className="progress-track-fill"
          initial={false}
          animate={{ width: `${(currentIndex / (STEPS.length - 1)) * 100}%` }}
          transition={{ duration: reduceMotion ? 0 : 0.24 }}
        />
        <div className="progress-steps">
          {STEPS.map((step, index) => {
            const completed = index < currentIndex;
            const current = index === currentIndex;
            return (
              <button
                key={step.id}
                type="button"
                className={`step-node ${current ? 'step-current' : ''} ${completed ? 'step-completed' : ''}`}
                onClick={() => index <= currentIndex && navigate(step.path)}
                disabled={index > currentIndex}
                aria-current={current ? 'step' : undefined}
              >
                <div className="step-badge">
                  {completed ? <Check size={14} /> : <span>{index + 1}</span>}
                </div>
                <span className="step-label">{step.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </nav>
  );
}
