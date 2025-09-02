'use client';

import { useState, useEffect } from 'react';
import { apiClient, handleApiResponse } from '@/lib/api';
import { useDebounce } from 'use-debounce';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Custom hook for managing prompt suggestions
// [GOAL]: Encapsulate prompt suggestion logic and provide a clean interface for UI components

// Kenya-first prompt suggestions for fallback
const KENYA_PROMPT_SUGGESTIONS = [
  "Create a video showcasing Kenya's beautiful landscapes and wildlife",
  "Generate content about Kenyan culture and traditions",
  "Make a video about Nairobi's vibrant business district",
  "Create educational content about Kenya's history",
  "Showcase traditional Kenyan music and dance",
  "Generate a video about Kenyan cuisine and local dishes",
  "Create content about Kenya's tech innovation hub",
  "Make a video about Maasai culture and traditions",
  "Generate content about Kenya's conservation efforts",
  "Create a video about Kenyan entrepreneurs and success stories"
];

function generateFallbackSuggestions(prompt: string): string[] {
  const lowerPrompt = prompt.toLowerCase();

  // Filter suggestions based on prompt content
  const filtered = KENYA_PROMPT_SUGGESTIONS.filter(suggestion =>
    suggestion.toLowerCase().includes(lowerPrompt) ||
    lowerPrompt.split(' ').some(word =>
      word.length > 2 && suggestion.toLowerCase().includes(word)
    )
  );

  // If no matches, return general Kenya-first suggestions
  if (filtered.length === 0) {
    return KENYA_PROMPT_SUGGESTIONS.slice(0, 5);
  }

  return filtered.slice(0, 5);
}

export function usePromptSuggester(value: string) {
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [debouncedValue] = useDebounce(value, 500);

  useEffect(() => {
    if (debouncedValue.length < 3) {
      setSuggestions([]);
      return;
    }

    const fetchSuggestions = async () => {
      setIsLoading(true);
      try {
        const response = await apiClient.getPromptSuggestions(debouncedValue);
        handleApiResponse(
          response,
          (data) => setSuggestions(data.suggestions || []),
          () => {
            // Fallback to local suggestions if API fails
            setSuggestions(generateFallbackSuggestions(debouncedValue));
          }
        );
      } catch (error) {
        // Fallback to local suggestions if API fails
        setSuggestions(generateFallbackSuggestions(debouncedValue));
      }
      setIsLoading(false);
    };

    fetchSuggestions();
  }, [debouncedValue]);

  return { suggestions, isLoading };
}
