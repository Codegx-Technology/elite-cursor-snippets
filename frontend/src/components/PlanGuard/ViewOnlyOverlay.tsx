import React from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";

interface ViewOnlyOverlayProps {
  expiredAt: string;
  onUpgrade: () => void;
}

const ViewOnlyOverlay: React.FC<ViewOnlyOverlayProps> = ({ expiredAt, onUpgrade }) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 p-4"
    >
      <motion.div
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="bg-white rounded-lg shadow-xl p-8 text-center max-w-md w-full"
      >
        <h2 className="text-2xl font-bold text-red-600 mb-4">Plan Expired!</h2>
        <p className="text-gray-700 mb-6">
          Your plan expired on <span className="font-semibold">{expiredAt}</span>. You are now in view-only mode.
          Please upgrade your plan to continue using all features.
        </p>
        <Button onClick={onUpgrade} className="bg-blue-600 hover:bg-blue-700 text-white">
          Upgrade Your Plan
        </Button>
      </motion.div>
    </motion.div>
  );
};

export default ViewOnlyOverlay;
