
import { useState } from 'react';
import { apiClient, handleApiResponse } from '@/lib/api';
import { useError } from '@/context/ErrorContext';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Custom hook for managing enterprise-grade video generation state and logic
// [GOAL]: Encapsulate video generation complexity and provide a clean interface for UI components

export interface VideoGenerationForm {
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

export interface GenerationProgress {
  stage: string;
  progress: number;
  message: string;
  isGenerating: boolean;
}

export function useVideoGenerator() {
  const [formData, setFormData] = useState<VideoGenerationForm>({
    script: '',
    voice: 'kenyan-male-professional',
    visualStyle: 'cinematic-documentary',
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
  const [scriptError, setScriptError] = useState<string | null>(null);
  const [currentJobId, setCurrentJobId] = useState<string | null>(null);
  const [friendlyFallback, setFriendlyFallback] = useState<{
    message: string;
    retryOptions: string[];
    spinnerType: string;
  } | null>(null);

  // Global error reporter from ErrorContext
  const { setGlobalError } = useError();

  const handleInputChange = (field: keyof VideoGenerationForm, value: string | boolean) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));

    if (field === 'script') {
      if (typeof value === 'string' && value.trim().length < 10) {
        setScriptError('Script must be at least 10 characters long.');
      } else {
        setScriptError(null);
      }
    }
  };

  const handleGenerateVideo = async () => {
    if (!formData.script.trim()) {
      setScriptError('Please enter a video script to continue.');
      return;
    }
    if (scriptError) {
      alert('Please fix the script errors before generating.');
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
      const mapVisualStyle = (val: string): 'realistic' | 'cartoon' | 'anime' | 'documentary' => {
        switch (val) {
          case 'authentic-realistic':
          case 'professional-corporate':
          case 'vibrant-colorful':
            return 'realistic';
          case 'animated-cartoon':
            return 'cartoon';
          case 'artistic-creative':
            return 'anime';
          case 'cinematic-documentary':
          default:
            return 'documentary';
        }
      };

      const mapCulturalPreset = (val: string): 'mount_kenya' | 'maasai_mara' | 'diani_beach' | 'nairobi_city' => {
        switch (val) {
          case 'mount-kenya':
            return 'mount_kenya';
          case 'coastal-beauty':
            return 'diani_beach';
          case 'wildlife-safari':
          case 'traditional-heritage':
            return 'maasai_mara';
          case 'modern-kenya':
          case 'cultural-fusion':
          case 'innovation-story':
          default:
            return 'nairobi_city';
        }
      };

      const response = await apiClient.generateVideo({
        prompt: formData.script,
        lang: formData.language.includes('swahili') ? 'sw' : 'en',
        scenes: 3,
        vertical: formData.duration === '15' || formData.duration === '30',
        style: mapVisualStyle(formData.visualStyle),
        duration: parseInt(formData.duration),
        voice_type: formData.voice.includes('female') ? 'female' : 'male',
        background_music: true,
        cultural_preset: mapCulturalPreset(formData.culturalPreset)
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
    } catch (err: any) {
      setError(err.message || 'Failed to start video generation');
      setGlobalError(err.message || 'Failed to start video generation');
    }
  };

  const pollJobStatus = async (jobId: string) => {
    const maxAttempts = 60; // 5 minutes max
    let attempts = 0;

    const stages = [
      { stage: 'Script Analysis', progress: 30, message: 'Analyzing your script and understanding the narrative.' },
      { stage: 'Generating Visuals', progress: 50, message: 'Creating stunning visuals based on your script.' },
      { stage: 'Adding Voice', progress: 70, message: 'Generating authentic voiceovers for your video.' },
      { stage: 'Cultural Enhancement', progress: 85, message: 'Infusing unique cultural elements and background music.' },
      { stage: 'Final Processing', progress: 95, message: 'Assembling and polishing your high-quality video.' }
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
              setError(null);
              setCurrentJobId(null);
              setFriendlyFallback({
                message: job.friendly_message ?? 'Service temporarily unavailable',
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
              setGlobalError(job.error_message || 'Video generation failed');
              setCurrentJobId(null);
            } else {
              const stageIndex = Math.min(Math.floor(job.progress / 20), stages.length - 1);
              const currentStage = stages[stageIndex] || stages[0];

              setProgress({
                stage: currentStage.stage,
                progress: job.progress || currentStage.progress,
                message: currentStage.message,
                isGenerating: true
              });

              attempts++;
              if (attempts < maxAttempts) {
                setTimeout(poll, 5000);
              } else {
                setProgress({
                  stage: 'Timeout',
                  progress: 0,
                  message: 'Video generation timed out',
                  isGenerating: false
                });
                setGlobalError('Video generation timed out. Please try again.');
                setCurrentJobId(null);
              }
            }
          },
          (error) => {
            setError(error);
            setProgress({
              stage: 'Error',
              progress: 0,
              message: 'Failed to check generation status',
              isGenerating: false
            });
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
        setGlobalError('Network error during generation');
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

  return {
    formData,
    progress,
    generatedVideo,
    error,
    setError,
    scriptError,
    friendlyFallback,
    handleInputChange,
    handleGenerateVideo,
    handleStopGeneration,
    setFriendlyFallback
  };
}
