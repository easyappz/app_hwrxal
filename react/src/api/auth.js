import instance from './axios';

/**
 * Authentication service for user registration, login, and profile management
 */
const authService = {
  /**
   * Register a new user
   * @param {Object} userData - User registration data
   * @param {string} userData.email - User email
   * @param {string} userData.first_name - User first name
   * @param {string} userData.last_name - User last name
   * @param {string} userData.password - User password
   * @returns {Promise} Registration response
   */
  register: async (userData) => {
    const response = await instance.post('/api/register/', userData);
    return response.data;
  },

  /**
   * Login user
   * @param {Object} credentials - Login credentials
   * @param {string} credentials.email - User email
   * @param {string} credentials.password - User password
   * @returns {Promise} Login response with tokens
   */
  login: async (credentials) => {
    const response = await instance.post('/api/login/', credentials);
    if (response.data.access) {
      localStorage.setItem('token', response.data.access);
      if (response.data.refresh) {
        localStorage.setItem('refreshToken', response.data.refresh);
      }
    }
    return response.data;
  },

  /**
   * Logout user
   */
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
  },

  /**
   * Get current user profile
   * @returns {Promise} User profile data
   */
  getProfile: async () => {
    const response = await instance.get('/api/profile/');
    return response.data;
  },

  /**
   * Update user profile
   * @param {Object} profileData - Profile data to update
   * @returns {Promise} Updated profile data
   */
  updateProfile: async (profileData) => {
    const response = await instance.put('/api/profile/', profileData);
    return response.data;
  },

  /**
   * Request password reset
   * @param {string} email - User email
   * @returns {Promise} Password reset response
   */
  requestPasswordReset: async (email) => {
    const response = await instance.post('/api/password-reset/', { email });
    return response.data;
  },

  /**
   * Confirm password reset
   * @param {Object} resetData - Password reset data
   * @param {string} resetData.token - Reset token
   * @param {string} resetData.password - New password
   * @returns {Promise} Password reset confirmation response
   */
  confirmPasswordReset: async (resetData) => {
    const response = await instance.post('/api/password-reset/confirm/', resetData);
    return response.data;
  },

  /**
   * Refresh access token
   * @returns {Promise} New access token
   */
  refreshToken: async () => {
    const refreshToken = localStorage.getItem('refreshToken');
    const response = await instance.post('/api/token/refresh/', { refresh: refreshToken });
    if (response.data.access) {
      localStorage.setItem('token', response.data.access);
    }
    return response.data;
  },
};

export default authService;
