import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electronAPI', {
  onAuthCallback: (callback: (url: string) => void) => {
    ipcRenderer.on('auth-callback', (_, url) => callback(url));
  },
  removeAuthCallback: () => {
    ipcRenderer.removeAllListeners('auth-callback');
  },
  isElectron: true
});