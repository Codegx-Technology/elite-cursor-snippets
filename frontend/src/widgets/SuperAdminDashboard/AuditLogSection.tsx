import React, { useState, useEffect } from 'react';
import { fetchAuditLogs } from './adminService';
import type { AuditLogEntry } from '@/lib/api';
import { Card } from '@/components/ui/card';
import { FaHistory, FaSpinner, FaExclamationTriangle } from 'react-icons/fa6';

const AuditLogSection: React.FC = () => {
  const [logs, setLogs] = useState<AuditLogEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const getLogs = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchAuditLogs();
        setLogs(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch audit logs.');
      } finally {
        setLoading(false);
      }
    };
    getLogs();
  }, []);

  if (loading) {
    return (
      <Card className="p-4 flex items-center justify-center">
        <FaSpinner className="animate-spin mr-2" /> Loading audit logs...
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="p-4 text-red-600 flex items-center">
        <FaExclamationTriangle className="mr-2" /> Error: {error}
      </Card>
    );
  }

  return (
    <Card className="p-4">
      <h4 className="text-lg font-semibold mb-4 flex items-center"><FaHistory className="mr-2" /> Audit Logs</h4>
      <p className="text-gray-600 mb-4">View system and user activity logs.</p>
      
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white">
          <thead>
            <tr>
              <th className="py-2 px-4 border-b text-left">Timestamp</th>
              <th className="py-2 px-4 border-b text-left">Event Type</th>
              <th className="py-2 px-4 border-b text-left">Message</th>
              <th className="py-2 px-4 border-b text-left">User ID</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id}>
                <td className="py-2 px-4 border-b text-sm">{new Date(log.timestamp).toLocaleString()}</td>
                <td className="py-2 px-4 border-b text-sm">{log.event_type}</td>
                <td className="py-2 px-4 border-b text-sm">{log.message}</td>
                <td className="py-2 px-4 border-b text-sm">{log.user_id || 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
};

export default AuditLogSection;
