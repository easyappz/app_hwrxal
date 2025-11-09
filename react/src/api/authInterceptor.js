import { instance } from './axios';

/**
 * List of public endpoints that don't require authentication
 * These endpoints should not have the Authorization header
 */
const PUBLIC_ENDPOINTS = [
  '/api/auth/login/',
  '/api/auth/register/',
  '/api/auth/token/refresh/',
  '/api/auth/password/reset/',
  '/api/auth/password/reset/confirm/',
];

/**
 * Check if the URL is a public endpoint that doesn't require authentication
 * @param {string} url - The request URL
 * @returns {boolean} - True if the endpoint is public
 */
const isPublicEndpoint = (url) => {
  if (!url) return false;
  
  return PUBLIC_ENDPOINTS.some(endpoint => {
    // Check if URL matches the public endpoint
    return url.includes(endpoint);
  });
};

/**
 * Configure request interceptor to conditionally add Authorization header
 * Public endpoints will not receive the Authorization header
 */
instance.interceptors.request.use(
  (config) => {
    const url = config.url || '';
    
    // Check if this is a public endpoint
    if (isPublicEndpoint(url)) {
      // Remove Authorization header for public endpoints
      delete config.headers['Authorization'];
      console.log('Public endpoint detected, Authorization header removed:', url);
    } else {
      // For protected endpoints, add Authorization header if token exists
      const token = localStorage.getItem('token');
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
        console.log('Protected endpoint, Authorization header added:', url);
      }
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default instance;
