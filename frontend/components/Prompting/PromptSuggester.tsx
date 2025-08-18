// frontend/components/Prompting/PromptSuggester.tsx (Conceptual)

import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { useDebounce } from 'use-debounce'; // Assuming a debounce hook for API calls
import { useRouter } from 'next/router';

interface PromptSuggesterProps {
  value: string;
  onChange: (newValue: string) => void;
  placeholder?: string;
}

const PromptSuggester: React.FC<PromptSuggesterProps> = ({ value, onChange, placeholder }) => {
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [isLoadingSuggestions, setIsLoadingSuggestions] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [debouncedPrompt] = useDebounce(value, 500); // Debounce API calls
  const router = useRouter();
  const inputRef = useRef<HTMLTextAreaElement>(null); // Ref for the textarea

  const getAuthHeaders = () => {
    const token = localStorage.getItem('jwt_token');
    if (!token) {
      router.push('/login');
      return {};
    }
    return { Authorization: `Bearer ${token}` };
  };

  useEffect(() => {
    const fetchSuggestions = async () => {
      if (debouncedPrompt.length < 3) { // Only fetch for prompts > 2 characters
        setSuggestions([]);
        setIsLoadingSuggestions(false);
        setShowSuggestions(false);
        return;
      }

      setIsLoadingSuggestions(true);
      setShowSuggestions(true); // Show suggestions container
      try {
        const headers = getAuthHeaders();
        if (!headers.Authorization) return;

        // Conceptual API endpoint for prompt suggestions
        const response = await axios.post('http://localhost:8000/ai/suggest_prompt', {
          partial_prompt: debouncedPrompt,
        }, { headers });

        setSuggestions(response.data.suggestions || []);
      } catch (err) {
        console.error('Error fetching prompt suggestions:', err);
        setSuggestions([]);
      } finally {
        setIsLoadingSuggestions(false);
      }
    };

    fetchSuggestions();
  }, [debouncedPrompt]); // Trigger fetch when debouncedPrompt changes

  const handleSelectSuggestion = (suggestion: string) => {
    onChange(suggestion); // Update the main prompt
    setSuggestions([]); // Clear suggestions
    setShowSuggestions(false); // Hide suggestions
  };

  const handleBlur = () => {
    // Hide suggestions after a short delay to allow click on suggestion
    setTimeout(() => setShowSuggestions(false), 100);
  };

  const handleFocus = () => {
    if (value.length >= 3) {
      setShowSuggestions(true);
    }
  };

  return (
    <div className="relative">
      <textarea
        ref={inputRef}
        className="form-input w-full p-3 rounded-lg h-24"
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onBlur={handleBlur}
        onFocus={handleFocus}
      ></textarea>

      {showSuggestions && (suggestions.length > 0 || isLoadingSuggestions) && (
        <div className="absolute z-10 bg-white border border-gray-200 rounded-lg shadow-lg mt-1 w-full max-h-60 overflow-y-auto">
          {isLoadingSuggestions ? (
            <div className="p-3 flex items-center justify-center text-soft-text">
              <div className="loading-spinner mr-2"></div> Fetching suggestions...
            </div>
          ) : (
            suggestions.map((suggestion, index) => (
              <div
                key={index}
                className="p-3 cursor-pointer hover:bg-gray-100 text-charcoal text-sm"
                onMouseDown={() => handleSelectSuggestion(suggestion)} // Use onMouseDown to prevent blur from hiding before click
              >
                {suggestion}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default PromptSuggester;