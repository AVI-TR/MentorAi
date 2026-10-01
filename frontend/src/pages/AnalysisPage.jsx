import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, useReducedMotion } from 'framer-motion';
import {
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  AlertTriangle,
  Award,
  Target,
  Sparkles,
  BarChart3,
} from 'lucide-react';
import AnimatedPage from '../components/AnimatedPage';
import { useMentor } from '../context/MentorContext';

export default function AnalysisPage() {
  const navigate = useNavigate();
  const shouldReduceMotion = useReducedMotion();
  const { analysisResult, selectedCareer } = useMentor();

  const [displayPercent, setDisplayPercent] = useState(0);

  // If no analysis result is present, redirect to assessment
  useEffect(() => {
    if (!analysisResult) {
      navigate('/skills');
    }
  }, [analysisResult, navigate]);

  const targetPercent = analysisResult?.readiness_percent ?? 0;

  // Animate readiness percentage counting upward
  useEffect(() => {
    if (shouldReduceMotion) {
      setDisplayPercent(targetPercent);
      return;
    }

    let start = 0;
    const duration = 1200; // ms
    const startTime = performance.now();

    const animateCount = (now) => {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // Ease out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = eased * targetPercent;
      setDisplayPercent(current);

      if (progress < 1) {
        requestAnimationFrame(animateCount);
      } else {
        setDisplayPercent(targetPercent);
      }
    };

    const animId = requestAnimationFrame(animateCount);
    return () => cancelAnimationFrame(animId);
  }, [targetPercent, shouldReduceMotion]);

  if (!analysisResult) {
    return null;
  }

  const items = analysisResult.items || [];

  // Sort items: High priority / large gaps first, then met skills
  const sortedItems = [...items].sort((a, b) => {
    if (b.priority_score !== a.priority_score) {
      return b.priority_score - a.priority_score;
    }
    return b.gap - a.gap;
  });

  const getPriorityLabel = (item) => {
    if (item.gap === 0) return { label: 'Met', class: 'priority-met' };
    if (item.priority_score >= 8 || item.gap >= 3)
      return { label: 'High Priority', class: 'priority-high' };
    if (item.priority_score >= 4 || item.gap >= 2)
      return { label: 'Medium Priority', class: 'priority-medium' };
    return { label: 'Low Priority', class: 'priority-low' };
  };

  const getLevelLabel = (level) => {
    switch (level) {
      case 1:
        return '1 (Beginner)';
      case 2:
        return '2 (Basic)';
      case 3:
        return '3 (Intermediate)';
      case 4:
        return '4 (Advanced)';
      case 5:
        return '5 (Expert)';
      default:
        return '0 (Unassessed)';
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: shouldReduceMotion
        ? { duration: 0.1 }
        : { staggerChildren: 0.08, delayChildren: 0.1 },
    },
  };

  const itemVariants = {
    hidden: shouldReduceMotion ? { opacity: 0 } : { opacity: 0, y: 16 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.35, ease: 'easeOut' },
    },
  };

  return (
    <AnimatedPage className="form-page analysis-page-wrapper">
      <div className="flow-card analysis-card">
        {/* Header */}
        <div className="flow-header">
          <div className="assessment-meta-row">
            <span className="step-tag">Step 4 of 5</span>
            <span className="career-pill">
              {selectedCareer?.name || 'Target Career'}
            </span>
          </div>

          <h1 className="flow-title">Your Career Readiness & Skill Gaps</h1>
          <p className="flow-description">
            Here is your current alignment with the benchmark requirements for{' '}
            <strong>{selectedCareer?.name}</strong>.
          </p>
        </div>

        {/* Readiness Overview Panel */}
        <div className="readiness-summary-panel">
          <div className="readiness-metric-card">
            <div className="metric-header">
              <span className="metric-title">Career Readiness</span>
              <Award className="metric-icon" size={20} />
            </div>

            <div className="metric-value-row">
              <span className="metric-huge-number">
                {displayPercent.toFixed(1)}%
              </span>
              <span
                className={`readiness-pill ${
                  targetPercent >= 75
                    ? 'pill-high'
                    : targetPercent >= 45
                    ? 'pill-mid'
                    : 'pill-starter'
                }`}
              >
                {targetPercent >= 75
                  ? 'Strong Alignment'
                  : targetPercent >= 45
                  ? 'In Progress'
                  : 'Starting Out'}
              </span>
            </div>

            {/* Smooth Animated Progress Bar */}
            <div className="progress-bar-container">
              <motion.div
                className="progress-bar-fill"
                initial={shouldReduceMotion ? false : { width: '0%' }}
                animate={{ width: `${targetPercent}%` }}
                transition={
                  shouldReduceMotion
                    ? { duration: 0 }
                    : { duration: 1.1, ease: [0.16, 1, 0.3, 1] }
                }
              />
            </div>

            <div className="metric-footer-stats">
              <span>
                <strong>{analysisResult.skills_met}</strong> of{' '}
                <strong>{analysisResult.total_skills}</strong> skills met
              </span>
              <span>
                Target Track:{' '}
                <strong>{selectedCareer?.name || 'Selected'}</strong>
              </span>
            </div>
          </div>
        </div>

        {/* Staggered Skill Results List */}
        <div className="analysis-breakdown-section">
          <div className="breakdown-headline">
            <h2 className="breakdown-heading">Skill Evaluation Breakdown</h2>
            <span className="breakdown-subtext">
              Gaps indicate areas where further learning will elevate your
              readiness.
            </span>
          </div>

          <motion.div
            className="skill-results-grid"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
          >
            {sortedItems.map((item) => {
              const isMet = item.gap === 0;
              const isLargeGap = item.gap >= 2;
              const priority = getPriorityLabel(item);

              return (
                <motion.div
                  key={item.id || item.skill_id}
                  variants={itemVariants}
                  className={`skill-result-card ${
                    isMet ? 'card-skill-met' : ''
                  } ${isLargeGap ? 'card-large-gap' : ''}`}
                >
                  <div className="skill-card-main">
                    <div className="skill-title-group">
                      <div className="skill-tag-row">
                        <span className="skill-category-badge">
                          {item.skill?.category || 'General'}
                        </span>
                        <span className={`priority-tag ${priority.class}`}>
                          {priority.label}
                        </span>
                      </div>

                      <h3 className="result-skill-name">
                        {item.skill?.name || `Skill #${item.skill_id}`}
                      </h3>
                    </div>

                    {/* Gap Badge with Subtle Success/Emphasis Animation */}
                    <div className="gap-indicator-wrapper">
                      {isMet ? (
                        <motion.div
                          className="gap-badge gap-badge-met"
                          initial={shouldReduceMotion ? false : { scale: 0.9 }}
                          animate={{ scale: 1 }}
                          transition={{ duration: 0.25 }}
                        >
                          <CheckCircle2 size={16} />
                          <span>Met</span>
                        </motion.div>
                      ) : (
                        <div
                          className={`gap-badge ${
                            isLargeGap ? 'gap-badge-large' : 'gap-badge-regular'
                          }`}
                        >
                          <AlertTriangle size={15} />
                          <span>Gap: -{item.gap}</span>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Level Comparison */}
                  <div className="level-comparison-box">
                    <div className="level-row">
                      <span className="level-label">Current Level:</span>
                      <span className="level-value student-val">
                        {getLevelLabel(item.student_level)}
                      </span>
                    </div>

                    <div className="level-row">
                      <span className="level-label">Required Level:</span>
                      <span className="level-value required-val">
                        {getLevelLabel(item.required_level)}
                      </span>
                    </div>

                    {/* Mini Visual Gauge */}
                    <div className="mini-gauge-track">
                      {/* Required Marker */}
                      <div
                        className="gauge-benchmark-marker"
                        style={{ left: `${(item.required_level / 5) * 100}%` }}
                        title={`Required: Level ${item.required_level}`}
                      />
                      {/* Current Level Fill */}
                      <motion.div
                        className={`mini-gauge-fill ${
                          isMet ? 'fill-met' : 'fill-gap'
                        }`}
                        initial={
                          shouldReduceMotion ? false : { width: '0%' }
                        }
                        animate={{
                          width: `${(item.student_level / 5) * 100}%`,
                        }}
                        transition={
                          shouldReduceMotion
                            ? { duration: 0 }
                            : { duration: 0.6, ease: 'easeOut', delay: 0.2 }
                        }
                      />
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </motion.div>
        </div>

        {/* Action Controls */}
        <div className="form-actions">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => navigate('/skills')}
          >
            <ArrowLeft size={16} />
            <span>Adjust Skills</span>
          </button>

          <button
            type="button"
            className="btn btn-primary btn-glow"
            onClick={() => navigate('/roadmap')}
            id="continue-roadmap-btn"
          >
            <span>View Next Steps</span>
            <ArrowRight size={16} />
          </button>
        </div>
      </div>
    </AnimatedPage>
  );
}
