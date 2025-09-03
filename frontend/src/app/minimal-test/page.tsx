import Link from 'next/link';

export default function MinimalTest() {
  return (
    <html>
      <head>
        <title>Shujaa Studio - Minimal Test</title>
      </head>
      <body style={{ 
        margin: 0, 
        padding: '40px', 
        fontFamily: 'Arial, sans-serif',
        background: 'linear-gradient(135deg, #00A651, #FFD700)',
        color: 'white',
        minHeight: '100vh'
      }}>
        <h1>🇰🇪 Shujaa Studio - Minimal Test</h1>
        <h2>✅ Frontend Working!</h2>
        <p>Time: {new Date().toLocaleString()}</p>
        <div style={{ marginTop: '20px' }}>
          <p>✅ Next.js: Running</p>
          <p>✅ TypeScript: Compiled</p>
          <p>✅ Server: http://localhost:3001</p>
        </div>
        <div style={{ marginTop: '30px' }}>
          <Link href="/dashboard" style={{ 
            background: '#2c3e50', 
            color: 'white', 
            padding: '10px 20px', 
            textDecoration: 'none', 
            borderRadius: '5px',
            marginRight: '10px'
          }}>
            Dashboard
          </Link>
          <Link href="/generate" style={{ 
            background: '#e74c3c', 
            color: 'white', 
            padding: '10px 20px', 
            textDecoration: 'none', 
            borderRadius: '5px'
          }}>
            Generate
          </Link>
        </div>
      </body>
    </html>
  );
}
