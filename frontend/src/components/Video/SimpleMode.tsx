
import { useState } from 'react';
import { FaArrowRight, FaArrowLeft } from 'react-icons/fa';
import { useVideoGenerator } from '@/hooks/useVideoGenerator';
import PromptSuggester from '@/components/Prompting/PromptSuggester';

export default function SimpleMode() {
  const { formData, handleInputChange, handleGenerateVideo, progress } = useVideoGenerator();
  const [step, setStep] = useState(1);

  const nextStep = () => setStep(step + 1);
  const prevStep = () => setStep(step - 1);

  return (
    <div>
      <div className="flex items-center justify-center mb-6">
        <div className="flex items-center space-x-4">
          {[1, 2, 3].map((stepNum) => (
            <div key={stepNum}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center font-semibold ${
                step >= stepNum ? 'bg-primary-gradient text-white' : 'bg-gray-200 text-gray-600'
              }`}>
                {stepNum}
              </div>
              {stepNum < 3 && <div className={`w-12 h-1 ${step > stepNum ? 'bg-primary-gradient' : 'bg-gray-200'}`}></div>}
            </div>
          ))}
        </div>
      </div>

      {step === 1 && (
        <div>
          <h3 className="section-subtitle mb-4">Step 1: Provide Content</h3>
          <PromptSuggester
            value={formData.script}
            onChange={(value) => handleInputChange('script', value)}
            placeholder="Enter your video script here..."
          />
          <div className="flex justify-end mt-4">
            <button type="button" className="btn-primary px-6 py-2 rounded-lg" onClick={nextStep}>
              Next <FaArrowRight className="inline ml-2" />
            </button>
          </div>
        </div>
      )}

      {step === 2 && (
        <div>
          <h3 className="section-subtitle mb-4">Step 2: Choose Style</h3>
          {/* Add style selection here */}
          <div className="flex justify-between mt-4">
            <button type="button" className="btn-secondary px-6 py-2 rounded-lg" onClick={prevStep}>
              <FaArrowLeft className="inline mr-2" /> Back
            </button>
            <button type="button" className="btn-primary px-6 py-2 rounded-lg" onClick={nextStep}>
              Next <FaArrowRight className="inline ml-2" />
            </button>
          </div>
        </div>
      )}

      {step === 3 && (
        <div>
          <h3 className="section-subtitle mb-4">Step 3: Review & Generate</h3>
          {/* Add review and generate button here */}
          <div className="flex justify-between mt-4">
            <button type="button" className="btn-secondary px-6 py-2 rounded-lg" onClick={prevStep}>
              <FaArrowLeft className="inline mr-2" /> Back
            </button>
            <button
              type="button"
              className="btn-primary px-6 py-2 rounded-lg flex items-center justify-center"
              onClick={handleGenerateVideo}
              disabled={progress.isGenerating}
            >
              {progress.isGenerating ? 'Generating...' : 'Generate Video'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
