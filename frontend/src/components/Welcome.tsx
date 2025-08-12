import Card from './Card';

export default function Welcome() {
  return (
    <Card className="text-center p-8">
      <img src="/shujaa-logo-placeholder.png" alt="Shujaa Studio Logo" className="mx-auto mb-6 w-32 h-32 object-contain" />
      <h1 className="section-title text-3xl mb-2">Welcome to Shujaa Studio</h1>
      <p className="section-subtitle text-xl text-soft-text mb-6">Your ultimate platform for AI-powered creative content generation.</p>
      <p className="text-lg text-charcoal-text mb-8">
        Experience seamless video production, intelligent scriptwriting, and dynamic content creation, all designed to elevate your storytelling.
      </p>
      <div className="flex justify-center space-x-4">
        <button className="btn-primary">Get Started</button>
        <button className="btn-elite">Learn More</button>
      </div>
    </Card>
  );
}
