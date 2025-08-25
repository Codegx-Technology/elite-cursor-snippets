'use client';
import React, { useState, useEffect } from 'react';
import { FaTimesCircle } from 'react-icons/fa6';
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
      <FaTimesCircle className="text-xl" />
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
