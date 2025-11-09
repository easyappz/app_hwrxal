import React, { useState } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Login.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [apiError, setApiError] = useState('');

  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const from = location.state?.from?.pathname || '/profile';

  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  };

  const validateForm = () => {
    const newErrors = {};

    if (!email) {
      newErrors.email = 'Email is required';
    } else if (!validateEmail(email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (!password) {
      newErrors.password = 'Password is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setApiError('');

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      const result = await login(email, password);
      if (result.success) {
        navigate(from, { replace: true });
      } else {
        setApiError(result.error);
      }
    } catch (error) {
      setApiError('An unexpected error occurred. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
    if (errors.email) {
      setErrors({ ...errors, email: '' });
    }
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
    if (errors.password) {
      setErrors({ ...errors, password: '' });
    }
  };

  return (
    <div className="login-container" data-easytag="id1-react/src/components/Login.js">
      <div className="login-card" data-easytag="id2-react/src/components/Login.js">
        <h1 className="login-title" data-easytag="id3-react/src/components/Login.js">Login</h1>
        <p className="login-subtitle" data-easytag="id4-react/src/components/Login.js">
          Welcome back! Please login to your account.
        </p>

        {apiError && (
          <div className="error-message" data-easytag="id5-react/src/components/Login.js">
            {apiError}
          </div>
        )}

        <form onSubmit={handleSubmit} className="login-form" data-easytag="id6-react/src/components/Login.js">
          <div className="form-group" data-easytag="id7-react/src/components/Login.js">
            <label htmlFor="email" data-easytag="id8-react/src/components/Login.js">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={handleEmailChange}
              className={errors.email ? 'error' : ''}
              placeholder="Enter your email"
              disabled={isSubmitting}
              data-easytag="id9-react/src/components/Login.js"
            />
            {errors.email && (
              <span className="field-error" data-easytag="id10-react/src/components/Login.js">
                {errors.email}
              </span>
            )}
          </div>

          <div className="form-group" data-easytag="id11-react/src/components/Login.js">
            <label htmlFor="password" data-easytag="id12-react/src/components/Login.js">Password</label>
            <div className="password-input-wrapper" data-easytag="id13-react/src/components/Login.js">
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                value={password}
                onChange={handlePasswordChange}
                className={errors.password ? 'error' : ''}
                placeholder="Enter your password"
                disabled={isSubmitting}
                data-easytag="id14-react/src/components/Login.js"
              />
              <button
                type="button"
                className="toggle-password"
                onClick={() => setShowPassword(!showPassword)}
                disabled={isSubmitting}
                data-easytag="id15-react/src/components/Login.js"
              >
                {showPassword ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
            {errors.password && (
              <span className="field-error" data-easytag="id16-react/src/components/Login.js">
                {errors.password}
              </span>
            )}
          </div>

          <div className="forgot-password-link" data-easytag="id17-react/src/components/Login.js">
            <Link to="/password-reset" data-easytag="id18-react/src/components/Login.js">
              Forgot password?
            </Link>
          </div>

          <button
            type="submit"
            className="submit-button"
            disabled={isSubmitting}
            data-easytag="id19-react/src/components/Login.js"
          >
            {isSubmitting ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="register-link" data-easytag="id20-react/src/components/Login.js">
          <p data-easytag="id21-react/src/components/Login.js">
            Don't have an account?{' '}
            <Link to="/register" data-easytag="id22-react/src/components/Login.js">
              Register here
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;