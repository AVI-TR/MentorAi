import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence, useReducedMotion } from 'framer-motion';
import { ArrowLeft, ArrowRight, Check, Sparkles, AlertCircle } from 'lucide-react';
import AnimatedPage from '../components/AnimatedPage';
import { useMentor } from '../context/useMentor';

const LEVELS = [
  { level: 0, title: 'No experience', description: 'I have not learned or used this skill yet.' },
  { level: 1, title: 'Beginner', description: 'I know the basic concepts but need guidance.' },
  { level: 2, title: 'Basic', description: 'I can perform simple tasks and handle small problems.' },
  { level: 3, title: 'Working', description: 'I can work independently on common problems.' },
  { level: 4, title: 'Proficient', description: 'I can handle complex problems and understand trade-offs.' },
  { level: 5, title: 'Expert', description: 'I have deep practical knowledge and can design, optimize, and guide others.' },
];

export default function SkillAssessmentPage() {
  const navigate = useNavigate();
  const reduceMotion = useReducedMotion();
  const {
    selectedCareer, careerDetails, skillLevels, setSkillLevel,
    runAnalysis, isAnalyzing, analysisError,
  } = useMentor();
  const [currentSkillIndex, setCurrentSkillIndex] = useState(0);
  const [submitError, setSubmitError] = useState(null);

  useEffect(() => {
    if (!selectedCareer) navigate('/goal', { replace: true });
  }, [selectedCareer, navigate]);

  const requiredSkills = careerDetails?.career_skills ?? [];
  const current = requiredSkills[currentSkillIndex];
  const currentLevel = current ? skillLevels[current.skill_id] : undefined;
  const allRated = requiredSkills.length > 0 && requiredSkills.every((skill) => skillLevels[skill.skill_id] !== undefined);

  const choose = (level) => {
    if (current) setSkillLevel(current.skill_id, level);
  };

  const complete = async () => {
    setSubmitError(null);
    if (!allRated) {
      setSubmitError('Rate every skill before continuing.');
      return;
    }
    try {
      await runAnalysis();
      navigate('/analysis');
    } catch (error) {
      setSubmitError(error.message || 'Unable to complete the analysis.');
    }
  };

  if (!selectedCareer || !careerDetails || !current) {
    return (
      <AnimatedPage className="form-page">
        <div className="flow-card">
          <div className="skeleton-stack" aria-label="Loading skills">
            <div className="skeleton skeleton-title" />
            <div className="skeleton skeleton-line" />
            <div className="skeleton skeleton-card" />
            <div className="skeleton skeleton-card" />
          </div>
        </div>
      </AnimatedPage>
    );
  }

  return (
    <AnimatedPage className="form-page">
      <div className="flow-card assessment-container">
        <div className="flow-header">
          <span className="step-tag">Step 3 of 5</span>
          <h1 className="flow-title">Let&apos;s understand your current level</h1>
          <p className="flow-description">This is your self-assessment. There is no default — choose the level that feels closest.</p>
        </div>

        <div className="skill-stepper-nav">
          <div className="stepper-count-row">
            <span>Skill <strong>{currentSkillIndex + 1}</strong> of <strong>{requiredSkills.length}</strong></span>
            <span className="stepper-skill-name">{current.skill?.name}</span>
          </div>
          <div className="skill-chips-row">
            {requiredSkills.map((skill, index) => (
              <button
                key={skill.skill_id}
                type="button"
                className={`skill-chip ${index === currentSkillIndex ? 'skill-chip-current' : ''} ${skillLevels[skill.skill_id] !== undefined ? 'skill-chip-assessed' : ''}`}
                onClick={() => setCurrentSkillIndex(index)}
              >
                <span className="chip-dot" />
                <span>{skill.skill?.name}</span>
              </button>
            ))}
          </div>
        </div>

        {(submitError || analysisError) && (
          <div className="form-alert form-alert-error" role="alert">
            <AlertCircle size={18} />
            <span>{submitError || analysisError}</span>
          </div>
        )}

        <AnimatePresence mode="wait" initial={false}>
          <motion.div
            key={current.skill_id}
            initial={reduceMotion ? { opacity: 0 } : { opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={reduceMotion ? { opacity: 0 } : { opacity: 0, x: -20 }}
            transition={{ duration: reduceMotion ? 0 : 0.24 }}
          >
            <div className="skill-banner">
              <div className="skill-badge-category">{current.skill?.category || 'Core Skill'}</div>
              <h2 className="skill-heading">{current.skill?.name}</h2>
              <p className="form-hint">Choose one level. Your answer is a self-estimate.</p>
            </div>

            <div className="proficiency-options-list" role="radiogroup" aria-label={`Proficiency for ${current.skill?.name}`}>
              {LEVELS.map((level) => {
                const selected = currentLevel === level.level;
                return (
                  <motion.button
                    key={level.level}
                    type="button"
                    role="radio"
                    aria-checked={selected}
                    className={`proficiency-card ${selected ? 'proficiency-card-selected' : ''}`}
                    onClick={() => choose(level.level)}
                    whileHover={reduceMotion ? undefined : { y: -2 }}
                    whileTap={reduceMotion ? undefined : { scale: 0.99 }}
                    transition={{ duration: reduceMotion ? 0 : 0.18 }}
                  >
                    <div className="proficiency-header">
                      <div className="proficiency-left">
                        <span className={`level-number-badge ${selected ? 'level-badge-active' : ''}`}>{level.level}</span>
                        <span className="proficiency-title">{level.title}</span>
                      </div>
                      <span className={`proficiency-radio ${selected ? 'radio-active' : ''}`}>
                        {selected && <Check size={14} />}
                      </span>
                    </div>
                    <p className="proficiency-desc">{level.description}</p>
                  </motion.button>
                );
              })}
            </div>
          </motion.div>
        </AnimatePresence>

        <div className="form-actions skill-actions">
          <button type="button" className="btn btn-secondary" onClick={() => currentSkillIndex ? setCurrentSkillIndex((i) => i - 1) : navigate('/goal')} disabled={isAnalyzing}>
            <ArrowLeft size={16} /> <span>{currentSkillIndex ? 'Previous Skill' : 'Back to Goal'}</span>
          </button>

          {currentSkillIndex < requiredSkills.length - 1 ? (
            <button type="button" className="btn btn-primary" onClick={() => setCurrentSkillIndex((i) => i + 1)} disabled={currentLevel === undefined || isAnalyzing}>
              <span>Next Skill</span><ArrowRight size={16} />
            </button>
          ) : (
            <button type="button" className="btn btn-primary" onClick={complete} disabled={!allRated || isAnalyzing}>
              <Sparkles size={16} /><span>{isAnalyzing ? 'Analyzing…' : 'Analyze My Skills'}</span>
            </button>
          )}
        </div>
      </div>
    </AnimatedPage>
  );
}
