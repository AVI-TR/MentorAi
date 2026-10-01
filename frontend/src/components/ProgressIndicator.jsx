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
  const shouldReduceMotion = useReducedMotion();

  // Find index of current step
  const currentIndex = STEPS.findIndex((s) => s.path === location.pathname);

  // If on welcome page (/), do not show or hide
  if (currentIndex === -1) {
    return null;
  }

  // Calculate percentage for the active connecting line
  const progressPercent = (currentIndex / (STEPS.length - 1)) * 100;

  return (
    <nav className="progress-container" aria-label="Onboarding Progress">
      <div className="progress-track">
        {/* Background track */}
        <div className="progress-track-bg" />

        {/* Animated fill line */}
        <motion.div
          className="progress-track-fill"
          initial={false}
          animate={{ width: `${progressPercent}%` }}
          transition={
            shouldReduceMotion
              ? { duration: 0 }
              : { duration: 0.4, ease: [0.16, 1, 0.3, 1] }
          }
        />

        {/* Step Nodes */}
        <div className="progress-steps">
          {STEPS.map((step, idx) => {
            const isCompleted = idx < currentIndex;
            const isCurrent = idx === currentIndex;
            const isUpcoming = idx > currentIndex;

            return (
              <button
                key={step.id}
                type="button"
                className={`step-node ${isCurrent ? 'step-current' : ''} ${
                  isCompleted ? 'step-completed' : ''
                } ${isUpcoming ? 'step-upcoming' : ''}`}
                onClick={() => {
                  // Allow navigation back to previous steps
                  if (idx <= currentIndex) {
                    navigate(step.path);
                  }
                }}
                disabled={isUpcoming}
                aria-current={isCurrent ? 'step' : undefined}
                aria-label={`${step.label} step ${idx + 1} of ${STEPS.length}${
                  isCompleted ? ' - completed' : isCurrent ? ' - current' : ''
                }`}
              >
                <div className="step-badge">
                  {isCompleted ? (
                    <motion.div
                      key="check"
                      initial={shouldReduceMotion ? false : { scale: 0.5, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ duration: 0.25 }}
                      className="step-check-icon"
                    >
                      <Check size={14} strokeWidth={2.6} />
                    </motion.div>
                  ) : (
                    <span className="step-number">{idx + 1}</span>
                  )}

                  {/* Active highlight ring */}
                  {isCurrent && (
                    <motion.div
                      layoutId="activeStepRing"
                      className="step-active-ring"
                      transition={
                        shouldReduceMotion
                          ? { duration: 0 }
                          : { type: 'spring', stiffness: 350, damping: 28 }
                      }
                    />
                  )}
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
