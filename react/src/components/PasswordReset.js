import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { requestPasswordReset } from '../api/auth';
import './AuthForm.css';

const PasswordReset = () => {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      await requestPasswordReset(email);
      setSuccess('Password reset instructions have been sent to your email.');
      setEmail('');
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to send reset instructions');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page" data-easytag="id79-react/src/components/PasswordReset.js">
      <div className="auth-container" data-easytag="id80-react/src/components/PasswordReset.js">
        <h2 data-easytag="id81-react/src/components/PasswordReset.js">Reset Password</h2>
        <form onSubmit={handleSubmit} className="auth-form" data-easytag="id82-react/src/components/PasswordReset.js">
          {error && (
            <div className="error-message" data-easytag="id83-react/src/components/PasswordReset.js">
              {error}
            </div>
          )}
          {success && (
            <div className="success-message" data-easytag="id84-react/src/components/PasswordReset.js">
              {success}
            </div>
          )}
          <div className="form-group" data-easytag="id85-react/src/components/PasswordReset.js">
            <label htmlFor="email" data-easytag="id86-react/src/components/PasswordReset.js">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={loading}
              data-easytag="id87-react/src/components/PasswordReset.js"
            />
          </div>
          <button 
            type="submit" 
            className="submit-button" 
            disabled={loading}
            data-easytag="id88-react/src/components/PasswordReset.js"
          >
            {loading ? 'Sending...' : 'Send Reset Instructions'}
          </button>
          <div className="auth-links" data-easytag="id89-react/src/components/PasswordReset.js">
            <Link to="/login" data-easytag="id90-react/src/components/PasswordReset.js">Back to Login</Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default PasswordReset;