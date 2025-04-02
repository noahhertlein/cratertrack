import React from 'react';

const StatusFilter = ({ currentFilter, onFilterChange }) => {
  const statuses = [
    { key: 'ALL', label: 'All Leads' },
    { key: 'NEW', label: 'New', badgeClass: 'bg-primary' },
    { key: 'SENT', label: 'Sent', badgeClass: 'bg-info' },
    { key: 'REPLIED', label: 'Replied', badgeClass: 'bg-warning' },
    { key: 'BOOKED', label: 'Booked', badgeClass: 'bg-success' }
  ];

  return (
    <div className="mb-4">
      <div className="d-flex flex-wrap gap-2">
        {statuses.map(status => (
          <button
            key={status.key}
            className={`btn ${currentFilter === status.key ? 'btn-light' : 'btn-outline-light'}`}
            onClick={() => onFilterChange(status.key)}
          >
            {status.key !== 'ALL' && (
              <span className={`badge ${status.badgeClass} me-2`}>
                {status.key}
              </span>
            )}
            {status.label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default StatusFilter;
