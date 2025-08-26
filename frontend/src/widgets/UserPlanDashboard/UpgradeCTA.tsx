// frontend/src/widgets/UserPlanDashboard/UpgradeCTA.tsx

import React from 'react';
import { Button } from '@/components/ui/button'; // Assuming you have a Button component
import { PlanMessages } from '@/ui/planMessages';

import { PlanStatus } from '@/widgets/PlanGuardWidget/types';

interface UpgradeCTAProps {
  planInfo: PlanStatus;
}

const UpgradeCTA: React.FC<UpgradeCTAProps> = ({ planInfo }) => {
  const handleUpgradeClick = () => {
    // TODO: Redirect to billing/upgrade page
    window.open('/billing', '_blank');
  };

  // Determine if an upgrade is relevant (e.g., not on Enterprise plan)
  const isUpgradeRelevant = !planInfo.tier.toLowerCase().includes('enterprise');

  if (!isUpgradeRelevant) {
    return (
      <div className="bg-green-100 border-l-4 border-green-500 text-green-700 p-4" role="alert">
        <p className="font-bold">You&apos;re on the top tier!</p>
        <p className="text-sm">Enjoy all the features your Enterprise plan offers.</p>
      </div>
    );
  }

  return (
    <div className="bg-indigo-600 text-white p-6 rounded-lg shadow-md text-center space-y-4">
      <h2 className="text-2xl font-bold">Unlock Full Power!</h2>
      <p className="text-lg">
        {planInfo.tier.toLowerCase().includes('free') ? PlanMessages.UPSELL_NUDGE_FREE_TO_PRO : PlanMessages.UPSELL_NUDGE_PRO_TO_ENTERPRISE}
      </p>
      <Button
        onClick={handleUpgradeClick}
        className="bg-white text-indigo-600 hover:bg-gray-100 font-semibold py-3 px-8 rounded-full shadow-lg transition-all duration-300"
      >
        Upgrade Your Plan Now
      </Button>
    </div>
  );
};

export default UpgradeCTA;
