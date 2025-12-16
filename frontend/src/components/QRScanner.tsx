import { useEffect } from 'react';
import { Html5QrcodeScanner, Html5QrcodeScanType } from 'html5-qrcode';
import { Typography, Paper } from '@mui/material';

interface QRScannerProps {
  onScan: (decodedText: string) => void;
  title: string;
}

export const QRScanner = ({ onScan, title }: QRScannerProps) => {
  useEffect(() => {
    const isMobile = window.innerWidth < 600;
    const boxSize = isMobile ? 200 : 250;

    const scanner = new Html5QrcodeScanner(
      "reader",
      { 
        fps: 10, 
        qrbox: { width: boxSize, height: boxSize },
        aspectRatio: 1.0,
        supportedScanTypes: [Html5QrcodeScanType.SCAN_TYPE_CAMERA],
        videoConstraints: {
            facingMode: { exact: "environment" }
        }
      },
      false
    );

    scanner.render(
      (decodedText) => {
        scanner.clear();
        onScan(decodedText);
      },
      (_) => {
        // Handle scan errors or ignore them for continuous scanning
      }
    );

    return () => {
        try {
            scanner.clear();
        } catch (e) {
            console.error("Error clearing scanner", e);
        }
    };
  }, [onScan]);

  return (
    <Paper 
      elevation={3} 
      sx={{ 
        p: 1, 
        background: 'rgba(255, 255, 255, 0.1)', 
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(255, 255, 255, 0.2)',
        borderRadius: '16px',
        maxWidth: '500px',
        width: '100%',
        margin: '0 auto',
        overflow: 'hidden'
      }}
    >
        <Typography variant="h6" align="center" sx={{ mb: 1, color: '#333' }}>
            {title}
        </Typography>
        <div id="reader"></div>
    </Paper>
  );
};
