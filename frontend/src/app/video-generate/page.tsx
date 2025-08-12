import Card from '@/components/Card';
import FormInput from '@/components/FormInput';

export default function VideoGeneratePage() {
  return (
    <Card className="p-6">
      <h1 className="section-title mb-4">Generate Video</h1>
      <p className="text-soft-text mb-6">Input details to generate your video.</p>
      <div className="mt-8">
        <FormInput
          label="Video Script"
          type="textarea"
          placeholder="Enter your video script here..."
          id="videoScript"
          name="videoScript"
        />
      </div>
    </Card>
  );
}
