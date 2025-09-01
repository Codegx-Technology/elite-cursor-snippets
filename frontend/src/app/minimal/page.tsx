'use client';

export default function MinimalPage() {
  return (
    <div style={{
      fontFamily: 'Arial, sans-serif',
      padding: '20px',
      minHeight: '100vh',
      background: '#f8f9fa'
    }}>
      <h1 style={{ color: 'green', fontSize: '2.5em', textAlign: 'center' }}>
        🎉 SUCCESS! This page works!
      </h1>
      <p style={{ fontSize: '1.2em', textAlign: 'center', color: '#666' }}>
        If you can see this, Next.js is working perfectly.
      </p>
      <p style={{ fontSize: '1em', textAlign: 'center', color: '#888' }}>
        Current time: {new Date().toISOString()}
      </p>
      <div style={{
        textAlign: 'center',
        marginTop: '30px',
        padding: '20px',
        background: 'white',
        borderRadius: '8px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}>
        <h2 style={{ color: '#2c3e50' }}>✅ Client Component Working</h2>
        <p>This is a proper Next.js 13+ Client Component</p>
      </div>
    </div>
  );
}
