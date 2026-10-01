import React from 'react';

export default function Pipeline({ currentStep }) {
  const steps = [
    {
      id: 1,
      name: 'Student Profile',
      desc: 'Academic & interests baseline',
    },
    {
      id: 2,
      name: 'Career Goal',
      desc: 'Target track & benchmark requirements',
    },
    {
      id: 3,
      name: 'Skill Gap Analysis',
      desc: 'Deterministic readiness engine',
    },
    {
      id: 4,
      name: 'Roadmap',
      desc: 'Personalized curriculum',
      isComingNext: true,
    },
  ];

  return (
    <div className="pipeline-container">
      <div className="pipeline-label-wrap">
        <span className="pipeline-tag">ARCHITECTURE PIPELINE</span>
        <span className="pipeline-subtext">Deterministic Backend Execution Pipeline</span>
      </div>

      <div className="pipeline-track">
        {steps.map((step, index) => {
          const isCompleted = currentStep > step.id;
          const isActive = currentStep === step.id;
          const isNext = step.isComingNext;

          let stepClass = 'step-upcoming';
          if (isCompleted) stepClass = 'step-completed';
          if (isActive) stepClass = 'step-active';
          if (isNext) stepClass += ' step-future';

          return (
            <React.Fragment key={step.id}>
              <div className={`pipeline-step ${stepClass}`}>
                <div className="step-indicator">
                  {isCompleted ? (
                    <span className="check-icon">✓</span>
                  ) : (
                    <span className="step-num">{step.id}</span>
                  )}
                </div>
                <div className="step-content">
                  <div className="step-header-line">
                    <span className="step-title">{step.name}</span>
                    {step.isComingNext && (
                      <span className="badge-coming-next">Coming next</span>
                    )}
                  </div>
                  <span className="step-desc">{step.desc}</span>
                </div>
              </div>

              {index < steps.length - 1 && (
                <div className={`pipeline-connector ${currentStep > step.id ? 'connector-active' : ''}`}>
                  <span className="arrow-indicator">→</span>
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
}
