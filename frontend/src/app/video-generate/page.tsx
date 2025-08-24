'use client';

import { useState } from 'react';
import Card from '@/components/Card';
import FormSelect from '@/components/FormSelect';
import { FaVideo, FaPlay, FaStop, FaDownload, FaEye, FaFlag, FaMountain, FaMicrophone, FaExclamationTriangle } from 'react-icons/fa';
import { useVideoGenerator } from '@/hooks/useVideoGenerator';
import PromptSuggester from '@/components/Video/PromptSuggester';
import SimpleMode from '@/components/Video/SimpleMode';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Enterprise-grade video generation interface with Kenya-first cultural elements
// [GOAL]: Create comprehensive video generation UI with real-time feedback and cultural authenticity
// [TASK]: Implement advanced video generation form with live preview, cultural presets, and progress tracking

export default function VideoGeneratePage() {
  const {
    formData,
    progress,
    generatedVideo,
    error,
    setError,
    friendlyFallback,
    scriptError,
    handleInputChange,
    handleGenerateVideo,
    handleStopGeneration,
    setFriendlyFallback
  } = useVideoGenerator();

  const [isSimpleMode, setIsSimpleMode] = useState(false);

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

  return (
    <div className="space-y-6">
      {/* Kenya-First Header */}
      <div className="bg-gradient-to-r from-green-600 via-red-600 to-black p-6 rounded-xl text-white">
        <div className="flex items-center space-x-4">
          <FaVideo className="text-3xl" aria-label="Video Icon" />
          <div>
            <h1 className="text-2xl font-bold">Generate Kenya-First Video 🎬</h1>
            <p className="text-green-100">Create authentic African stories with AI-powered video generation</p>
          </div>
          <div className="ml-auto flex items-center space-x-2">
            <div className="flex items-center space-x-2">
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  aria-label="Simple Mode"
                  checked={isSimpleMode}
                  onChange={() => setIsSimpleMode(!isSimpleMode)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                <span className="text-sm">Simple Mode</span>
              </label>
            </div>
            <FaFlag className="text-2xl text-yellow-300" aria-label="Kenyan Flag" />
            <FaMountain className="text-2xl text-white" aria-label="Mount Kenya" />
          </div>
        </div>
      </div>

      {isSimpleMode ? (
        <SimpleMode />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Video Generation Form */}
          <Card className="p-6">
            <h2 className="section-title mb-4 text-charcoal">Video Configuration</h2>

            <div className="space-y-6">
              {/* Script Input */}
              <div>
                <label htmlFor="videoScript" className="block text-sm font-medium text-charcoal mb-2">
                  <FaMicrophone className="inline mr-2" aria-label="Microphone Icon" />
                  Video Script *
                </label>
                <PromptSuggester
                  id="videoScript"
                  value={formData.script}
                  onChange={(value) => handleInputChange('script', value)}
                  placeholder="Enter your video script here...\nExample: 'Welcome to Kenya, the heart of East Africa. From the snow-capped peaks of Mount Kenya to the pristine beaches of Diani, our country offers breathtaking diversity...'"
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
                className="text-white bg-neutral-800 border-gray-600 focus:border-green-500 focus:ring-green-200"
                labelClassName="text-charcoal"
              />

              {/* Voice Selection */}
              <FormSelect
                label="🎤 Voice & Narration"
                options={voiceOptions}
                id="voice"
                name="voice"
                value={formData.voice}
                onChange={(e) => handleInputChange('voice', e.target.value)}
                className="text-white bg-neutral-800 border-gray-600 focus:border-green-500 focus:ring-green-200"
                labelClassName="text-charcoal"
              />

              {/* Language Mix */}
              <FormSelect
                label="🗣️ Language Style"
                options={languageOptions}
                id="language"
                name="language"
                value={formData.language}
                onChange={(e) => handleInputChange('language', e.target.value)}
                className="text-white bg-neutral-800 border-gray-600 focus:border-green-500 focus:ring-green-200"
                labelClassName="text-charcoal"
              />

              {/* Visual Style */}
              <FormSelect
                label="🎨 Visual Style"
                options={visualStyles}
                id="visualStyle"
                name="visualStyle"
                value={formData.visualStyle}
                onChange={(e) => handleInputChange('visualStyle', e.target.value)}
                className="text-white bg-neutral-800 border-gray-600 focus:border-green-500 focus:ring-green-200"
                labelClassName="text-charcoal"
              />

              {/* Duration */}
              <FormSelect
                label="⏱️ Video Duration"
                options={durationOptions}
                id="duration"
                name="duration"
                value={formData.duration}
                onChange={(e) => handleInputChange('duration', e.target.value)}
                className="text-white bg-neutral-800 border-gray-600 focus:border-green-500 focus:ring-green-200"
                labelClassName="text-charcoal"
              />

              {/* Music Style */}
              <FormSelect
                label="🎵 Background Music"
                options={musicStyles}
                id="musicStyle"
                name="musicStyle"
                value={formData.musicStyle}
                onChange={(e) => handleInputChange('musicStyle', e.target.value)}
                className="text-white bg-neutral-800 border-gray-600 focus:border-green-500 focus:ring-green-200"
                labelClassName="text-charcoal"
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
                  <label className="block text-sm font-medium text-charcoal mb-2">
                    📱 Export Format
                  </label>
                  <select
                    value={formData.exportFormat}
                    onChange={(e) => handleInputChange('exportFormat', e.target.value)}
                    className="form-input w-full bg-neutral-800 text-white border-gray-600 focus:border-green-500 focus:ring-green-200"
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
                    <FaExclamationTriangle className="text-red-600" aria-label="Error Icon" />
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
                                        disabled={!formData.script.trim() || !!scriptError}
                  >
                    <FaPlay aria-label="Play Icon" />
                    <span>Generate Kenya-First Video</span>
                  </button>
                ) : (
                  <button
                    onClick={handleStopGeneration}
                    className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg flex items-center space-x-2 flex-1"
                  >
                    <FaStop aria-label="Stop Icon" />
                    <span>Stop Generation</span>
                  </button>
                )}

                <button className="btn-elite flex items-center space-x-2">
                  <FaEye aria-label="Preview Icon" />
                  <span>Preview</span>
                </button>
              </div>
            </div>
          </Card>

          {/* Progress and Preview */}
          <Card className="p-6">
            <h2 className="section-title mb-4 text-charcoal">Generation Progress</h2>

            {/* Progress Bar */}
            <div className="mb-6">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-charcoal">{progress.stage}</span>
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
                      Harambee! We&apos;re working hard to bring you amazing content.
                    </p>

                    {/* Retry Options */}
                    {friendlyFallback.retryOptions.length > 0 && (
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
                    )}

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
                    <FaVideo className="text-green-600" aria-label="Video Icon" />
                  </div>
                  <p className="text-sm text-green-700 mb-3">
                    Your Kenya-first video &quot;{generatedVideo}&quot; is ready for download.
                  </p>
                  <div className="flex space-x-2">
                    <button className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded text-sm flex items-center space-x-1">
                      <FaDownload aria-label="Download Icon" />
                      <span>Download</span>
                    </button>
                    <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm flex items-center space-x-1">
                      <FaPlay aria-label="Play Icon" />
                      <span>Preview</span>
                    </button>
                  </div>
                </div>
              )}

              {/* Cultural Tips */}
              <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
                <h3 className="font-medium text-yellow-800 mb-2">🇰🇪 Cultural Tips</h3>
                <ul className="text-sm text-yellow-700 space-y-1">
                  <li>• Use &quot;Karibu&quot; (Welcome) for greetings</li>
                  <li>• Include &quot;Harambee&quot; spirit for community themes</li>
                  <li>• Reference local landmarks like Mount Kenya, Maasai Mara</li>
                  <li>• Mix English and Swahili naturally</li>
                </ul>
              </div>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}