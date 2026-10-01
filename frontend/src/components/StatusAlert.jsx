import React from 'react';

export default function StatusAlert({ type = 'error', message, onDismiss }) {
  if (!message) return null;

  return (
    <div className={`status-alert alert-${type}`}>
      <div className="alert-content">
        <span className="alert-icon">
          {type === 'error' && '✕'}
          {type === 'warning' && '⚠'}
          {type === 'success' && '✓'}
          {type === 'info' && 'ℹ'}
        </span>
        <div className="alert-text">{message}</div>
      </div>
      {onDismiss && (
        <button type="button" className="alert-dismiss-btn" onClick={onDismiss}>
          ×
        </button>
      )}
    </div>
  );
}
