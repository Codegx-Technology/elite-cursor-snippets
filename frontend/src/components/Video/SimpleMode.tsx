
import React, { useState } from 'react';
import { FaArrowRight, FaArrowLeft, FaVideo, FaMusic, FaFlag, FaMountain, FaPlay, FaSpinner } from 'react-icons/fa6';
import { useVideoGenerator } from '@/hooks/useVideoGenerator';
import PromptSuggester from '@/components/Video/PromptSuggester';
import Card from '@/components/Card'; // Import Card component

export default function SimpleMode() {
  const { formData, handleInputChange, handleGenerateVideo, progress } = useVideoGenerator();
  const [step, setStep] = useState(1);

  const nextStep = () => setStep(step + 1);
  const prevStep = () => setStep(step - 1);

  // Define simplified options for Simple Mode
  const culturalPresets = [
    { value: 'modern-kenya', label: '🏙️ Modern Kenya' },
    { value: 'wildlife-safari', label: '🦁 Wildlife Safari' },
    { value: 'mount-kenya', label: '🏔️ Mount Kenya' },
  ];

  const visualStyles = [
    { value: 'cinematic-documentary', label: '🎬 Cinematic' },
    { value: 'vibrant-colorful', label: '🌈 Vibrant' },
    { value: 'animated-cartoon', label: '🎭 Cartoon' },
  ];

  const musicStyles = [
    { value: 'afrobeat', label: '🥁 Afrobeat' },
    { value: 'traditional-kenyan', label: '🎵 Traditional' },
    { value: 'no-music', label: '🔇 No Music' },
  ];

  const getOptionLabel = (options: { value: string; label: string }[], value: string) => {
    return options.find(option => option.value === value)?.label || value;
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-center mb-6">
        <div className="flex items-center space-x-4">
          {[1, 2, 3].map((stepNum) => (
            <React.Fragment key={stepNum}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center font-semibold ${
                step >= stepNum ? 'bg-gradient-to-r from-green-600 to-blue-600 text-white' : 'bg-gray-200 text-gray-600'
              }`}>
                {stepNum}
              </div>
              {stepNum < 3 && <div className={`w-12 h-1 ${step > stepNum ? 'bg-gradient-to-r from-green-600 to-blue-600' : 'bg-gray-200'}`}></div>}
            </React.Fragment>
          ))}
        </div>
      </div>

      {step === 1 && (
        <Card className="p-6">
          <h3 className="section-subtitle mb-4 text-charcoal">Step 1: Provide Your Script</h3>
          <PromptSuggester
            value={formData.script}
            onChange={(value) => handleInputChange('script', value)}
            placeholder="Enter your video script here... e.g., 'A vibrant journey through Nairobi's tech scene, showcasing innovation and culture.'"
          />
          <div className="flex justify-end mt-4">
            <button type="button" className="btn-primary px-6 py-2 rounded-lg" onClick={nextStep} disabled={!formData.script.trim()}>
              Next <FaArrowRight className="inline ml-2" />
            </button>
          </div>
        </Card>
      )}

      {step === 2 && (
        <Card className="p-6">
          <h3 className="section-subtitle mb-4 text-charcoal">Step 2: Choose Your Style</h3>
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-charcoal mb-2">🇰🇪 Cultural Preset</label>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {culturalPresets.map((option) => (
                  <button
                    key={option.value}
                    className={`p-3 border rounded-lg text-center transition-all duration-200 ${
                      formData.culturalPreset === option.value
                        ? 'border-green-500 bg-green-50 text-green-800 shadow-md'
                        : 'border-gray-300 bg-white text-gray-700 hover:border-green-400'
                    }`}
                    onClick={() => handleInputChange('culturalPreset', option.value)}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-charcoal mb-2">🎨 Visual Style</label>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {visualStyles.map((option) => (
                  <button
                    key={option.value}
                    className={`p-3 border rounded-lg text-center transition-all duration-200 ${
                      formData.visualStyle === option.value
                        ? 'border-blue-500 bg-blue-50 text-blue-800 shadow-md'
                        : 'border-gray-300 bg-white text-gray-700 hover:border-blue-400'
                    }`}
                    onClick={() => handleInputChange('visualStyle', option.value)}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-charcoal mb-2">🎵 Background Music</label>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {musicStyles.map((option) => (
                  <button
                    key={option.value}
                    className={`p-3 border rounded-lg text-center transition-all duration-200 ${
                      formData.musicStyle === option.value
                        ? 'border-purple-500 bg-purple-50 text-purple-800 shadow-md'
                        : 'border-gray-300 bg-white text-gray-700 hover:border-purple-400'
                    }`}
                    onClick={() => handleInputChange('musicStyle', option.value)}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="flex justify-between mt-6">
            <button type="button" className="btn-secondary px-6 py-2 rounded-lg" onClick={prevStep}>
              <FaArrowLeft className="inline mr-2" /> Back
            </button>
            <button type="button" className="btn-primary px-6 py-2 rounded-lg" onClick={nextStep}>
              Next <FaArrowRight className="inline ml-2" />
            </button>
          </div>
        </Card>
      )}

      {step === 3 && (
        <Card className="p-6">
          <h3 className="section-subtitle mb-4 text-charcoal">Step 3: Review & Generate</h3>
          <div className="space-y-4 mb-6 text-charcoal">
            <div>
              <p className="font-medium">Your Script:</p>
              <p className="text-sm text-gray-700 italic bg-gray-50 p-3 rounded-md">{formData.script || 'No script provided.'}</p>
            </div>
            <div>
              <p className="font-medium">Selected Style:</p>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>🇰🇪 Preset: {getOptionLabel(culturalPresets, formData.culturalPreset)}</li>
                <li>🎨 Visual: {getOptionLabel(visualStyles, formData.visualStyle)}</li>
                <li>🎵 Music: {getOptionLabel(musicStyles, formData.musicStyle)}</li>
              </ul>
            </div>
          </div>

          {progress.isGenerating && (
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
          )}

          <div className="flex justify-between mt-4">
            <button type="button" className="btn-secondary px-6 py-2 rounded-lg" onClick={prevStep}>
              <FaArrowLeft className="inline mr-2" /> Back
            </button>
            <button
              type="button"
              className="btn-primary px-6 py-2 rounded-lg flex items-center justify-center"
              onClick={handleGenerateVideo}
              disabled={progress.isGenerating || !formData.script.trim()}
            >
              {progress.isGenerating ? (
                <>
                  <FaSpinner className="animate-spin mr-2" /> Generating...
                </>
              ) : (
                <>
                  <FaPlay className="inline mr-2" /> Generate Video
                </>
              )}
            </button>
          </div>
        </Card>
      )}
    </div>
  );
}

