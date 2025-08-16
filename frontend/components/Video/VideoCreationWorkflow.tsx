// frontend/components/Video/VideoCreationWorkflow.tsx (Conceptual)

import React, { useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/router';
import VideoGenerationForm from './VideoGenerationForm'; // Reusing the form component

interface WorkflowStepProps {
  onNext: () => void;
  onBack: () => void;
  // Other props specific to the step
}

// Conceptual Step Components
const Step1ContentInput: React.FC<WorkflowStepProps & { prompt: string, setPrompt: (p: string) => void }> = ({ onNext, prompt, setPrompt }) => (
  <div className="elite-card p-6 mb-4">
    <h3 className="section-subtitle mb-4">Step 1: Provide Content</h3>
    <textarea
      className="form-input w-full p-3 rounded-lg h-32"
      placeholder="Enter your video prompt, or paste a news URL/script..."
      value={prompt}
      onChange={(e) => setPrompt(e.target.value)}
    ></textarea>
    <div className="flex justify-end mt-4">
      <button type="button" className="btn-primary px-6 py-2 rounded-lg" onClick={onNext}>Next</button>
    </div>
  </div>
);

const Step2DialectStyle: React.FC<WorkflowStepProps & { dialect: string, setDialect: (d: string) => void, style: string, setStyle: (s: string) => void }> = ({ onNext, onBack, dialect, setDialect, style, setStyle }) => (
  <div className="elite-card p-6 mb-4">
    <h3 className="section-subtitle mb-4">Step 2: Choose Dialect & Style</h3>
    <div className="mb-4">
      <label htmlFor="dialect-select" className="block text-soft-text text-sm font-medium mb-2">Dialect</label>
      <select id="dialect-select" className="form-input w-full p-3 rounded-lg" value={dialect} onChange={(e) => setDialect(e.target.value)}>
        <option value="english">English</option>
        <option value="yoruba">Yoruba</option>
        <option value="swahili">Swahili</option>
        {/* ... other dialects */}
      </select>
    </div>
    <div className="mb-4">
      <label htmlFor="style-select" className="block text-soft-text text-sm font-medium mb-2">Video Style</label>
      <select id="style-select" className="form-input w-full p-3 rounded-lg" value={style} onChange={(e) => setStyle(e.target.value)}>
        <option value="cinematic">Cinematic</option>
        <option value="cartoon">Cartoon</option>
        {/* ... other styles */}
      </select>
    </div>
    <div className="flex justify-between mt-4">
      <button type="button" className="btn-secondary px-6 py-2 rounded-lg" onClick={onBack}>Back</button>
      <button type="button" className="btn-primary px-6 py-2 rounded-lg" onClick={onNext}>Next</button>
    </div>
  </div>
);

const Step3ReviewConfirm: React.FC<WorkflowStepProps & { prompt: string, dialect: string, style: string, onSubmit: () => void, isLoading: boolean }> = ({ onNext, onBack, prompt, dialect, style, onSubmit, isLoading }) => (
  <div className="elite-card p-6 mb-4">
    <h3 className="section-subtitle mb-4">Step 3: Review & Generate</h3>
    <p className="text-soft-text mb-2">Prompt: <span className="font-medium text-charcoal">{prompt}</span></p>
    <p className="text-soft-text mb-2">Dialect: <span className="font-medium text-charcoal">{dialect}</span></p>
    <p className="text-soft-text mb-4">Style: <span className="font-medium text-charcoal">{style}</span></p>
    <div className="flex justify-between mt-4">
      <button type="button" className="btn-secondary px-6 py-2 rounded-lg" onClick={onBack}>Back</button>
      <button
        type="button"
        className="btn-primary px-6 py-2 rounded-lg flex items-center justify-center"
        onClick={onSubmit}
        disabled={isLoading}
      >
        {isLoading ? <div className="loading-spinner mr-2"></div> : 'Generate Video'}
      </button>
    </div>
  </div>
);

const VideoCreationWorkflow: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [prompt, setPrompt] = useState('');
  const [dialect, setDialect] = useState('english');
  const [style, setStyle] = useState('cinematic');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<any>(null); // For the final generation result
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleNext = () => setCurrentStep((prev) => prev + 1);
  const handleBack = () => setCurrentStep((prev) => prev - 1);

  const getAuthHeaders = () => {
    const token = localStorage.getItem('jwt_token');
    if (!token) {
      router.push('/login');
      return {};
    }
    return { Authorization: `Bearer ${token}` };
  };

  const handleGenerate = async () => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const headers = getAuthHeaders();
      if (!headers.Authorization) return;

      const response = await axios.post('http://localhost:8000/generate_video', {
        prompt,
        dialect,
        style, // Pass style to backend if API supports it
        upload_youtube: false, // Example: hardcode for now
      }, { headers });

      setResult(response.data);
      setCurrentStep(4); // Move to a final progress/result step

    } catch (err: any) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('An unexpected error occurred during generation. Please try again.');
      }
      console.error('Video generation error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return <Step1ContentInput onNext={handleNext} onBack={handleBack} prompt={prompt} setPrompt={setPrompt} />;
      case 2:
        return <Step2DialectStyle onNext={handleNext} onBack={handleBack} dialect={dialect} setDialect={setDialect} style={style} setStyle={setStyle} />;
      case 3:
        return <Step3ReviewConfirm onNext={handleNext} onBack={handleBack} prompt={prompt} dialect={dialect} style={style} onSubmit={handleGenerate} isLoading={isLoading} />;
      case 4:
        return (
          <div className="elite-card p-6 mb-4">
            <h3 className="section-subtitle mb-4">Step 4: Generation Progress & Result</h3>
            {isLoading && (
              <div className="flex items-center justify-center mb-4">
                <div className="loading-spinner mr-2"></div>
                <p className="text-soft-text">Generating your video...</p>
              </div>
            )}
            {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
            {result && (
              <div>
                <p className="text-soft-text mb-2">Status: <span className={`font-semibold ${result.status === 'success' ? 'text-green-500' : 'text-red-500'}`}> {result.status}</span></p>
                {result.message && <p className="text-soft-text mb-2">Message: {result.message}</p>}
                {result.rendered_output_path && (
                  <div className="mt-4">
                    <p className="text-soft-text mb-2">Rendered Video:</p>
                    <a 
                      href={result.rendered_output_path} 
                      target="_blank" 
                      rel="noopener noreferrer" 
                      className="text-blue-500 hover:underline font-medium"
                    >
                      View Generated Video
                    </a>
                  </div>
                )}
              </div>
            )}
            <div className="flex justify-center mt-4">
              <button type="button" className="btn-secondary px-6 py-2 rounded-lg" onClick={() => router.push('/dashboard')}>Go to Dashboard</button>
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="elite-container my-10">
      <h1 className="section-title text-center mb-8">New Video Creation</h1>
      <div className="flex justify-center mb-6">
        <div className="flex items-center space-x-4">
          {[1, 2, 3, 4].map((stepNum) => (
            <React.Fragment key={stepNum}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center font-semibold ${currentStep >= stepNum ? 'bg-primary-gradient text-white' : 'bg-gray-200 text-gray-600'}`}>
                {stepNum}
              </div>
              {stepNum < 4 && <div className={`w-12 h-1 ${currentStep > stepNum ? 'bg-primary-gradient' : 'bg-gray-200'}`}></div>}
            </React.Fragment>
          ))}
        </div>
      </div>
      {renderStep()}
    </div>
  );
};

export default VideoCreationWorkflow;