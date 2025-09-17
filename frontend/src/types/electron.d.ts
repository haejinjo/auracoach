declare global {
  interface Window {
    electronAPI?: {
      onAuthCallback: (callback: (url: string) => void) => void;
      removeAuthCallback: () => void;
      isElectron: boolean;
    };
  }
}

export {};