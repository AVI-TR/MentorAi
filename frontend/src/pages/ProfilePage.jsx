import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, ArrowRight, Mail, GraduationCap, Calendar, Sparkles, AlertCircle } from 'lucide-react';
import AnimatedPage from '../components/AnimatedPage';
import { useMentor } from '../context/useMentor';

const YEAR_OPTIONS = [
  '1st Year (Freshman)',
  '2nd Year (Sophomore)',
  '3rd Year (Junior)',
  '4th Year (Senior)',
  'Graduate / Post-Grad',
  'Self-Taught / Career Transition',
];

export default function ProfilePage() {
  const navigate = useNavigate();
  const { profile, updateProfile } = useMentor();
  const [error, setError] = useState(null);

  const handleChange = (field, value) => {
    updateProfile({ [field]: value });
    if (field === 'email' && error) {
      setError(null);
    }
  };

  const handleContinue = (e) => {
    e.preventDefault();

    const trimmedEmail = profile.email?.trim();
    if (!trimmedEmail) {
      setError('Please provide your email address to continue.');
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(trimmedEmail)) {
      setError('Please enter a valid email address (e.g., you@domain.com).');
      return;
    }

    setError(null);
    navigate('/goal');
  };

  return (
    <AnimatedPage className="form-page">
      <div className="flow-card">
        <div className="flow-header">
          <span className="step-tag">Step 1 of 5</span>
          <h1 className="flow-title">Let's get to know you</h1>
          <p className="flow-description">
            Share your academic background and interests so Mentor can frame your journey accurately.
          </p>
        </div>

        {error && (
          <div className="form-alert form-alert-error" role="alert">
            <AlertCircle size={18} className="alert-icon" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleContinue} className="form-stack">
          {/* Email */}
          <div className="form-group">
            <label htmlFor="profile-email" className="form-label">
              <Mail size={16} className="label-icon" />
              <span>Email Address</span>
              <span className="required-mark">*</span>
            </label>
            <input
              id="profile-email"
              type="email"
              className={`form-input ${error ? 'input-error' : ''}`}
              placeholder="student.engineer@mentor.ai"
              value={profile.email}
              onChange={(e) => handleChange('email', e.target.value)}
              autoComplete="email"
              required
            />
            <span className="form-hint">
              Used to securely save your goals and progress.
            </span>
          </div>

          {/* Education */}
          <div className="form-group">
            <label htmlFor="profile-education" className="form-label">
              <GraduationCap size={16} className="label-icon" />
              <span>Education / Degree</span>
            </label>
            <input
              id="profile-education"
              type="text"
              className="form-input"
              placeholder="e.g. B.Tech in Computer Science, BS Software Engineering"
              value={profile.education}
              onChange={(e) => handleChange('education', e.target.value)}
            />
          </div>

          {/* Academic Year */}
          <div className="form-group">
            <label htmlFor="profile-year" className="form-label">
              <Calendar size={16} className="label-icon" />
              <span>Academic Year / Stage</span>
            </label>
            <div className="select-wrapper">
              <select
                id="profile-year"
                className="form-select"
                value={profile.year || ''}
                onChange={(e) => handleChange('year', e.target.value)}
              >
                <option value="">Select your academic year</option>
                {YEAR_OPTIONS.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Interests */}
          <div className="form-group">
            <label htmlFor="profile-interests" className="form-label">
              <Sparkles size={16} className="label-icon" />
              <span>Interests & Areas of Passion</span>
            </label>
            <textarea
              id="profile-interests"
              className="form-textarea"
              rows={3}
              placeholder="e.g. Distributed systems, APIs, cloud architecture, machine learning..."
              value={profile.interests}
              onChange={(e) => handleChange('interests', e.target.value)}
            />
            <span className="form-hint">
              Helps connect your skill development to what genuinely excites you.
            </span>
          </div>

          {/* Navigation Controls */}
          <div className="form-actions">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => navigate('/')}
            >
              <ArrowLeft size={16} />
              <span>Back</span>
            </button>

            <button type="submit" className="btn btn-primary" id="profile-continue-btn">
              <span>Continue</span>
              <ArrowRight size={16} />
            </button>
          </div>
        </form>
      </div>
    </AnimatedPage>
  );
}
