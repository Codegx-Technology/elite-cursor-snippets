import React, { useEffect, useRef, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area'; // Assuming this component exists
import { useToast } from '@/components/ui/use-toast';

interface JobLogPanelProps {
  jobId: string;
}

const JobLogPanel: React.FC<JobLogPanelProps> = ({ jobId }) => {
  const [logs, setLogs] = useState<string[]>([]);
  const [jobStatus, setJobStatus] = useState<string>('pending');
  const wsRef = useRef<WebSocket | null>(null);
  const logEndRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();

  const connectWebSocket = () => {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws/jobs/${jobId}/logs`; // Assuming a job log WebSocket endpoint
    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onopen = () => {
      console.log(`WebSocket connected for job ${jobId}`);
      setJobStatus('connected');
    };

    wsRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.event === 'job_log') {
        setLogs(prevLogs => [...prevLogs, data.message]);
      } else if (data.event === 'job_status_update') {
        setJobStatus(data.status);
        if (data.status === 'completed' || data.status === 'failed') {
          toast({
            title: `Job ${data.status.charAt(0).toUpperCase() + data.status.slice(1)}: ${jobId}`,
            description: data.message || `Job ${jobId} has ${data.status}`,
            variant: data.status === 'failed' ? 'destructive' : 'default',
          });
          wsRef.current?.close();
        }
      }
    };

    wsRef.current.onclose = () => {
      console.log(`WebSocket disconnected for job ${jobId}`);
      if (jobStatus === 'pending' || jobStatus === 'connected') {
        setJobStatus('disconnected');
      }
    };

    wsRef.current.onerror = (err) => {
      console.error(`WebSocket error for job ${jobId}:`, err);
      setJobStatus('error');
      toast({
        title: "WebSocket Error",
        description: `Failed to stream logs for job ${jobId}`,
        variant: "destructive",
      });
    };
  };

  useEffect(() => {
    connectWebSocket();

    return () => {
      wsRef.current?.close();
    };
  }, [jobId]);

  useEffect(() => {
    if (logEndRef.current) {
      logEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [logs]);

  const handleCopyToClipboard = () => {
    navigator.clipboard.writeText(logs.join('\n'))
      .then(() => toast({ title: "Logs copied to clipboard" }))
      .catch(err => console.error('Failed to copy logs:', err));
  };

  return (
    <Card className="rounded-2xl shadow-lg p-4">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-xl font-bold">Job Logs: {jobId}</CardTitle>
        <Button variant="outline" size="sm" onClick={handleCopyToClipboard}>
          Copy Logs
        </Button>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[300px] w-full rounded-md border p-4 font-mono text-sm bg-gray-900 text-gray-100">
          {logs.length === 0 && jobStatus === 'pending' ? (
            <div className="text-gray-400">Waiting for logs...</div>
          ) : logs.length === 0 && jobStatus === 'disconnected' ? (
            <div className="text-red-400">Disconnected from log stream.</div>
          ) : (
            logs.map((log, index) => (
              <div key={index} className="whitespace-pre-wrap">{log}</div>
            ))
          )}
          <div ref={logEndRef} />
        </ScrollArea>
        <div classNameName="text-right text-sm text-gray-500 mt-2">
          Status: {jobStatus}
        </div>
      </CardContent>
    </Card>
  );
};

export default JobLogPanel;
