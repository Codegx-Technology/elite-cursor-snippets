'use client';
import React, { createContext, useState, useContext, ReactNode, useCallback } from 'react';

interface ErrorContextType {
  globalError: string | null;
  setGlobalError: (message: string | null) => void;
  clearError: () => void;
}

const ErrorContext = createContext<ErrorContextType | undefined>(undefined);

export const ErrorProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [globalError, setGlobalError] = useState<string | null>(null);

  const memoizedSetGlobalError = useCallback((message: string | null) => {
    setGlobalError(message);
  }, []);

  const clearError = useCallback(() => {
    setGlobalError(null);
  }, []);

  return (
    <ErrorContext.Provider value={{ globalError, setGlobalError: memoizedSetGlobalError, clearError }}>
      {children}
    </ErrorContext.Provider>
  );
};

export const useError = () => {
  const context = useContext(ErrorContext);
  if (context === undefined) {
    throw new Error('useError must be used within an ErrorProvider');
  }
  return context;
};
