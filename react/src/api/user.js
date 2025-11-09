import { instance } from './axios';

export const getProfile = () => {
  return instance.get('/api/profile/');
};

export const updateProfile = (data) => {
  return instance.put('/api/profile/', data);
};