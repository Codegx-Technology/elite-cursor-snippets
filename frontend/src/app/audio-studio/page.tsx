'use client';

import { useState } from 'react';
import Card from '@/components/Card';
import FormInput from '@/components/FormInput';
import FormSelect from '@/components/FormSelect';
import { FaDownload, FaFlag, FaMicrophone, FaMountain, FaMusic, FaPause, FaPlay, FaStop, FaVolumeHigh, FaWaveSquare } from 'react-icons/fa6';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorintent
// [CONTEXT]: Audio Studio page for voice and music creation with Kenya-first design
// [GOAL]: Create comprehensive audio creation interface with mobile-first approach
// [TASK]: Implement audio studio with proper controls and cultural authenticity

interface AudioProject {
  id: string;
  name: string;
  type: 'voice' | 'music' | 'sound-effect';
  duration: string;
  createdAt: string;
  status: 'draft' | 'processing' | 'completed';
}

export default function AudioStudioPage() {
  const [activeTab, setActiveTab] = useState<'voice' | 'music' | 'effects'>('voice');
  const [isRecording, setIsRecording] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [projects, setProjects] = useState<AudioProject[]>([]);
  const [voiceSettings, setVoiceSettings] = useState({
    text: '',
    language: 'swahili',
    voice: 'female',
    speed: '1.0',
    pitch: '1.0'
  });

  const [musicSettings, setMusicSettings] = useState({
    genre: 'traditional',
    mood: 'uplifting',
    duration: '30',
    instruments: 'african-drums'
  });

  const languageOptions = [
    { value: 'swahili', label: 'Kiswahili' },
    { value: 'english', label: 'English' },
    { value: 'kikuyu', label: 'Kikuyu' },
    { value: 'luo', label: 'Luo' },
    { value: 'luhya', label: 'Luhya' },
    { value: 'sheng', label: 'Sheng' }
  ];

  const voiceOptions = [
    { value: 'female', label: 'Female Voice' },
    { value: 'male', label: 'Male Voice' },
    { value: 'child', label: 'Child Voice' }
  ];

  const genreOptions = [
    { value: 'traditional', label: 'Traditional Kenyan' },
    { value: 'benga', label: 'Benga' },
    { value: 'gospel', label: 'Gospel' },
    { value: 'afrobeat', label: 'Afrobeat' },
    { value: 'rumba', label: 'Rumba' },
    { value: 'modern', label: 'Modern' }
  ];

  const handleVoiceGeneration = () => {
    if (!voiceSettings.text.trim()) {
      alert('Please enter text to generate voice');
      return;
    }
    
    // Simulate voice generation
    console.log('Generating voice with settings:', voiceSettings);
    alert('Voice generation started! This feature will be connected to the backend soon.');
  };

  const handleMusicGeneration = () => {
    // Simulate music generation
    console.log('Generating music with settings:', musicSettings);
    alert('Music generation started! This feature will be connected to the backend soon.');
  };

  return (
    <div className="space-y-6">
      {/* Kenya-First Header */}
      <div className="bg-gradient-to-r from-green-600 via-red-600 to-black p-6 rounded-xl text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <FaMusic className="text-3xl" />
            <div>
              <h1 className="text-2xl font-bold">Audio Studio 🇰🇪</h1>
              <p className="text-green-100">Create authentic Kenyan voices and music</p>
            </div>
          </div>
          <div className="hidden md:block">
            <FaMountain className="text-4xl text-yellow-300" />
          </div>
        </div>
      </div>

      {/* Tab Navigation */}
      <Card className="p-6">
        <div className="flex flex-wrap gap-2 mb-6">
          {[
            { key: 'voice', label: 'Voice Generation', icon: FaMicrophone },
            { key: 'music', label: 'Music Creation', icon: FaMusic },
            { key: 'effects', label: 'Sound Effects', icon: FaWaveSquare }
          ].map(({ key, label, icon: Icon }) => (
            <button
              key={key}
              onClick={() => setActiveTab(key as 'voice' | 'music' | 'effects')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors duration-200 ${
                activeTab === key
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <Icon className="text-sm" />
              <span className="font-medium">{label}</span>
            </button>
          ))}
        </div>

        {/* Voice Generation Tab */}
        {activeTab === 'voice' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Text-to-Speech Generation</h3>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Text to Convert
                    </label>
                    <textarea
                      value={voiceSettings.text}
                      onChange={(e) => setVoiceSettings({...voiceSettings, text: e.target.value})}
                      placeholder="Enter text in Kiswahili, English, or local languages..."
                      className="w-full h-32 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none"
                    />
                  </div>

                  <FormSelect
                    label="Language"
                    value={voiceSettings.language}
                    onChange={(e) => setVoiceSettings({...voiceSettings, language: (e.target as HTMLSelectElement).value})}
                    options={languageOptions}
                  />

                  <FormSelect
                    label="Voice Type"
                    value={voiceSettings.voice}
                    onChange={(e) => setVoiceSettings({...voiceSettings, voice: (e.target as HTMLSelectElement).value})}
                    options={voiceOptions}
                  />
                </div>

                <div className="space-y-4">
                  <FormInput
                    label="Speed"
                    type="range"
                    min="0.5"
                    max="2.0"
                    step="0.1"
                    value={voiceSettings.speed}
                    onChange={(e) => setVoiceSettings({...voiceSettings, speed: (e.target as HTMLInputElement).value})}
                  />

                  <FormInput
                    label="Pitch"
                    type="range"
                    min="0.5"
                    max="2.0"
                    step="0.1"
                    value={voiceSettings.pitch}
                    onChange={(e) => setVoiceSettings({...voiceSettings, pitch: (e.target as HTMLInputElement).value})}
                  />

                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <h4 className="font-medium text-blue-800 mb-2">Preview Controls</h4>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => setIsPlaying(!isPlaying)}
                        className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors duration-200"
                      >
                        {isPlaying ? <FaPause /> : <FaPlay />}
                        <span>{isPlaying ? 'Pause' : 'Preview'}</span>
                      </button>
                      <button className="flex items-center space-x-2 bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg transition-colors duration-200">
                        <FaStop />
                        <span>Stop</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex justify-end mt-6">
                <button
                  onClick={handleVoiceGeneration}
                  className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200"
                >
                  Generate Voice
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Music Creation Tab */}
        {activeTab === 'music' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">AI Music Generation</h3>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <FormSelect
                    label="Genre"
                    value={musicSettings.genre}
                    onChange={(e) => setMusicSettings({...musicSettings, genre: (e.target as HTMLSelectElement).value})}
                    options={genreOptions}
                  />

                  <FormSelect
                    label="Mood"
                    value={musicSettings.mood}
                    onChange={(e) => setMusicSettings({...musicSettings, mood: (e.target as HTMLSelectElement).value})}
                    options={[
                      { value: 'uplifting', label: 'Uplifting' },
                      { value: 'calm', label: 'Calm' },
                      { value: 'energetic', label: 'Energetic' },
                      { value: 'dramatic', label: 'Dramatic' },
                      { value: 'celebratory', label: 'Celebratory' }
                    ]}
                  />
                </div>

                <div className="space-y-4">
                  <FormInput
                    label="Duration (seconds)"
                    type="number"
                    min="10"
                    max="300"
                    value={musicSettings.duration}
                    onChange={(e) => setMusicSettings({...musicSettings, duration: (e.target as HTMLInputElement).value})}
                  />

                  <FormSelect
                    label="Primary Instruments"
                    value={musicSettings.instruments}
                    onChange={(e) => setMusicSettings({...musicSettings, instruments: (e.target as HTMLSelectElement).value})}
                    options={[
                      { value: 'african-drums', label: 'African Drums' },
                      { value: 'guitar', label: 'Guitar' },
                      { value: 'piano', label: 'Piano' },
                      { value: 'traditional', label: 'Traditional Instruments' },
                      { value: 'modern', label: 'Modern Instruments' }
                    ]}
                  />
                </div>
              </div>

              <div className="flex justify-end mt-6">
                <button
                  onClick={handleMusicGeneration}
                  className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200"
                >
                  Generate Music
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Sound Effects Tab */}
        {activeTab === 'effects' && (
          <div className="text-center py-12">
            <FaWaveSquare className="text-6xl text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-800 mb-2">Sound Effects Studio</h3>
            <p className="text-gray-600 mb-4">
              Create custom sound effects for your Kenya-first content
            </p>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 max-w-md mx-auto">
              <p className="text-blue-800 text-sm">
                <strong>Coming Soon:</strong> Advanced sound effects generation including 
                nature sounds, urban environments, and cultural audio elements.
              </p>
            </div>
          </div>
        )}
      </Card>

      {/* Recent Projects */}
      <Card className="p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Recent Audio Projects</h2>
        {projects.length === 0 ? (
          <div className="text-center py-8">
            <FaMusic className="text-4xl text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 font-medium mb-2">No audio projects yet</p>
            <p className="text-sm text-gray-500">
              Start creating voice narrations and music to see your projects here.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {projects.map((project) => (
              <div key={project.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="bg-green-100 p-2 rounded-lg">
                    {project.type === 'voice' ? <FaMicrophone className="text-green-600" /> : <FaMusic className="text-green-600" />}
                  </div>
                  <div>
                    <p className="font-medium text-gray-800">{project.name}</p>
                    <p className="text-sm text-gray-500">{project.duration} • {project.createdAt}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    project.status === 'completed' ? 'bg-green-100 text-green-800' :
                    project.status === 'processing' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {project.status}
                  </span>
                  <button className="p-2 text-gray-600 hover:text-green-600 transition-colors duration-200">
                    <FaPlay className="text-sm" />
                  </button>
                  <button className="p-2 text-gray-600 hover:text-blue-600 transition-colors duration-200">
                    <FaDownload className="text-sm" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>

      {/* Cultural Footer */}
      <div className="bg-gradient-to-r from-yellow-400 via-red-500 to-green-600 p-4 rounded-lg text-white text-center">
        <div className="flex items-center justify-center space-x-2">
          <FaFlag className="text-lg" />
          <span className="font-medium">Preserving Kenyan voices and musical heritage through AI</span>
          <FaVolumeUp className="text-lg" />
        </div>
      </div>
    </div>
  );
}

