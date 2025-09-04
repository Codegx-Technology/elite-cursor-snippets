import { render, screen } from '@testing-library/react';
import VideoGeneratePage from './page';

interface MockPromptSuggesterProps {
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
  id: string;
}

interface MockFormSelectOption {
  value: string;
  label: string;
}

interface MockFormSelectProps {
  label: string;
  options: MockFormSelectOption[];
  id: string;
  name: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
}

// Mock the useVideoGenerator hook
jest.mock('@/hooks/useVideoGenerator', () => ({
  useVideoGenerator: () => ({
    formData: { script: '', culturalPreset: '', voice: '', language: '', visualStyle: '', duration: '', musicStyle: '', removeWatermark: false, enableSubtitles: false, exportFormat: 'mp4' },
    progress: { isGenerating: false, stage: '', progress: 0, message: '' },
    generatedVideo: null,
    error: null,
    friendlyFallback: null,
    handleInputChange: jest.fn(),
    handleGenerateVideo: jest.fn(),
    handleStopGeneration: jest.fn(),
    setFriendlyFallback: jest.fn(),
  }),
}));

// Mock the PromptSuggester component as it's a child component
jest.mock('@/components/Video/PromptSuggester', () => {
  return function MockPromptSuggester({ value, onChange, placeholder, id }: MockPromptSuggesterProps) {
    return (
      <input
        data-testid="prompt-suggester-mock"
        id={id}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
      />
    );
  };
});

// Mock the SimpleMode component
jest.mock('@/components/Video/SimpleMode', () => {
  return function MockSimpleMode() {
    return <div data-testid="simple-mode-mock">Simple Mode Content</div>;
  };
});

// Mock FormSelect component
jest.mock('@/components/FormSelect', () => {
  return function MockFormSelect({ label, options, id, name, value, onChange }: MockFormSelectProps) {
    return (
      <div>
        <label htmlFor={id}>{label}</label>
        <select id={id} name={name} value={value} onChange={onChange}>
          {options.map((option: MockFormSelectOption) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
    );
  };
});

describe('VideoGeneratePage', () => {
  it('renders the main heading and key form elements correctly in default mode', () => {
    render(<VideoGeneratePage />);

    // Check if the main heading is present
    expect(screen.getByRole('heading', { name: /Generate Kenya-First Video/i })).toBeInTheDocument();

    // Check if the Video Script input is present (mocked as an input field)
    expect(screen.getByLabelText(/Video Script/i)).toBeInTheDocument();
    expect(screen.getByTestId('prompt-suggester-mock')).toBeInTheDocument();

    // Check if the Generate Video button is present
    expect(screen.getByRole('button', { name: /Generate Kenya-First Video/i })).toBeInTheDocument();

    // Check if the Simple Mode toggle is present
    expect(screen.getByLabelText(/Simple Mode/i)).toBeInTheDocument();

    // Ensure SimpleMode is NOT rendered initially
    expect(screen.queryByTestId('simple-mode-mock')).not.toBeInTheDocument();
  });
});
