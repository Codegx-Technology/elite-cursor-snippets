import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { fetchPlanStatus } from '@/widgets/PlanGuardWidget/planService';
import type { PlanStatus } from '@/widgets/PlanGuardWidget/types';

interface PlanGuardContextType {
  planStatus: PlanStatus | null;
  loading: boolean;
  error: string | null;
}

const PlanGuardContext = createContext<PlanGuardContextType | undefined>(undefined);

interface PlanGuardProviderProps {
  children: ReactNode;
  userId?: string; // Optional userId for multi-tenant scenarios
}

export const PlanGuardProvider: React.FC<PlanGuardProviderProps> = ({ children, userId }) => {
  const [planStatus, setPlanStatus] = useState<PlanStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadPlanStatus() {
      setLoading(true);
      setError(null);
      try {
        const status = await fetchPlanStatus(userId);
        setPlanStatus(status);
      } catch (err: any) {
        console.error("PlanGuardContext: Failed to fetch plan status", err);
        setError(err.message || "Failed to load plan status");
      } finally {
        setLoading(false);
      }
    }

    loadPlanStatus();
  }, [userId]);

  return (
    <PlanGuardContext.Provider value={{ planStatus, loading, error }}>
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
