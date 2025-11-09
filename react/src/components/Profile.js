import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Profile.css';

const Profile = () => {
  const { user, logout, updateProfile, checkAuth } = useAuth();
  const navigate = useNavigate();
  
  const [isEditMode, setIsEditMode] = useState(false);
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadUserData();
  }, [user]);

  const loadUserData = async () => {
    if (user) {
      setFirstName(user.first_name || '');
      setLastName(user.last_name || '');
      setIsLoading(false);
    } else {
      await checkAuth();
      setIsLoading(false);
    }
  };

  const handleEdit = () => {
    setIsEditMode(true);
    setSuccessMessage('');
    setErrorMessage('');
  };

  const handleCancel = () => {
    setIsEditMode(false);
    setFirstName(user.first_name || '');
    setLastName(user.last_name || '');
    setErrorMessage('');
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSuccessMessage('');
    setErrorMessage('');
    setIsSubmitting(true);

    try {
      const result = await updateProfile({
        first_name: firstName,
        last_name: lastName
      });

      if (result.success) {
        setSuccessMessage('Profile updated successfully!');
        setIsEditMode(false);
        await checkAuth();
        setTimeout(() => setSuccessMessage(''), 3000);
      } else {
        setErrorMessage(typeof result.error === 'string' ? result.error : 'Failed to update profile.');
      }
    } catch (error) {
      setErrorMessage('An unexpected error occurred. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (isLoading) {
    return (
      <div className="profile-loading" data-easytag="id1-react/src/components/Profile.js">
        <div className="loading-spinner" data-easytag="id2-react/src/components/Profile.js">Loading...</div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="profile-container" data-easytag="id3-react/src/components/Profile.js">
      <div className="profile-card" data-easytag="id4-react/src/components/Profile.js">
        <div className="profile-header" data-easytag="id5-react/src/components/Profile.js">
          <h1 data-easytag="id6-react/src/components/Profile.js">User Profile</h1>
          <button
            onClick={handleLogout}
            className="logout-button"
            data-easytag="id7-react/src/components/Profile.js"
          >
            Logout
          </button>
        </div>

        {successMessage && (
          <div className="success-message" data-easytag="id8-react/src/components/Profile.js">
            {successMessage}
          </div>
        )}

        {errorMessage && (
          <div className="error-message" data-easytag="id9-react/src/components/Profile.js">
            {errorMessage}
          </div>
        )}

        <div className="profile-content" data-easytag="id10-react/src/components/Profile.js">
          {!isEditMode ? (
            <div className="profile-view-mode" data-easytag="id11-react/src/components/Profile.js">
              <div className="profile-field" data-easytag="id12-react/src/components/Profile.js">
                <label data-easytag="id13-react/src/components/Profile.js">Email</label>
                <div className="profile-value" data-easytag="id14-react/src/components/Profile.js">
                  {user.email}
                </div>
              </div>

              <div className="profile-field" data-easytag="id15-react/src/components/Profile.js">
                <label data-easytag="id16-react/src/components/Profile.js">First Name</label>
                <div className="profile-value" data-easytag="id17-react/src/components/Profile.js">
                  {user.first_name || 'Not set'}
                </div>
              </div>

              <div className="profile-field" data-easytag="id18-react/src/components/Profile.js">
                <label data-easytag="id19-react/src/components/Profile.js">Last Name</label>
                <div className="profile-value" data-easytag="id20-react/src/components/Profile.js">
                  {user.last_name || 'Not set'}
                </div>
              </div>

              <div className="profile-field" data-easytag="id21-react/src/components/Profile.js">
                <label data-easytag="id22-react/src/components/Profile.js">Roles</label>
                <div className="profile-roles" data-easytag="id23-react/src/components/Profile.js">
                  {user.roles && user.roles.length > 0 ? (
                    user.roles.map((role, index) => (
                      <span key={index} className="role-badge" data-easytag="id24-react/src/components/Profile.js">
                        {role.name}
                      </span>
                    ))
                  ) : (
                    <span className="no-roles" data-easytag="id25-react/src/components/Profile.js">No roles assigned</span>
                  )}
                </div>
              </div>

              <div className="profile-field" data-easytag="id26-react/src/components/Profile.js">
                <label data-easytag="id27-react/src/components/Profile.js">Date Joined</label>
                <div className="profile-value" data-easytag="id28-react/src/components/Profile.js">
                  {formatDate(user.date_joined)}
                </div>
              </div>

              <div className="profile-actions" data-easytag="id29-react/src/components/Profile.js">
                <button
                  onClick={handleEdit}
                  className="edit-button"
                  data-easytag="id30-react/src/components/Profile.js"
                >
                  Edit Profile
                </button>
                <Link
                  to="/password-reset"
                  className="change-password-link"
                  data-easytag="id31-react/src/components/Profile.js"
                >
                  Change Password
                </Link>
              </div>
            </div>
          ) : (
            <form onSubmit={handleSave} className="profile-edit-mode" data-easytag="id32-react/src/components/Profile.js">
              <div className="profile-field" data-easytag="id33-react/src/components/Profile.js">
                <label data-easytag="id34-react/src/components/Profile.js">Email</label>
                <div className="profile-value readonly" data-easytag="id35-react/src/components/Profile.js">
                  {user.email}
                </div>
                <small className="field-hint" data-easytag="id36-react/src/components/Profile.js">Email cannot be changed</small>
              </div>

              <div className="form-group" data-easytag="id37-react/src/components/Profile.js">
                <label htmlFor="firstName" data-easytag="id38-react/src/components/Profile.js">First Name</label>
                <input
                  type="text"
                  id="firstName"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  placeholder="Enter your first name"
                  disabled={isSubmitting}
                  data-easytag="id39-react/src/components/Profile.js"
                />
              </div>

              <div className="form-group" data-easytag="id40-react/src/components/Profile.js">
                <label htmlFor="lastName" data-easytag="id41-react/src/components/Profile.js">Last Name</label>
                <input
                  type="text"
                  id="lastName"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                  placeholder="Enter your last name"
                  disabled={isSubmitting}
                  data-easytag="id42-react/src/components/Profile.js"
                />
              </div>

              <div className="profile-field" data-easytag="id43-react/src/components/Profile.js">
                <label data-easytag="id44-react/src/components/Profile.js">Roles</label>
                <div className="profile-roles" data-easytag="id45-react/src/components/Profile.js">
                  {user.roles && user.roles.length > 0 ? (
                    user.roles.map((role, index) => (
                      <span key={index} className="role-badge" data-easytag="id46-react/src/components/Profile.js">
                        {role.name}
                      </span>
                    ))
                  ) : (
                    <span className="no-roles" data-easytag="id47-react/src/components/Profile.js">No roles assigned</span>
                  )}
                </div>
                <small className="field-hint" data-easytag="id48-react/src/components/Profile.js">Roles are managed by administrators</small>
              </div>

              <div className="form-actions" data-easytag="id49-react/src/components/Profile.js">
                <button
                  type="submit"
                  className="save-button"
                  disabled={isSubmitting}
                  data-easytag="id50-react/src/components/Profile.js"
                >
                  {isSubmitting ? 'Saving...' : 'Save Changes'}
                </button>
                <button
                  type="button"
                  onClick={handleCancel}
                  className="cancel-button"
                  disabled={isSubmitting}
                  data-easytag="id51-react/src/components/Profile.js"
                >
                  Cancel
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default Profile;