import Card from '@/components/Card';
import FormInput from '@/components/FormInput';
import FormSelect from '@/components/FormSelect';

export default function VideoGeneratePage() {
  const voiceOptions = [
    { value: 'male-voice-1', label: 'Male Voice 1' },
    { value: 'female-voice-1', label: 'Female Voice 1' },
    { value: 'kenyan-sheng', label: 'Kenyan Sheng' },
  ];

  return (
    <Card className="p-6">
      <h1 className="section-title mb-4">Generate Video</h1>
      <p className="text-soft-text mb-6">Input details to generate your video.</p>
      <div className="mt-8">
        <FormInput
          label="Video Script"
          type="text"
          placeholder="Enter your video script here..."
          id="videoScript"
          name="videoScript"
        />
        <FormSelect
          label="Voice Selection"
          options={voiceOptions}
          id="voiceSelection"
          name="voiceSelection"
        />
        <FormInput
          label="Visual Style/Theme"
          type="text"
          placeholder="e.g., Modern, Cinematic, Cartoon"
          id="visualStyle"
          name="visualStyle"
        />
      </div>
    </Card>
  );
}
