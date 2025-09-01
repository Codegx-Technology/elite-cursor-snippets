'use client';

export default function TestSimple() {
  return (
    <div style={{ 
      padding: '40px', 
      fontFamily: 'Arial, sans-serif', 
      textAlign: 'center',
      background: 'linear-gradient(135deg, #00A651, #FFD700)',
      minHeight: '100vh',
      color: 'white'
    }}>
      <h1 style={{ fontSize: '3em', marginBottom: '20px' }}>
        🇰🇪 Shujaa Studio Test Page
      </h1>
      <h2 style={{ color: '#FFD700', marginBottom: '30px' }}>
        ✅ Frontend is Working!
      </h2>
      <p style={{ fontSize: '1.2em', marginBottom: '20px' }}>
        Time: {new Date().toLocaleString()}
      </p>
      <div style={{ 
        background: 'rgba(255,255,255,0.1)', 
        padding: '20px', 
        borderRadius: '10px',
        margin: '20px auto',
        maxWidth: '600px'
      }}>
        <h3>🚀 Server Status</h3>
        <p>✅ Frontend: http://localhost:3001</p>
        <p>✅ Backend: http://localhost:8000</p>
        <p>✅ API Docs: http://localhost:8000/docs</p>
      </div>
      <div style={{ marginTop: '30px' }}>
        <a
          href="/dashboard"
          style={{
            background: '#2c3e50',
            color: 'white',
            padding: '15px 30px',
            textDecoration: 'none',
            borderRadius: '5px',
            fontSize: '1.1em',
            margin: '10px',
            display: 'inline-block'
          }}
        >
          🎬 Go to Dashboard
        </a>
        <a
          href="/generate"
          style={{
            background: '#e74c3c',
            color: 'white',
            padding: '15px 30px',
            textDecoration: 'none',
            borderRadius: '5px',
            fontSize: '1.1em',
            margin: '10px',
            display: 'inline-block'
          }}
        >
          🎥 Generate Video
        </a>
      </div>
    </div>
  );
}
