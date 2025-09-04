'use client';

import { useState, useEffect } from 'react';
import { FaHeartbeat, FaShieldAlt, FaPlay, FaPause, FaVolumeUp, FaVolumeMute, FaCog, FaExclamationTriangle, FaCheckCircle, FaSpinner } from 'react-icons/fa6';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorintent + augmentsearch
// [CONTEXT]: Health scanner UI component with Kenya-first design and real-time monitoring
// [GOAL]: Provide intuitive interface for AI health scanner with cultural authenticity
// [TASK]: Create comprehensive health monitoring dashboard with controls

interface HealthMetrics {
  timestamp: string;
  frontend_status: 'healthy' | 'warning' | 'critical' | 'down';
  backend_status: 'healthy' | 'warning' | 'critical' | 'down';
  api_response_time: number;
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  network_latency: number;
  error_count: number;
  active_connections: number;
}

interface ScannerStatus {
  scanner_status: 'running' | 'stopped';
  muted: boolean;
  last_scan: HealthMetrics;
  auto_fix_count: number;
  scan_history_count: number;
  overall_health: 'healthy' | 'warning' | 'critical' | 'unknown';
}

export default function HealthScanner() {
  const [scannerStatus, setScannerStatus] = useState<ScannerStatus | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [autoRefresh, setAutoRefresh] = useState(true);

  useEffect(() => {
    fetchScannerStatus();
    
    if (autoRefresh) {
      const interval = setInterval(fetchScannerStatus, 30000); // Refresh every 30 seconds
      return () => clearInterval(interval);
    }
  }, [autoRefresh]);

  const fetchScannerStatus = async () => {
    try {
      // In a real implementation, this would call the health scanner API
      // For now, we'll simulate the data
      const mockStatus: ScannerStatus = {
        scanner_status: 'running',
        muted: false,
        last_scan: {
          timestamp: new Date().toISOString(),
          frontend_status: 'healthy',
          backend_status: 'healthy',
          api_response_time: 150,
          cpu_usage: 45,
          memory_usage: 60,
          disk_usage: 35,
          network_latency: 25,
          error_count: 0,
          active_connections: 12
        },
        auto_fix_count: 2,
        scan_history_count: 45,
        overall_health: 'healthy'
      };
      
      setScannerStatus(mockStatus);
      setIsLoading(false);
    } catch (err) {
      setError('Failed to fetch scanner status');
      setIsLoading(false);
    }
  };

  const toggleScanner = async () => {
    // Implementation would call scanner start/stop API
    console.log('Toggle scanner');
  };

  const toggleMute = async () => {
    // Implementation would call scanner mute/unmute API
    console.log('Toggle mute');
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'text-green-600';
      case 'warning': return 'text-yellow-600';
      case 'critical': return 'text-red-600';
      case 'down': return 'text-red-800';
      default: return 'text-gray-600';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy': return <FaCheckCircle className="text-green-600" />;
      case 'warning': return <FaExclamationTriangle className="text-yellow-600" />;
      case 'critical': return <FaExclamationTriangle className="text-red-600" />;
      case 'down': return <FaExclamationTriangle className="text-red-800" />;
      default: return <FaSpinner className="text-gray-600 animate-spin" />;
    }
  };

  const getUsageColor = (usage: number) => {
    if (usage > 90) return 'bg-red-500';
    if (usage > 70) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex items-center justify-center h-32">
          <div className="text-center">
            <FaSpinner className="w-8 h-8 text-green-600 animate-spin mx-auto mb-2" />
            <span className="text-gray-600">Loading health scanner...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="text-center text-red-600">
          <FaExclamationTriangle className="w-8 h-8 mx-auto mb-2" />
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!scannerStatus) return null;

  return (
    <div className="space-y-6">
      {/* Kenya-First Header */}
      <div className="bg-gradient-to-r from-green-600 via-red-600 to-black p-6 rounded-xl text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <FaShieldAlt className="text-3xl" />
            <div>
              <h2 className="text-2xl font-bold">AI Health Scanner 🇰🇪</h2>
              <p className="text-green-100">Intelligent system monitoring with Harambee spirit</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${scannerStatus.scanner_status === 'running' ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`}></div>
            <span className="text-sm">{scannerStatus.scanner_status}</span>
          </div>
        </div>
      </div>

      {/* Scanner Controls */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-800">Scanner Controls</h3>
          <div className="flex space-x-2">
            <button
              onClick={toggleScanner}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                scannerStatus.scanner_status === 'running'
                  ? 'bg-red-600 hover:bg-red-700 text-white'
                  : 'bg-green-600 hover:bg-green-700 text-white'
              }`}
            >
              {scannerStatus.scanner_status === 'running' ? <FaPause /> : <FaPlay />}
              <span>{scannerStatus.scanner_status === 'running' ? 'Stop' : 'Start'}</span>
            </button>
            
            <button
              onClick={toggleMute}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                scannerStatus.muted
                  ? 'bg-gray-600 hover:bg-gray-700 text-white'
                  : 'bg-blue-600 hover:bg-blue-700 text-white'
              }`}
            >
              {scannerStatus.muted ? <FaVolumeMute /> : <FaVolumeUp />}
              <span>{scannerStatus.muted ? 'Unmute' : 'Mute'}</span>
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center space-x-2 mb-2">
              <FaHeartbeat className="text-red-500" />
              <span className="font-medium">Overall Health</span>
            </div>
            <div className={`text-2xl font-bold ${getStatusColor(scannerStatus.overall_health)}`}>
              {scannerStatus.overall_health.toUpperCase()}
            </div>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center space-x-2 mb-2">
              <FaCog className="text-blue-500" />
              <span className="font-medium">Auto Fixes</span>
            </div>
            <div className="text-2xl font-bold text-blue-600">
              {scannerStatus.auto_fix_count}
            </div>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center space-x-2 mb-2">
              <FaShieldAlt className="text-green-500" />
              <span className="font-medium">Total Scans</span>
            </div>
            <div className="text-2xl font-bold text-green-600">
              {scannerStatus.scan_history_count}
            </div>
          </div>
        </div>
      </div>

      {/* System Status */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">System Status</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Service Status */}
          <div>
            <h4 className="font-medium text-gray-700 mb-3">Services</h4>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  {getStatusIcon(scannerStatus.last_scan.frontend_status)}
                  <span>Frontend</span>
                </div>
                <span className={`font-medium ${getStatusColor(scannerStatus.last_scan.frontend_status)}`}>
                  {scannerStatus.last_scan.frontend_status}
                </span>
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  {getStatusIcon(scannerStatus.last_scan.backend_status)}
                  <span>Backend</span>
                </div>
                <span className={`font-medium ${getStatusColor(scannerStatus.last_scan.backend_status)}`}>
                  {scannerStatus.last_scan.backend_status}
                </span>
              </div>
              
              <div className="flex items-center justify-between">
                <span>API Response Time</span>
                <span className={`font-medium ${scannerStatus.last_scan.api_response_time > 1000 ? 'text-red-600' : 'text-green-600'}`}>
                  {scannerStatus.last_scan.api_response_time}ms
                </span>
              </div>
            </div>
          </div>

          {/* Resource Usage */}
          <div>
            <h4 className="font-medium text-gray-700 mb-3">Resource Usage</h4>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>CPU Usage</span>
                  <span>{scannerStatus.last_scan.cpu_usage}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${getUsageColor(scannerStatus.last_scan.cpu_usage)}`}
                    style={{ width: `${scannerStatus.last_scan.cpu_usage}%` }}
                  ></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Memory Usage</span>
                  <span>{scannerStatus.last_scan.memory_usage}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${getUsageColor(scannerStatus.last_scan.memory_usage)}`}
                    style={{ width: `${scannerStatus.last_scan.memory_usage}%` }}
                  ></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Disk Usage</span>
                  <span>{scannerStatus.last_scan.disk_usage}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${getUsageColor(scannerStatus.last_scan.disk_usage)}`}
                    style={{ width: `${scannerStatus.last_scan.disk_usage}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Additional Metrics */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Additional Metrics</h3>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">{scannerStatus.last_scan.network_latency}ms</div>
            <div className="text-sm text-gray-600">Network Latency</div>
          </div>
          
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-600">{scannerStatus.last_scan.error_count}</div>
            <div className="text-sm text-gray-600">Recent Errors</div>
          </div>
          
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">{scannerStatus.last_scan.active_connections}</div>
            <div className="text-sm text-gray-600">Active Connections</div>
          </div>
          
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600">
              {new Date(scannerStatus.last_scan.timestamp).toLocaleTimeString()}
            </div>
            <div className="text-sm text-gray-600">Last Scan</div>
          </div>
        </div>
      </div>

      {/* Kenya-First Footer */}
      <div className="bg-gradient-to-r from-yellow-400 via-red-500 to-green-600 p-4 rounded-lg text-white text-center">
        <div className="flex items-center justify-center space-x-2">
          <FaShieldAlt className="text-lg" />
          <span className="font-medium">Protecting your Shujaa Studio with AI intelligence • Harambee spirit</span>
          <FaHeartbeat className="text-lg" />
        </div>
      </div>
    </div>
  );
}

