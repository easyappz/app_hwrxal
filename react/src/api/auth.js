import { instance } from './axios';

/**
 * API functions for authentication
 */

export const authAPI = {
  /**
   * Login user
   * @param {Object} credentials - User credentials
   * @param {string} credentials.email - User email
   * @param {string} credentials.password - User password
   * @returns {Promise} - Response with tokens and user data
   */
  login: async (credentials) => {
    const response = await instance.post('/api/auth/login/', credentials);
    return response.data;
  },

  /**
   * Register new user
   * @param {Object} userData - User registration data
   * @param {string} userData.email - User email
   * @param {string} userData.password - User password
   * @param {string} userData.first_name - User first name
   * @param {string} userData.last_name - User last name
   * @returns {Promise} - Response with tokens and user data
   */
  register: async (userData) => {
    const response = await instance.post('/api/auth/register/', userData);
    return response.data;
  },

  /**
   * Get current user profile
   * @returns {Promise} - User data
   */
  getCurrentUser: async () => {
    const response = await instance.get('/api/auth/profile/');
    return response.data;
  },

  /**
   * Refresh access token
   * @param {string} refreshToken - Refresh token
   * @returns {Promise} - Response with new access token
   */
  refreshToken: async (refreshToken) => {
    const response = await instance.post('/api/auth/refresh/', {
      refresh: refreshToken,
    });
    return response.data;
  },

  /**
   * Logout user
   * @returns {Promise} - Response
   */
  logout: async () => {
    const response = await instance.post('/api/auth/logout/');
    return response.data;
  },

  /**
   * Update user profile
   * @param {Object} userData - User data to update
   * @returns {Promise} - Updated user data
   */
  updateProfile: async (userData) => {
    const response = await instance.patch('/api/auth/profile/', userData);
    return response.data;
  },
};
