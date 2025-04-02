import React, { useState } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';

const NoteForm = ({ show, lead, onHide, onSubmit }) => {
  const [noteContent, setNoteContent] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate content
    if (!noteContent.trim()) {
      setError('Note content is required');
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      const success = await onSubmit(noteContent);
      if (success) {
        setNoteContent('');
        onHide();
      }
    } catch (err) {
      console.error('Error submitting note:', err);
    } finally {
      setIsSubmitting(false);
    }
  };
  
  // Reset form when modal is closed
  const handleClose = () => {
    setNoteContent('');
    setError('');
    onHide();
  };
  
  return (
    <Modal show={show} onHide={handleClose} centered backdrop="static">
      <Modal.Header closeButton>
        <Modal.Title>
          Add Note {lead && <span className="text-muted">for {lead.name}</span>}
        </Modal.Title>
      </Modal.Header>
      
      <Form onSubmit={handleSubmit}>
        <Modal.Body>
          {lead && (
            <div className="mb-3">
              <div><strong>Lead:</strong> {lead.name}</div>
              <div><strong>Phone:</strong> {lead.phone}</div>
              <div><strong>Status:</strong> {lead.status}</div>
            </div>
          )}
          
          <Form.Group>
            <Form.Label>Note Content</Form.Label>
            <Form.Control
              as="textarea"
              rows={4}
              value={noteContent}
              onChange={(e) => {
                setNoteContent(e.target.value);
                if (error) setError('');
              }}
              isInvalid={!!error}
              disabled={isSubmitting}
              placeholder="Enter your note here..."
            />
            <Form.Control.Feedback type="invalid">
              {error}
            </Form.Control.Feedback>
          </Form.Group>
        </Modal.Body>
        
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose} disabled={isSubmitting}>
            Cancel
          </Button>
          <Button type="submit" variant="primary" disabled={isSubmitting}>
            {isSubmitting ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Saving...
              </>
            ) : (
              'Save Note'
            )}
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
};

export default NoteForm;
