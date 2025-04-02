import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Row, Col } from 'react-bootstrap';

const LeadForm = ({ show, lead, onHide, onSubmit }) => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone_1: '',
    phone_2: '',
    phone_3: '',
    phone_4: '',
    address: '',
    zip: '',
    resort: '',
    mortgaged: false,
    status: 'NEW'
  });
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState({});
  
  // Reset form when modal opens/closes or lead changes
  useEffect(() => {
    if (lead) {
      setFormData({
        first_name: lead.first_name || '',
        last_name: lead.last_name || '',
        email: lead.email || '',
        phone_1: lead.phone_1 || '',
        phone_2: lead.phone_2 || '',
        phone_3: lead.phone_3 || '',
        phone_4: lead.phone_4 || '',
        address: lead.address || '',
        zip: lead.zip || '',
        resort: lead.resort || '',
        mortgaged: lead.mortgaged || false,
        status: lead.status || 'NEW'
      });
    } else {
      setFormData({
        first_name: '',
        last_name: '',
        email: '',
        phone_1: '',
        phone_2: '',
        phone_3: '',
        phone_4: '',
        address: '',
        zip: '',
        resort: '',
        mortgaged: false,
        status: 'NEW'
      });
    }
    setErrors({});
  }, [lead, show]);
  
  // Handle form input changes
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
    
    // Clear error for this field
    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: null
      });
    }
  };
  
  // Validate form
  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.first_name.trim()) {
      newErrors.first_name = 'First name is required';
    }
    
    if (!formData.last_name.trim()) {
      newErrors.last_name = 'Last name is required';
    }
    
    if (!formData.phone_1.trim()) {
      newErrors.phone_1 = 'Primary phone is required';
    } else if (!/^[0-9+\- ()]{7,20}$/.test(formData.phone_1)) {
      newErrors.phone_1 = 'Please enter a valid phone number';
    }
    
    // Validate additional phone numbers only if they're provided
    if (formData.phone_2 && !/^[0-9+\- ()]{7,20}$/.test(formData.phone_2)) {
      newErrors.phone_2 = 'Please enter a valid phone number';
    }
    
    if (formData.phone_3 && !/^[0-9+\- ()]{7,20}$/.test(formData.phone_3)) {
      newErrors.phone_3 = 'Please enter a valid phone number';
    }
    
    if (formData.phone_4 && !/^[0-9+\- ()]{7,20}$/.test(formData.phone_4)) {
      newErrors.phone_4 = 'Please enter a valid phone number';
    }
    
    if (formData.email && !/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }
    
    if (formData.zip && !/^\d{5}(-\d{4})?$/.test(formData.zip)) {
      newErrors.zip = 'Please enter a valid ZIP code';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      const success = await onSubmit(formData);
      if (success) {
        onHide();
      }
    } catch (error) {
      console.error('Error submitting form:', error);
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <Modal show={show} onHide={onHide} centered backdrop="static">
      <Modal.Header closeButton>
        <Modal.Title>{lead ? 'Edit Lead' : 'Add New Lead'}</Modal.Title>
      </Modal.Header>
      
      <Form onSubmit={handleSubmit}>
        <Modal.Body>
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>First Name</Form.Label>
                <Form.Control
                  type="text"
                  name="first_name"
                  value={formData.first_name}
                  onChange={handleChange}
                  isInvalid={!!errors.first_name}
                  required
                />
                <Form.Control.Feedback type="invalid">
                  {errors.first_name}
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Last Name</Form.Label>
                <Form.Control
                  type="text"
                  name="last_name"
                  value={formData.last_name}
                  onChange={handleChange}
                  isInvalid={!!errors.last_name}
                  required
                />
                <Form.Control.Feedback type="invalid">
                  {errors.last_name}
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
          </Row>
          
          <Form.Group className="mb-3">
            <Form.Label>Email</Form.Label>
            <Form.Control
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              isInvalid={!!errors.email}
              disabled={isSubmitting}
              placeholder="Enter email address"
            />
            <Form.Control.Feedback type="invalid">
              {errors.email}
            </Form.Control.Feedback>
          </Form.Group>
          
          <h5 className="mt-4 mb-3">Phone Numbers</h5>
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Primary Phone *</Form.Label>
                <Form.Control
                  type="tel"
                  name="phone_1"
                  value={formData.phone_1}
                  onChange={handleChange}
                  isInvalid={!!errors.phone_1}
                  disabled={isSubmitting}
                  placeholder="Primary phone number"
                  required
                />
                <Form.Control.Feedback type="invalid">
                  {errors.phone_1}
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Secondary Phone</Form.Label>
                <Form.Control
                  type="tel"
                  name="phone_2"
                  value={formData.phone_2}
                  onChange={handleChange}
                  isInvalid={!!errors.phone_2}
                  disabled={isSubmitting}
                  placeholder="Secondary phone (optional)"
                />
                <Form.Control.Feedback type="invalid">
                  {errors.phone_2}
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
          </Row>
          
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Additional Phone</Form.Label>
                <Form.Control
                  type="tel"
                  name="phone_3"
                  value={formData.phone_3}
                  onChange={handleChange}
                  isInvalid={!!errors.phone_3}
                  disabled={isSubmitting}
                  placeholder="Additional phone (optional)"
                />
                <Form.Control.Feedback type="invalid">
                  {errors.phone_3}
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Additional Phone</Form.Label>
                <Form.Control
                  type="tel"
                  name="phone_4"
                  value={formData.phone_4}
                  onChange={handleChange}
                  isInvalid={!!errors.phone_4}
                  disabled={isSubmitting}
                  placeholder="Additional phone (optional)"
                />
                <Form.Control.Feedback type="invalid">
                  {errors.phone_4}
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
          </Row>
          
          <h5 className="mt-4 mb-3">Property Information</h5>
          <Form.Group className="mb-3">
            <Form.Label>Address</Form.Label>
            <Form.Control
              type="text"
              name="address"
              value={formData.address}
              onChange={handleChange}
              isInvalid={!!errors.address}
              disabled={isSubmitting}
              placeholder="Street address"
            />
            <Form.Control.Feedback type="invalid">
              {errors.address}
            </Form.Control.Feedback>
          </Form.Group>
          
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>ZIP Code</Form.Label>
                <Form.Control
                  type="text"
                  name="zip"
                  value={formData.zip}
                  onChange={handleChange}
                  isInvalid={!!errors.zip}
                  disabled={isSubmitting}
                  placeholder="ZIP code"
                />
                <Form.Control.Feedback type="invalid">
                  {errors.zip}
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Resort</Form.Label>
                <Form.Control
                  type="text"
                  name="resort"
                  value={formData.resort}
                  onChange={handleChange}
                  isInvalid={!!errors.resort}
                  disabled={isSubmitting}
                  placeholder="Resort name"
                />
                <Form.Control.Feedback type="invalid">
                  {errors.resort}
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
          </Row>
          
          <Form.Group className="mb-3">
            <Form.Check
              type="checkbox"
              id="mortgaged"
              name="mortgaged"
              label="Property is mortgaged"
              checked={formData.mortgaged}
              onChange={handleChange}
              disabled={isSubmitting}
            />
          </Form.Group>
          
          <Form.Group className="mb-3">
            <Form.Label>Status</Form.Label>
            <Form.Select
              name="status"
              value={formData.status}
              onChange={handleChange}
              disabled={isSubmitting}
            >
              <option value="NEW">NEW</option>
              <option value="SENT">SENT</option>
              <option value="REPLIED">REPLIED</option>
              <option value="BOOKED">BOOKED</option>
            </Form.Select>
          </Form.Group>
        </Modal.Body>
        
        <Modal.Footer>
          <Button variant="secondary" onClick={onHide} disabled={isSubmitting}>
            Cancel
          </Button>
          <Button type="submit" variant="primary" disabled={isSubmitting}>
            {isSubmitting ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Saving...
              </>
            ) : (
              'Save Lead'
            )}
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
};

export default LeadForm;
