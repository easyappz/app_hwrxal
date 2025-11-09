import { instance } from './axios';

/**
 * Authentication service for handling user registration, login, logout,
 * token management, and profile operations
 */

const TOKEN_KEY = 'token';
const REFRESH_TOKEN_KEY = 'refresh_token';

/**
 * Save tokens to localStorage
 * @param {string} accessToken - JWT access token
 * @param {string} refreshToken - JWT refresh token
 */
const saveTokens = (accessToken, refreshToken) => {
  if (accessToken) {
    localStorage.setItem(TOKEN_KEY, accessToken);
  }
  if (refreshToken) {
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  }
};

/**
 * Clear tokens from localStorage
 */
const clearTokens = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
};

/**
 * Get access token from localStorage
 * @returns {string|null} Access token
 */
export const getAccessToken = () => {
  return localStorage.getItem(TOKEN_KEY);
};

/**
 * Get refresh token from localStorage
 * @returns {string|null} Refresh token
 */
export const getRefreshToken = () => {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
};

/**
 * Register a new user
 * @param {Object} userData - User registration data
 * @param {string} userData.email - User email
 * @param {string} userData.password - User password
 * @param {string} userData.password_confirm - Password confirmation
 * @param {string} userData.first_name - User first name
 * @param {string} userData.last_name - User last name
 * @returns {Promise} Response with user data and tokens
 */
export const register = async (userData) => {
  try {
    const response = await instance.post('/api/auth/register/', userData);
    
    if (response.data.access && response.data.refresh) {
      saveTokens(response.data.access, response.data.refresh);
    }
    
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Login user
 * @param {Object} credentials - User login credentials
 * @param {string} credentials.email - User email
 * @param {string} credentials.password - User password
 * @returns {Promise} Response with user data and tokens
 */
export const login = async (credentials) => {
  try {
    const response = await instance.post('/api/auth/login/', credentials);
    
    if (response.data.access && response.data.refresh) {
      saveTokens(response.data.access, response.data.refresh);
    }
    
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Logout user
 * @param {string} refreshToken - Refresh token to invalidate (optional, will use stored token if not provided)
 * @returns {Promise} Response confirmation
 */
export const logout = async (refreshToken = null) => {
  try {
    const token = refreshToken || getRefreshToken();
    
    if (token) {
      await instance.post('/api/auth/logout/', { refresh: token });
    }
    
    clearTokens();
    
    return { success: true };
  } catch (error) {
    // Clear tokens even if request fails
    clearTokens();
    throw error;
  }
};

/**
 * Refresh access token
 * @param {string} refreshToken - Refresh token (optional, will use stored token if not provided)
 * @returns {Promise} Response with new access token
 */
export const refreshToken = async (refreshToken = null) => {
  try {
    const token = refreshToken || getRefreshToken();
    
    if (!token) {
      throw new Error('No refresh token available');
    }
    
    const response = await instance.post('/api/auth/token/refresh/', { refresh: token });
    
    if (response.data.access) {
      localStorage.setItem(TOKEN_KEY, response.data.access);
    }
    
    // Some implementations return a new refresh token as well
    if (response.data.refresh) {
      localStorage.setItem(REFRESH_TOKEN_KEY, response.data.refresh);
    }
    
    return response.data;
  } catch (error) {
    // If refresh fails, clear tokens
    clearTokens();
    throw error;
  }
};

/**
 * Get current user profile
 * @returns {Promise} Response with user profile data
 */
export const getCurrentUser = async () => {
  try {
    const response = await instance.get('/api/auth/me/');
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Update user profile
 * @param {Object} userData - User profile data to update
 * @param {string} userData.first_name - User first name (optional)
 * @param {string} userData.last_name - User last name (optional)
 * @param {string} userData.email - User email (optional)
 * @returns {Promise} Response with updated user data
 */
export const updateProfile = async (userData) => {
  try {
    const response = await instance.patch('/api/auth/me/', userData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Change user password
 * @param {Object} passwordData - Password change data
 * @param {string} passwordData.old_password - Current password
 * @param {string} passwordData.new_password - New password
 * @param {string} passwordData.new_password_confirm - New password confirmation
 * @returns {Promise} Response confirmation
 */
export const changePassword = async (passwordData) => {
  try {
    const response = await instance.post('/api/auth/password/change/', passwordData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Request password reset
 * @param {string} email - User email
 * @returns {Promise} Response confirmation
 */
export const requestPasswordReset = async (email) => {
  try {
    const response = await instance.post('/api/auth/password/reset/', { email });
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Confirm password reset with token
 * @param {Object} resetData - Password reset confirmation data
 * @param {string} resetData.token - Password reset token
 * @param {string} resetData.new_password - New password
 * @param {string} resetData.new_password_confirm - New password confirmation
 * @returns {Promise} Response confirmation
 */
export const confirmPasswordReset = async (resetData) => {
  try {
    const response = await instance.post('/api/auth/password/reset/confirm/', resetData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Check if user is authenticated
 * @returns {boolean} True if access token exists
 */
export const isAuthenticated = () => {
  return !!getAccessToken();
};

const authService = {
  register,
  login,
  logout,
  refreshToken,
  getCurrentUser,
  updateProfile,
  changePassword,
  requestPasswordReset,
  confirmPasswordReset,
  isAuthenticated,
  getAccessToken,
  getRefreshToken,
};

export default authService;
