'use client';

import { useState, useEffect } from 'react';
import { apiClient, handleApiResponse } from '@/lib/api';
import { useDebounce } from 'use-debounce';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Custom hook for managing prompt suggestions
// [GOAL]: Encapsulate prompt suggestion logic and provide a clean interface for UI components

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
      const response = await apiClient.getPromptSuggestions(debouncedValue);
      handleApiResponse(
        response,
        (data) => setSuggestions(data.suggestions || []),
        () => setSuggestions([])
      );
      setIsLoading(false);
    };

    fetchSuggestions();
  }, [debouncedValue]);

  return { suggestions, isLoading };
}