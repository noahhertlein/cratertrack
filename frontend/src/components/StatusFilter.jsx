import React from 'react';
import { ButtonGroup, Button } from 'react-bootstrap';

const StatusFilter = ({ activeFilter, onFilterChange }) => {
  const statuses = [
    { label: 'All', value: 'ALL' },
    { label: 'New', value: 'NEW' },
    { label: 'Sent', value: 'SENT' },
    { label: 'Replied', value: 'REPLIED' },
    { label: 'Booked', value: 'BOOKED' }
  ];
  
  return (
    <div className="mb-3">
      <span className="me-2">Filter by status:</span>
      <ButtonGroup>
        {statuses.map(status => (
          <Button
            key={status.value}
            variant={activeFilter === status.value ? 'primary' : 'outline-primary'}
            onClick={() => onFilterChange(status.value)}
          >
            {status.label}
          </Button>
        ))}
      </ButtonGroup>
    </div>
  );
};

export default StatusFilter;
