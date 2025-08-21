// [TASK]: Create a reusable Toast hook and provider.
// [GOAL]: Provide a consistent, enterprise-grade toast notification system.
// [CONSTRAINTS]: Use React Context, support various toast types (success, error, info), and auto-dismissal.
// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + atomicstrategy
// [CONTEXT]: Building core UI components for the Shujaa Studio enterprise frontend.

"use client";

import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { v4 as uuidv4 } from 'uuid'; // Assuming uuid is installed for unique IDs

interface Toast {
  id: string;
  title?: string;
  description?: string;
  type: 'default' | 'success' | 'error' | 'info' | 'warning' | 'destructive';
  duration?: number; // in milliseconds
}

interface ToastContextType {
  addToast: (toast: Omit<Toast, 'id'>) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export const ToastProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = useCallback(({
    title,
    description,
    type = 'default',
    duration = 5000,
  }: Omit<Toast, 'id'>) => {
    const id = uuidv4();
    setToasts((prevToasts) => [...prevToasts, { id, title, description, type, duration }]);

    setTimeout(() => {
      setToasts((prevToasts) => prevToasts.filter((toast) => toast.id !== id));
    }, duration);
  }, []);

  return (
    <ToastContext.Provider value={{ addToast }}>
      {children}
      <div className="fixed bottom-4 right-4 z-[9999] space-y-2">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className={`p-4 rounded-lg shadow-lg text-white flex items-center space-x-3
              ${toast.type === 'success' ? 'bg-green-600' : ''}
              ${toast.type === 'error' || toast.type === 'destructive' ? 'bg-red-600' : ''}
              ${toast.type === 'info' ? 'bg-blue-600' : ''}
              ${toast.type === 'warning' ? 'bg-yellow-600' : ''}
              ${toast.type === 'default' ? 'bg-gray-800' : ''}
            `}
          >
            <div className="flex-1">
              {toast.title && <p className="font-semibold">{toast.title}</p>}
              {toast.description && <p className="text-sm opacity-90">{toast.description}</p>}
            </div>
            <button onClick={() => setToasts((prevToasts) => prevToasts.filter((t) => t.id !== toast.id))} className="ml-auto text-white/80 hover:text-white">
              &times;
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
};

export const useToast = () => {
  const context = useContext(ToastContext);
  if (context === undefined) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};
