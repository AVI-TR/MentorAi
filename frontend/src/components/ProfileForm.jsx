import React from 'react';

export default function ProfileForm({
  email,
  setEmail,
  education,
  setEducation,
  year,
  setYear,
  interests,
  setInterests,
  error,
}) {
  return (
    <section className="card profile-card">
      <div className="card-header">
        <div>
          <span className="section-badge">STAGE 2</span>
          <h2 className="card-title">Student Information</h2>
          <p className="card-subtitle">
            Profile metadata stored via <code>/users</code> and <code>/users/{'{id}'}/profile</code>.
          </p>
        </div>
      </div>

      <div className="form-grid">
        <div className="form-field full-width">
          <label htmlFor="student-email" className="field-label required">
            Student Email Address <span className="required-star">*</span>
          </label>
          <input
            id="student-email"
            type="email"
            className={`input-control ${error?.field === 'email' ? 'input-error' : ''}`}
            placeholder="e.g. alex.developer@university.edu"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          {error?.field === 'email' && (
            <span className="field-error-msg">{error.message}</span>
          )}
          <span className="field-hint">
            Used to query or create the user in the database.
          </span>
        </div>

        <div className="form-field">
          <label htmlFor="student-education" className="field-label">
            Degree / Education
          </label>
          <input
            id="student-education"
            type="text"
            className="input-control"
            placeholder="e.g. B.Tech Computer Science"
            value={education}
            onChange={(e) => setEducation(e.target.value)}
          />
        </div>

        <div className="form-field">
          <label htmlFor="student-year" className="field-label">
            Current Academic Year
          </label>
          <input
            id="student-year"
            type="text"
            className="input-control"
            placeholder="e.g. 3rd Year / Junior"
            value={year}
            onChange={(e) => setYear(e.target.value)}
          />
        </div>

        <div className="form-field full-width">
          <label htmlFor="student-interests" className="field-label">
            Interests & Domain Focus
          </label>
          <textarea
            id="student-interests"
            className="textarea-control"
            rows="2"
            placeholder="e.g. Backend APIs, Distributed Systems, Cloud Architecture, High-throughput services"
            value={interests}
            onChange={(e) => setInterests(e.target.value)}
          ></textarea>
        </div>
      </div>
    </section>
  );
}
