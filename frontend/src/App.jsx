import React, { useState, useEffect } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import LeadTable from './components/LeadTable';
import LeadForm from './components/LeadForm';
import NoteForm from './components/NoteForm';
import StatusFilter from './components/StatusFilter';
import { fetchLeads, createLead, updateLead, addNote } from './services/api';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [leads, setLeads] = useState([]);
  const [filteredLeads, setFilteredLeads] = useState([]);
  const [selectedLead, setSelectedLead] = useState(null);
  const [showLeadForm, setShowLeadForm] = useState(false);
  const [showNoteForm, setShowNoteForm] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeFilter, setActiveFilter] = useState('ALL');

  // Fetch leads on component mount
  useEffect(() => {
    loadLeads();
  }, []);

  // Apply filter when leads or filter changes
  useEffect(() => {
    if (activeFilter === 'ALL') {
      setFilteredLeads(leads);
    } else {
      setFilteredLeads(leads.filter(lead => lead.status === activeFilter));
    }
  }, [leads, activeFilter]);

  // Load leads from API
  const loadLeads = async () => {
    setIsLoading(true);
    try {
      const data = await fetchLeads();
      setLeads(data.leads);
      setError(null);
    } catch (err) {
      setError('Failed to load leads. Please try again.');
      console.error('Error loading leads:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle lead creation
  const handleCreateLead = async (leadData) => {
    try {
      const response = await createLead(leadData);
      setLeads([...leads, response.lead]);
      setShowLeadForm(false);
      return true;
    } catch (err) {
      setError('Failed to create lead. Please try again.');
      console.error('Error creating lead:', err);
      return false;
    }
  };

  // Handle lead update
  const handleUpdateLead = async (leadId, leadData) => {
    try {
      const response = await updateLead(leadId, leadData);
      setLeads(leads.map(lead => lead.id === leadId ? response.lead : lead));
      setSelectedLead(null);
      setShowLeadForm(false);
      return true;
    } catch (err) {
      setError('Failed to update lead. Please try again.');
      console.error('Error updating lead:', err);
      return false;
    }
  };

  // Handle adding a note
  const handleAddNote = async (leadId, noteContent) => {
    try {
      const response = await addNote(leadId, { content: noteContent });
      
      // Update the leads state with the new note
      setLeads(leads.map(lead => {
        if (lead.id === leadId) {
          return {
            ...lead,
            notes: [...lead.notes, response.note]
          };
        }
        return lead;
      }));
      
      setShowNoteForm(false);
      return true;
    } catch (err) {
      setError('Failed to add note. Please try again.');
      console.error('Error adding note:', err);
      return false;
    }
  };

  // Status filter handler
  const handleFilterChange = (status) => {
    setActiveFilter(status);
  };

  // Open lead form for editing
  const handleEditLead = (lead) => {
    setSelectedLead(lead);
    setShowLeadForm(true);
  };

  // Open note form for adding note
  const handleOpenNoteForm = (lead) => {
    setSelectedLead(lead);
    setShowNoteForm(true);
  };

  return (
    <Container className="py-4">
      <h1 className="mb-4">SMS Campaign CRM</h1>
      
      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
          <button 
            type="button" 
            className="btn-close float-end" 
            onClick={() => setError(null)}
            aria-label="Close"
          ></button>
        </div>
      )}
      
      <Row className="mb-4">
        <Col>
          <StatusFilter 
            activeFilter={activeFilter} 
            onFilterChange={handleFilterChange} 
          />
        </Col>
        <Col className="text-end">
          <button 
            className="btn btn-primary" 
            onClick={() => {
              setSelectedLead(null);
              setShowLeadForm(true);
            }}
          >
            Add New Lead
          </button>
        </Col>
      </Row>
      
      {isLoading ? (
        <div className="text-center py-5">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      ) : (
        <LeadTable 
          leads={filteredLeads} 
          onEditLead={handleEditLead}
          onAddNote={handleOpenNoteForm}
        />
      )}
      
      {/* Lead Form Modal */}
      <LeadForm 
        show={showLeadForm}
        lead={selectedLead}
        onHide={() => {
          setShowLeadForm(false);
          setSelectedLead(null);
        }}
        onSubmit={selectedLead ? 
          (data) => handleUpdateLead(selectedLead.id, data) : 
          handleCreateLead
        }
      />
      
      {/* Note Form Modal */}
      <NoteForm 
        show={showNoteForm}
        lead={selectedLead}
        onHide={() => {
          setShowNoteForm(false);
          setSelectedLead(null);
        }}
        onSubmit={(content) => selectedLead && handleAddNote(selectedLead.id, content)}
      />
    </Container>
  );
}

export default App;
