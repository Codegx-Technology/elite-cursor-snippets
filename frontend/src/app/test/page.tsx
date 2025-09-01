'use client';

export default function TestPage() {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>🎉 Shujaa Studio Test Page</h1>
      <p>If you can see this, the Next.js server is working!</p>
      <div style={{ background: '#f0f0f0', padding: '10px', margin: '10px 0' }}>
        <h2>System Status:</h2>
        <ul>
          <li>✅ Next.js Server: Running</li>
          <li>✅ React Rendering: Working</li>
          <li>✅ Routing: Functional</li>
        </ul>
      </div>
      <p>
        <a href="/en" style={{ color: 'blue', textDecoration: 'underline' }}>
          Go to Main App (with i18n)
        </a>
      </p>
      <p>
        <a href="/" style={{ color: 'blue', textDecoration: 'underline' }}>
          Go to Root (should redirect to /en)
        </a>
      </p>
    </div>
  );
}
