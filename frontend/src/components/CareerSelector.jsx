import React from 'react';

export default function CareerSelector({
  careers,
  selectedCareerId,
  onSelectCareer,
  careerDetails,
  loadingDetails,
}) {
  return (
    <section className="card career-card">
      <div className="card-header">
        <div>
          <span className="section-badge">STAGE 1</span>
          <h2 className="card-title">Target Career Track</h2>
          <p className="card-subtitle">
            Select an industry benchmark track loaded dynamically from the catalog API.
          </p>
        </div>
      </div>

      <div className="career-selector-group">
        <label htmlFor="career-select" className="field-label">
          Select Career Benchmark Track
        </label>
        <select
          id="career-select"
          className="select-control"
          value={selectedCareerId || ''}
          onChange={(e) => onSelectCareer(Number(e.target.value))}
        >
          {careers.map((career) => (
            <option key={career.id} value={career.id}>
              {career.name} (ID: #{career.id})
            </option>
          ))}
        </select>
      </div>

      {loadingDetails && (
        <div className="loading-skeleton">
          <div className="skeleton-bar short"></div>
          <div className="skeleton-bar long"></div>
        </div>
      )}

      {!loadingDetails && careerDetails && (
        <div className="career-info-box">
          <div className="career-meta-row">
            <div className="career-title-wrap">
              <h3 className="career-name">{careerDetails.name}</h3>
              <span className="mono-badge">ID: {careerDetails.id}</span>
            </div>
            <span className="pill-count">
              {careerDetails.career_skills?.length || 0} Required Skills
            </span>
          </div>

          {careerDetails.description && (
            <p className="career-desc">{careerDetails.description}</p>
          )}

          <div className="required-skills-summary">
            <h4 className="subheading">Required Skills & Benchmark Weights:</h4>
            <div className="skill-chip-grid">
              {careerDetails.career_skills?.map((cs) => (
                <div key={cs.id} className="career-skill-chip">
                  <div className="chip-top">
                    <span className="chip-name">{cs.skill?.name || `Skill #${cs.skill_id}`}</span>
                    {cs.skill?.category && (
                      <span className="chip-category">{cs.skill.category}</span>
                    )}
                  </div>
                  <div className="chip-metrics">
                    <span className="chip-metric">
                      Required Lvl: <strong>{cs.required_level}/5</strong>
                    </span>
                    <span className="chip-dot">•</span>
                    <span className="chip-metric">
                      Weight: <strong>{cs.weight}/5</strong>
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
