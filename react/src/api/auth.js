import instance from './axios';

export const loginUser = async (email, password) => {
  const response = await instance.post('/api/auth/login/', {
    email,
    password
  });
  return response.data;
};

export const registerUser = async (email, password, firstName, lastName) => {
  const response = await instance.post('/api/auth/register/', {
    email,
    password,
    first_name: firstName,
    last_name: lastName
  });
  return response.data;
};

export const getUserProfile = async () => {
  const response = await instance.get('/api/auth/profile/');
  return response.data;
};

export const updateUserProfile = async (data) => {
  const response = await instance.put('/api/auth/profile/', data);
  return response.data;
};

export const requestPasswordReset = async (email) => {
  const response = await instance.post('/api/auth/password-reset/', {
    email
  });
  return response.data;
};

export const confirmPasswordReset = async (token, newPassword) => {
  const response = await instance.post('/api/auth/password-reset/confirm/', {
    token,
    new_password: newPassword
  });
  return response.data;
};

export const refreshToken = async (refreshToken) => {
  const response = await instance.post('/api/auth/token/refresh/', {
    refresh: refreshToken
  });
  return response.data;
};