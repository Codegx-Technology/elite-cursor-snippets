"use client";

import React from 'react';

export default function TestDashboard() {
  return (
    <div style={{ 
      padding: '40px', 
      fontFamily: 'Arial, sans-serif', 
      textAlign: 'center',
      background: '#f0f0f0',
      minHeight: '100vh'
    }}>
      <h1>🇰🇪 Dashboard Test</h1>
      <p>This is a simple test to see if routing works</p>
      <p>Time: {new Date().toLocaleString()}</p>
    </div>
  );
}
