import axios from 'axios';

const API_BASE_URL = 'https://hsplusgenerateadcopy-production.up.railway.app';

export const api = {
  scrapeProduct: async (url) => {
    const response = await axios.post(`${API_BASE_URL}/scrape`, { url });
    return response.data;
  },

  generateCopy: async (formData) => {
    const response = await axios.post(`${API_BASE_URL}/generate`, formData);
    return response.data;
  },

  getExamples: async () => {
    const response = await axios.get(`${API_BASE_URL}/examples`);
    return response.data;
  },

  healthCheck: async () => {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  }
};
