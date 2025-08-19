import { Lock } from "lucide-react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";

interface Props {
  expiredAt: string;
  onUpgrade: () => void;
}

export default function ViewOnlyOverlay({ expiredAt, onUpgrade }: Props) {
  return (
    <motion.div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <motion.div
        className="bg-white max-w-lg w-full mx-4 p-8 rounded-2xl shadow-2xl text-center space-y-6"
        initial={{ scale: 0.9 }}
        animate={{ scale: 1 }}
      >
        <div className="flex flex-col items-center space-y-3">
          <Lock className="w-12 h-12 text-red-500" />
          <h2 className="text-2xl font-bold">🔒 View-Only Mode</h2>
          <p className="text-gray-600">
            Your plan expired on <span className="font-semibold">{expiredAt}</span>.  
            You can still browse past data, but all actions are disabled until you upgrade.
          </p>
        </div>

        <div className="flex flex-col gap-3">
          <Button onClick={onUpgrade} className="bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl py-3 text-lg shadow-md">
            Upgrade Now
          </Button>
          <p className="text-sm text-gray-500">Need help? Contact support anytime.</p>
        </div>
      </motion.div>
    </motion.div>
  );
}

export default ViewOnlyOverlay;
