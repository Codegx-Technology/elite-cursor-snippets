'use client';

import { useState, useEffect } from 'react';
import Card from '@/components/Card';
import FormInput from '@/components/FormInput';
import FormSelect from '@/components/FormSelect';
import { FaVideo, FaPlay, FaStop, FaDownload, FaEye, FaFlag, FaMountain, FaGlobe, FaMusic, FaImage, FaMicrophone, FaExclamationTriangle } from 'react-icons/fa';
import { apiClient, handleApiResponse } from '@/lib/api';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Enterprise-grade video generation interface with Kenya-first cultural elements
// [GOAL]: Create comprehensive video generation UI with real-time feedback and cultural authenticity
// [TASK]: Implement advanced video generation form with live preview, cultural presets, and progress tracking

interface VideoGenerationForm {
  script: string;
  voice: string;
  visualStyle: string;
  duration: string;
  culturalPreset: string;
  language: string;
  musicStyle: string;
  removeWatermark: boolean;
  enableSubtitles: boolean;
  exportFormat: string;
}

interface GenerationProgress {
  stage: string;
  progress: number;
  message: string;
  isGenerating: boolean;
}

export default function VideoGeneratePage() {
  const [formData, setFormData] = useState<VideoGenerationForm>({
    script: '',
    voice: '',
    visualStyle: '',
    duration: '30',
    culturalPreset: 'modern-kenya',
    language: 'english-swahili',
    musicStyle: 'afrobeat',
    removeWatermark: true,
    enableSubtitles: true,
    exportFormat: 'mp4'
  });

  const [progress, setProgress] = useState<GenerationProgress>({
    stage: 'Ready',
    progress: 0,
    message: 'Ready to create your Kenya-first video',
    isGenerating: false
  });

  const [generatedVideo, setGeneratedVideo] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [currentJobId, setCurrentJobId] = useState<string | null>(null);
  const [friendlyFallback, setFriendlyFallback] = useState<{
    message: string;
    retryOptions: string[];
    spinnerType: string;
  } | null>(null);

  // [SNIPPET]: kenyafirst + thinkwithai
  // [TASK]: Define Kenya-first options and cultural presets
  const voiceOptions = [
    { value: 'kenyan-male-professional', label: '🇰🇪 Kenyan Male (Professional)' },
    { value: 'kenyan-female-warm', label: '🇰🇪 Kenyan Female (Warm)' },
    { value: 'kenyan-sheng-youth', label: '🎤 Kenyan Sheng (Youth)' },
    { value: 'swahili-coastal', label: '🌊 Swahili Coastal' },
    { value: 'kikuyu-traditional', label: '🏔️ Kikuyu Traditional' },
    { value: 'luo-storyteller', label: '📚 Luo Storyteller' }
  ];

  const culturalPresets = [
    { value: 'modern-kenya', label: '🏙️ Modern Kenya (Nairobi Tech Hub)' },
    { value: 'traditional-heritage', label: '🏺 Traditional Heritage' },
    { value: 'coastal-beauty', label: '🏖️ Coastal Beauty (Diani & Malindi)' },
    { value: 'wildlife-safari', label: '🦁 Wildlife Safari (Maasai Mara)' },
    { value: 'mount-kenya', label: '🏔️ Mount Kenya Majesty' },
    { value: 'cultural-fusion', label: '🎭 Cultural Fusion' },
    { value: 'innovation-story', label: '💡 Innovation Story' }
  ];

  const visualStyles = [
    { value: 'cinematic-documentary', label: '🎬 Cinematic Documentary' },
    { value: 'vibrant-colorful', label: '🌈 Vibrant & Colorful' },
    { value: 'professional-corporate', label: '💼 Professional Corporate' },
    { value: 'artistic-creative', label: '🎨 Artistic & Creative' },
    { value: 'authentic-realistic', label: '📸 Authentic & Realistic' },
    { value: 'animated-cartoon', label: '🎭 Animated Cartoon' }
  ];

  const durationOptions = [
    { value: '15', label: '15 seconds (TikTok/Instagram)' },
    { value: '30', label: '30 seconds (Social Media)' },
    { value: '60', label: '1 minute (YouTube Shorts)' },
    { value: '120', label: '2 minutes (Detailed Story)' },
    { value: '300', label: '5 minutes (Full Documentary)' }
  ];

  const languageOptions = [
    { value: 'english-swahili', label: '🇰🇪 English + Swahili Mix' },
    { value: 'pure-swahili', label: '🗣️ Pure Swahili' },
    { value: 'english-primary', label: '🇬🇧 English Primary' },
    { value: 'sheng-modern', label: '🎤 Modern Sheng' },
    { value: 'multilingual', label: '🌍 Multilingual (EN/SW/Local)' }
  ];

  const musicStyles = [
    { value: 'afrobeat', label: '🥁 Afrobeat' },
    { value: 'traditional-kenyan', label: '🎵 Traditional Kenyan' },
    { value: 'modern-fusion', label: '🎶 Modern Fusion' },
    { value: 'ambient-nature', label: '🌿 Ambient Nature' },
    { value: 'upbeat-celebration', label: '🎉 Upbeat Celebration' },
    { value: 'no-music', label: '🔇 No Background Music' }
  ];

  // [SNIPPET]: surgicalfix + thinkwithai
  // [TASK]: Handle form input changes with type safety
  const handleInputChange = (field: keyof VideoGenerationForm, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // [SNIPPET]: refactorclean + kenyafirst + augmentsearch
  // [TASK]: Real video generation with Kenya-first progress messages and API integration
  const handleGenerateVideo = async () => {
    if (!formData.script.trim()) {
      alert('Please enter a video script to continue.');
      return;
    }

    setError(null);
    setProgress({
      stage: 'Starting',
      progress: 5,
      message: 'Initializing Kenya-first video generation...',
      isGenerating: true
    });

    try {
      // Call real API
      const response = await apiClient.generateVideo({
        prompt: formData.script,
        lang: formData.language.includes('swahili') ? 'sw' : 'en',
        scenes: 3,
        vertical: formData.duration === '15' || formData.duration === '30',
        style: formData.visualStyle,
        duration: parseInt(formData.duration),
        voice_type: formData.voice.includes('female') ? 'female' : 'male',
        background_music: true,
        cultural_preset: formData.culturalPreset
      });

      handleApiResponse(
        response,
        (data) => {
          setCurrentJobId(data.video_id);
          setProgress({
            stage: 'Processing',
            progress: 20,
            message: 'Video generation started successfully...',
            isGenerating: true
          });
          // Start polling for job status
          pollJobStatus(data.video_id);
        },
        (error) => {
          setError(error);
          setProgress({
            stage: 'Error',
            progress: 0,
            message: 'Failed to start video generation',
            isGenerating: false
          });
        }
      );
    } catch (err) {
      setError('Failed to start video generation');
      setProgress({
        stage: 'Error',
        progress: 0,
        message: 'Network error occurred',
        isGenerating: false
      });
    }
  };

  const pollJobStatus = async (jobId: string) => {
    const maxAttempts = 60; // 5 minutes max
    let attempts = 0;

    const stages = [
      { stage: 'Script Analysis', progress: 30, message: 'Understanding your Kenya-first narrative...' },
      { stage: 'Generating Visuals', progress: 50, message: 'Creating authentic African imagery...' },
      { stage: 'Adding Voice', progress: 70, message: 'Recording Kenyan voice narration...' },
      { stage: 'Cultural Enhancement', progress: 85, message: 'Infusing cultural elements and music...' },
      { stage: 'Final Processing', progress: 95, message: 'Polishing your masterpiece...' }
    ];

    const poll = async () => {
      try {
        const response = await apiClient.getGenerationJob(jobId);
        handleApiResponse(
          response,
          (job) => {
            if (job.status === 'completed') {
              setProgress({
                stage: 'Complete',
                progress: 100,
                message: 'Your Kenya-first video is ready! 🇰🇪',
                isGenerating: false
              });
              setGeneratedVideo(job.result_url || `kenya_video_${Date.now()}.mp4`);
              setCurrentJobId(null);
            } else if (job.status === 'friendly_fallback') {
              setProgress({
                stage: 'Friendly Fallback',
                progress: 0,
                message: job.friendly_message || 'Service temporarily unavailable',
                isGenerating: false
              });
              setError(null); // Clear error since this is a friendly fallback
              setCurrentJobId(null);

              // Show Kenya-first friendly message
              setFriendlyFallback({
                message: job.friendly_message,
                retryOptions: job.retry_options || [],
                spinnerType: job.spinner_type || 'kenya_flag'
              });
            } else if (job.status === 'failed') {
              setProgress({
                stage: 'Error',
                progress: 0,
                message: 'Video generation failed',
                isGenerating: false
              });
              setError(job.error_message || 'Video generation failed');
              setCurrentJobId(null);
            } else {
              // Still processing, update progress with cultural messages
              const stageIndex = Math.min(Math.floor(job.progress / 20), stages.length - 1);
              const currentStage = stages[stageIndex] || stages[0];

              setProgress({
                stage: currentStage.stage,
                progress: job.progress || currentStage.progress,
                message: currentStage.message,
                isGenerating: true
              });

              // Continue polling
              attempts++;
              if (attempts < maxAttempts) {
                setTimeout(poll, 5000); // Poll every 5 seconds
              } else {
                setProgress({
                  stage: 'Timeout',
                  progress: 0,
                  message: 'Video generation timed out',
                  isGenerating: false
                });
                setError('Video generation timed out. Please try again.');
                setCurrentJobId(null);
              }
            }
          },
          (error) => {
            setProgress({
              stage: 'Error',
              progress: 0,
              message: 'Failed to check generation status',
              isGenerating: false
            });
            setError(error);
            setCurrentJobId(null);
          }
        );
      } catch (err) {
        setProgress({
          stage: 'Error',
          progress: 0,
          message: 'Network error during generation',
          isGenerating: false
        });
        setError('Network error during generation');
        setCurrentJobId(null);
      }
    };

    poll();
  };

  const handleStopGeneration = () => {
    setProgress({
      stage: 'Stopped',
      progress: 0,
      message: 'Generation stopped by user',
      isGenerating: false
    });
  };

  return (
    <div className="space-y-6">
      {/* Kenya-First Header */}
      <div className="bg-gradient-to-r from-green-600 via-red-600 to-black p-6 rounded-xl text-white">
        <div className="flex items-center space-x-4">
          <FaVideo className="text-3xl" />
          <div>
            <h1 className="text-2xl font-bold">Generate Kenya-First Video 🎬</h1>
            <p className="text-green-100">Create authentic African stories with AI-powered video generation</p>
          </div>
          <div className="ml-auto flex space-x-2">
            <FaFlag className="text-2xl text-yellow-300" />
            <FaMountain className="text-2xl text-white" />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Video Generation Form */}
        <Card className="p-6">
          <h2 className="section-title mb-4">Video Configuration</h2>

          <div className="space-y-6">
            {/* Script Input */}
            <div>
              <label className="block text-sm font-medium text-charcoal-text mb-2">
                <FaMicrophone className="inline mr-2" />
                Video Script *
              </label>
              <textarea
                className="form-input w-full h-32 resize-none"
                placeholder="Enter your video script here...
Example: 'Welcome to Kenya, the heart of East Africa. From the snow-capped peaks of Mount Kenya to the pristine beaches of Diani, our country offers breathtaking diversity...'"
                value={formData.script}
                onChange={(e) => handleInputChange('script', e.target.value)}
              />
              <p className="text-xs text-soft-text mt-1">
                Tip: Include Swahili phrases for authentic cultural touch
              </p>
            </div>

            {/* Cultural Preset */}
            <FormSelect
              label="🇰🇪 Cultural Preset"
              options={culturalPresets}
              id="culturalPreset"
              name="culturalPreset"
              value={formData.culturalPreset}
              onChange={(e) => handleInputChange('culturalPreset', e.target.value)}
            />

            {/* Voice Selection */}
            <FormSelect
              label="🎤 Voice & Narration"
              options={voiceOptions}
              id="voice"
              name="voice"
              value={formData.voice}
              onChange={(e) => handleInputChange('voice', e.target.value)}
            />

            {/* Language Mix */}
            <FormSelect
              label="🗣️ Language Style"
              options={languageOptions}
              id="language"
              name="language"
              value={formData.language}
              onChange={(e) => handleInputChange('language', e.target.value)}
            />

            {/* Visual Style */}
            <FormSelect
              label="🎨 Visual Style"
              options={visualStyles}
              id="visualStyle"
              name="visualStyle"
              value={formData.visualStyle}
              onChange={(e) => handleInputChange('visualStyle', e.target.value)}
            />

            {/* Duration */}
            <FormSelect
              label="⏱️ Video Duration"
              options={durationOptions}
              id="duration"
              name="duration"
              value={formData.duration}
              onChange={(e) => handleInputChange('duration', e.target.value)}
            />

            {/* Music Style */}
            <FormSelect
              label="🎵 Background Music"
              options={musicStyles}
              id="musicStyle"
              name="musicStyle"
              value={formData.musicStyle}
              onChange={(e) => handleInputChange('musicStyle', e.target.value)}
            />

            {/* Advanced Options */}
            <div className="bg-gray-50 p-4 rounded-lg space-y-4">
              <h3 className="font-medium text-gray-800 mb-3">🔧 Advanced Options</h3>

              {/* Watermark Removal */}
              <div className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  id="removeWatermark"
                  checked={formData.removeWatermark}
                  onChange={(e) => handleInputChange('removeWatermark', e.target.checked)}
                  className="w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
                />
                <label htmlFor="removeWatermark" className="text-sm text-gray-700">
                  🚫 Remove watermarks from generated images
                </label>
              </div>

              {/* Subtitles */}
              <div className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  id="enableSubtitles"
                  checked={formData.enableSubtitles}
                  onChange={(e) => handleInputChange('enableSubtitles', e.target.checked)}
                  className="w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
                />
                <label htmlFor="enableSubtitles" className="text-sm text-gray-700">
                  📝 Generate subtitles (English & Swahili)
                </label>
              </div>

              {/* Export Format */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  📱 Export Format
                </label>
                <select
                  value={formData.exportFormat}
                  onChange={(e) => handleInputChange('exportFormat', e.target.value)}
                  className="form-input w-full"
                >
                  <option value="mp4">MP4 (Universal)</option>
                  <option value="tiktok">TikTok Optimized (9:16)</option>
                  <option value="instagram">Instagram Stories (9:16)</option>
                  <option value="whatsapp">WhatsApp Friendly (16:9)</option>
                  <option value="youtube">YouTube Shorts (9:16)</option>
                </select>
              </div>
            </div>

            {/* Error Display */}
            {error && (
              <div className="bg-red-50 border border-red-200 p-4 rounded-lg mb-4">
                <div className="flex items-center space-x-2">
                  <FaExclamationTriangle className="text-red-600" />
                  <p className="text-red-800 font-medium">Generation Error</p>
                </div>
                <p className="text-red-700 text-sm mt-1">{error}</p>
                <button
                  onClick={() => setError(null)}
                  className="text-red-600 hover:text-red-800 text-sm mt-2 underline"
                >
                  Dismiss
                </button>
              </div>
            )}

            {/* Generation Controls */}
            <div className="flex space-x-4 pt-4">
              {!progress.isGenerating ? (
                <button
                  onClick={handleGenerateVideo}
                  className="btn-primary flex items-center space-x-2 flex-1"
                  disabled={!formData.script.trim()}
                >
                  <FaPlay />
                  <span>Generate Kenya-First Video</span>
                </button>
              ) : (
                <button
                  onClick={handleStopGeneration}
                  className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg flex items-center space-x-2 flex-1"
                >
                  <FaStop />
                  <span>Stop Generation</span>
                </button>
              )}

              <button className="btn-elite flex items-center space-x-2">
                <FaEye />
                <span>Preview</span>
              </button>
            </div>
          </div>
        </Card>

        {/* Progress and Preview */}
        <Card className="p-6">
          <h2 className="section-title mb-4">Generation Progress</h2>

          {/* Progress Bar */}
          <div className="mb-6">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-charcoal-text">{progress.stage}</span>
              <span className="text-sm text-soft-text">{progress.progress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className="bg-gradient-to-r from-green-600 to-blue-600 h-3 rounded-full transition-all duration-500 ease-out"
                style={{ width: `${progress.progress}%` }}
              ></div>
            </div>
            <p className="text-sm text-soft-text mt-2">{progress.message}</p>
          </div>

          {/* Live Status */}
          <div className="space-y-4">
            <div className="bg-gray-50 p-4 rounded-lg">
              <h3 className="font-medium text-charcoal-text mb-2">Current Configuration</h3>
              <div className="text-sm space-y-1">
                <p><span className="text-soft-text">Preset:</span> {culturalPresets.find(p => p.value === formData.culturalPreset)?.label}</p>
                <p><span className="text-soft-text">Duration:</span> {formData.duration} seconds</p>
                <p><span className="text-soft-text">Language:</span> {languageOptions.find(l => l.value === formData.language)?.label}</p>
                <p><span className="text-soft-text">Music:</span> {musicStyles.find(m => m.value === formData.musicStyle)?.label}</p>
              </div>
            </div>

            {/* Kenya-First Friendly Fallback */}
            {friendlyFallback && (
              <div className="bg-gradient-to-r from-green-50 via-red-50 to-yellow-50 border-2 border-green-200 p-6 rounded-lg">
                <div className="text-center">
                  {/* Kenya Flag Spinner */}
                  <div className="mb-4">
                    <div className="w-16 h-16 mx-auto relative">
                      <div className="absolute inset-0 rounded-full border-4 border-green-600 border-t-red-600 border-r-black animate-spin"></div>
                      <div className="absolute inset-2 flex items-center justify-center">
                        <span className="text-2xl">🇰🇪</span>
                      </div>
                    </div>
                  </div>

                  {/* Friendly Message */}
                  <h3 className="font-bold text-lg text-gray-800 mb-2">
                    {friendlyFallback.message}
                  </h3>

                  <p className="text-gray-600 mb-4">
                    Harambee! We're working hard to bring you amazing content.
                  </p>

                  {/* Retry Options */}
                  <div className="space-y-2">
                    {friendlyFallback.retryOptions.map((option, index) => (
                      <button
                        key={index}
                        onClick={() => {
                          if (option.includes('Try again')) {
                            setFriendlyFallback(null);
                            handleGenerateVideo();
                          } else if (option.includes('Browse')) {
                            // Navigate to gallery
                            window.location.href = '/gallery';
                          }
                        }}
                        className="block w-full bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-200"
                      >
                        {option}
                      </button>
                    ))}
                  </div>

                  <button
                    onClick={() => setFriendlyFallback(null)}
                    className="mt-4 text-gray-500 hover:text-gray-700 text-sm underline"
                  >
                    Dismiss
                  </button>
                </div>
              </div>
            )}

            {/* Generated Video Preview */}
            {generatedVideo && (
              <div className="bg-green-50 border border-green-200 p-4 rounded-lg">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-medium text-green-800">Video Generated Successfully! 🎉</h3>
                  <FaVideo className="text-green-600" />
                </div>
                <p className="text-sm text-green-700 mb-3">
                  Your Kenya-first video "{generatedVideo}" is ready for download.
                </p>
                <div className="flex space-x-2">
                  <button className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded text-sm flex items-center space-x-1">
                    <FaDownload />
                    <span>Download</span>
                  </button>
                  <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm flex items-center space-x-1">
                    <FaPlay />
                    <span>Preview</span>
                  </button>
                </div>
              </div>
            )}

            {/* Cultural Tips */}
            <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
              <h3 className="font-medium text-yellow-800 mb-2">🇰🇪 Cultural Tips</h3>
              <ul className="text-sm text-yellow-700 space-y-1">
                <li>• Use "Karibu" (Welcome) for greetings</li>
                <li>• Include "Harambee" spirit for community themes</li>
                <li>• Reference local landmarks like Mount Kenya, Maasai Mara</li>
                <li>• Mix English and Swahili naturally</li>
              </ul>
            </div>
          </div>
        </Card>
      </div>

      {/* Recent Generations */}
      <Card className="p-6">
        <h2 className="section-title mb-4">Recent Kenya-First Videos</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            { title: 'Mount Kenya Adventure', duration: '30s', status: 'completed', thumbnail: '🏔️' },
            { title: 'Nairobi Tech Innovation', duration: '60s', status: 'completed', thumbnail: '💻' },
            { title: 'Coastal Beauty Story', duration: '45s', status: 'processing', thumbnail: '🏖️' }
          ].map((video, index) => (
            <div key={index} className="bg-gray-50 p-4 rounded-lg hover:bg-gray-100 transition-colors">
              <div className="text-3xl mb-2">{video.thumbnail}</div>
              <h3 className="font-medium text-charcoal-text">{video.title}</h3>
              <p className="text-sm text-soft-text">{video.duration}</p>
              <span className={`inline-block mt-2 px-2 py-1 rounded-full text-xs ${
                video.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
              }`}>
                {video.status}
              </span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
