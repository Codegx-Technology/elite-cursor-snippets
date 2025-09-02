'use client';

import Card from '@/components/Card';
import { FaChartLine, FaVideo, FaExclamationTriangle } from 'react-icons/fa6';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + uxfix
// [CONTEXT]: Admin reporting overview page
// [GOAL]: Provide visible, high-contrast summary widgets so the page is not blank

export default function AdminReportingPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-600 via-red-600 to-black p-6 rounded-xl text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">Admin Reporting</h1>
            <p className="text-green-100">Operational health and usage insights</p>
          </div>
          <FaChartLine className="text-3xl text-yellow-300" aria-label="Reporting" />
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="p-5">
          <div className="text-charcoal text-sm">Active Users</div>
          <div className="text-3xl font-bold text-charcoal mt-1">—</div>
        </Card>
        <Card className="p-5">
          <div className="text-charcoal text-sm">Videos Generated (24h)</div>
          <div className="text-3xl font-bold text-charcoal mt-1">—</div>
        </Card>
        <Card className="p-5">
          <div className="text-charcoal text-sm">Avg. Queue Time</div>
          <div className="text-3xl font-bold text-charcoal mt-1">—</div>
        </Card>
        <Card className="p-5">
          <div className="text-charcoal text-sm">Errors (24h)</div>
          <div className="text-3xl font-bold text-red-600 mt-1">—</div>
        </Card>
      </div>

      {/* Recent Activity / Status */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6">
          <h2 className="section-title mb-3 text-charcoal">Recent Activity</h2>
          <ul className="text-sm text-soft-text space-y-2">
            <li>• Activity feed will appear here.</li>
            <li>• Integrate backend metrics when ready.</li>
          </ul>
        </Card>
        <Card className="p-6">
          <h2 className="section-title mb-3 text-charcoal">System Health</h2>
          <div className="flex items-start space-x-3">
            <FaExclamationTriangle className="text-yellow-500 mt-1" />
            <p className="text-sm text-soft-text">
              No live data connected yet. Hook this page to your metrics API to populate charts and KPIs.
            </p>
          </div>
        </Card>
      </div>

      {/* Generation Summary */}
      <Card className="p-6">
        <h2 className="section-title mb-3 text-charcoal">Generation Summary</h2>
        <div className="flex items-center space-x-2 text-soft-text">
          <FaVideo />
          <span className="text-sm">Summary charts coming soon.</span>
        </div>
      </Card>
    </div>
  );
}

