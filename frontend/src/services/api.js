import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || '';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
});

export async function geocodeAddress(address) {
  const { data } = await api.get('/api/geocode', { params: { address } });
  return data;
}

export async function getRiskProfile(lat, lng) {
  const { data } = await api.get('/api/risk-profile', { params: { lat, lng } });
  return data;
}

export async function getShelters(lat, lng) {
  const { data } = await api.get('/api/shelters', { params: { lat, lng } });
  return data;
}

export async function getAIReport(riskData) {
  const { data } = await api.post('/api/ai-report', riskData);
  return data;
}

export async function getEmergencyContacts(state) {
  const { data } = await api.get('/api/emergency-contacts', { params: { state } });
  return data;
}

export async function createCheckoutSession(amount) {
  const { data } = await api.post('/api/create-checkout-session', {
    amount: amount * 100,
    success_url: `${window.location.origin}/donation-success`,
    cancel_url: `${window.location.origin}/dashboard`,
  });
  return data;
}

export async function exportPDF(reportData) {
  const response = await api.post('/api/export-pdf', reportData, {
    responseType: 'blob',
  });
  return response.data;
}

export async function getNOAAAlerts(lat, lng) {
  const { data } = await api.get('/api/noaa-alerts', { params: { lat, lng } });
  return data;
}

export async function getHistoricalDisasters(state) {
  const { data } = await api.get('/api/historical-disasters', { params: { state } });
  return data;
}

export default api;
