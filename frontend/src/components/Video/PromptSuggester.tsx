
import { useState, useRef } from 'react';
import { usePromptSuggester } from '@/hooks/usePromptSuggester';
import { FaSpinner } from 'react-icons/fa6';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Reusable prompt suggester component
// [GOAL]: Provide a clean and reusable component for prompt suggestions

interface PromptSuggesterProps {
  value: string;
  onChange: (newValue: string) => void;
  placeholder?: string;
  id?: string;
}

const PromptSuggester: React.FC<PromptSuggesterProps> = ({ value, onChange, placeholder, id }) => {
  const { suggestions, isLoading } = usePromptSuggester(value);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const handleSelectSuggestion = (suggestion: string) => {
    onChange(suggestion);
    setShowSuggestions(false);
  };

  const handleBlur = () => {
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
        id={id}
        ref={inputRef}
        className="form-input w-full p-3 rounded-lg h-24"
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onBlur={handleBlur}
        onFocus={handleFocus}
      ></textarea>

      {showSuggestions && (suggestions.length > 0 || isLoading) && (
        <div className="absolute z-10 bg-white border border-gray-200 rounded-lg shadow-lg mt-1 w-full max-h-60 overflow-y-auto">
          {isLoading ? (
            <div className="p-3 flex items-center justify-center text-soft-text">
              <FaSpinner className="animate-spin mr-2" /> Fetching suggestions...
            </div>
          ) : (
            suggestions.map((suggestion, index) => (
              <div
                key={index}
                className="p-3 cursor-pointer hover:bg-gray-100 text-charcoal text-sm"
                onMouseDown={() => handleSelectSuggestion(suggestion)}
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

