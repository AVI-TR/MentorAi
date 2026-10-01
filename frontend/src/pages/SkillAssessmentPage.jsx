import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence, useReducedMotion } from 'framer-motion';
import {
  ArrowLeft,
  ArrowRight,
  Sparkles,
  CheckCircle2,
  Check,
  AlertCircle,
  HelpCircle,
} from 'lucide-react';
import AnimatedPage from '../components/AnimatedPage';
import { useMentor } from '../context/MentorContext';

const PROFICIENCY_LEVELS = [
  {
    level: 1,
    title: 'Beginner',
    description: 'I know the basic concepts but need guidance.',
  },
  {
    level: 2,
    title: 'Basic',
    description: 'I can perform simple tasks and handle small problems.',
  },
  {
    level: 3,
    title: 'Intermediate',
    description: 'I can work independently on common problems.',
  },
  {
    level: 4,
    title: 'Advanced',
    description: 'I can handle complex problems and understand trade-offs.',
  },
  {
    level: 5,
    title: 'Expert',
    description:
      'I have deep practical knowledge and can design, optimize, and guide others.',
  },
];

export default function SkillAssessmentPage() {
  const navigate = useNavigate();
  const shouldReduceMotion = useReducedMotion();
  const {
    selectedCareer,
    careerDetails,
    skillLevels,
    setSkillLevel,
    runAnalysis,
    isAnalyzing,
    analysisError,
  } = useMentor();

  const [currentSkillIndex, setCurrentSkillIndex] = useState(0);
  const [submitError, setSubmitError] = useState(null);

  // If no career was selected yet, redirect to career goal page
  useEffect(() => {
    if (!selectedCareer) {
      navigate('/goal');
    }
  }, [selectedCareer, navigate]);

  const requiredSkills = careerDetails?.career_skills || [];
  const currentCareerSkill = requiredSkills[currentSkillIndex];
  const currentSkill = currentCareerSkill?.skill;

  const currentLevel = currentCareerSkill
    ? skillLevels[currentCareerSkill.skill_id] || 1
    : 1;

  const handleSelectLevel = (level) => {
    if (currentCareerSkill) {
      setSkillLevel(currentCareerSkill.skill_id, level);
    }
  };

  const handlePrev = () => {
    if (currentSkillIndex > 0) {
      setCurrentSkillIndex((prev) => prev - 1);
    } else {
      navigate('/goal');
    }
  };

  const handleNext = () => {
    if (currentSkillIndex < requiredSkills.length - 1) {
      setCurrentSkillIndex((prev) => prev + 1);
    }
  };

  const handleCompleteAssessment = async () => {
    setSubmitError(null);
    try {
      await runAnalysis();
      navigate('/analysis');
    } catch (err) {
      setSubmitError(err.message || 'Failed to complete analysis.');
    }
  };

  if (!selectedCareer || !careerDetails || requiredSkills.length === 0) {
    return (
      <AnimatedPage className="form-page">
        <div className="flow-card">
          <div className="career-loading-state">
            <div className="loading-spinner" />
            <p>Loading required skills for {selectedCareer?.name || 'career track'}...</p>
          </div>
        </div>
      </AnimatedPage>
    );
  }

  const isLastSkill = currentSkillIndex === requiredSkills.length - 1;

  // Variants for smooth transition between skills
  const skillCardVariants = {
    enter: (direction) =>
      shouldReduceMotion
        ? { opacity: 0 }
        : { opacity: 0, x: direction > 0 ? 28 : -28 },
    center: {
      opacity: 1,
      x: 0,
      transition: shouldReduceMotion
        ? { duration: 0.05 }
        : { duration: 0.28, ease: 'easeOut' },
    },
    exit: (direction) =>
      shouldReduceMotion
        ? { opacity: 0 }
        : {
            opacity: 0,
            x: direction > 0 ? -28 : 28,
            transition: { duration: 0.22, ease: 'easeIn' },
          },
  };

  return (
    <AnimatedPage className="form-page">
      <div className="flow-card assessment-container">
        <div className="flow-header">
          <div className="assessment-meta-row">
            <span className="step-tag">Step 3 of 5</span>
            <span className="career-pill">{selectedCareer.name}</span>
          </div>

          <h1 className="flow-title">Let's understand your current level</h1>
          <p className="flow-description emphasis-note">
            This is your self-assessment. Choose the level that feels closest.
          </p>
        </div>

        {/* Skill Progress Bar & Chips */}
        <div className="skill-stepper-nav" aria-label="Skills navigation">
          <div className="stepper-count-row">
            <span className="stepper-label">
              Skill <strong>{currentSkillIndex + 1}</strong> of{' '}
              <strong>{requiredSkills.length}</strong>
            </span>
            <span className="stepper-skill-name">
              {currentSkill?.name}
            </span>
          </div>

          <div className="skill-chips-row">
            {requiredSkills.map((cs, index) => {
              const isAssessed = !!skillLevels[cs.skill_id];
              const isCurrent = index === currentSkillIndex;

              return (
                <button
                  key={cs.skill_id}
                  type="button"
                  className={`skill-chip ${isCurrent ? 'skill-chip-current' : ''} ${
                    isAssessed ? 'skill-chip-assessed' : ''
                  }`}
                  onClick={() => setCurrentSkillIndex(index)}
                  title={cs.skill?.name}
                >
                  <span className="chip-dot" />
                  <span className="chip-label">{cs.skill?.name || `Skill ${index + 1}`}</span>
                </button>
              );
            })}
          </div>
        </div>

        {(submitError || analysisError) && (
          <div className="form-alert form-alert-error" role="alert">
            <AlertCircle size={18} className="alert-icon" />
            <span>{submitError || analysisError}</span>
          </div>
        )}

        {/* Animated Skill Assessment Section */}
        <div className="skill-animated-wrapper">
          <AnimatePresence mode="wait" initial={false}>
            <motion.div
              key={currentCareerSkill.skill_id}
              variants={skillCardVariants}
              initial="enter"
              animate="center"
              exit="exit"
              className="skill-content-panel"
            >
              <div className="skill-banner">
                <div className="skill-badge-category">
                  {currentSkill?.category || 'Core Skill'}
                </div>
                <h2 className="skill-heading">{currentSkill?.name}</h2>
              </div>

              <div
                className="proficiency-options-list"
                role="radiogroup"
                aria-label={`Proficiency level for ${currentSkill?.name}`}
              >
                {PROFICIENCY_LEVELS.map((lvl) => {
                  const isSelected = currentLevel === lvl.level;

                  return (
                    <motion.div
                      key={lvl.level}
                      role="radio"
                      aria-checked={isSelected}
                      tabIndex={0}
                      className={`proficiency-card ${
                        isSelected ? 'proficiency-card-selected' : ''
                      }`}
                      onClick={() => handleSelectLevel(lvl.level)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter' || e.key === ' ') {
                          e.preventDefault();
                          handleSelectLevel(lvl.level);
                        }
                      }}
                      layout={!shouldReduceMotion}
                      transition={
                        shouldReduceMotion
                          ? { duration: 0 }
                          : { duration: 0.22, ease: 'easeOut' }
                      }
                    >
                      <div className="proficiency-header">
                        <div className="proficiency-left">
                          <span
                            className={`level-number-badge ${
                              isSelected ? 'level-badge-active' : ''
                            }`}
                          >
                            {lvl.level}
                          </span>
                          <span className="proficiency-title">
                            {lvl.level} — {lvl.title}
                          </span>
                        </div>

                        <div
                          className={`proficiency-radio ${
                            isSelected ? 'radio-active' : ''
                          }`}
                        >
                          {isSelected && <Check size={14} className="check-svg" />}
                        </div>
                      </div>

                      {/* Explanation text fades and slides in smoothly */}
                      <AnimatePresence>
                        <motion.p
                          className="proficiency-desc"
                          initial={
                            shouldReduceMotion
                              ? false
                              : { opacity: 0.7, y: 2 }
                          }
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ duration: 0.2 }}
                        >
                          "{lvl.description}"
                        </motion.p>
                      </AnimatePresence>
                    </motion.div>
                  );
                })}
              </div>
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Skill Navigation Controls */}
        <div className="form-actions skill-actions">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={handlePrev}
            disabled={isAnalyzing}
          >
            <ArrowLeft size={16} />
            <span>
              {currentSkillIndex === 0 ? 'Back to Goal' : 'Previous Skill'}
            </span>
          </button>

          {!isLastSkill ? (
            <button
              type="button"
              className="btn btn-primary"
              onClick={handleNext}
              disabled={isAnalyzing}
              id="next-skill-btn"
            >
              <span>Next Skill</span>
              <ArrowRight size={16} />
            </button>
          ) : (
            <button
              type="button"
              className="btn btn-primary btn-glow"
              onClick={handleCompleteAssessment}
              disabled={isAnalyzing}
              id="complete-assessment-btn"
            >
              {isAnalyzing ? (
                <>
                  <div className="btn-spinner" />
                  <span>Analyzing Your Skills...</span>
                </>
              ) : (
                <>
                  <Sparkles size={16} />
                  <span>Analyze My Skills</span>
                </>
              )}
            </button>
          )}
        </div>
      </div>
    </AnimatedPage>
  );
}
