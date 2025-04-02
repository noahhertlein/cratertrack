import axios from 'axios';

// Base URL for API requests
const API_BASE_URL = 'http://localhost:5000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Handle errors globally
api.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API Error:', error.response || error);
    return Promise.reject(error.response?.data || error);
  }
);

// API functions

/**
 * Fetch all leads
 * @param {string} [status] - Optional status filter
 * @returns {Promise<{leads: Array}>}
 */
export const fetchLeads = (status) => {
  const params = status ? { status } : {};
  return api.get('/leads', { params });
};

/**
 * Create a new lead
 * @param {Object} leadData - Lead data to create
 * @returns {Promise<{lead: Object}>}
 */
export const createLead = (leadData) => {
  return api.post('/leads', leadData);
};

/**
 * Update an existing lead
 * @param {number} leadId - ID of the lead to update
 * @param {Object} leadData - Updated lead data
 * @returns {Promise<{lead: Object}>}
 */
export const updateLead = (leadId, leadData) => {
  return api.patch(`/leads/${leadId}`, leadData);
};

/**
 * Add a note to a lead
 * @param {number} leadId - ID of the lead
 * @param {Object} noteData - Note data to add
 * @returns {Promise<{note: Object}>}
 */
export const addNote = (leadId, noteData) => {
  return api.post(`/notes/${leadId}`, noteData);
};

export default api;
