'use client';

import Link from 'next/link';

export default function SimplePage() {
  return (
    <div style={{ 
      padding: '40px', 
      fontFamily: 'Arial, sans-serif',
      maxWidth: '800px',
      margin: '0 auto',
      lineHeight: '1.6'
    }}>
      <div style={{ textAlign: 'center', marginBottom: '40px' }}>
        <h1 style={{ color: '#2c3e50', fontSize: '2.5em', marginBottom: '10px' }}>
          🇰🇪 Shujaa Studio
        </h1>
        <p style={{ color: '#7f8c8d', fontSize: '1.2em' }}>
          Kenya-First AI Video Platform
        </p>
      </div>

      <div style={{ 
        background: '#e8f5e8', 
        padding: '20px', 
        borderRadius: '8px',
        marginBottom: '30px'
      }}>
        <h2 style={{ color: '#27ae60', marginTop: '0' }}>✅ System Status</h2>
        <ul style={{ margin: '0', paddingLeft: '20px' }}>
          <li>✅ Next.js Server: Running</li>
          <li>✅ React Rendering: Working</li>
          <li>✅ Client-Side JavaScript: Functional</li>
          <li>✅ Routing: Active</li>
        </ul>
      </div>

      <div style={{ 
        background: '#f8f9fa', 
        padding: '20px', 
        borderRadius: '8px',
        marginBottom: '30px'
      }}>
        <h2 style={{ color: '#495057', marginTop: '0' }}>🚀 Quick Actions</h2>
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          <Link 
            href="/test" 
            style={{ 
              background: '#007bff', 
              color: 'white', 
              padding: '10px 20px', 
              textDecoration: 'none',
              borderRadius: '5px',
              display: 'inline-block'
            }}
          >
            Test Page
          </Link>
          <Link 
            href="/en" 
            style={{ 
              background: '#28a745', 
              color: 'white', 
              padding: '10px 20px', 
              textDecoration: 'none',
              borderRadius: '5px',
              display: 'inline-block'
            }}
          >
            Main App (i18n)
          </Link>
          <Link 
            href="/" 
            style={{ 
              background: '#ffc107', 
              color: 'black', 
              padding: '10px 20px', 
              textDecoration: 'none',
              borderRadius: '5px',
              display: 'inline-block'
            }}
          >
            Root (Redirect)
          </Link>
        </div>
      </div>

      <div style={{ 
        background: '#fff3cd', 
        padding: '20px', 
        borderRadius: '8px',
        marginBottom: '30px'
      }}>
        <h2 style={{ color: '#856404', marginTop: '0' }}>🔧 Troubleshooting</h2>
        <p>If the main app shows a blank page, try these steps:</p>
        <ol style={{ paddingLeft: '20px' }}>
          <li>Check browser console for JavaScript errors (F12)</li>
          <li>Verify all dependencies are installed: <code>npm install</code></li>
          <li>Clear browser cache and reload</li>
          <li>Check if backend is running: <a href="http://localhost:8000" target="_blank">http://localhost:8000</a></li>
        </ol>
      </div>

      <div style={{ 
        background: '#d1ecf1', 
        padding: '20px', 
        borderRadius: '8px'
      }}>
        <h2 style={{ color: '#0c5460', marginTop: '0' }}>📊 Server Information</h2>
        <p><strong>Frontend:</strong> http://localhost:3000</p>
        <p><strong>Backend:</strong> http://localhost:8000</p>
        <p><strong>API Docs:</strong> http://localhost:8000/docs</p>
        <p><strong>Current Time:</strong> {new Date().toLocaleString()}</p>
      </div>
    </div>
  );
}
