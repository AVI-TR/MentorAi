import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, useReducedMotion } from 'framer-motion';
import { ArrowRight, Compass, Target, CheckCircle2, TrendingUp } from 'lucide-react';
import AnimatedPage from '../components/AnimatedPage';

export default function WelcomePage() {
  const navigate = useNavigate();
  const shouldReduceMotion = useReducedMotion();

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: shouldReduceMotion
        ? { duration: 0.1 }
        : { staggerChildren: 0.12, delayChildren: 0.08 },
    },
  };

  const itemVariants = {
    hidden: shouldReduceMotion ? { opacity: 0 } : { opacity: 0, y: 16 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.38, ease: 'easeOut' },
    },
  };

  return (
    <AnimatedPage className="welcome-page">
      {/* Lightweight subtle ambient background glow */}
      <div className="ambient-background" aria-hidden="true">
        <motion.div
          className="ambient-orb orb-1"
          animate={
            shouldReduceMotion
              ? {}
              : {
                  scale: [1, 1.08, 1],
                  opacity: [0.18, 0.28, 0.18],
                }
          }
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
        <motion.div
          className="ambient-orb orb-2"
          animate={
            shouldReduceMotion
              ? {}
              : {
                  scale: [1, 1.12, 1],
                  opacity: [0.12, 0.22, 0.12],
                }
          }
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
      </div>

      <motion.div
        className="welcome-card"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <motion.div className="welcome-badge-wrapper" variants={itemVariants}>
          <div className="welcome-badge">
            <Compass size={16} className="badge-icon" />
            <span>AI Career Mentorship</span>
          </div>
        </motion.div>

        <motion.h1 className="welcome-title" variants={itemVariants}>
          Welcome to <span className="highlight-gradient">Mentor AI</span>
        </motion.h1>

        <motion.p className="welcome-tagline" variants={itemVariants}>
          Your personalized path from where you are now to where you want to be.
        </motion.p>

        <motion.div className="welcome-highlights" variants={itemVariants}>
          <div className="highlight-item">
            <div className="highlight-icon-wrap">
              <Target size={18} />
            </div>
            <div>
              <strong>Target Career Roles</strong>
              <p>Explore industry-standard roles and benchmarks</p>
            </div>
          </div>

          <div className="highlight-item">
            <div className="highlight-icon-wrap">
              <CheckCircle2 size={18} />
            </div>
            <div>
              <strong>Intuitive Self-Assessment</strong>
              <p>Calibrate your current proficiency honestly and simply</p>
            </div>
          </div>

          <div className="highlight-item">
            <div className="highlight-icon-wrap">
              <TrendingUp size={18} />
            </div>
            <div>
              <strong>Instant Readiness Analysis</strong>
              <p>Uncover exact skill gaps and focused priorities</p>
            </div>
          </div>
        </motion.div>

        <motion.div className="welcome-actions" variants={itemVariants}>
          <button
            type="button"
            className="btn btn-primary btn-large btn-glow"
            onClick={() => navigate('/profile')}
            id="get-started-button"
          >
            <span>Get Started</span>
            <ArrowRight size={18} className="btn-arrow" />
          </button>
        </motion.div>
      </motion.div>
    </AnimatedPage>
  );
}
