import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { changePassword } from '../api/auth';
import './AuthForm.css';

const ChangePassword = () => {
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (newPassword !== confirmPassword) {
      setError('New passwords do not match');
      return;
    }

    setLoading(true);

    try {
      await changePassword(oldPassword, newPassword);
      setSuccess('Password changed successfully!');
      setTimeout(() => {
        navigate('/profile');
      }, 2000);
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to change password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page" data-easytag="id91-react/src/components/ChangePassword.js">
      <div className="auth-container" data-easytag="id92-react/src/components/ChangePassword.js">
        <h2 data-easytag="id93-react/src/components/ChangePassword.js">Change Password</h2>
        <form onSubmit={handleSubmit} className="auth-form" data-easytag="id94-react/src/components/ChangePassword.js">
          {error && (
            <div className="error-message" data-easytag="id95-react/src/components/ChangePassword.js">
              {error}
            </div>
          )}
          {success && (
            <div className="success-message" data-easytag="id96-react/src/components/ChangePassword.js">
              {success}
            </div>
          )}
          <div className="form-group" data-easytag="id97-react/src/components/ChangePassword.js">
            <label htmlFor="oldPassword" data-easytag="id98-react/src/components/ChangePassword.js">Current Password</label>
            <input
              type="password"
              id="oldPassword"
              value={oldPassword}
              onChange={(e) => setOldPassword(e.target.value)}
              required
              disabled={loading}
              data-easytag="id99-react/src/components/ChangePassword.js"
            />
          </div>
          <div className="form-group" data-easytag="id100-react/src/components/ChangePassword.js">
            <label htmlFor="newPassword" data-easytag="id101-react/src/components/ChangePassword.js">New Password</label>
            <input
              type="password"
              id="newPassword"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
              disabled={loading}
              data-easytag="id102-react/src/components/ChangePassword.js"
            />
          </div>
          <div className="form-group" data-easytag="id103-react/src/components/ChangePassword.js">
            <label htmlFor="confirmPassword" data-easytag="id104-react/src/components/ChangePassword.js">Confirm New Password</label>
            <input
              type="password"
              id="confirmPassword"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              disabled={loading}
              data-easytag="id105-react/src/components/ChangePassword.js"
            />
          </div>
          <button 
            type="submit" 
            className="submit-button" 
            disabled={loading}
            data-easytag="id106-react/src/components/ChangePassword.js"
          >
            {loading ? 'Changing...' : 'Change Password'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChangePassword;