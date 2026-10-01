import React, { useState } from 'react';

export default function GapAnalysisView({ analysis, targetCareerName, onReset }) {
  const [filter, setFilter] = useState('all'); // 'all', 'gaps', 'met'

  if (!analysis) return null;

  const items = analysis.items || [];

  const filteredItems = items.filter((item) => {
    if (filter === 'gaps') return item.gap > 0;
    if (filter === 'met') return item.gap === 0;
    return true;
  });

  // Sort by priority score descending by default
  const sortedItems = [...filteredItems].sort((a, b) => {
    if (b.priority_score !== a.priority_score) {
      return b.priority_score - a.priority_score;
    }
    return b.gap - a.gap;
  });

  const readiness = analysis.readiness_percent;
  let readinessColor = '#ef4444'; // Red for low
  let readinessLabel = 'Early Stage';
  if (readiness >= 75) {
    readinessColor = '#10b981'; // Green
    readinessLabel = 'Job Ready / Advanced';
  } else if (readiness >= 45) {
    readinessColor = '#f59e0b'; // Amber
    readinessLabel = 'In Progress';
  }

  return (
    <section className="card analysis-card" id="gap-analysis-section">
      <div className="card-header analysis-header">
        <div>
          <span className="section-badge live-badge">REAL-TIME SNAPSHOT</span>
          <h2 className="card-title">Skill Gap Analysis Results</h2>
          <p className="card-subtitle">
            Evaluated for target career: <strong>{targetCareerName}</strong> (Goal #{analysis.goal_id}, Snapshot #{analysis.id})
          </p>
        </div>

        {onReset && (
          <button type="button" className="btn btn-secondary" onClick={onReset}>
            Re-evaluate Skills
          </button>
        )}
      </div>

      {/* Main KPI Dashboard Row */}
      <div className="kpi-grid">
        <div className="kpi-card readiness-kpi">
          <div className="kpi-label">Readiness Score</div>
          <div className="kpi-readiness-row">
            <span className="kpi-huge-value" style={{ color: readinessColor }}>
              {readiness.toFixed(1)}%
            </span>
            <span className="kpi-status-badge" style={{ borderColor: readinessColor, color: readinessColor }}>
              {readinessLabel}
            </span>
          </div>
          <div className="readiness-bar-track">
            <div
              className="readiness-bar-fill"
              style={{
                width: `${readiness}%`,
                backgroundColor: readinessColor,
              }}
            ></div>
          </div>
          <span className="kpi-footnote">
            Weighted Achieved: {analysis.weighted_achieved} / {analysis.weighted_required} pts
          </span>
        </div>

        <div className="kpi-card">
          <div className="kpi-label">Skills Met</div>
          <div className="kpi-value text-accent">
            {analysis.skills_met} <span className="kpi-unit">/ {analysis.total_skills}</span>
          </div>
          <span className="kpi-footnote">
            {analysis.total_skills - analysis.skills_met} skills require upskilling
          </span>
        </div>

        <div className="kpi-card">
          <div className="kpi-label">Total Required Skills</div>
          <div className="kpi-value">{analysis.total_skills}</div>
          <span className="kpi-footnote">Benchmark competencies for track</span>
        </div>

        <div className="kpi-card">
          <div className="kpi-label">Weighted Competency</div>
          <div className="kpi-value">
            {analysis.weighted_required > 0
              ? `${Math.round((analysis.weighted_achieved / analysis.weighted_required) * 100)}%`
              : '0%'}
          </div>
          <span className="kpi-footnote">
            {analysis.weighted_achieved} achieved out of {analysis.weighted_required} max
          </span>
        </div>
      </div>

      {/* Skill Breakdown Table */}
      <div className="breakdown-section">
        <div className="breakdown-header">
          <h3 className="breakdown-title">Competency Gap Breakdown</h3>
          <div className="filter-pill-group">
            <button
              type="button"
              className={`filter-btn ${filter === 'all' ? 'filter-active' : ''}`}
              onClick={() => setFilter('all')}
            >
              All Skills ({items.length})
            </button>
            <button
              type="button"
              className={`filter-btn ${filter === 'gaps' ? 'filter-active' : ''}`}
              onClick={() => setFilter('gaps')}
            >
              Gaps Only ({items.filter((i) => i.gap > 0).length})
            </button>
            <button
              type="button"
              className={`filter-btn ${filter === 'met' ? 'filter-active' : ''}`}
              onClick={() => setFilter('met')}
            >
              Met ({items.filter((i) => i.gap === 0).length})
            </button>
          </div>
        </div>

        <div className="table-responsive">
          <table className="data-table">
            <thead>
              <tr>
                <th>Skill Name</th>
                <th>Category</th>
                <th>Student Lvl</th>
                <th>Required Lvl</th>
                <th>Level Comparison</th>
                <th>Gap</th>
                <th>Weight</th>
                <th>Priority Score</th>
              </tr>
            </thead>
            <tbody>
              {sortedItems.map((item) => {
                const isMet = item.gap === 0;
                let gapClass = 'gap-zero';
                if (item.gap >= 3) {
                  gapClass = 'gap-critical';
                } else if (item.gap > 0) {
                  gapClass = 'gap-moderate';
                }

                return (
                  <tr key={item.id} className={isMet ? 'row-met' : 'row-gap'}>
                    <td className="cell-skill-name">
                      <span className="font-semibold">
                        {item.skill?.name || `Skill #${item.skill_id}`}
                      </span>
                    </td>

                    <td>
                      <span className="category-tag">
                        {item.skill?.category || 'Core'}
                      </span>
                    </td>

                    <td className="cell-mono">
                      <span className={`level-indicator ${item.student_level > 0 ? 'level-has' : 'level-zero'}`}>
                        {item.student_level > 0 ? `${item.student_level} / 5` : '0 (None)'}
                      </span>
                    </td>

                    <td className="cell-mono">
                      <span className="level-indicator required-indicator">
                        {item.required_level} / 5
                      </span>
                    </td>

                    <td className="cell-visual-bar">
                      <div className="comparison-bar-container" title={`Student: ${item.student_level}/5 | Required: ${item.required_level}/5`}>
                        <div className="gauge-track">
                          {/* Required benchmark indicator */}
                          <div
                            className="required-marker"
                            style={{ left: `${(item.required_level / 5) * 100}%` }}
                            title={`Required Level: ${item.required_level}`}
                          ></div>
                          {/* Student level bar */}
                          <div
                            className={`gauge-fill ${isMet ? 'gauge-met' : 'gauge-gap'}`}
                            style={{ width: `${(item.student_level / 5) * 100}%` }}
                          ></div>
                        </div>
                      </div>
                    </td>

                    <td>
                      <span className={`badge-gap ${gapClass}`}>
                        {isMet ? '✓ Met' : `-${item.gap}`}
                      </span>
                    </td>

                    <td className="cell-mono">
                      <span className="weight-badge">{item.weight}x</span>
                    </td>

                    <td className="cell-mono">
                      <span className={`priority-badge ${item.priority_score > 8 ? 'priority-high' : item.priority_score > 0 ? 'priority-mid' : 'priority-none'}`}>
                        {item.priority_score}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        <div className="analysis-footer-note">
          <span className="info-icon">ℹ</span>
          <span>
            <strong>Deterministic Calculation:</strong> Priority Score = <code>gap × weight</code>. Skills with highest priority scores indicate urgent focus areas.
          </span>
        </div>
      </div>
    </section>
  );
}
