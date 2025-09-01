'use client';

import { useTranslations } from "next-intl";

export default function Home() {
  const t = useTranslations("Index");

  return (
    <div style={{ padding: '40px', fontFamily: 'Arial, sans-serif', textAlign: 'center' }}>
      <h1 style={{ color: '#2c3e50', fontSize: '3em' }}>🇰🇪 {t("title")}</h1>
      <h2 style={{ color: '#27ae60' }}>✅ i18n WORKING!</h2>
      <p style={{ fontSize: '1.2em', color: '#7f8c8d' }}>
        Internationalization is now functional! Time: {new Date().toLocaleString()}
      </p>
      <div style={{ marginTop: '30px' }}>
        <a
          href="/"
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
          Back to Main
        </a>
        <a
          href="/sw"
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
          Swahili (sw)
        </a>
      </div>
      <div style={{ marginTop: '40px', background: '#f8f9fa', padding: '20px', borderRadius: '8px' }}>
        <h3>🌍 Language: {t("title")}</h3>
        <p>This page uses Next.js i18n with next-intl</p>
        <p>Current locale: <strong>en</strong></p>
      </div>
    </div>
  );
}
