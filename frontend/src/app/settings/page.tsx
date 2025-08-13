import FormInput from '@/components/FormInput';
import Card from '@/components/Card';

export default function SettingsPage() {
  return (
    <Card className="p-6">
      <h1 className="section-title mb-4">Settings</h1>
      <p className="text-soft-text mb-6">Adjust your application settings.</p>

      <form>
        <FormInput
          label="Username"
          type="text"
          placeholder="Enter your username"
          id="username"
          name="username"
        />
        <FormInput
          label="Email"
          type="email"
          placeholder="Enter your email"
          id="email"
          name="email"
        />
        <button type="submit" className="btn-primary mt-4">Save Changes</button>
      </form>
    </Card>
  );
}