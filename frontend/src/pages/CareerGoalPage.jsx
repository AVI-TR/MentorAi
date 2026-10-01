import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, ArrowRight, CheckCircle2, Briefcase, Sparkles, AlertCircle } from 'lucide-react';
import AnimatedPage from '../components/AnimatedPage';
import { useMentor } from '../context/MentorContext';

export default function CareerGoalPage() {
  const navigate = useNavigate();
  const {
    careers,
    selectedCareer,
    selectCareer,
    isLoadingCareers,
    isLoadingDetails,
    sessionError,
    restoreSession,
  } = useMentor();

  const [selectionError, setSelectionError] = useState(null);

  const handleSelect = (career) => {
    selectCareer(career);
    setSelectionError(null);
  };

  const handleContinue = () => {
    if (!selectedCareer) {
      setSelectionError('Please choose a career path to work toward.');
      return;
    }
    navigate('/skills');
  };

  return (
    <AnimatedPage className="form-page">
      <div className="flow-card">
        <div className="flow-header">
          <span className="step-tag">Step 2 of 5</span>
          <h1 className="flow-title">What do you want to work toward?</h1>
          <p className="flow-description">
            Select the target career path you aspire to master. Mentor will benchmark your skills against industry expectations for this track.
          </p>
        </div>

        {selectionError && (
          <div className="form-alert form-alert-error" role="alert">
            <AlertCircle size={18} className="alert-icon" />
            <span>{selectionError}</span>
          </div>
        )}

        {sessionError && (
          <div className="form-alert form-alert-error" role="alert">
            <span>{sessionError}</span>
            <button type="button" className="btn btn-secondary" onClick={restoreSession}>Retry</button>
          </div>
        )}

        {isLoadingCareers ? (
          <div className="skeleton-stack" aria-label="Loading career paths">
            <div className="skeleton skeleton-card" />
            <div className="skeleton skeleton-card" />
            <div className="skeleton skeleton-card" />
          </div>
        ) : careers.length === 0 ? (
          <div className="career-empty-state">
            <Briefcase size={36} className="empty-icon" />
            <p>No career paths found. Please check that the server is active.</p>
          </div>
        ) : (
          <div className="career-cards-grid" role="radiogroup" aria-label="Select target career">
            {careers.map((career) => {
              const isSelected = selectedCareer?.id === career.id;

              return (
                <div
                  key={career.id}
                  role="radio"
                  aria-checked={isSelected}
                  tabIndex={0}
                  className={`career-card ${isSelected ? 'career-card-selected' : ''}`}
                  onClick={() => handleSelect(career)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      handleSelect(career);
                    }
                  }}
                >
                  <div className="career-card-top">
                    <div className="career-icon-badge">
                      <Briefcase size={20} />
                    </div>
                    <div className={`selection-indicator ${isSelected ? 'indicator-active' : ''}`}>
                      {isSelected ? <CheckCircle2 size={20} className="check-active" /> : <div className="indicator-circle" />}
                    </div>
                  </div>

                  <h3 className="career-card-title">{career.name}</h3>
                  <p className="career-card-desc">{career.description}</p>
                </div>
              );
            })}
          </div>
        )}

        <div className="form-actions">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => navigate('/profile')}
          >
            <ArrowLeft size={16} />
            <span>Back</span>
          </button>

          <button
            type="button"
            className="btn btn-primary"
            onClick={handleContinue}
            disabled={!selectedCareer || isLoadingDetails}
            id="career-continue-btn"
          >
            <span>{isLoadingDetails ? 'Loading Skills...' : 'Continue'}</span>
            <ArrowRight size={16} />
          </button>
        </div>
      </div>
    </AnimatedPage>
  );
}
