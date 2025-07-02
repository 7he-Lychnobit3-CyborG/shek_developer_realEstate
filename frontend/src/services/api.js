import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Property API
export const propertyAPI = {
  getAll: (params = {}) => {
    const queryParams = new URLSearchParams(params).toString();
    return axios.get(`${API}/properties${queryParams ? `?${queryParams}` : ''}`);
  },
  
  getById: (id) => axios.get(`${API}/properties/${id}`),
  
  create: (data) => axios.post(`${API}/properties`, data),
  
  update: (id, data) => axios.put(`${API}/properties/${id}`, data),
  
  delete: (id) => axios.delete(`${API}/properties/${id}`),
  
  search: (searchParams) => axios.post(`${API}/properties/search`, searchParams),
};

// Favorites API
export const favoritesAPI = {
  getAll: () => axios.get(`${API}/favorites`),
  
  add: (propertyId) => axios.post(`${API}/favorites/${propertyId}`),
  
  remove: (propertyId) => axios.delete(`${API}/favorites/${propertyId}`),
};

// Inquiries API
export const inquiriesAPI = {
  getAll: () => axios.get(`${API}/inquiries`),
  
  create: (data) => axios.post(`${API}/inquiries`, data),
};

// Stats API
export const statsAPI = {
  getStats: () => axios.get(`${API}/stats`),
};

export default {
  propertyAPI,
  favoritesAPI,
  inquiriesAPI,
  statsAPI,
};