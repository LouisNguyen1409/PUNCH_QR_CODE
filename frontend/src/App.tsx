import { useState, useEffect } from 'react';
import { 
  Container, 
  Typography, 
  Button, 
  Box, 
  Paper, 
  List, 
  ListItem, 
  ListItemText, 
  Chip, 
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  Divider
} from '@mui/material';
import { CheckCircle, Cancel, History as HistoryIcon, QrCodeScanner } from '@mui/icons-material';
import { QRScanner } from './components/QRScanner';
import { saveScan, getHistory, ScanData } from './api';
import './App.css';

// Glassmorphism Card Style
const glassStyle = {
  background: 'rgba(255, 255, 255, 0.25)',
  boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
  backdropFilter: 'blur(4px)',
  WebkitBackdropFilter: 'blur(4px)',
  borderRadius: '16px',
  border: '1px solid rgba(255, 255, 255, 0.18)',
  padding: '1.5rem',
  textAlign: 'center' as const,
  marginTop: '1rem',
};

function App() {
  const [step, setStep] = useState<number>(0);
  const [qr1, setQr1] = useState<string>('');
  const [qr2, setQr2] = useState<string>('');
  const [history, setHistory] = useState<ScanData[]>([]);
  const [showHistory, setShowHistory] = useState(false);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    const data = await getHistory();
    if (Array.isArray(data)) {
      setHistory(data);
    }
  };

  const playSound = (type: 'OK' | 'SAI') => {
    const audio = new Audio(type === 'OK' ? '/ok.mp3' : '/sai.mp3');
    audio.load(); // Ensure it's loaded
    audio.play().catch(e => console.error("Error playing sound:", e));
  };

  const handleStart = () => {
    // Unlock audio context if needed by playing a short silence or just state change
    setStep(1);
  };

  const handleScan1 = (code: string) => {
    setQr1(code);
    setStep(2);
  };

  const handleScan2 = (code: string) => {
    setQr2(code);
    finishScan(qr1, code);
  };

  const finishScan = async (code1: string, code2: string) => {
    const isMatch = code1 === code2;
    const status = isMatch ? 'OK' : 'SAI';
    
    // Play Sound
    playSound(status);

    // Save Data
    const newData: ScanData = {
      qr1: code1,
      qr2: code2,
      status: status,
      timestamp: new Date().toISOString()
    };
    
    try {
      await saveScan(newData);
      loadHistory(); // Refresh history
    } catch (e) {
      console.error("Failed to save scan", e);
    }

    setStep(3);
  };

  const handleReset = () => {
    setQr1('');
    setQr2('');
    setStep(1);
  };

  return (
    <Container maxWidth="sm" sx={{ pb: 2, pt: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h5" sx={{ fontWeight: 'bold', color: '#333' }}>
           PUNCH QR CODE SCANNER 🔍
        </Typography>
        <IconButton onClick={() => setShowHistory(true)} sx={{ color: '#333' }}>
          <HistoryIcon />
        </IconButton>
      </Box>

      {step === 0 && (
        <Paper sx={glassStyle}>
          <QrCodeScanner sx={{ fontSize: 80, color: '#333', mb: 2 }} />
          <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold' }}>
            Ready to Scan?
          </Typography>
          <Button 
            variant="contained" 
            size="large" 
            onClick={handleStart}
            sx={{ 
              borderRadius: 20, 
              background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
              boxShadow: '0 3px 5px 2px rgba(33, 203, 243, .3)'
            }}
          >
            Start Scanning
          </Button>
        </Paper>
      )}

      {step === 1 && (
        <Box sx={{ mt: 4 }}>
          <QRScanner onScan={handleScan1} title="Step 1: Scan SHEET QR" />
          <Button onClick={() => setStep(0)} sx={{ mt: 2 }}>Cancel</Button>
        </Box>
      )}

      {step === 2 && (
        <Box sx={{ mt: 4 }}>
          <Typography variant="body2" sx={{ mb: 2, textAlign: 'center', background: '#fff', p: 1, borderRadius: 1 }}>
            Match against: <strong>{qr1}</strong>
          </Typography>
          <QRScanner onScan={handleScan2} title="Step 2: Scan TOOL BOX QR" />
          <Button onClick={() => setStep(0)} sx={{ mt: 2 }}>Cancel</Button>
        </Box>
      )}

      {step === 3 && (
        <Paper sx={glassStyle}>
          {qr1 === qr2 ? (
            <CheckCircle sx={{ fontSize: 100, color: 'green', mb: 2 }} />
          ) : (
            <Cancel sx={{ fontSize: 100, color: 'red', mb: 2 }} />
          )}
          
          <Typography variant="h3" sx={{ 
            fontWeight: 'bold', 
            color: qr1 === qr2 ? 'green' : 'red',
            mb: 2 
          }}>
            {qr1 === qr2 ? 'OK' : 'SAI'}
          </Typography>

          <Box sx={{ textAlign: 'left', mb: 3, background: 'rgba(255,255,255,0.5)', p: 2, borderRadius: 2 }}>
            <Typography><strong>Sheet:</strong> {qr1}</Typography>
            <Typography><strong>Tool:</strong> {qr2}</Typography>
          </Box>

          <Button 
            variant="contained" 
            size="large" 
            onClick={handleReset}
            fullWidth
            sx={{ mb: 2 }}
          >
            Scan Next Pair
          </Button>
        </Paper>
      )}

      {/* History Dialog */}
      <Dialog 
        open={showHistory} 
        onClose={() => setShowHistory(false)}
        PaperProps={{
          sx: { ...glassStyle, margin: 2, maxHeight: '80vh', overflowY: 'auto', p: 0 }
        }}
      >
        <DialogTitle sx={{ background: 'rgba(255,255,255,0.1)' }}>Scan History</DialogTitle>
        <DialogContent>
          <List>
            {history.map((item, index) => (
              <Box key={index}>
                <ListItem>
                  <ListItemText 
                    primary={
                      <Box display="flex" justifyContent="space-between">
                        <Typography variant="body2">{new Date(item.timestamp).toLocaleString()}</Typography>
                        <Chip 
                          label={item.status} 
                          color={item.status === 'OK' ? 'success' : 'error'} 
                          size="small" 
                        />
                      </Box>
                    }
                    secondary={
                      <>
                        <Typography variant="caption" display="block">S: {item.qr1}</Typography>
                        <Typography variant="caption" display="block">T: {item.qr2}</Typography>
                      </>
                    }
                  />
                </ListItem>
                <Divider />
              </Box>
            ))}
            {history.length === 0 && <Typography sx={{ p: 2 }}>No history yet.</Typography>}
          </List>
        </DialogContent>
      </Dialog>
    </Container>
  );
}

export default App;
