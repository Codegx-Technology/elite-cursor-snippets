
import { useState } from 'react';
import { apiClient, handleApiResponse } from '@/lib/api';

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
  const [currentJobId, setCurrentJobId] = useState<string | null>(null);
  const [friendlyFallback, setFriendlyFallback] = useState<{
    message: string;
    retryOptions: string[];
    spinnerType: string;
  } | null>(null);

  const handleInputChange = (field: keyof VideoGenerationForm, value: string | boolean) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

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
              setError(job.error_message || 'Video generation failed');
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

  return {
    formData,
    progress,
    generatedVideo,
    error,
    friendlyFallback,
    handleInputChange,
    handleGenerateVideo,
    handleStopGeneration,
    setFriendlyFallback
  };
}
