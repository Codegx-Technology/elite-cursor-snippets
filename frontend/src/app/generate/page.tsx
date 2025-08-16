import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation'; // Use next/navigation for App Router

interface VideoGenerationResult {
  status: string;
  video_path?: string;
  rendered_output_path?: string; // Path to the final rendered video
  message?: string;
}

const GenerateVideoPage: React.FC = () => { // Renamed to GenerateVideoPage
  const [prompt, setPrompt] = useState('');
  const [dialect, setDialect] = useState('english'); // Default to English
  const [uploadYoutube, setUploadYoutube] = useState(false);
  const [result, setResult] = useState<VideoGenerationResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  // Example dialects (should come from backend or config)
  const dialects = ['english', 'yoruba', 'swahili', 'igbo', 'kikuyu'];

  const getAuthHeaders = () => {
    const token = localStorage.getItem('jwt_token');
    if (!token) {
      router.push('/login'); // Redirect to login if no token
      return {};
    }
    return { Authorization: `Bearer ${token}` };
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setResult(null);
    setError(null);
    setIsLoading(true);

    try {
      const headers = getAuthHeaders();
      if (!headers.Authorization) return;

      const response = await axios.post('http://localhost:8000/generate_video', {
        prompt,
        dialect,
        upload_youtube: uploadYoutube,
      }, { headers });

      setResult(response.data);

    } catch (err: any) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('An unexpected error occurred during video generation. Please try again.');
      }
      console.error('Video generation error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="elite-card p-8 max-w-2xl mx-auto my-10 rounded-xl shadow-lg">
      <h2 className="section-title text-center mb-6">Generate Cinematic Video</h2>
      <form onSubmit={handleSubmit}>
        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
        
        <div className="mb-4">
          <label htmlFor="prompt" className="block text-soft-text text-sm font-medium mb-2">Video Prompt</label>
          <textarea
            id="prompt"
            className="form-input w-full p-3 rounded-lg h-24"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            required
            placeholder="e.g., A cinematic story about a young Kenyan entrepreneur building a tech startup in Nairobi."
          ></textarea>
        </div>

        <div className="mb-4">
          <label htmlFor="dialect" className="block text-soft-text text-sm font-medium mb-2">Dialect</label>
          <select
            id="dialect"
            className="form-input w-full p-3 rounded-lg"
            value={dialect}
            onChange={(e) => setDialect(e.target.value)}
          >
            {dialects.map((d) => (
              <option key={d} value={d}>{d.charAt(0).toUpperCase() + d.slice(1)}</option>
            ))}
          </select>
        </div>

        <div className="mb-6 flex items-center">
          <input
            type="checkbox"
            id="uploadYoutube"
            className="mr-2"
            checked={uploadYoutube}
            onChange={(e) => setUploadYoutube(e.target.checked)}
          />
          <label htmlFor="uploadYoutube" className="text-soft-text text-sm font-medium">Upload to YouTube</label>
        </div>

        <button
          type="submit"
          className="btn-primary w-full py-3 rounded-lg text-white font-semibold flex items-center justify-center"
          disabled={isLoading}
        >
          {isLoading ? (
            <div className="loading-spinner mr-2"></div>
          ) : (
            'Generate Video'
          )}
        </button>
      </form>

      {result && (
        <div className="mt-8 p-6 elite-card rounded-lg">
          <h3 className="section-title mb-4">Generation Result:</h3>
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
    </div>
  );
};

export default GenerateVideoPage; // Export as default for page component