import axios from 'axios';

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000' });

export const getStations = async () => (await api.get('/stations')).data;
export const getObs = async (params: any) => (await api.get('/observations', { params })).data;
export const getHourly = async (params: any) => (await api.get('/analytics/hourly', { params })).data;
export const getStatsSummary = async () => (await api.get('/stats/summary')).data;

export default api;
