import React, { useState, useEffect } from 'react';
import LeadTable from './components/LeadTable';
import LeadForm from './components/LeadForm';
import StatusFilter from './components/StatusFilter';
import { fetchLeads, createLead, updateLead, addNote } from './services/api';

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

  // Load leads from API
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

  // Handle filter change
  const handleFilterChange = (filter) => {
    setCurrentFilter(filter);
  };

  // Handle lead creation
  const handleCreateLead = async (leadData) => {
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

  // Handle lead update
  const handleUpdateLead = async (leadId, updatedData) => {
    setIsLoading(true);
    setError(null);
    try {
      const updatedLead = await updateLead(leadId, updatedData);
      setLeads(leads.map(lead => lead.id === leadId ? updatedLead : lead));
      setSelectedLead(null);
      setShowLeadForm(false);
    } catch (err) {
      setError('Failed to update lead. Please try again.');
      console.error('Error updating lead:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle adding a note
  const handleAddNote = async (leadId, noteContent) => {
    setIsLoading(true);
    setError(null);
    try {
      const newNote = await addNote(leadId, { content: noteContent });
      
      // Update the lead with the new note
      setLeads(leads.map(lead => {
        if (lead.id === leadId) {
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

  // Open lead form for creating a new lead
  const openCreateLeadForm = () => {
    setSelectedLead(null);
    setShowLeadForm(true);
    setShowNoteForm(false);
  };

  // Open lead form for editing an existing lead
  const openEditLeadForm = (lead) => {
    setSelectedLead(lead);
    setShowLeadForm(true);
    setShowNoteForm(false);
  };

  // Open note form for adding a note to a lead
  const openNoteForm = (lead) => {
    setSelectedLead(lead);
    setShowLeadForm(false);
    setShowNoteForm(true);
  };

  // Close all forms
  const closeAllForms = () => {
    setShowLeadForm(false);
    setShowNoteForm(false);
    setSelectedLead(null);
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

      <StatusFilter 
        currentFilter={currentFilter} 
        onFilterChange={handleFilterChange} 
      />

      {isLoading ? (
        <div className="d-flex justify-content-center my-5">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      ) : (
        <LeadTable 
          leads={filteredLeads} 
          onEdit={openEditLeadForm} 
          onAddNote={openNoteForm}
        />
      )}

      {/* Lead Form Modal */}
      {showLeadForm && (
        <LeadForm 
          lead={selectedLead} 
          onSubmit={selectedLead ? handleUpdateLead : handleCreateLead} 
          onClose={closeAllForms}
        />
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
                <form onSubmit={(e) => {
                  e.preventDefault();
                  handleAddNote(selectedLead.id, e.target.note.value);
                }}>
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

export default App;
