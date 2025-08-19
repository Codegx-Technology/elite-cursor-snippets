import React, { useState, useEffect } from 'react';
import { FaClock, FaExclamationTriangle } from 'react-icons/fa';

interface GraceCountdownOverlayProps {
  graceExpiresAt: string; // ISO string from API
  onUpgradeClick: () => void;
}

const GraceCountdownOverlay: React.FC<GraceCountdownOverlayProps> = ({
  graceExpiresAt,
  onUpgradeClick,
}) => {
  const calculateTimeLeft = () => {
    const now = new Date();
    const expirationDate = new Date(graceExpiresAt);
    const difference = expirationDate.getTime() - now.getTime();

    let timeLeft = {};

    if (difference > 0) {
      timeLeft = {
        hours: Math.floor((difference / (1000 * 60 * 60)) % 24),
        minutes: Math.floor((difference / 1000 / 60) % 60),
        seconds: Math.floor((difference / 1000) % 60),
      };
    } else {
      timeLeft = { hours: 0, minutes: 0, seconds: 0 };
    }
    return timeLeft;
  };

  const [timeLeft, setTimeLeft] = useState(calculateTimeLeft());

  useEffect(() => {
    const timer = setTimeout(() => {
      setTimeLeft(calculateTimeLeft());
    }, 1000);

    return () => clearTimeout(timer);
  });

  const { hours, minutes, seconds } = timeLeft as any;
  const totalHours = hours + minutes / 60 + seconds / 3600;

  let bannerColorClass = 'bg-green-500'; // Default green
  if (totalHours < 12 && totalHours >= 1) {
    bannerColorClass = 'bg-yellow-500'; // Yellow for <12h
  } else if (totalHours < 1) {
    bannerColorClass = 'bg-red-500 animate-pulse'; // Red blinking for <1h
  }

  if (totalHours <= 0) {
    return null; // Hide overlay if grace period is over
  }

  return (
    <div
      className={`fixed bottom-4 right-4 p-4 rounded-lg shadow-lg text-white flex items-center space-x-3 z-50 ${bannerColorClass}`}
    >
      <FaExclamationTriangle className="text-2xl" />
      <div>
        <p className="font-bold text-lg">Plan Expiring: Grace Mode Active</p>
        <p className="text-sm">
          {hours}h {minutes}m {seconds}s left before full lock.
        </p>
      </div>
      <button
        onClick={onUpgradeClick}
        className="ml-4 px-4 py-2 bg-white text-gray-800 rounded-md font-semibold hover:bg-gray-100 transition-colors"
      >
        Upgrade Now
      </button>
    </div>
  );
};

export default GraceCountdownOverlay;
