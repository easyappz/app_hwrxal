import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './AuthForm.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(email, password);
    
    if (result.success) {
      navigate('/profile');
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  return (
    <div className="auth-page" data-easytag="id20-react/src/components/Login.js">
      <div className="auth-container" data-easytag="id21-react/src/components/Login.js">
        <h2 data-easytag="id22-react/src/components/Login.js">Login</h2>
        <form onSubmit={handleSubmit} className="auth-form" data-easytag="id23-react/src/components/Login.js">
          {error && (
            <div className="error-message" data-easytag="id24-react/src/components/Login.js">
              {error}
            </div>
          )}
          <div className="form-group" data-easytag="id25-react/src/components/Login.js">
            <label htmlFor="email" data-easytag="id26-react/src/components/Login.js">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={loading}
              data-easytag="id27-react/src/components/Login.js"
            />
          </div>
          <div className="form-group" data-easytag="id28-react/src/components/Login.js">
            <label htmlFor="password" data-easytag="id29-react/src/components/Login.js">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={loading}
              data-easytag="id30-react/src/components/Login.js"
            />
          </div>
          <button 
            type="submit" 
            className="submit-button" 
            disabled={loading}
            data-easytag="id31-react/src/components/Login.js"
          >
            {loading ? 'Loading...' : 'Login'}
          </button>
          <div className="auth-links" data-easytag="id32-react/src/components/Login.js">
            <Link to="/register" data-easytag="id33-react/src/components/Login.js">Don't have an account? Register</Link>
            <Link to="/password-reset" data-easytag="id34-react/src/components/Login.js">Forgot password?</Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;