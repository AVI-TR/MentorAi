import React from 'react';

const LEVEL_LABELS = {
  0: '0 - Not Recorded',
  1: '1 - Novice',
  2: '2 - Adv. Beginner',
  3: '3 - Competent',
  4: '4 - Proficient',
  5: '5 - Expert',
};

export default function SkillAssessment({
  careerSkills,
  skillLevels,
  onChangeLevel,
}) {
  if (!careerSkills || careerSkills.length === 0) {
    return null;
  }

  return (
    <section className="card skills-card">
      <div className="card-header">
        <div>
          <span className="section-badge">STAGE 3</span>
          <h2 className="card-title">Current Skill Self-Assessment</h2>
          <p className="card-subtitle">
            Rate your proficiency (0–5). Level <strong>0</strong> means unrecorded (will not be posted to API; evaluated as 0 gap by engine).
          </p>
        </div>
      </div>

      <div className="skills-list">
        {careerSkills.map((cs) => {
          const skillId = cs.skill_id;
          const currentLevel = skillLevels[skillId] ?? 0;
          const reqLevel = cs.required_level;
          const isMet = currentLevel >= reqLevel;
          const gap = Math.max(0, reqLevel - currentLevel);

          return (
            <div key={cs.id} className="skill-assessment-row">
              <div className="skill-info-column">
                <div className="skill-main-header">
                  <span className="skill-name">{cs.skill?.name || `Skill #${skillId}`}</span>
                  {cs.skill?.category && (
                    <span className="category-badge">{cs.skill.category}</span>
                  )}
                </div>

                <div className="skill-benchmark-row">
                  <span className="benchmark-tag">
                    Target Level: <strong>{reqLevel}/5</strong>
                  </span>
                  <span className="benchmark-tag weight-tag">
                    Weight: <strong>{cs.weight}/5</strong>
                  </span>
                  {currentLevel > 0 && (
                    <span className={`status-pill-small ${isMet ? 'pill-met' : 'pill-gap'}`}>
                      {isMet ? '✓ Benchmark Met' : `Gap: -${gap}`}
                    </span>
                  )}
                  {currentLevel === 0 && (
                    <span className="status-pill-small pill-unrecorded">
                      Unrecorded (0)
                    </span>
                  )}
                </div>
              </div>

              <div className="skill-selector-column">
                <span className="selector-label">Your Current Level:</span>
                <div className="level-btn-group" role="radiogroup" aria-label={`Proficiency for ${cs.skill?.name}`}>
                  {[0, 1, 2, 3, 4, 5].map((level) => {
                    const isSelected = currentLevel === level;
                    return (
                      <button
                        key={level}
                        type="button"
                        className={`level-btn ${isSelected ? 'level-btn-selected' : ''} ${level === 0 ? 'level-zero-btn' : ''}`}
                        onClick={() => onChangeLevel(skillId, level)}
                        title={LEVEL_LABELS[level]}
                      >
                        <span className="lvl-num">{level}</span>
                        <span className="lvl-title">{level === 0 ? 'None' : `L${level}`}</span>
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
