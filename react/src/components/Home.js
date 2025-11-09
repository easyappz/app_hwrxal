import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Home.css';

const Home = () => {
  const { user } = useAuth();

  return (
    <div className="home-container" data-easytag="id12-react/src/components/Home.js">
      <div className="home-content" data-easytag="id13-react/src/components/Home.js">
        <h1 className="home-title" data-easytag="id14-react/src/components/Home.js">
          Welcome to MyApp
        </h1>
        
        <p className="home-description" data-easytag="id15-react/src/components/Home.js">
          A modern web application with authentication and user management.
        </p>

        {user ? (
          <div className="home-user-section" data-easytag="id16-react/src/components/Home.js">
            <h2 className="home-subtitle" data-easytag="id17-react/src/components/Home.js">
              Hello, {user.first_name || user.email}!
            </h2>
            <p className="home-text" data-easytag="id18-react/src/components/Home.js">
              You are successfully logged in.
            </p>
            <div className="home-actions" data-easytag="id19-react/src/components/Home.js">
              <Link to="/profile" className="home-button home-button-primary" data-easytag="id20-react/src/components/Home.js">
                Go to Profile
              </Link>
              <Link to="/change-password" className="home-button home-button-secondary" data-easytag="id21-react/src/components/Home.js">
                Change Password
              </Link>
            </div>
          </div>
        ) : (
          <div className="home-guest-section" data-easytag="id22-react/src/components/Home.js">
            <h2 className="home-subtitle" data-easytag="id23-react/src/components/Home.js">
              Get Started
            </h2>
            <p className="home-text" data-easytag="id24-react/src/components/Home.js">
              Create an account or sign in to access your profile and manage your data.
            </p>
            <div className="home-actions" data-easytag="id25-react/src/components/Home.js">
              <Link to="/register" className="home-button home-button-primary" data-easytag="id26-react/src/components/Home.js">
                Register
              </Link>
              <Link to="/login" className="home-button home-button-secondary" data-easytag="id27-react/src/components/Home.js">
                Login
              </Link>
            </div>
          </div>
        )}

        <div className="home-features" data-easytag="id28-react/src/components/Home.js">
          <div className="feature-card" data-easytag="id29-react/src/components/Home.js">
            <h3 className="feature-title" data-easytag="id30-react/src/components/Home.js">Secure Authentication</h3>
            <p className="feature-description" data-easytag="id31-react/src/components/Home.js">
              JWT-based authentication with refresh tokens for enhanced security.
            </p>
          </div>
          <div className="feature-card" data-easytag="id32-react/src/components/Home.js">
            <h3 className="feature-title" data-easytag="id33-react/src/components/Home.js">User Roles</h3>
            <p className="feature-description" data-easytag="id34-react/src/components/Home.js">
              Advanced role-based access control system that's easy to extend.
            </p>
          </div>
          <div className="feature-card" data-easytag="id35-react/src/components/Home.js">
            <h3 className="feature-title" data-easytag="id36-react/src/components/Home.js">Profile Management</h3>
            <p className="feature-description" data-easytag="id37-react/src/components/Home.js">
              Manage your personal information and account settings easily.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;