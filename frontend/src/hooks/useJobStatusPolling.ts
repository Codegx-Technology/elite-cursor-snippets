import { useState, useEffect, useRef } from 'react';
import { apiClient, handleApiResponse } from '@/lib/api';

export interface JobProgress {
  stage: string;
  progress: number;
  message: string;
  isGenerating: boolean;
}

export interface JobStatusResponse {
  status: 'pending' | 'processing' | 'completed' | 'failed' | 'friendly_fallback';
  progress?: number;
  friendly_message?: string;
  error_message?: string;
  result_url?: string;
  video_id?: string;
  retry_options?: string[];
  spinner_type?: string;
}

const stages = [
  { stage: 'Starting Generation', progress: 5, message: 'Initiating the creative process...' },
  { stage: 'Script Analysis', progress: 20, message: 'Analyzing your script and understanding the narrative.' },
  { stage: 'Generating Visuals', progress: 40, message: 'Creating stunning visuals to accompany your story.' },
  { stage: 'Adding Voice', progress: 60, message: 'Generating authentic voiceovers for your video.' },
  { stage: 'Cultural Enhancement', progress: 75, message: 'Infusing unique cultural elements and background music.' },
  { stage: 'Final Processing', progress: 90, message: 'Assembling and polishing your masterpiece.' }
];

export function useJobStatusPolling() {
  const [progress, setProgress] = useState<JobProgress>({
    stage: 'Ready',
    progress: 0,
    message: 'Ready to create your content',
    isGenerating: false
  });
  const [generatedUrl, setGeneratedUrl] = useState<string | null>(null);
  const [jobError, setJobError] = useState<string | null>(null);
  const [friendlyFallback, setFriendlyFallback] = useState<{
    message: string;
    retryOptions: string[];
    spinnerType: string;
  } | null>(null);
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const startPolling = (jobId: string) => {
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
    }

    setProgress({
      stage: 'Starting',
      progress: 5,
      message: 'Generation initiated...',
      isGenerating: true
    });
    setGeneratedUrl(null);
    setJobError(null);
    setFriendlyFallback(null);

    let attempts = 0;
    const maxAttempts = 120; // 10 minutes max (5 seconds * 120 attempts)

    const poll = async () => {
      try {
        const response = await apiClient.getGenerationJob(jobId);
        handleApiResponse(
          response,
          (job: JobStatusResponse) => {
            if (job.status === 'completed') {
              setProgress({
                stage: 'Complete',
                progress: 100,
                message: 'Your content is ready!',
                isGenerating: false
              });
              setGeneratedUrl(job.result_url || null);
              if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
            } else if (job.status === 'friendly_fallback') {
              setProgress({
                stage: 'Friendly Fallback',
                progress: 0,
                message: job.friendly_message || 'Service temporarily unavailable',
                isGenerating: false
              });
              setJobError(null);
              setFriendlyFallback({
                message: job.friendly_message ?? 'Service temporarily unavailable',
                retryOptions: job.retry_options || [],
                spinnerType: job.spinner_type || 'kenya_flag'
              });
              if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
            } else if (job.status === 'failed') {
              setProgress({
                stage: 'Error',
                progress: 0,
                message: 'Generation failed',
                isGenerating: false
              });
              setJobError(job.error_message || 'An unknown error occurred during generation.');
              if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
            } else {
              // Still processing
              const currentStage = stages.find(s => job.progress && job.progress >= s.progress) || stages[0];
              
              setProgress({
                stage: currentStage.stage,
                progress: job.progress || currentStage.progress,
                message: job.friendly_message || currentStage.message, // Use friendly_message if available
                isGenerating: true
              });

              attempts++;
              if (attempts < maxAttempts) {
                pollIntervalRef.current = setTimeout(poll, 5000);
              } else {
                setProgress({
                  stage: 'Timeout',
                  progress: 0,
                  message: 'Generation timed out',
                  isGenerating: false
                });
                setJobError('Generation timed out. Please try again.');
                if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
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
            setJobError(error);
            if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
          }
        );
      } catch (err: any) {
        setProgress({
          stage: 'Error',
          progress: 0,
          message: 'Network error during polling',
          isGenerating: false
        });
        setJobError(err.message || 'Network error during polling.');
        if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
      }
    };

    pollIntervalRef.current = setTimeout(poll, 5000); // Start polling after 5 seconds
  };

  const stopPolling = () => {
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
      pollIntervalRef.current = null;
    }
    setProgress(prev => ({
      ...prev,
      isGenerating: false,
      stage: 'Stopped',
      message: 'Generation stopped by user.'
    }));
  };

  useEffect(() => {
    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
    };
  }, []);

  return {
    progress,
    generatedUrl,
    jobError,
    friendlyFallback,
    startPolling,
    stopPolling,
    setJobError, // Allow external components to clear jobError
    setFriendlyFallback // Allow external components to clear friendlyFallback
  };
}
