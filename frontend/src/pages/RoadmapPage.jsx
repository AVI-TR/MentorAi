import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, useReducedMotion } from 'framer-motion';
import { ArrowLeft, RotateCcw, CheckCircle2, Circle, Clock3, Compass } from 'lucide-react';
import AnimatedPage from '../components/AnimatedPage';
import { useMentor } from '../context/useMentor';

const STATUS_OPTIONS = [
  { value: 'todo', label: 'To do', icon: Circle },
  { value: 'in_progress', label: 'In progress', icon: Clock3 },
  { value: 'done', label: 'Done', icon: CheckCircle2 },
];

export default function RoadmapPage() {
  const navigate = useNavigate();
  const reduceMotion = useReducedMotion();
  const { selectedCareer, roadmap, isLoadingRoadmap, roadmapError, updateRoadmapItem, resetSession } = useMentor();

  if (isLoadingRoadmap || !roadmap) {
    return (
      <AnimatedPage className="form-page">
        <motion.div className="flow-card roadmap-card" initial={{ opacity: 0, y: reduceMotion ? 0 : 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: reduceMotion ? 0 : 0.24 }}>
          <div className="flow-header">
            <span className="step-tag">Step 5 of 5</span>
            <h1 className="flow-title">Building your roadmap</h1>
            <p className="flow-description">Turning your skill gaps into a deterministic learning sequence for {selectedCareer?.name || 'your target career'}.</p>
          </div>
          {roadmapError && <div className="form-alert form-alert-error" role="alert">{roadmapError}</div>}
          <div className="skeleton-stack" aria-label="Loading roadmap">
            <div className="skeleton skeleton-title" />
            <div className="skeleton skeleton-card" />
            <div className="skeleton skeleton-card" />
          </div>
        </motion.div>
      </AnimatedPage>
    );
  }

  const percent = roadmap.percent ?? 0;
  return (
    <AnimatedPage className="form-page">
      <motion.div className="flow-card roadmap-card" initial={{ opacity: 0, y: reduceMotion ? 0 : 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: reduceMotion ? 0 : 0.24 }}>
        <div className="flow-header">
          <span className="step-tag">Step 5 of 5</span>
          <h1 className="flow-title">Your learning roadmap</h1>
          <p className="flow-description">A deterministic sequence built from your assessed gaps for <strong>{selectedCareer?.name || 'your target career'}</strong>.</p>
        </div>

        <div className="readiness-summary-panel">
          <div className="readiness-metric-card">
            <div className="metric-header"><span className="metric-title">Roadmap progress</span><Compass className="metric-icon" size={20} /></div>
            <div className="metric-value-row"><span className="metric-huge-number">{percent.toFixed(1)}%</span></div>
            <div className="progress-bar-container">
              <motion.div className="progress-bar-fill" initial={reduceMotion ? false : { width: 0 }} animate={{ width: percent + '%' }} transition={{ duration: reduceMotion ? 0 : 0.3 }} />
            </div>
            <div className="metric-footer-stats"><span><strong>{roadmap.done}</strong> of <strong>{roadmap.total}</strong> modules complete</span><span>Roadmap v{roadmap.version}</span></div>
          </div>
        </div>

        {roadmap.items.length === 0 ? (
          <div className="roadmap-hero-box">
            <div className="roadmap-box-inner">
              <div className="roadmap-icon-sphere"><CheckCircle2 size={32} /></div>
              <h2 className="roadmap-feature-title">No learning gaps</h2>
              <p className="roadmap-box-desc">Your current assessed levels already meet the required career benchmarks.</p>
            </div>
          </div>
        ) : (
          <motion.div className="skill-results-grid" initial="hidden" animate="visible" variants={{ visible: { transition: { staggerChildren: reduceMotion ? 0 : 0.04 } } }}>
            {roadmap.items.map((item) => {
              const statusOption = STATUS_OPTIONS.find((option) => option.value === item.status) || STATUS_OPTIONS[0];
              const StatusIcon = statusOption.icon;
              return (
                <motion.article key={item.id} className="skill-result-card" variants={{ hidden: { opacity: 0, y: reduceMotion ? 0 : 8 }, visible: { opacity: 1, y: 0 } }} transition={{ duration: reduceMotion ? 0 : 0.2 }}>
                  <div className="skill-card-main">
                    <div>
                      <span className="skill-category-badge">Module {item.position}</span>
                      <h2 className="result-skill-name">{item.module.title}</h2>
                      <p className="form-hint">{item.module.skill.name}</p>
                    </div>
                    <span className="gap-badge gap-badge-regular">Level {item.module.to_level}</span>
                  </div>
                  <p className="form-hint">{item.module.outline}</p>
                  <div className="form-actions" style={{ marginTop: '1rem' }}>
                    <label className="field-label" htmlFor={'roadmap-status-' + item.id}>Status</label>
                    <select id={'roadmap-status-' + item.id} className="input-control" value={item.status} onChange={(event) => updateRoadmapItem(item.id, event.target.value)}>
                      {STATUS_OPTIONS.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
                    </select>
                    <span className="gap-badge gap-badge-met"><StatusIcon size={15} /> {statusOption.label}</span>
                  </div>
                </motion.article>
              );
            })}
          </motion.div>
        )}

        <div className="form-actions">
          <button type="button" className="btn btn-secondary" onClick={() => navigate('/analysis')}><ArrowLeft size={16} /> Review analysis</button>
          <button type="button" className="btn btn-primary" onClick={resetSession}><RotateCcw size={16} /> Start fresh</button>
        </div>
      </motion.div>
    </AnimatedPage>
  );
}
