import React from 'react';
import { useAuth } from '../context/AuthContext';
import './Home.css';

const Home = () => {
  const { isAuthenticated, user } = useAuth();

  return (
    <div className="home" data-easytag="id12-react/src/components/Home.js">
      <div className="home-container" data-easytag="id13-react/src/components/Home.js">
        <h1 data-easytag="id14-react/src/components/Home.js">Welcome to My App</h1>
        {isAuthenticated ? (
          <div className="welcome-message" data-easytag="id15-react/src/components/Home.js">
            <p data-easytag="id16-react/src/components/Home.js">
              Hello, {user?.first_name} {user?.last_name}!
            </p>
            <p data-easytag="id17-react/src/components/Home.js">
              You are successfully logged in.
            </p>
          </div>
        ) : (
          <div className="welcome-message" data-easytag="id18-react/src/components/Home.js">
            <p data-easytag="id19-react/src/components/Home.js">
              Please login or register to continue.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;