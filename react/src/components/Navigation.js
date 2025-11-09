import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navigation.css';

const Navigation = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navigation" data-easytag="id2-react/src/components/Navigation.js">
      <div className="nav-container" data-easytag="id3-react/src/components/Navigation.js">
        <Link to="/" className="nav-logo" data-easytag="id4-react/src/components/Navigation.js">
          MyApp
        </Link>
        
        <div className="nav-links" data-easytag="id5-react/src/components/Navigation.js">
          {user ? (
            <>
              <span className="nav-user-email" data-easytag="id6-react/src/components/Navigation.js">
                {user.email}
              </span>
              <Link to="/profile" className="nav-link" data-easytag="id7-react/src/components/Navigation.js">
                Profile
              </Link>
              <Link to="/change-password" className="nav-link" data-easytag="id8-react/src/components/Navigation.js">
                Change Password
              </Link>
              <button onClick={handleLogout} className="nav-button" data-easytag="id9-react/src/components/Navigation.js">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="nav-link" data-easytag="id10-react/src/components/Navigation.js">
                Login
              </Link>
              <Link to="/register" className="nav-link nav-link-primary" data-easytag="id11-react/src/components/Navigation.js">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navigation;