'use client';
import React, { useEffect, useState, useRef, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { useToast } from '@/components/ui/use-toast';
import JobLogPanel from './JobLogPanel'; // Import JobLogPanel

interface Dependency {
  name: string;
  installed_version: string;
  required_range: string;
  status: 'HEALTHY' | 'OUTDATED' | 'MISSING' | 'UNSUPPORTED';
  message: string;
}

const DependencyWatcher: React.FC = () => {
  const [dependencies, setDependencies] = useState<Dependency[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [alertedDeps, setAlertedDeps] = useState<Set<string>>(new Set());
  const { addToast } = useToast();
  const prevDependenciesRef = useRef<Dependency[]>([]);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectAttempts = useRef(0);

  const [showJobLogPanel, setShowJobLogPanel] = useState<boolean>(false);
  const [currentJobId, setCurrentJobId] = useState<string | null>(null);

  const processNewDependencies = useCallback((newDependencies: Dependency[]) => {
    if (prevDependenciesRef.current.length > 0) {
      newDependencies.forEach(newDep => {
        const oldDep = prevDependenciesRef.current.find(d => d.name === newDep.name);

        if (oldDep && oldDep.status !== newDep.status) {
          if ((newDep.status === 'MISSING' || newDep.status === 'OUTDATED') && !alertedDeps.has(newDep.name)) {
            addToast({
              title: "Dependency Issue Detected",
              description: `${newDep.name} is now ${newDep.status}. ${newDep.message}`,
              type: newDep.status === 'MISSING' ? 'destructive' : 'warning',
            });
            setAlertedDeps(prev => new Set(prev).add(newDep.name));
          } else if (newDep.status === 'HEALTHY' && alertedDeps.has(newDep.name)) {
            setAlertedDeps(prev => {
              const newSet = new Set(prev);
              newSet.delete(newDep.name);
              return newSet;
            });
          }
        }
      });
    }
    setDependencies(newDependencies);
    prevDependenciesRef.current = newDependencies;
  }, [alertedDeps, addToast]);

  const connectWebSocket = useCallback(() => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      return;
    }

    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws/dependencies`;
    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onopen = () => {
      console.log('WebSocket connected');
      reconnectAttempts.current = 0; // Reset reconnect attempts on successful connection
      setLoading(false); // Once connected, stop showing initial loading
      setError(null);
    };

    wsRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.event === 'dependency_status') {
        processNewDependencies(data.data);
      }
    };

    wsRef.current.onclose = (event) => {
      console.log('WebSocket disconnected:', event.code, event.reason);
      if (event.code !== 1000) { // 1000 is normal closure
        reconnectAttempts.current++;
        const delay = Math.min(1000 * (2 ** reconnectAttempts.current), 30000); // Max 30 seconds
        console.log(`Attempting to reconnect in ${delay / 1000} seconds...`);
        setTimeout(connectWebSocket, delay);
      }
    };

    wsRef.current.onerror = (err) => {
      console.error('WebSocket error:', err);
      setError('WebSocket connection error. Real-time updates may be unavailable.');
      wsRef.current?.close(); // Close to trigger onclose and reconnect logic
    };
  }, [processNewDependencies]);

  useEffect(() => {
    connectWebSocket();

    return () => {
      wsRef.current?.close();
    };
  }, [connectWebSocket]);

  const handleManualRefresh = async () => {
    setLoading(true);
    setError(null);
    try {
      // Send a request to the backend to force a re-check and broadcast
      await axios.get('/api/dependencies/status?force=true');
      // The WebSocket will then receive the updated status
    } catch (err) {
      console.error('Failed to trigger manual refresh:', err);
      setError('Failed to trigger manual refresh. Check console for details.');
    } finally {
      setLoading(false);
    }
  };

  const getBadgeVariant = (status: Dependency['status']) => {
    switch (status) {
      case 'HEALTHY':
        return 'default';
      case 'OUTDATED':
        return 'warning';
      case 'MISSING':
        return 'destructive';
      case 'UNSUPPORTED':
        return 'secondary';
      default:
        return 'outline';
    }
  };

  const handleDryRun = async (dep: Dependency) => {
    try {
      // Assuming you need to create a plan first, then dry-run it
      const planResponse = await axios.post('/api/depwatcher/plan', [{
        name: dep.name,
        kind: dep.message.includes('Model') ? 'model' : 'pip',
        toVersion: dep.required_range.split('-')[0] || dep.installed_version,
        env: dep.message.includes('venv') ? dep.message.split('venv: ')[1].split(')')[0] : undefined,
      }]);
      const planId = planResponse.data.id;

      await axios.post(`/api/depwatcher/dry-run/${planId}`);
      addToast({
        title: "Dry Run Initiated",
        description: `Dry run for ${dep.name} simulated. Plan ID: ${planId}. Check backend logs for details.`,
        type: "info",
      });
      // Optionally, show a modal with dryRunResponse.data
    } catch (err: unknown) {
      console.error('Dry Run failed:', err);
      let description = "Failed to initiate dry run.";
      if (axios.isAxiosError(err) && err.response?.data?.detail) {
          description = err.response.data.detail;
      }
      addToast({
        title: "Dry Run Failed",
        description,
        type: "destructive",
      });
    }
  };

  const handleApprove = async (dep: Dependency) => {
    try {
      // This assumes a plan already exists or is created implicitly
      // For simplicity, we'll create a plan and then approve it
      const planResponse = await axios.post('/api/depwatcher/plan', [{
        name: dep.name,
        kind: dep.message.includes('Model') ? 'model' : 'pip',
        toVersion: dep.required_range.split('-')[0] || dep.installed_version,
        env: dep.message.includes('venv') ? dep.message.split('venv: ')[1].split(')')[0] : undefined,
      }]);
      const planId = planResponse.data.id;

      await axios.post(`/api/depwatcher/approve/${planId}`);
      addToast({
        title: "Approval Sent",
        description: `Approval for ${dep.name} (Plan ID: ${planId}) sent.`,
        type: "info",
      });
    } catch (err: unknown) {
      console.error('Approval failed:', err);
      let description = "Failed to approve plan.";
      if (axios.isAxiosError(err) && err.response?.data?.detail) {
          description = err.response.data.detail;
      }
      addToast({
        title: "Approval Failed",
        description,
        type: "destructive",
      });
    }
  };

  const handleApply = async (dep: Dependency) => {
    try {
      // For simplicity, we'll create a plan and then apply it
      const planResponse = await axios.post('/api/depwatcher/plan', [{
        name: dep.name,
        kind: dep.message.includes('Model') ? 'model' : 'pip',
        toVersion: dep.required_range.split('-')[0] || dep.installed_version,
        env: dep.message.includes('venv') ? dep.message.split('venv: ')[1].split(')')[0] : undefined,
      }]);
      const planId = planResponse.data.id;

      const applyResponse = await axios.post(`/api/depwatcher/apply/${planId}`);
      const jobId = applyResponse.data.job_id;
      
      addToast({
        title: "Apply Initiated",
        description: `Applying patch for ${dep.name}. Job ID: ${jobId}.`,
        type: "info",
      });
      setCurrentJobId(jobId);
      setShowJobLogPanel(true);
    } catch (err: unknown) {
      console.error('Apply failed:', err);
      let description = "Failed to apply patch.";
      if (axios.isAxiosError(err) && err.response?.data?.detail) {
          description = err.response.data.detail;
      }
      addToast({
        title: "Apply Failed",
        description,
        type: "destructive",
      });
    }
  };

  return (
    <Card className="rounded-2xl shadow-lg p-4">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-2xl font-bold">Dependency Health</CardTitle>
        <Button onClick={handleManualRefresh} disabled={loading}>
          {loading ? 'Refreshing...' : 'Refresh'}
        </Button>
      </CardHeader>
      <CardContent>
        {loading && dependencies.length === 0 ? (
          <div className="text-center py-8">Connecting to real-time updates...</div>
        ) : error ? (
          <div className="text-center py-8 text-red-500">{error}</div>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Installed Version</TableHead>
                  <TableHead>Required Range</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Message</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <AnimatePresence>
                  {dependencies.map((dep, index) => (
                    <motion.tr
                      key={dep.name}
                      initial={{ opacity: 0, y: -5 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: 5 }}
                      transition={{ duration: 0.3 }}
                      className={index % 2 === 0 ? 'bg-gray-50' : ''}
                    >
                      <TableCell className="font-medium">{dep.name}</TableCell>
                      <TableCell>{dep.installed_version}</TableCell>
                      <TableCell>{dep.required_range}</TableCell>
                      <TableCell>
                        <Badge variant={getBadgeVariant(dep.status)}>{dep.status}</Badge>
                      </TableCell>
                      <TableCell>{dep.message}</TableCell>
                      <TableCell>
                        {(dep.status === 'MISSING' || dep.status === 'OUTDATED') && (
                          <div className="flex space-x-2">
                            <Button variant="outline" size="sm" onClick={() => handleDryRun(dep)}>Dry Run</Button>
                            <Button variant="secondary" size="sm" onClick={() => handleApprove(dep)}>Approve</Button>
                            <Button size="sm" onClick={() => handleApply(dep)}>Apply</Button>
                          </div>
                        )}
                      </TableCell>
                    </motion.tr>
                  ))}
                </AnimatePresence>
              </TableBody>
            </Table>
          </motion.div>
        )}
      </CardContent>
      {showJobLogPanel && currentJobId && (
        <CardContent className="mt-4">
          <JobLogPanel jobId={currentJobId} />
        </CardContent>
      )}
    </Card>
  );
};

export default DependencyWatcher;
