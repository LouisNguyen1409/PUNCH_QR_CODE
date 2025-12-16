import axios from 'axios';

export interface ScanData {
  qr1: string;
  qr2: string;
  status: 'OK' | 'SAI';
  timestamp: string;
}

const api = axios.create({
  baseURL: '/api', // Vite proxy will handle this
});

export const saveScan = async (data: ScanData) => {
  try {
    const response = await api.post('/scan', data);
    return response.data;
  } catch (error) {
    console.error("Error saving scan:", error);
    throw error;
  }
};

export const getHistory = async () => {
  try {
    const response = await api.get('/history');
    return response.data; // Expecting { history: ScanData[] } or similar
  } catch (error) {
    console.error("Error fetching history:", error);
    return [];
  }
};
