import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, useReducedMotion } from 'framer-motion';
import { Compass, ArrowLeft, RotateCcw } from 'lucide-react';
import AnimatedPage from '../components/AnimatedPage';
import { useMentor } from '../context/MentorContext';

export default function RoadmapPage() {
  const navigate = useNavigate();
  const reduceMotion = useReducedMotion();
  const { selectedCareer, analysisResult } = useMentor();
  return (
    <AnimatedPage className="form-page">
      <motion.div
        className="flow-card roadmap-card"
        initial={{ opacity: 0, y: reduceMotion ? 0 : 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: reduceMotion ? 0 : 0.24 }}
      >
        <div className="flow-header">
          <span className="step-tag">Step 5 of 5</span>
          <h1 className="flow-title">Your starting point is ready.</h1>
          <p className="flow-description">Your personalized roadmap is the next step.</p>
        </div>
        <div className="roadmap-hero-box">
          <div className="roadmap-box-inner">
            <div className="roadmap-icon-sphere"><Compass size={32} /></div>
            <h2 className="roadmap-feature-title">Personalized Roadmap</h2>
            <div className="roadmap-status-pill"><span>Coming Next</span></div>
            <p className="roadmap-box-desc">
              A future version will turn your assessed gaps into milestones, learning resources, and practice plans for <strong>{selectedCareer?.name || 'your target career'}</strong>.
            </p>
            {analysisResult && (
              <div className="roadmap-summary-snippet">
                <div className="snippet-item"><span className="snippet-num">{analysisResult.readiness_percent.toFixed(0)}%</span><span className="snippet-label">Current readiness</span></div>
                <div className="snippet-divider" />
                <div className="snippet-item"><span className="snippet-num">{analysisResult.total_skills - analysisResult.skills_met}</span><span className="snippet-label">Skills with gaps</span></div>
              </div>
            )}
          </div>
        </div>
        <div className="form-actions">
          <button type="button" className="btn btn-secondary" onClick={() => navigate('/analysis')}><ArrowLeft size={16} /> Review analysis</button>
          <button type="button" className="btn btn-primary" onClick={() => navigate('/')}><RotateCcw size={16} /> Start fresh</button>
        </div>
      </motion.div>
    </AnimatedPage>
  );
}
