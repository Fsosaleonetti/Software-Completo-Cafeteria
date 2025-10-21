import axios from 'axios';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api'
});

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export async function login(username: string, password: string) {
  const { data } = await api.post<AuthResponse>('/auth/login', { username, password });
  return data;
}
