import { instance } from './axios';

export const login = (email, password) => {
  return instance.post('/api/auth/login/', { email, password });
};

export const register = (email, password, firstName, lastName, passwordConfirm) => {
  return instance.post('/api/auth/register/', {
    email,
    password,
    password_confirm: passwordConfirm,
    first_name: firstName,
    last_name: lastName
  });
};

export const logout = (refreshToken) => {
  return instance.post('/api/auth/logout/', { refresh: refreshToken });
};

export const refreshToken = (refresh) => {
  return instance.post('/api/auth/token/refresh/', { refresh });
};

export const requestPasswordReset = (email) => {
  return instance.post('/api/auth/password/reset/', { email });
};

export const confirmPasswordReset = (token, newPassword) => {
  return instance.post('/api/auth/password/reset/confirm/', {
    token,
    new_password: newPassword
  });
};

export const changePassword = (oldPassword, newPassword) => {
  return instance.post('/api/auth/password/change/', {
    old_password: oldPassword,
    new_password: newPassword
  });
};