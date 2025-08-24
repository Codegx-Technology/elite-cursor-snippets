// frontend/src/widgets/SuperAdminDashboard/TTSVoiceManagementSection.tsx

import React, { useEffect, useState } from 'react';
import { useAuth } from '@/context/AuthContext';

interface VoiceVersion {
  version: string;
  registered_at: string;
  metadata?: unknown;
}

interface VoiceStatus {
  voice_name: string;
  active_version?: VoiceVersion;
  available_versions: VoiceVersion[];
}

const TTSVoiceManagementSection: React.FC = () => {
  const { user, isAuthenticated } = useAuth();
  const [voiceStatus, setVoiceStatus] = useState<VoiceStatus[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchVoiceStatus = async () => {
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('jwt_token');
      const response = await fetch('http://localhost:8000/admin/voices/status', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setVoiceStatus(data);
    } catch (err: unknown) {
      setError((err as Error).message || 'Failed to fetch voice status.');
    } finally {
      setLoading(false);
    }
  };

  const handleActivateVoice = async (voiceName: string, version: string) => {
    // TODO: Implement API call to activate a specific voice version
    console.log(`Activating voice ${voiceName} version ${version}`);
    // After activation, refetch voice status
    // fetchVoiceStatus();
  };

  useEffect(() => {
    if (isAuthenticated && user?.role === 'admin') {
      fetchVoiceStatus();
    }
  }, [isAuthenticated, user]);

  if (loading) {
    return <p>Loading TTS voice status...</p>;
  }

  if (error) {
    return <p className="text-red-500">Error: {error}</p>;
  }

  return (
    <div className="bg-gray-50 p-4 rounded-lg">
      <h4 className="text-lg font-semibold mb-2">Manage TTS Voices</h4>
      <p className="text-gray-600 mb-4">View available TTS voice models and activate specific versions.</p>

      {voiceStatus.length === 0 ? (
        <p>No TTS voice models found.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white shadow-md rounded-lg overflow-hidden">
            <thead className="bg-gray-200 text-gray-600 uppercase text-sm leading-normal">
              <tr>
                <th className="py-3 px-6 text-left">Voice Name</th>
                <th className="py-3 px-6 text-left">Active Version</th>
                <th className="py-3 px-6 text-left">Available Versions</th>
                <th className="py-3 px-6 text-center">Actions</th>
              </tr>
            </thead>
            <tbody className="text-gray-600 text-sm font-light">
              {voiceStatus.map((voice) => (
                <tr key={voice.voice_name} className="border-b border-gray-200 hover:bg-gray-100">
                  <td className="py-3 px-6 text-left whitespace-nowrap">{voice.voice_name}</td>
                  <td className="py-3 px-6 text-left">{voice.active_version?.version || 'N/A'}</td>
                  <td className="py-3 px-6 text-left">
                    {voice.available_versions.map((v) => v.version).join(', ')}
                  </td>
                  <td className="py-3 px-6 text-center">
                    <select
                      onChange={(e) => handleActivateVoice(voice.voice_name, e.target.value)}
                      className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                      defaultValue=""
                    >
                      <option value="" disabled>Activate Version</option>
                      {voice.available_versions.map((v) => (
                        <option key={v.version} value={v.version}>
                          {v.version}
                        </option>
                      ))}
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default TTSVoiceManagementSection;
