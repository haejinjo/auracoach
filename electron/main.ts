import { app, BrowserWindow } from 'electron';
import * as path from 'path';

const isDev = process.env.NODE_ENV === 'development';
let mainWindow: BrowserWindow | null = null;

// Simple protocol registration
app.setAsDefaultProtocolClient('auracoach');

// Handle protocol URLs
function handleProtocolUrl(url: string): void {
  if (url.startsWith('auracoach://auth/callback') && mainWindow) {
    mainWindow.focus();
    mainWindow.webContents.send('auth-callback', url);
  }
}

// Protocol handlers
app.on('open-url', (event, url) => {
  event.preventDefault();
  handleProtocolUrl(url);
});

app.on('second-instance', (event, commandLine) => {
  if (mainWindow) {
    if (mainWindow.isMinimized()) mainWindow.restore();
    mainWindow.focus();
  }
  const protocolUrl = commandLine.find(arg => arg.startsWith('auracoach://'));
  if (protocolUrl) handleProtocolUrl(protocolUrl);
});

// Prevent multiple instances
const gotTheLock = app.requestSingleInstanceLock();
if (!gotTheLock) {
  app.quit();
} else {
  app.whenReady().then(createWindow);
}

function createWindow(): void {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  if (isDev) {
    mainWindow.loadURL('http://localhost:5173');
  } else {
    mainWindow.loadFile('../frontend/dist/index.html');
  }

  // Handle Windows protocol on startup
  if (process.platform === 'win32' && process.argv.length >= 2) {
    const protocolUrl = process.argv.find(arg => arg.startsWith('auracoach://'));
    if (protocolUrl) {
      setTimeout(() => handleProtocolUrl(protocolUrl), 1000);
    }
  }
}

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});