"use client";
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { fetchPlanStatus } from '@/widgets/PlanGuardWidget/planService';
import type { PlanStatus } from '@/widgets/PlanGuardWidget/types';
import { useAuth } from '@/context/AuthContext';

interface PlanGuardContextType {
  planStatus: PlanStatus | null;
  loading: boolean;
  error: string | null;
  refreshPlanStatus: () => void;
}

const PlanGuardContext = createContext<PlanGuardContextType | undefined>(undefined);

export const PlanGuardProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [planStatus, setPlanStatus] = useState<PlanStatus | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const { token, isAuthenticated } = useAuth();

  const getPlanStatus = async () => {
    setLoading(true);
    setError(null);
    try {
      const status = await fetchPlanStatus();
      setPlanStatus(status);
    } catch (err) {
      console.error("Failed to fetch plan status:", err);
      const msg = err instanceof Error ? err.message : "Failed to load plan status. Please try again.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Only fetch when authenticated and token is available
    if (isAuthenticated && token) {
      getPlanStatus();
    } else {
      // Not authenticated yet; don't call the API to avoid 401
      setLoading(false);
      setPlanStatus(null);
      setError(null);
    }
  }, [isAuthenticated, token]);

  const refreshPlanStatus = () => {
    getPlanStatus();
  };

  return (
    <PlanGuardContext.Provider value={{ planStatus, loading, error, refreshPlanStatus }}>
      {children}
    </PlanGuardContext.Provider>
  );
};

export const usePlanGuard = () => {
  const context = useContext(PlanGuardContext);
  if (context === undefined) {
    throw new Error('usePlanGuard must be used within a PlanGuardProvider');
  }
  return context;
};
