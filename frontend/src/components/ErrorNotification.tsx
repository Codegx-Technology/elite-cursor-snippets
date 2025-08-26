'use client';
import React, { useState, useEffect } from 'react';
import { useError } from '@/context/ErrorContext';

const ErrorNotification: React.FC = () => {
  const { globalError, clearError } = useError();
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (globalError) {
      setIsVisible(true);
      const timer = setTimeout(() => {
        setIsVisible(false);
        clearError();
      }, 5000); // Auto-dismiss after 5 seconds
      return () => clearTimeout(timer);
    } else {
      setIsVisible(false);
    }
  }, [globalError, clearError]);

  if (!isVisible || !globalError) return null;

  return (
    <div className="fixed bottom-4 right-4 bg-red-600 text-white p-4 rounded-lg shadow-lg flex items-center space-x-3 z-50 animate-slideInUp">
      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
      </svg>
      <p className="font-medium">Error: {globalError}</p>
      <button onClick={() => {
        setIsVisible(false);
        clearError();
      }} className="ml-auto text-white hover:text-red-200">
        &times;
      </button>
    </div>
  );
};

export default ErrorNotification;
