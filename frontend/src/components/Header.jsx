import React from 'react';

export default function Header({ healthStatus, apiUrl }) {
  const isHealthy = healthStatus && healthStatus.status === 'healthy';

  return (
    <header className="app-header">
      <div className="header-brand">
        <div className="logo-icon">
          <span className="logo-mark">⚡</span>
        </div>
        <div>
          <div className="brand-title-wrap">
            <h1 className="brand-title">MentorAi</h1>
            <span className="brand-badge">Dev Engine</span>
          </div>
          <p className="brand-subtitle">Campus Skill Gap & Career Readiness Platform</p>
        </div>
      </div>

      <div className="header-meta">
        <div className="endpoint-pill" title={`Active API Base URL: ${apiUrl}`}>
          <span className="mono-text">{apiUrl}</span>
        </div>

        <div className={`status-pill ${isHealthy ? 'status-online' : 'status-offline'}`}>
          <span className="status-dot"></span>
          <span>{isHealthy ? 'Backend Connected' : 'Connecting to API...'}</span>
          {isHealthy && healthStatus.version && (
            <span className="version-tag">v{healthStatus.version}</span>
          )}
        </div>
      </div>
    </header>
  );
}
