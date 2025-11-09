import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { registerUser } from '../api/auth';
import './Register.css';

const Register = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [apiError, setApiError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const navigate = useNavigate();

  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  };

  const validatePassword = (password) => {
    return password.length >= 8;
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!validateEmail(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (!formData.firstName) {
      newErrors.firstName = 'First name is required';
    }

    if (!formData.lastName) {
      newErrors.lastName = 'Last name is required';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (!validatePassword(formData.password)) {
      newErrors.password = 'Password must be at least 8 characters long';
    }

    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setApiError('');
    setSuccessMessage('');

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      await registerUser(
        formData.email,
        formData.password,
        formData.firstName,
        formData.lastName
      );
      setSuccessMessage('Registration successful! Redirecting to login...');
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (error) {
      console.error('Registration failed:', error);
      const errorMessage = error.response?.data?.email?.[0] ||
                          error.response?.data?.detail ||
                          'Registration failed. Please try again.';
      setApiError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (field) => (e) => {
    setFormData({ ...formData, [field]: e.target.value });
    if (errors[field]) {
      setErrors({ ...errors, [field]: '' });
    }
  };

  return (
    <div className="register-container" data-easytag="id1-react/src/components/Register.js">
      <div className="register-card" data-easytag="id2-react/src/components/Register.js">
        <h1 className="register-title" data-easytag="id3-react/src/components/Register.js">Create Account</h1>
        <p className="register-subtitle" data-easytag="id4-react/src/components/Register.js">
          Sign up to get started
        </p>

        {apiError && (
          <div className="error-message" data-easytag="id5-react/src/components/Register.js">
            {apiError}
          </div>
        )}

        {successMessage && (
          <div className="success-message" data-easytag="id6-react/src/components/Register.js">
            {successMessage}
          </div>
        )}

        <form onSubmit={handleSubmit} className="register-form" data-easytag="id7-react/src/components/Register.js">
          <div className="form-row" data-easytag="id8-react/src/components/Register.js">
            <div className="form-group" data-easytag="id9-react/src/components/Register.js">
              <label htmlFor="firstName" data-easytag="id10-react/src/components/Register.js">First Name</label>
              <input
                type="text"
                id="firstName"
                value={formData.firstName}
                onChange={handleChange('firstName')}
                className={errors.firstName ? 'error' : ''}
                placeholder="John"
                disabled={isSubmitting}
                data-easytag="id11-react/src/components/Register.js"
              />
              {errors.firstName && (
                <span className="field-error" data-easytag="id12-react/src/components/Register.js">
                  {errors.firstName}
                </span>
              )}
            </div>

            <div className="form-group" data-easytag="id13-react/src/components/Register.js">
              <label htmlFor="lastName" data-easytag="id14-react/src/components/Register.js">Last Name</label>
              <input
                type="text"
                id="lastName"
                value={formData.lastName}
                onChange={handleChange('lastName')}
                className={errors.lastName ? 'error' : ''}
                placeholder="Doe"
                disabled={isSubmitting}
                data-easytag="id15-react/src/components/Register.js"
              />
              {errors.lastName && (
                <span className="field-error" data-easytag="id16-react/src/components/Register.js">
                  {errors.lastName}
                </span>
              )}
            </div>
          </div>

          <div className="form-group" data-easytag="id17-react/src/components/Register.js">
            <label htmlFor="email" data-easytag="id18-react/src/components/Register.js">Email</label>
            <input
              type="email"
              id="email"
              value={formData.email}
              onChange={handleChange('email')}
              className={errors.email ? 'error' : ''}
              placeholder="john.doe@example.com"
              disabled={isSubmitting}
              data-easytag="id19-react/src/components/Register.js"
            />
            {errors.email && (
              <span className="field-error" data-easytag="id20-react/src/components/Register.js">
                {errors.email}
              </span>
            )}
          </div>

          <div className="form-group" data-easytag="id21-react/src/components/Register.js">
            <label htmlFor="password" data-easytag="id22-react/src/components/Register.js">Password</label>
            <div className="password-input-wrapper" data-easytag="id23-react/src/components/Register.js">
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                value={formData.password}
                onChange={handleChange('password')}
                className={errors.password ? 'error' : ''}
                placeholder="At least 8 characters"
                disabled={isSubmitting}
                data-easytag="id24-react/src/components/Register.js"
              />
              <button
                type="button"
                className="toggle-password"
                onClick={() => setShowPassword(!showPassword)}
                disabled={isSubmitting}
                data-easytag="id25-react/src/components/Register.js"
              >
                {showPassword ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
            {errors.password && (
              <span className="field-error" data-easytag="id26-react/src/components/Register.js">
                {errors.password}
              </span>
            )}
          </div>

          <div className="form-group" data-easytag="id27-react/src/components/Register.js">
            <label htmlFor="confirmPassword" data-easytag="id28-react/src/components/Register.js">Confirm Password</label>
            <div className="password-input-wrapper" data-easytag="id29-react/src/components/Register.js">
              <input
                type={showConfirmPassword ? 'text' : 'password'}
                id="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange('confirmPassword')}
                className={errors.confirmPassword ? 'error' : ''}
                placeholder="Re-enter your password"
                disabled={isSubmitting}
                data-easytag="id30-react/src/components/Register.js"
              />
              <button
                type="button"
                className="toggle-password"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                disabled={isSubmitting}
                data-easytag="id31-react/src/components/Register.js"
              >
                {showConfirmPassword ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
            {errors.confirmPassword && (
              <span className="field-error" data-easytag="id32-react/src/components/Register.js">
                {errors.confirmPassword}
              </span>
            )}
          </div>

          <button
            type="submit"
            className="submit-button"
            disabled={isSubmitting}
            data-easytag="id33-react/src/components/Register.js"
          >
            {isSubmitting ? 'Creating Account...' : 'Register'}
          </button>
        </form>

        <div className="login-link" data-easytag="id34-react/src/components/Register.js">
          <p data-easytag="id35-react/src/components/Register.js">
            Already have an account?{' '}
            <Link to="/login" data-easytag="id36-react/src/components/Register.js">
              Login here
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;