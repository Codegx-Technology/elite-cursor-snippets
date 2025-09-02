'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function PricingPage() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to localized pricing page
    router.push('/en/pricing');
  }, [router]);

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      height: '100vh',
      background: 'linear-gradient(135deg, #00A651, #FFD700)',
      color: 'white',
      fontFamily: 'Arial, sans-serif'
    }}>
      <div style={{ textAlign: 'center' }}>
        <h1>🇰🇪 Shujaa Studio</h1>
        <p>Redirecting to Pricing...</p>
      </div>
    </div>
  );
}
