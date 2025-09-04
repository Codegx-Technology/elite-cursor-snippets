// frontend/src/widgets/UserPlanDashboard/EventTimeline.tsx

import React from 'react';

// This component will display a timeline of PlanGuard enforcement events
// It will likely fetch its own data from a backend API (e.g., /api/user/plan-events)

interface EventTimelineProps {
  className?: string;
}

const EventTimeline: React.FC<EventTimelineProps> = () => {
  // TODO: Implement fetching and displaying of user-specific PlanGuard events
  // Example events:
  // - Plan activated/renewed
  // - Quota warning (e.g., 90% usage)
  // - Slowdown initiated
  // - View-only mode activated
  // - Feature blocked
  // - Grace period started/ended

  const events = [
    { id: 1, timestamp: '2025-08-15T10:00:00Z', type: 'PLAN_ACTIVATED', message: 'Plan activated: Professional' },
    { id: 2, timestamp: '2025-08-20T09:30:00Z', type: 'QUOTA_WARNING', message: 'Video minutes 90% used' },
    { id: 3, timestamp: '2025-08-20T10:00:00Z', type: 'SLOWDOWN_INITIATED', message: 'Responses may be slower due to plan limits' },
    { id: 4, timestamp: '2025-08-21T10:00:00Z', type: 'VIEW_ONLY_MODE', message: 'Plan expired. View-only mode activated.' },
  ];

  return (
    <div className="bg-white p-6 rounded-lg shadow-md space-y-4">
      <h2 className="text-xl font-semibold text-gray-800">Event History</h2>
      <div className="space-y-3">
        {events.length === 0 ? (
          <p className="text-gray-500">No recent plan events.</p>
        ) : (
          events.map((event) => (
            <div key={event.id} className="border-l-4 border-blue-500 pl-3 py-1">
              <p className="text-sm text-gray-600">{new Date(event.timestamp).toLocaleString()}</p>
              <p className="font-medium text-gray-800">{event.message}</p>
              <span className="text-xs text-blue-700 bg-blue-100 px-2 py-1 rounded-full">{event.type}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default EventTimeline;
