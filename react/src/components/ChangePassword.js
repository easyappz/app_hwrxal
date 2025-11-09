import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import authService from '../api/authService';
import './ChangePassword.css';

const ChangePassword = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const [showPasswords, setShowPasswords] = useState({
    current: false,
    new: false,
    confirm: false
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  const validateForm = () => {
    const newErrors = {};

    if (!formData.currentPassword) {
      newErrors.currentPassword = 'Current password is required';
    }

    if (!formData.newPassword) {
      newErrors.newPassword = 'New password is required';
    } else if (formData.newPassword.length < 8) {
      newErrors.newPassword = 'Password must be at least 8 characters long';
    }

    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your new password';
    }

    if (formData.newPassword && formData.currentPassword && formData.newPassword === formData.currentPassword) {
      newErrors.newPassword = 'New password must be different from current password';
    }

    if (formData.newPassword && formData.confirmPassword && formData.newPassword !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const calculatePasswordStrength = (password) => {
    if (!password) return { strength: 0, label: '', color: '' };

    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[^a-zA-Z\d]/.test(password)) strength++;

    const levels = [
      { strength: 0, label: '', color: '' },
      { strength: 1, label: 'Weak', color: '#ff4444' },
      { strength: 2, label: 'Fair', color: '#ff8c00' },
      { strength: 3, label: 'Good', color: '#ffd700' },
      { strength: 4, label: 'Strong', color: '#9acd32' },
      { strength: 5, label: 'Very Strong', color: '#00cc00' }
    ];

    return levels[strength];
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const togglePasswordVisibility = (field) => {
    setShowPasswords(prev => ({
      ...prev,
      [field]: !prev[field]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setLoading(true);
    setErrors({});

    try {
      await authService.changePassword({
        old_password: formData.currentPassword,
        new_password: formData.newPassword,
        new_password_confirm: formData.confirmPassword
      });

      setSuccessMessage('Password changed successfully! Logging out...');
      
      setTimeout(async () => {
        await authService.logout();
        navigate('/login');
      }, 2000);
    } catch (error) {
      const errorMessage = error.response?.data;
      
      if (typeof errorMessage === 'object') {
        setErrors({
          currentPassword: errorMessage.old_password?.[0] || '',
          newPassword: errorMessage.new_password?.[0] || '',
          confirmPassword: errorMessage.new_password_confirm?.[0] || '',
          general: errorMessage.detail || errorMessage.non_field_errors?.[0] || 'Failed to change password'
        });
      } else {
        setErrors({ general: 'Failed to change password. Please try again.' });
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    navigate('/profile');
  };

  const passwordStrength = calculatePasswordStrength(formData.newPassword);

  return (
    <div className="change-password-container" data-easytag="id1-react/src/components/ChangePassword.js">
      <div className="change-password-card" data-easytag="id2-react/src/components/ChangePassword.js">
        <h2 className="change-password-title" data-easytag="id3-react/src/components/ChangePassword.js">
          Change Password
        </h2>
        
        {successMessage && (
          <div className="success-message" data-easytag="id4-react/src/components/ChangePassword.js">
            {successMessage}
          </div>
        )}
        
        {errors.general && (
          <div className="error-message" data-easytag="id5-react/src/components/ChangePassword.js">
            {errors.general}
          </div>
        )}

        <form onSubmit={handleSubmit} className="change-password-form" data-easytag="id6-react/src/components/ChangePassword.js">
          <div className="form-group" data-easytag="id7-react/src/components/ChangePassword.js">
            <label htmlFor="currentPassword" data-easytag="id8-react/src/components/ChangePassword.js">
              Current Password *
            </label>
            <div className="password-input-wrapper" data-easytag="id9-react/src/components/ChangePassword.js">
              <input
                type={showPasswords.current ? 'text' : 'password'}
                id="currentPassword"
                name="currentPassword"
                value={formData.currentPassword}
                onChange={handleChange}
                className={errors.currentPassword ? 'input-error' : ''}
                disabled={loading}
                data-easytag="id10-react/src/components/ChangePassword.js"
              />
              <button
                type="button"
                className="toggle-password"
                onClick={() => togglePasswordVisibility('current')}
                disabled={loading}
                data-easytag="id11-react/src/components/ChangePassword.js"
              >
                {showPasswords.current ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
            {errors.currentPassword && (
              <span className="field-error" data-easytag="id12-react/src/components/ChangePassword.js">
                {errors.currentPassword}
              </span>
            )}
          </div>

          <div className="form-group" data-easytag="id13-react/src/components/ChangePassword.js">
            <label htmlFor="newPassword" data-easytag="id14-react/src/components/ChangePassword.js">
              New Password *
            </label>
            <div className="password-input-wrapper" data-easytag="id15-react/src/components/ChangePassword.js">
              <input
                type={showPasswords.new ? 'text' : 'password'}
                id="newPassword"
                name="newPassword"
                value={formData.newPassword}
                onChange={handleChange}
                className={errors.newPassword ? 'input-error' : ''}
                disabled={loading}
                data-easytag="id16-react/src/components/ChangePassword.js"
              />
              <button
                type="button"
                className="toggle-password"
                onClick={() => togglePasswordVisibility('new')}
                disabled={loading}
                data-easytag="id17-react/src/components/ChangePassword.js"
              >
                {showPasswords.new ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
            {formData.newPassword && (
              <div className="password-strength" data-easytag="id18-react/src/components/ChangePassword.js">
                <div className="strength-bar" data-easytag="id19-react/src/components/ChangePassword.js">
                  <div
                    className="strength-fill"
                    style={{
                      width: `${(passwordStrength.strength / 5) * 100}%`,
                      backgroundColor: passwordStrength.color
                    }}
                    data-easytag="id20-react/src/components/ChangePassword.js"
                  ></div>
                </div>
                <span className="strength-label" style={{ color: passwordStrength.color }} data-easytag="id21-react/src/components/ChangePassword.js">
                  {passwordStrength.label}
                </span>
              </div>
            )}
            {errors.newPassword && (
              <span className="field-error" data-easytag="id22-react/src/components/ChangePassword.js">
                {errors.newPassword}
              </span>
            )}
          </div>

          <div className="form-group" data-easytag="id23-react/src/components/ChangePassword.js">
            <label htmlFor="confirmPassword" data-easytag="id24-react/src/components/ChangePassword.js">
              Confirm New Password *
            </label>
            <div className="password-input-wrapper" data-easytag="id25-react/src/components/ChangePassword.js">
              <input
                type={showPasswords.confirm ? 'text' : 'password'}
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className={errors.confirmPassword ? 'input-error' : ''}
                disabled={loading}
                data-easytag="id26-react/src/components/ChangePassword.js"
              />
              <button
                type="button"
                className="toggle-password"
                onClick={() => togglePasswordVisibility('confirm')}
                disabled={loading}
                data-easytag="id27-react/src/components/ChangePassword.js"
              >
                {showPasswords.confirm ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
            {errors.confirmPassword && (
              <span className="field-error" data-easytag="id28-react/src/components/ChangePassword.js">
                {errors.confirmPassword}
              </span>
            )}
          </div>

          <div className="form-actions" data-easytag="id29-react/src/components/ChangePassword.js">
            <button
              type="button"
              onClick={handleCancel}
              className="btn-cancel"
              disabled={loading}
              data-easytag="id30-react/src/components/ChangePassword.js"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn-submit"
              disabled={loading}
              data-easytag="id31-react/src/components/ChangePassword.js"
            >
              {loading ? 'Changing...' : 'Change Password'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ChangePassword;