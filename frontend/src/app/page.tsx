'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function RootPage() {
  const router = useRouter();

  useEffect(() => {
    // Client-side redirect to dashboard
    router.push('/dashboard');
  }, [router]);

  // Show loading state while redirecting
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
        <p>Loading...</p>
      </div>
    </div>
  );
}
