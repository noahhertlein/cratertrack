import logging
import os
from flask import jsonify, request, send_from_directory, current_app
from backend.app import db
from backend.models import Lead, Note

logger = logging.getLogger(__name__)

def register_routes(app):
    """
    Register all API routes with the Flask app
    """
    
    @app.route('/api/leads', methods=['GET'])
    def get_leads():
        """
        Get all leads with optional status filtering
        """
        try:
            status = request.args.get('status')
            
            if status:
                leads = Lead.query.filter_by(status=status).all()
            else:
                leads = Lead.query.all()
                
            return jsonify({
                'success': True,
                'data': [lead.to_dict() for lead in leads]
            }), 200
            
        except Exception as e:
            logger.error(f"Error retrieving leads: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to retrieve leads',
                'message': str(e)
            }), 500
    
    @app.route('/api/leads', methods=['POST'])
    def create_lead():
        """
        Create a new lead
        """
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['first_name', 'last_name', 'email', 'phone']
            for field in required_fields:
                if field not in data:
                    return jsonify({
                        'success': False,
                        'error': f'Missing required field: {field}'
                    }), 400
            
            # Create new lead
            new_lead = Lead(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                phone=data['phone'],
                status=data.get('status', 'NEW')
            )
            
            db.session.add(new_lead)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'data': new_lead.to_dict(),
                'message': 'Lead created successfully'
            }), 201
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating lead: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to create lead',
                'message': str(e)
            }), 500
    
    @app.route('/api/leads/<int:lead_id>', methods=['PATCH'])
    def update_lead(lead_id):
        """
        Update lead status or other fields
        """
        try:
            lead = Lead.query.get(lead_id)
            
            if not lead:
                return jsonify({
                    'success': False,
                    'error': 'Lead not found'
                }), 404
            
            data = request.get_json()
            
            # Update fields if provided
            if 'status' in data:
                lead.status = data['status']
            if 'first_name' in data:
                lead.first_name = data['first_name']
            if 'last_name' in data:
                lead.last_name = data['last_name']
            if 'email' in data:
                lead.email = data['email']
            if 'phone' in data:
                lead.phone = data['phone']
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'data': lead.to_dict(),
                'message': 'Lead updated successfully'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating lead: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to update lead',
                'message': str(e)
            }), 500
    
    @app.route('/api/notes/<int:lead_id>', methods=['POST'])
    def add_note(lead_id):
        """
        Add a note to a lead
        """
        try:
            lead = Lead.query.get(lead_id)
            
            if not lead:
                return jsonify({
                    'success': False,
                    'error': 'Lead not found'
                }), 404
            
            data = request.get_json()
            
            if 'content' not in data or not data['content'].strip():
                return jsonify({
                    'success': False,
                    'error': 'Note content is required'
                }), 400
            
            new_note = Note(
                content=data['content'],
                lead_id=lead_id
            )
            
            db.session.add(new_note)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'data': new_note.to_dict(),
                'message': 'Note added successfully'
            }), 201
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error adding note: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to add note',
                'message': str(e)
            }), 500
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """
        Health check endpoint
        """
        return jsonify({
            'status': 'healthy',
            'message': 'API is running'
        }), 200
    
    # Create a simple HTML index page to show when accessing the root URL
    @app.route('/')
    def index():
        """
        Serve a simple HTML page as the main interface
        """
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SMS Campaign CRM</title>
            <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        </head>
        <body data-bs-theme="dark">
            <div class="container py-4">
                <header class="pb-3 mb-4 border-bottom">
                    <h1 class="h2">SMS Campaign CRM</h1>
                </header>
                <div class="p-5 mb-4 bg-body-tertiary rounded-3">
                    <div class="container-fluid py-5">
                        <h1 class="display-5 fw-bold">Manage Your SMS Campaigns</h1>
                        <p class="col-md-8 fs-4">Track leads, manage status, and keep notes for your SMS marketing campaigns.</p>
                        <a href="/app" class="btn btn-primary btn-lg" type="button">Open CRM Dashboard</a>
                    </div>
                </div>
                <div class="row align-items-md-stretch">
                    <div class="col-md-6">
                        <div class="h-100 p-5 text-bg-primary rounded-3">
                            <h2>Lead Management</h2>
                            <p>Create and organize leads based on their current status in your SMS workflow.</p>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="h-100 p-5 bg-body-tertiary border rounded-3">
                            <h2>Note Tracking</h2>
                            <p>Keep detailed notes for each lead to improve your follow-up process.</p>
                        </div>
                    </div>
                </div>
                <footer class="pt-3 mt-4 text-muted border-top">
                    &copy; 2025 SMS Campaign CRM
                </footer>
            </div>
        </body>
        </html>
        """
        return html
        
    @app.route('/app')
    def app_page():
        """
        Serve the React app interface
        """
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SMS Campaign CRM</title>
            <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        </head>
        <body data-bs-theme="dark">
            <div id="root"></div>
            <script src="https://cdn.jsdelivr.net/npm/react@18.2.0/umd/react.production.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/react-dom@18.2.0/umd/react-dom.production.min.js"></script>
            <script src="https://unpkg.com/babel-standalone@6/babel.min.js"></script>
            
            <script type="text/babel">
                const { useState, useEffect } = React;
                
                // Main App Component
                function App() {
                    const [leads, setLeads] = useState([]);
                    const [filteredLeads, setFilteredLeads] = useState([]);
                    const [selectedLead, setSelectedLead] = useState(null);
                    const [showLeadForm, setShowLeadForm] = useState(false);
                    const [showNoteForm, setShowNoteForm] = useState(false);
                    const [currentFilter, setCurrentFilter] = useState('ALL');
                    const [isLoading, setIsLoading] = useState(false);
                    const [error, setError] = useState(null);
                
                    // Fetch leads on component mount
                    useEffect(() => {
                        loadLeads();
                    }, []);
                
                    // Filter leads when leads array or filter changes
                    useEffect(() => {
                        if (currentFilter === 'ALL') {
                            setFilteredLeads(leads);
                        } else {
                            setFilteredLeads(leads.filter(lead => lead.status === currentFilter));
                        }
                    }, [leads, currentFilter]);
                
                    // API Functions
                    const apiRequest = async (endpoint, method = 'GET', data = null) => {
                        const url = `/api${endpoint}`;
                        
                        const options = {
                            method,
                            headers: {
                                'Content-Type': 'application/json',
                            },
                        };
                    
                        if (data) {
                            options.body = JSON.stringify(data);
                        }
                    
                        try {
                            const response = await fetch(url, options);
                            const result = await response.json();
                            
                            if (!response.ok) {
                                throw new Error(result.message || 'API request failed');
                            }
                            
                            return result.data;
                        } catch (error) {
                            console.error(`API error (${method} ${endpoint}):`, error);
                            throw error;
                        }
                    };
                
                    const fetchLeads = async (status = null) => {
                        const endpoint = status ? `/leads?status=${status}` : '/leads';
                        return apiRequest(endpoint);
                    };
                
                    const createLead = async (leadData) => {
                        return apiRequest('/leads', 'POST', leadData);
                    };
                
                    const updateLead = async (leadId, updateData) => {
                        return apiRequest(`/leads/${leadId}`, 'PATCH', updateData);
                    };
                
                    const addNote = async (leadId, noteData) => {
                        return apiRequest(`/notes/${leadId}`, 'POST', noteData);
                    };
                
                    // Event handlers
                    const loadLeads = async () => {
                        setIsLoading(true);
                        setError(null);
                        try {
                            const data = await fetchLeads();
                            setLeads(data);
                        } catch (err) {
                            setError('Failed to load leads. Please try again.');
                            console.error('Error loading leads:', err);
                        } finally {
                            setIsLoading(false);
                        }
                    };
                
                    const handleFilterChange = (filter) => {
                        setCurrentFilter(filter);
                    };
                
                    const handleCreateLead = async (e) => {
                        e.preventDefault();
                        const formData = new FormData(e.target);
                        const leadData = {
                            first_name: formData.get('firstName'),
                            last_name: formData.get('lastName'),
                            email: formData.get('email'),
                            phone: formData.get('phone')
                        };
                
                        setIsLoading(true);
                        setError(null);
                        try {
                            const newLead = await createLead(leadData);
                            setLeads([...leads, newLead]);
                            setShowLeadForm(false);
                        } catch (err) {
                            setError('Failed to create lead. Please try again.');
                            console.error('Error creating lead:', err);
                        } finally {
                            setIsLoading(false);
                        }
                    };
                
                    const handleUpdateStatus = async (leadId, newStatus) => {
                        setIsLoading(true);
                        setError(null);
                        try {
                            const updatedLead = await updateLead(leadId, { status: newStatus });
                            setLeads(leads.map(lead => lead.id === leadId ? updatedLead : lead));
                        } catch (err) {
                            setError('Failed to update lead status. Please try again.');
                            console.error('Error updating lead status:', err);
                        } finally {
                            setIsLoading(false);
                        }
                    };
                
                    const handleAddNote = async (e) => {
                        e.preventDefault();
                        const noteContent = e.target.elements.note.value;
                        
                        setIsLoading(true);
                        setError(null);
                        try {
                            const newNote = await addNote(selectedLead.id, { content: noteContent });
                            
                            setLeads(leads.map(lead => {
                                if (lead.id === selectedLead.id) {
                                    return {
                                        ...lead,
                                        notes: [...lead.notes, newNote]
                                    };
                                }
                                return lead;
                            }));
                            
                            setSelectedLead(null);
                            setShowNoteForm(false);
                        } catch (err) {
                            setError('Failed to add note. Please try again.');
                            console.error('Error adding note:', err);
                        } finally {
                            setIsLoading(false);
                        }
                    };
                
                    // UI Functions
                    const openCreateLeadForm = () => {
                        setSelectedLead(null);
                        setShowLeadForm(true);
                        setShowNoteForm(false);
                    };
                
                    const openNoteForm = (lead) => {
                        setSelectedLead(lead);
                        setShowLeadForm(false);
                        setShowNoteForm(true);
                    };
                
                    const closeAllForms = () => {
                        setShowLeadForm(false);
                        setShowNoteForm(false);
                        setSelectedLead(null);
                    };
                
                    // Status filter component
                    const StatusFilter = () => {
                        const statuses = [
                            { value: 'ALL', label: 'All Leads' },
                            { value: 'NEW', label: 'New' },
                            { value: 'SENT', label: 'Sent' },
                            { value: 'REPLIED', label: 'Replied' },
                            { value: 'BOOKED', label: 'Booked' }
                        ];
                
                        return (
                            <div className="d-flex justify-content-center mb-4">
                                <div className="btn-group" role="group">
                                    {statuses.map(status => (
                                        <button
                                            key={status.value}
                                            type="button"
                                            className={`btn ${currentFilter === status.value ? 'btn-primary' : 'btn-outline-secondary'}`}
                                            onClick={() => handleFilterChange(status.value)}
                                        >
                                            {status.label}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        );
                    };
                
                    // Lead table component
                    const LeadTable = () => {
                        if (filteredLeads.length === 0) {
                            return (
                                <div className="alert alert-info text-center">
                                    No leads found. Create your first lead by clicking the "New Lead" button.
                                </div>
                            );
                        }
                
                        return (
                            <div className="table-responsive">
                                <table className="table table-striped table-hover">
                                    <thead>
                                        <tr>
                                            <th>Name</th>
                                            <th>Email</th>
                                            <th>Phone</th>
                                            <th>Status</th>
                                            <th>Notes</th>
                                            <th>Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {filteredLeads.map(lead => (
                                            <tr key={lead.id}>
                                                <td>{lead.first_name} {lead.last_name}</td>
                                                <td>
                                                    <a href={`mailto:${lead.email}`} className="text-decoration-none">
                                                        {lead.email}
                                                    </a>
                                                </td>
                                                <td>
                                                    <a href={`tel:${lead.phone}`} className="text-decoration-none">
                                                        {lead.phone}
                                                    </a>
                                                </td>
                                                <td>
                                                    <select
                                                        className="form-select form-select-sm"
                                                        value={lead.status}
                                                        onChange={(e) => handleUpdateStatus(lead.id, e.target.value)}
                                                    >
                                                        <option value="NEW">New</option>
                                                        <option value="SENT">Sent</option>
                                                        <option value="REPLIED">Replied</option>
                                                        <option value="BOOKED">Booked</option>
                                                    </select>
                                                </td>
                                                <td>
                                                    <span className="badge bg-secondary">
                                                        {lead.notes.length} notes
                                                    </span>
                                                </td>
                                                <td>
                                                    <button
                                                        className="btn btn-sm btn-outline-primary me-1"
                                                        onClick={() => openNoteForm(lead)}
                                                        title="Add Note"
                                                    >
                                                        <i className="fas fa-sticky-note"></i>
                                                    </button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        );
                    };
                
                    return (
                        <div className="container py-4">
                            <header className="pb-3 mb-4 border-bottom">
                                <div className="d-flex justify-content-between align-items-center">
                                    <h1 className="h2">SMS Campaign CRM</h1>
                                    <button 
                                        className="btn btn-primary" 
                                        onClick={openCreateLeadForm}
                                    >
                                        <i className="fas fa-plus me-2"></i>New Lead
                                    </button>
                                </div>
                            </header>
                
                            {error && (
                                <div className="alert alert-danger alert-dismissible fade show" role="alert">
                                    {error}
                                    <button 
                                        type="button" 
                                        className="btn-close" 
                                        onClick={() => setError(null)} 
                                        aria-label="Close"
                                    ></button>
                                </div>
                            )}
                
                            <StatusFilter />
                
                            {isLoading ? (
                                <div className="d-flex justify-content-center my-5">
                                    <div className="spinner-border" role="status">
                                        <span className="visually-hidden">Loading...</span>
                                    </div>
                                </div>
                            ) : (
                                <LeadTable />
                            )}
                
                            {/* Lead Form Modal */}
                            {showLeadForm && (
                                <div className="modal d-block" tabIndex="-1" style={{backgroundColor: 'rgba(0,0,0,0.5)'}}>
                                    <div className="modal-dialog">
                                        <div className="modal-content">
                                            <div className="modal-header">
                                                <h5 className="modal-title">New Lead</h5>
                                                <button type="button" className="btn-close" onClick={closeAllForms}></button>
                                            </div>
                                            <div className="modal-body">
                                                <form onSubmit={handleCreateLead}>
                                                    <div className="mb-3">
                                                        <label htmlFor="firstName" className="form-label">First Name</label>
                                                        <input type="text" className="form-control" id="firstName" name="firstName" required />
                                                    </div>
                                                    <div className="mb-3">
                                                        <label htmlFor="lastName" className="form-label">Last Name</label>
                                                        <input type="text" className="form-control" id="lastName" name="lastName" required />
                                                    </div>
                                                    <div className="mb-3">
                                                        <label htmlFor="email" className="form-label">Email</label>
                                                        <input type="email" className="form-control" id="email" name="email" required />
                                                    </div>
                                                    <div className="mb-3">
                                                        <label htmlFor="phone" className="form-label">Phone</label>
                                                        <input type="tel" className="form-control" id="phone" name="phone" required />
                                                    </div>
                                                    <div className="d-flex justify-content-end">
                                                        <button type="button" className="btn btn-secondary me-2" onClick={closeAllForms}>
                                                            Cancel
                                                        </button>
                                                        <button type="submit" className="btn btn-primary">
                                                            Save Lead
                                                        </button>
                                                    </div>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}
                
                            {/* Note Form Modal */}
                            {showNoteForm && selectedLead && (
                                <div className="modal d-block" tabIndex="-1" style={{backgroundColor: 'rgba(0,0,0,0.5)'}}>
                                    <div className="modal-dialog">
                                        <div className="modal-content">
                                            <div className="modal-header">
                                                <h5 className="modal-title">Add Note to {selectedLead.first_name} {selectedLead.last_name}</h5>
                                                <button type="button" className="btn-close" onClick={closeAllForms}></button>
                                            </div>
                                            <div className="modal-body">
                                                <form onSubmit={handleAddNote}>
                                                    <div className="mb-3">
                                                        <label htmlFor="note" className="form-label">Note</label>
                                                        <textarea 
                                                            className="form-control" 
                                                            id="note" 
                                                            name="note" 
                                                            rows="3" 
                                                            required
                                                        ></textarea>
                                                    </div>
                                                    <div className="d-flex justify-content-end">
                                                        <button type="button" className="btn btn-secondary me-2" onClick={closeAllForms}>
                                                            Cancel
                                                        </button>
                                                        <button type="submit" className="btn btn-primary">
                                                            Add Note
                                                        </button>
                                                    </div>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    );
                }
                
                // Render the App component
                ReactDOM.render(<App />, document.getElementById('root'));
            </script>
        </body>
        </html>
        """
        return html
