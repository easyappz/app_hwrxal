import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './AuthForm.css';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);
    const result = await register(email, password, firstName, lastName, confirmPassword);
    
    if (result.success) {
      navigate('/profile');
    } else {
      if (typeof result.error === 'object') {
        const errorMessages = Object.entries(result.error)
          .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
          .join('; ');
        setError(errorMessages);
      } else {
        setError(result.error);
      }
    }
    
    setLoading(false);
  };

  return (
    <div className="auth-page" data-easytag="id35-react/src/components/Register.js">
      <div className="auth-container" data-easytag="id36-react/src/components/Register.js">
        <h2 data-easytag="id37-react/src/components/Register.js">Register</h2>
        <form onSubmit={handleSubmit} className="auth-form" data-easytag="id38-react/src/components/Register.js">
          {error && (
            <div className="error-message" data-easytag="id39-react/src/components/Register.js">
              {error}
            </div>
          )}
          <div className="form-group" data-easytag="id40-react/src/components/Register.js">
            <label htmlFor="firstName" data-easytag="id41-react/src/components/Register.js">First Name</label>
            <input
              type="text"
              id="firstName"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
              disabled={loading}
              data-easytag="id42-react/src/components/Register.js"
            />
          </div>
          <div className="form-group" data-easytag="id43-react/src/components/Register.js">
            <label htmlFor="lastName" data-easytag="id44-react/src/components/Register.js">Last Name</label>
            <input
              type="text"
              id="lastName"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              required
              disabled={loading}
              data-easytag="id45-react/src/components/Register.js"
            />
          </div>
          <div className="form-group" data-easytag="id46-react/src/components/Register.js">
            <label htmlFor="email" data-easytag="id47-react/src/components/Register.js">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={loading}
              data-easytag="id48-react/src/components/Register.js"
            />
          </div>
          <div className="form-group" data-easytag="id49-react/src/components/Register.js">
            <label htmlFor="password" data-easytag="id50-react/src/components/Register.js">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={loading}
              data-easytag="id51-react/src/components/Register.js"
            />
          </div>
          <div className="form-group" data-easytag="id52-react/src/components/Register.js">
            <label htmlFor="confirmPassword" data-easytag="id53-react/src/components/Register.js">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              disabled={loading}
              data-easytag="id54-react/src/components/Register.js"
            />
          </div>
          <button 
            type="submit" 
            className="submit-button" 
            disabled={loading}
            data-easytag="id55-react/src/components/Register.js"
          >
            {loading ? 'Loading...' : 'Register'}
          </button>
          <div className="auth-links" data-easytag="id56-react/src/components/Register.js">
            <Link to="/login" data-easytag="id57-react/src/components/Register.js">Already have an account? Login</Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;