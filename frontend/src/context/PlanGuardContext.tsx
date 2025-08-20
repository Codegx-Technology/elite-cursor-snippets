"use client";
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { fetchPlanStatus } from '@/widgets/PlanGuardWidget/planService';
import type { PlanStatus } from '@/widgets/PlanGuardWidget/types';

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

  const getPlanStatus = async () => {
    setLoading(true);
    setError(null);
    try {
      const status = await fetchPlanStatus();
      setPlanStatus(status);
    } catch (err) {
      console.error("Failed to fetch plan status:", err);
      setError("Failed to load plan status. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getPlanStatus();
  }, []);

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