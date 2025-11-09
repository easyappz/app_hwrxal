import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import authService from '../api/auth';
import './Register.css';

const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    first_name: '',
    last_name: '',
    password: '',
    confirmPassword: '',
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [apiError, setApiError] = useState('');

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!validateEmail(formData.email)) {
      newErrors.email = 'Invalid email format';
    }

    if (!formData.first_name.trim()) {
      newErrors.first_name = 'First name is required';
    }

    if (!formData.last_name.trim()) {
      newErrors.last_name = 'Last name is required';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: '',
      });
    }
    setApiError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setApiError('');
    setSuccessMessage('');

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      const { confirmPassword, ...registrationData } = formData;
      await authService.register(registrationData);
      setSuccessMessage('Registration successful! Redirecting to login...');
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (error) {
      console.error('Registration error:', error);
      if (error.response?.data) {
        const errorData = error.response.data;
        if (typeof errorData === 'object') {
          // Handle field-specific errors
          const fieldErrors = {};
          Object.keys(errorData).forEach((key) => {
            if (Array.isArray(errorData[key])) {
              fieldErrors[key] = errorData[key][0];
            } else {
              fieldErrors[key] = errorData[key];
            }
          });
          setErrors(fieldErrors);
        } else {
          setApiError(errorData.message || 'Registration failed. Please try again.');
        }
      } else {
        setApiError('Registration failed. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleLoginClick = () => {
    navigate('/login');
  };

  return (
    <div className="register-container" data-easytag="id1-react/src/components/Register.js">
      <div className="register-card" data-easytag="id2-react/src/components/Register.js">
        <h1 className="register-title" data-easytag="id3-react/src/components/Register.js">Create Account</h1>
        <p className="register-subtitle" data-easytag="id4-react/src/components/Register.js">Sign up to get started</p>

        {successMessage && (
          <div className="success-message" data-easytag="id5-react/src/components/Register.js">
            {successMessage}
          </div>
        )}

        {apiError && (
          <div className="error-message" data-easytag="id6-react/src/components/Register.js">
            {apiError}
          </div>
        )}

        <form onSubmit={handleSubmit} className="register-form" data-easytag="id7-react/src/components/Register.js">
          <div className="form-group" data-easytag="id8-react/src/components/Register.js">
            <label htmlFor="email" data-easytag="id9-react/src/components/Register.js">Email *</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className={errors.email ? 'input-error' : ''}
              placeholder="your.email@example.com"
              disabled={isLoading}
              data-easytag="id10-react/src/components/Register.js"
            />
            {errors.email && (
              <span className="field-error" data-easytag="id11-react/src/components/Register.js">{errors.email}</span>
            )}
          </div>

          <div className="form-row" data-easytag="id12-react/src/components/Register.js">
            <div className="form-group" data-easytag="id13-react/src/components/Register.js">
              <label htmlFor="first_name" data-easytag="id14-react/src/components/Register.js">First Name *</label>
              <input
                type="text"
                id="first_name"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                className={errors.first_name ? 'input-error' : ''}
                placeholder="John"
                disabled={isLoading}
                data-easytag="id15-react/src/components/Register.js"
              />
              {errors.first_name && (
                <span className="field-error" data-easytag="id16-react/src/components/Register.js">{errors.first_name}</span>
              )}
            </div>

            <div className="form-group" data-easytag="id17-react/src/components/Register.js">
              <label htmlFor="last_name" data-easytag="id18-react/src/components/Register.js">Last Name *</label>
              <input
                type="text"
                id="last_name"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                className={errors.last_name ? 'input-error' : ''}
                placeholder="Doe"
                disabled={isLoading}
                data-easytag="id19-react/src/components/Register.js"
              />
              {errors.last_name && (
                <span className="field-error" data-easytag="id20-react/src/components/Register.js">{errors.last_name}</span>
              )}
            </div>
          </div>

          <div className="form-group" data-easytag="id21-react/src/components/Register.js">
            <label htmlFor="password" data-easytag="id22-react/src/components/Register.js">Password *</label>
            <div className="password-input-wrapper" data-easytag="id23-react/src/components/Register.js">
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className={errors.password ? 'input-error' : ''}
                placeholder="••••••••"
                disabled={isLoading}
                data-easytag="id24-react/src/components/Register.js"
              />
              <button
                type="button"
                className="toggle-password"
                onClick={() => setShowPassword(!showPassword)}
                disabled={isLoading}
                data-easytag="id25-react/src/components/Register.js"
              >
                {showPassword ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
            {errors.password && (
              <span className="field-error" data-easytag="id26-react/src/components/Register.js">{errors.password}</span>
            )}
          </div>

          <div className="form-group" data-easytag="id27-react/src/components/Register.js">
            <label htmlFor="confirmPassword" data-easytag="id28-react/src/components/Register.js">Confirm Password *</label>
            <div className="password-input-wrapper" data-easytag="id29-react/src/components/Register.js">
              <input
                type={showConfirmPassword ? 'text' : 'password'}
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className={errors.confirmPassword ? 'input-error' : ''}
                placeholder="••••••••"
                disabled={isLoading}
                data-easytag="id30-react/src/components/Register.js"
              />
              <button
                type="button"
                className="toggle-password"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                disabled={isLoading}
                data-easytag="id31-react/src/components/Register.js"
              >
                {showConfirmPassword ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
            {errors.confirmPassword && (
              <span className="field-error" data-easytag="id32-react/src/components/Register.js">{errors.confirmPassword}</span>
            )}
          </div>

          <button
            type="submit"
            className="register-button"
            disabled={isLoading}
            data-easytag="id33-react/src/components/Register.js"
          >
            {isLoading ? 'Creating Account...' : 'Sign Up'}
          </button>
        </form>

        <div className="login-link-container" data-easytag="id34-react/src/components/Register.js">
          <p data-easytag="id35-react/src/components/Register.js">
            Already have an account?{' '}
            <button
              type="button"
              onClick={handleLoginClick}
              className="link-button"
              disabled={isLoading}
              data-easytag="id36-react/src/components/Register.js"
            >
              Sign In
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
