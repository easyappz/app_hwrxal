import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getProfile, updateProfile } from '../api/user';
import './Profile.css';

const Profile = () => {
  const { user, updateUser } = useAuth();
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const response = await getProfile();
      const profileData = response.data;
      setFirstName(profileData.first_name || '');
      setLastName(profileData.last_name || '');
      setEmail(profileData.email || '');
    } catch (error) {
      console.error('Failed to load profile:', error);
      if (user) {
        setFirstName(user.first_name || '');
        setLastName(user.last_name || '');
        setEmail(user.email || '');
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      const response = await updateProfile({
        first_name: firstName,
        last_name: lastName
      });
      
      updateUser(response.data);
      setSuccess('Profile updated successfully!');
      setIsEditing(false);
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="profile-page" data-easytag="id58-react/src/components/Profile.js">
      <div className="profile-container" data-easytag="id59-react/src/components/Profile.js">
        <h2 data-easytag="id60-react/src/components/Profile.js">Profile</h2>
        
        {error && (
          <div className="error-message" data-easytag="id61-react/src/components/Profile.js">
            {error}
          </div>
        )}
        
        {success && (
          <div className="success-message" data-easytag="id62-react/src/components/Profile.js">
            {success}
          </div>
        )}

        <form onSubmit={handleSubmit} className="profile-form" data-easytag="id63-react/src/components/Profile.js">
          <div className="form-group" data-easytag="id64-react/src/components/Profile.js">
            <label htmlFor="firstName" data-easytag="id65-react/src/components/Profile.js">First Name</label>
            <input
              type="text"
              id="firstName"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              disabled={!isEditing || loading}
              data-easytag="id66-react/src/components/Profile.js"
            />
          </div>
          
          <div className="form-group" data-easytag="id67-react/src/components/Profile.js">
            <label htmlFor="lastName" data-easytag="id68-react/src/components/Profile.js">Last Name</label>
            <input
              type="text"
              id="lastName"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              disabled={!isEditing || loading}
              data-easytag="id69-react/src/components/Profile.js"
            />
          </div>
          
          <div className="form-group" data-easytag="id70-react/src/components/Profile.js">
            <label htmlFor="email" data-easytag="id71-react/src/components/Profile.js">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              disabled
              data-easytag="id72-react/src/components/Profile.js"
            />
          </div>

          <div className="profile-actions" data-easytag="id73-react/src/components/Profile.js">
            {!isEditing ? (
              <button 
                type="button" 
                onClick={() => setIsEditing(true)} 
                className="edit-button"
                data-easytag="id74-react/src/components/Profile.js"
              >
                Edit Profile
              </button>
            ) : (
              <>
                <button 
                  type="submit" 
                  className="save-button" 
                  disabled={loading}
                  data-easytag="id75-react/src/components/Profile.js"
                >
                  {loading ? 'Saving...' : 'Save Changes'}
                </button>
                <button 
                  type="button" 
                  onClick={() => {
                    setIsEditing(false);
                    loadProfile();
                  }} 
                  className="cancel-button"
                  disabled={loading}
                  data-easytag="id76-react/src/components/Profile.js"
                >
                  Cancel
                </button>
              </>
            )}
          </div>
        </form>

        <div className="profile-links" data-easytag="id77-react/src/components/Profile.js">
          <Link to="/change-password" className="link-button" data-easytag="id78-react/src/components/Profile.js">
            Change Password
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Profile;