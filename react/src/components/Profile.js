import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { updateUserProfile } from '../api/auth';
import './Profile.css';

const Profile = () => {
  const { user, logout, checkAuth } = useAuth();
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: ''
  });
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [apiError, setApiError] = useState('');

  useEffect(() => {
    if (user) {
      setFormData({
        firstName: user.first_name || '',
        lastName: user.last_name || '',
        email: user.email || ''
      });
    }
  }, [user]);

  const validateForm = () => {
    const newErrors = {};

    if (!formData.firstName) {
      newErrors.firstName = 'First name is required';
    }

    if (!formData.lastName) {
      newErrors.lastName = 'Last name is required';
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
      await updateUserProfile({
        first_name: formData.firstName,
        last_name: formData.lastName
      });
      setSuccessMessage('Profile updated successfully!');
      setIsEditing(false);
      await checkAuth();
    } catch (error) {
      console.error('Profile update failed:', error);
      setApiError(error.response?.data?.detail || 'Failed to update profile. Please try again.');
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

  const handleCancel = () => {
    setIsEditing(false);
    setFormData({
      firstName: user.first_name || '',
      lastName: user.last_name || '',
      email: user.email || ''
    });
    setErrors({});
    setApiError('');
    setSuccessMessage('');
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!user) {
    return (
      <div className="profile-container" data-easytag="id1-react/src/components/Profile.js">
        <div className="profile-card" data-easytag="id2-react/src/components/Profile.js">
          <p data-easytag="id3-react/src/components/Profile.js">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-container" data-easytag="id4-react/src/components/Profile.js">
      <div className="profile-card" data-easytag="id5-react/src/components/Profile.js">
        <div className="profile-header" data-easytag="id6-react/src/components/Profile.js">
          <h1 className="profile-title" data-easytag="id7-react/src/components/Profile.js">My Profile</h1>
          <button
            className="logout-button"
            onClick={handleLogout}
            data-easytag="id8-react/src/components/Profile.js"
          >
            Logout
          </button>
        </div>

        {successMessage && (
          <div className="success-message" data-easytag="id9-react/src/components/Profile.js">
            {successMessage}
          </div>
        )}

        {apiError && (
          <div className="error-message" data-easytag="id10-react/src/components/Profile.js">
            {apiError}
          </div>
        )}

        <div className="profile-info" data-easytag="id11-react/src/components/Profile.js">
          <div className="user-avatar" data-easytag="id12-react/src/components/Profile.js">
            <div className="avatar-circle" data-easytag="id13-react/src/components/Profile.js">
              {formData.firstName.charAt(0)}{formData.lastName.charAt(0)}
            </div>
          </div>

          <form onSubmit={handleSubmit} className="profile-form" data-easytag="id14-react/src/components/Profile.js">
            <div className="form-row" data-easytag="id15-react/src/components/Profile.js">
              <div className="form-group" data-easytag="id16-react/src/components/Profile.js">
                <label htmlFor="firstName" data-easytag="id17-react/src/components/Profile.js">First Name</label>
                <input
                  type="text"
                  id="firstName"
                  value={formData.firstName}
                  onChange={handleChange('firstName')}
                  className={errors.firstName ? 'error' : ''}
                  disabled={!isEditing || isSubmitting}
                  data-easytag="id18-react/src/components/Profile.js"
                />
                {errors.firstName && (
                  <span className="field-error" data-easytag="id19-react/src/components/Profile.js">
                    {errors.firstName}
                  </span>
                )}
              </div>

              <div className="form-group" data-easytag="id20-react/src/components/Profile.js">
                <label htmlFor="lastName" data-easytag="id21-react/src/components/Profile.js">Last Name</label>
                <input
                  type="text"
                  id="lastName"
                  value={formData.lastName}
                  onChange={handleChange('lastName')}
                  className={errors.lastName ? 'error' : ''}
                  disabled={!isEditing || isSubmitting}
                  data-easytag="id22-react/src/components/Profile.js"
                />
                {errors.lastName && (
                  <span className="field-error" data-easytag="id23-react/src/components/Profile.js">
                    {errors.lastName}
                  </span>
                )}
              </div>
            </div>

            <div className="form-group" data-easytag="id24-react/src/components/Profile.js">
              <label htmlFor="email" data-easytag="id25-react/src/components/Profile.js">Email</label>
              <input
                type="email"
                id="email"
                value={formData.email}
                disabled
                className="disabled-field"
                data-easytag="id26-react/src/components/Profile.js"
              />
              <small className="field-hint" data-easytag="id27-react/src/components/Profile.js">
                Email cannot be changed
              </small>
            </div>

            <div className="form-group" data-easytag="id28-react/src/components/Profile.js">
              <label data-easytag="id29-react/src/components/Profile.js">Role</label>
              <div className="roles-display" data-easytag="id30-react/src/components/Profile.js">
                {user.roles && user.roles.length > 0 ? (
                  user.roles.map((role, index) => (
                    <span key={index} className="role-badge" data-easytag="id31-react/src/components/Profile.js">
                      {role.name}
                    </span>
                  ))
                ) : (
                  <span className="role-badge" data-easytag="id32-react/src/components/Profile.js">user</span>
                )}
              </div>
            </div>

            {!isEditing ? (
              <button
                type="button"
                className="edit-button"
                onClick={() => setIsEditing(true)}
                data-easytag="id33-react/src/components/Profile.js"
              >
                Edit Profile
              </button>
            ) : (
              <div className="button-group" data-easytag="id34-react/src/components/Profile.js">
                <button
                  type="button"
                  className="cancel-button"
                  onClick={handleCancel}
                  disabled={isSubmitting}
                  data-easytag="id35-react/src/components/Profile.js"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="save-button"
                  disabled={isSubmitting}
                  data-easytag="id36-react/src/components/Profile.js"
                >
                  {isSubmitting ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            )}
          </form>
        </div>
      </div>
    </div>
  );
};

export default Profile;