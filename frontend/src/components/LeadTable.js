import React from 'react';

// Status badge component for consistent styling
const StatusBadge = ({ status }) => {
  let badgeClass = '';
  
  switch (status) {
    case 'NEW':
      badgeClass = 'bg-primary';
      break;
    case 'SENT':
      badgeClass = 'bg-info';
      break;
    case 'REPLIED':
      badgeClass = 'bg-warning';
      break;
    case 'BOOKED':
      badgeClass = 'bg-success';
      break;
    default:
      badgeClass = 'bg-secondary';
  }
  
  return <span className={`badge ${badgeClass}`}>{status}</span>;
};

const LeadTable = ({ leads, onEdit, onAddNote }) => {
  // Format date to a more readable string
  const formatDate = (dateString) => {
    const options = { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  return (
    <div className="table-responsive">
      {leads.length === 0 ? (
        <div className="text-center py-5">
          <p className="lead">No leads found. Create a new lead to get started.</p>
        </div>
      ) : (
        <table className="table table-hover">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Status</th>
              <th>Created</th>
              <th>Notes</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {leads.map(lead => (
              <tr key={lead.id}>
                <td>{lead.first_name} {lead.last_name}</td>
                <td>{lead.email}</td>
                <td>
                  <a 
                    href={`tel:${lead.phone}`} 
                    className="text-decoration-none"
                    title="Click to call"
                  >
                    <i className="fas fa-phone-alt me-2 text-success"></i>
                    {lead.phone}
                  </a>
                </td>
                <td><StatusBadge status={lead.status} /></td>
                <td>{formatDate(lead.created_at)}</td>
                <td>
                  {lead.notes && lead.notes.length > 0 ? (
                    <span className="badge bg-secondary">
                      {lead.notes.length}
                    </span>
                  ) : (
                    <span className="text-muted">No notes</span>
                  )}
                </td>
                <td>
                  <div className="btn-group">
                    <button 
                      onClick={() => onEdit(lead)} 
                      className="btn btn-sm btn-outline-primary"
                      title="Edit lead"
                    >
                      <i className="fas fa-edit"></i>
                    </button>
                    <button 
                      onClick={() => onAddNote(lead)} 
                      className="btn btn-sm btn-outline-info ms-1"
                      title="Add note"
                    >
                      <i className="fas fa-sticky-note"></i>
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default LeadTable;
