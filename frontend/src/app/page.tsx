export default function RootPage() {
  return (
    <div style={{ padding: '40px', fontFamily: 'Arial, sans-serif', textAlign: 'center' }}>
      <h1 style={{ color: '#2c3e50', fontSize: '3em' }}>🇰🇪 Shujaa Studio</h1>
      <h2 style={{ color: '#27ae60' }}>✅ WORKING!</h2>
      <p style={{ fontSize: '1.2em', color: '#7f8c8d' }}>
        Frontend is now functional! Time: {new Date().toLocaleString()}
      </p>
      <div style={{ marginTop: '30px' }}>
        <a
          href="/minimal"
          style={{
            background: '#3498db',
            color: 'white',
            padding: '15px 30px',
            textDecoration: 'none',
            borderRadius: '5px',
            fontSize: '1.1em',
            margin: '10px'
          }}
        >
          Test Minimal Page
        </a>
        <a
          href="/en"
          style={{
            background: '#e74c3c',
            color: 'white',
            padding: '15px 30px',
            textDecoration: 'none',
            borderRadius: '5px',
            fontSize: '1.1em',
            margin: '10px'
          }}
        >
          Try Complex App
        </a>
      </div>
      <div style={{ marginTop: '40px', background: '#f8f9fa', padding: '20px', borderRadius: '8px' }}>
        <h3>🔧 Backend Status</h3>
        <p>Backend API: <a href="http://localhost:8000" target="_blank">http://localhost:8000</a></p>
        <p>API Docs: <a href="http://localhost:8000/docs" target="_blank">http://localhost:8000/docs</a></p>
      </div>
    </div>
  );
}
