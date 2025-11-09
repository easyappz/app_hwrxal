import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { authAPI } from '../api/auth';
import { instance } from '../api/axios';

/**
 * Authentication context
 */
const AuthContext = createContext(null);

/**
 * Custom hook to use authentication context
 * @returns {Object} Authentication context value
 */
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

/**
 * Authentication provider component
 * Manages authentication state and provides auth functions to the app
 */
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [refreshTimer, setRefreshTimer] = useState(null);

  /**
   * Refresh access token using refresh token
   */
  const refreshAccessToken = useCallback(async () => {
    try {
      const refreshToken = localStorage.getItem('refreshToken');
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const data = await authAPI.refreshToken(refreshToken);
      
      if (data.access) {
        localStorage.setItem('token', data.access);
        return true;
      }
      
      return false;
    } catch (error) {
      console.error('Token refresh failed:', error);
      await logout();
      return false;
    }
  }, []);

  /**
   * Set up automatic token refresh
   * Refresh token 1 minute before expiration
   */
  const setupTokenRefresh = useCallback(() => {
    // Clear existing timer
    if (refreshTimer) {
      clearTimeout(refreshTimer);
    }

    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      // Decode JWT to get expiration time
      const payload = JSON.parse(atob(token.split('.')[1]));
      const expiresIn = payload.exp * 1000 - Date.now();
      
      // Refresh 1 minute before expiration
      const refreshTime = expiresIn - 60000;
      
      if (refreshTime > 0) {
        const timer = setTimeout(() => {
          refreshAccessToken();
        }, refreshTime);
        
        setRefreshTimer(timer);
      } else {
        // Token already expired or about to expire, refresh immediately
        refreshAccessToken();
      }
    } catch (error) {
      console.error('Error setting up token refresh:', error);
    }
  }, [refreshAccessToken, refreshTimer]);

  /**
   * Load user data from API
   */
  const loadUser = useCallback(async () => {
    try {
      const userData = await authAPI.getCurrentUser();
      setUser(userData);
      setIsAuthenticated(true);
      setupTokenRefresh();
    } catch (error) {
      console.error('Failed to load user:', error);
      // If loading user fails, clear tokens and logout
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
      setUser(null);
      setIsAuthenticated(false);
    } finally {
      setIsLoading(false);
    }
  }, [setupTokenRefresh]);

  /**
   * Login user
   * @param {string} email - User email
   * @param {string} password - User password
   */
  const login = async (email, password) => {
    try {
      const data = await authAPI.login({ email, password });
      
      // Store tokens
      if (data.access) {
        localStorage.setItem('token', data.access);
      }
      if (data.refresh) {
        localStorage.setItem('refreshToken', data.refresh);
      }
      
      // Set user data
      if (data.user) {
        setUser(data.user);
        setIsAuthenticated(true);
        setupTokenRefresh();
      } else {
        // If user data not in response, load it
        await loadUser();
      }
      
      return { success: true, data };
    } catch (error) {
      console.error('Login failed:', error);
      
      // If token-related error, ensure logout
      if (error.message && error.message.toLowerCase().includes('token')) {
        await logout();
      }
      
      return { 
        success: false, 
        error: error.message || 'Login failed. Please try again.'
      };
    }
  };

  /**
   * Register new user
   * @param {Object} userData - User registration data
   */
  const register = async (userData) => {
    try {
      const data = await authAPI.register(userData);
      
      // Store tokens
      if (data.access) {
        localStorage.setItem('token', data.access);
      }
      if (data.refresh) {
        localStorage.setItem('refreshToken', data.refresh);
      }
      
      // Set user data
      if (data.user) {
        setUser(data.user);
        setIsAuthenticated(true);
        setupTokenRefresh();
      } else {
        // If user data not in response, load it
        await loadUser();
      }
      
      return { success: true, data };
    } catch (error) {
      console.error('Registration failed:', error);
      return { 
        success: false, 
        error: error.message || 'Registration failed. Please try again.'
      };
    }
  };

  /**
   * Logout user
   */
  const logout = async () => {
    try {
      const refreshToken = localStorage.getItem('refreshToken');
      if (refreshToken) {
        await authAPI.logout(refreshToken);
      }
    } catch (error) {
      console.error('Logout API call failed:', error);
    } finally {
      // Clear tokens and user data
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
      setUser(null);
      setIsAuthenticated(false);
      
      // Clear refresh timer
      if (refreshTimer) {
        clearTimeout(refreshTimer);
        setRefreshTimer(null);
      }
    }
  };

  /**
   * Update user data
   * @param {Object} userData - User data to update
   */
  const updateUser = async (userData) => {
    try {
      const updatedUser = await authAPI.updateProfile(userData);
      setUser(updatedUser);
      return { success: true, data: updatedUser };
    } catch (error) {
      console.error('Update user failed:', error);
      
      // If token-related error, logout
      if (error.message && error.message.toLowerCase().includes('token')) {
        await logout();
      }
      
      return { 
        success: false, 
        error: error.message || 'Update failed. Please try again.'
      };
    }
  };

  /**
   * Check if user is authenticated on mount
   */
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      loadUser();
    } else {
      setIsLoading(false);
    }

    // Cleanup timer on unmount
    return () => {
      if (refreshTimer) {
        clearTimeout(refreshTimer);
      }
    };
  }, []);

  const value = {
    user,
    isAuthenticated,
    isLoading,
    login,
    logout,
    register,
    updateUser,
    refreshAccessToken,
  };

  return (
    <AuthContext.Provider value={value} data-easytag="id1-react/src/contexts/AuthContext.js">
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
