import { instance } from './axios';

export const login = (email, password) => {
  return instance.post('/api/login/', { email, password });
};

export const register = (email, password, firstName, lastName) => {
  return instance.post('/api/register/', {
    email,
    password,
    first_name: firstName,
    last_name: lastName
  });
};

export const logout = (refreshToken) => {
  return instance.post('/api/logout/', { refresh: refreshToken });
};

export const refreshToken = (refresh) => {
  return instance.post('/api/token/refresh/', { refresh });
};

export const requestPasswordReset = (email) => {
  return instance.post('/api/password-reset/', { email });
};

export const confirmPasswordReset = (token, newPassword) => {
  return instance.post('/api/password-reset/confirm/', {
    token,
    new_password: newPassword
  });
};

export const changePassword = (oldPassword, newPassword) => {
  return instance.post('/api/change-password/', {
    old_password: oldPassword,
    new_password: newPassword
  });
};