import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = {
  searchWord: async (word) => {
    try {
      const response = await axios.post(`${API_URL}/api/search`, { word });
      return response.data;
    } catch (error) {
      console.error('API request failed:', error.response ? error.response.data : error.message);
      throw error;
    }
  },
};

export default api;