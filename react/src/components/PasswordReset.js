import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { requestPasswordReset } from '../api/auth';
import './PasswordReset.css';

const PasswordReset = () => {
  const [email, setEmail] = useState('');
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [apiError, setApiError] = useState('');

  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  };

  const validateForm = () => {
    const newErrors = {};

    if (!email) {
      newErrors.email = 'Email is required';
    } else if (!validateEmail(email)) {
      newErrors.email = 'Please enter a valid email address';
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
      await requestPasswordReset(email);
      setSuccessMessage('Password reset instructions have been sent to your email.');
      setEmail('');
    } catch (error) {
      console.error('Password reset request failed:', error);
      setApiError(error.response?.data?.detail || 'Failed to send reset email. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
    if (errors.email) {
      setErrors({ ...errors, email: '' });
    }
  };

  return (
    <div className="password-reset-container" data-easytag="id1-react/src/components/PasswordReset.js">
      <div className="password-reset-card" data-easytag="id2-react/src/components/PasswordReset.js">
        <h1 className="password-reset-title" data-easytag="id3-react/src/components/PasswordReset.js">Reset Password</h1>
        <p className="password-reset-subtitle" data-easytag="id4-react/src/components/PasswordReset.js">
          Enter your email address and we'll send you instructions to reset your password.
        </p>

        {apiError && (
          <div className="error-message" data-easytag="id5-react/src/components/PasswordReset.js">
            {apiError}
          </div>
        )}

        {successMessage && (
          <div className="success-message" data-easytag="id6-react/src/components/PasswordReset.js">
            {successMessage}
          </div>
        )}

        <form onSubmit={handleSubmit} className="password-reset-form" data-easytag="id7-react/src/components/PasswordReset.js">
          <div className="form-group" data-easytag="id8-react/src/components/PasswordReset.js">
            <label htmlFor="email" data-easytag="id9-react/src/components/PasswordReset.js">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={handleEmailChange}
              className={errors.email ? 'error' : ''}
              placeholder="Enter your email"
              disabled={isSubmitting}
              data-easytag="id10-react/src/components/PasswordReset.js"
            />
            {errors.email && (
              <span className="field-error" data-easytag="id11-react/src/components/PasswordReset.js">
                {errors.email}
              </span>
            )}
          </div>

          <button
            type="submit"
            className="submit-button"
            disabled={isSubmitting}
            data-easytag="id12-react/src/components/PasswordReset.js"
          >
            {isSubmitting ? 'Sending...' : 'Send Reset Instructions'}
          </button>
        </form>

        <div className="back-to-login" data-easytag="id13-react/src/components/PasswordReset.js">
          <Link to="/login" data-easytag="id14-react/src/components/PasswordReset.js">
            ← Back to Login
          </Link>
        </div>
      </div>
    </div>
  );
};

export default PasswordReset;