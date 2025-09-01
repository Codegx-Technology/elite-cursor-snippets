export default function MinimalPage() {
  return (
    <html>
      <head>
        <title>Minimal Test</title>
      </head>
      <body>
        <h1>🎉 SUCCESS! This page works!</h1>
        <p>If you can see this, Next.js is working.</p>
        <p>Current time: {new Date().toISOString()}</p>
        <style jsx>{`
          body { font-family: Arial, sans-serif; padding: 20px; }
          h1 { color: green; }
        `}</style>
      </body>
    </html>
  );
}
