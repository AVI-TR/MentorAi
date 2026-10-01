import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, useReducedMotion } from 'framer-motion';
import {
  Compass,
  ArrowLeft,
  Sparkles,
  Milestone,
  CheckCircle2,
  Layers,
  RotateCcw,
} from 'lucide-react';
import AnimatedPage from '../components/AnimatedPage';
import { useMentor } from '../context/MentorContext';

export default function RoadmapPage() {
  const navigate = useNavigate();
  const shouldReduceMotion = useReducedMotion();
  const { selectedCareer, analysisResult } = useMentor();

  const containerVariants = {
    hidden: { opacity: 0, y: shouldReduceMotion ? 0 : 16 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: shouldReduceMotion ? 0.1 : 0.4,
        ease: 'easeOut',
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: shouldReduceMotion ? 0 : 10 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.3 },
    },
  };

  return (
    <AnimatedPage className="form-page roadmap-page-wrapper">
      <motion.div
        className="flow-card roadmap-card"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <motion.div className="flow-header text-center" variants={itemVariants}>
          <span className="step-tag">Step 5 of 5</span>
          <div className="roadmap-badge-pill">
            <Milestone size={16} />
            <span>Coming Next</span>
          </div>

          <h1 className="flow-title">Your starting point is ready.</h1>
          <p className="flow-description text-center max-w-lg mx-auto">
            Mentor has identified the skills you should focus on.
          </p>
        </motion.div>

        {/* Placeholder Feature Card */}
        <motion.div className="roadmap-hero-box" variants={itemVariants}>
          <div className="roadmap-box-glow" />
          <div className="roadmap-box-inner">
            <div className="roadmap-icon-sphere">
              <Compass size={32} className="compass-icon" />
            </div>

            <h2 className="roadmap-feature-title">Personalized Roadmap</h2>

            <div className="roadmap-status-pill">
              <span className="status-dot-pulse" />
              <span>Coming Next</span>
            </div>

            <p className="roadmap-box-desc">
              Next-generation step-by-step milestones, curated learning resources,
              and focused practice plans calibrated specifically for your{' '}
              <strong>{selectedCareer?.name || 'target career'}</strong> track.
            </p>

            {analysisResult && (
              <div className="roadmap-summary-snippet">
                <div className="snippet-item">
                  <span className="snippet-num">{analysisResult.readiness_percent.toFixed(0)}%</span>
                  <span className="snippet-label">Current Readiness</span>
                </div>
                <div className="snippet-divider" />
                <div className="snippet-item">
                  <span className="snippet-num">{analysisResult.total_skills - analysisResult.skills_met}</span>
                  <span className="snippet-label">Skills to Master</span>
                </div>
              </div>
            )}
          </div>
        </motion.div>

        {/* Actions */}
        <motion.div className="form-actions roadmap-actions" variants={itemVariants}>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => navigate('/analysis')}
          >
            <ArrowLeft size={16} />
            <span>Review Analysis</span>
          </button>

          <button
            type="button"
            className="btn btn-primary"
            onClick={() => navigate('/')}
          >
            <RotateCcw size={16} />
            <span>Start Fresh</span>
          </button>
        </motion.div>
      </motion.div>
    </AnimatedPage>
  );
}
