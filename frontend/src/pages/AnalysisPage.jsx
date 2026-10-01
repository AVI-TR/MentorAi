import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { animate, motion, useMotionValue, useReducedMotion, useTransform } from 'framer-motion';
import { ArrowLeft, ArrowRight, CheckCircle2, AlertTriangle, Award } from 'lucide-react';
import AnimatedPage from '../components/AnimatedPage';
import { useMentor } from '../context/useMentor';

const levelLabel = (level) => ({
  0: '0 (No experience)', 1: '1 (Beginner)', 2: '2 (Basic)',
  3: '3 (Working)', 4: '4 (Proficient)', 5: '5 (Expert)',
}[level] || '0 (No experience)');

export default function AnalysisPage() {
  const navigate = useNavigate();
  const reduceMotion = useReducedMotion();
  const { analysisResult, selectedCareer, sessionLoading, sessionError, restoreSession } = useMentor();
  const readinessValue = useMotionValue(0);
  const displayPercent = useTransform(readinessValue, (value) => `${value.toFixed(1)}%`);

  useEffect(() => {
    if (!sessionLoading && !analysisResult) navigate('/skills', { replace: true });
  }, [analysisResult, sessionLoading, navigate]);

  useEffect(() => {
    const target = analysisResult?.readiness_percent ?? 0;
    readinessValue.set(0);
    if (reduceMotion) {
      readinessValue.set(target);
      return undefined;
    }
    const controls = animate(readinessValue, target, { duration: 0.28, ease: 'easeOut' });
    return () => controls.stop();
  }, [analysisResult?.readiness_percent, reduceMotion, readinessValue]);

  if (sessionLoading || !analysisResult) {
    return (
      <AnimatedPage className="form-page">
        <div className="flow-card">
          <div className="skeleton-stack">
            <div className="skeleton skeleton-title" />
            <div className="skeleton skeleton-card" />
            <div className="skeleton skeleton-card" />
          </div>
        </div>
      </AnimatedPage>
    );
  }

  const items = [...(analysisResult.items || [])].sort(
    (a, b) => b.priority_score - a.priority_score || b.gap - a.gap,
  );

  return (
    <AnimatedPage className="form-page">
      <div className="flow-card analysis-card">
        <div className="flow-header">
          <span className="step-tag">Step 4 of 5</span>
          <h1 className="flow-title">Your career readiness</h1>
          <p className="flow-description">A transparent comparison between your self-assessment and the selected career benchmark.</p>
        </div>

        {sessionError && (
          <div className="form-alert form-alert-error" role="alert">
            <span>{sessionError}</span>
            <button className="btn btn-secondary" type="button" onClick={restoreSession}>Retry</button>
          </div>
        )}

        <div className="readiness-summary-panel">
          <div className="readiness-metric-card">
            <div className="metric-header">
              <span className="metric-title">Career Readiness</span><Award className="metric-icon" size={20} />
            </div>
            <div className="metric-value-row"><motion.span className="metric-huge-number">{displayPercent}</motion.span></div>
            <div className="progress-bar-container">
              <motion.div
                className="progress-bar-fill"
                initial={reduceMotion ? false : { width: '0%' }}
                animate={{ width: `${analysisResult.readiness_percent}%` }}
                transition={{ duration: reduceMotion ? 0 : 0.28 }}
              />
            </div>
            <div className="metric-footer-stats">
              <span><strong>{analysisResult.skills_met}</strong> of <strong>{analysisResult.total_skills}</strong> skills met</span>
              <span>{selectedCareer?.name || 'Selected career'}</span>
            </div>
          </div>
        </div>

        <div className="analysis-breakdown-section">
          <div className="breakdown-headline">
            <h2 className="breakdown-heading">Skill evaluation</h2>
            <span className="breakdown-subtext">Priority score = gap × weight.</span>
          </div>

          <motion.div
            className="skill-results-grid"
            initial="hidden"
            animate="visible"
            variants={{ visible: { transition: { staggerChildren: reduceMotion ? 0 : 0.05 } } }}
          >
            {items.map((item) => (
              <motion.div
                key={item.id}
                className={`skill-result-card ${item.gap === 0 ? 'card-skill-met' : ''}`}
                variants={{
                  hidden: { opacity: 0, y: reduceMotion ? 0 : 8 },
                  visible: { opacity: 1, y: 0 },
                }}
                transition={{ duration: reduceMotion ? 0 : 0.24 }}
              >
                <div className="skill-card-main">
                  <div>
                    <span className="skill-category-badge">{item.skill?.category || 'General'}</span>
                    <h3 className="result-skill-name">{item.skill?.name || `Skill #${item.skill_id}`}</h3>
                  </div>
                  {item.gap === 0 ? (
                    <span className="gap-badge gap-badge-met"><CheckCircle2 size={16} /> Met</span>
                  ) : (
                    <span className="gap-badge gap-badge-regular"><AlertTriangle size={15} /> Gap: -{item.gap}</span>
                  )}
                </div>
                <div className="level-comparison-box">
                  <div className="level-row"><span className="level-label">Current</span><span className="level-value student-val">{levelLabel(item.student_level)}</span></div>
                  <div className="level-row"><span className="level-label">Required</span><span className="level-value required-val">{levelLabel(item.required_level)}</span></div>
                  <div className="mini-gauge-track">
                    <div className="gauge-benchmark-marker" style={{ left: `${(item.required_level / 5) * 100}%` }} />
                    <motion.div className={`mini-gauge-fill ${item.gap === 0 ? 'fill-met' : 'fill-gap'}`} initial={{ width: '0%' }} animate={{ width: `${(item.student_level / 5) * 100}%` }} transition={{ duration: reduceMotion ? 0 : 0.24 }} />
                  </div>
                  <span className="form-hint">Priority score: {item.priority_score}</span>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>

        <div className="form-actions">
          <button type="button" className="btn btn-secondary" onClick={() => navigate('/skills')}><ArrowLeft size={16} /> Adjust skills</button>
          <button type="button" className="btn btn-primary" onClick={() => navigate('/roadmap')}><span>Continue</span><ArrowRight size={16} /></button>
        </div>
      </div>
    </AnimatedPage>
  );
}
