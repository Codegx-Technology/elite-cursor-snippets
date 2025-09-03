'use client';

import { useState, useEffect } from 'react';
import Footer from './Footer';
import dynamic from 'next/dynamic';
import Header from './Header';
import Sidebar from './Sidebar';
import ErrorBoundary from './ErrorBoundary';
import SuperAdminMenu from './SuperAdminMenu'; // New import

// Dynamically import ScrollToTop on client only to avoid hydration mismatch
const ScrollToTop = dynamic(() => import('./ScrollToTop'), { ssr: false });

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean + refactorintent
// [CONTEXT]: Enterprise-grade layout with Kenya-first design system and mobile-first approach
// [GOAL]: Create responsive layout with cultural authenticity and modern UX
// [TASK]: Implement layout with proper spacing, gradients, and mobile responsiveness

export default function Layout({ children }: { children: React.ReactNode }) {
  const [isSidebarOpen, setSidebarOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  // Handle responsive behavior with improved mobile detection
  useEffect(() => {
    const checkMobile = () => {
      const isMobileDevice = window.innerWidth < 768;
      setIsMobile(isMobileDevice);

      // Auto-close sidebar on desktop
      if (window.innerWidth >= 768) {
        setSidebarOpen(false);
      }
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Sidebar */}
      <Sidebar isSidebarOpen={isSidebarOpen} setSidebarOpen={setSidebarOpen} />

      {/* Main Content Area */}
      <div className={`transition-all duration-300 ease-in-out ${
        isMobile ? 'ml-0' : 'md:ml-72'
      }`}>
        {/* Header */}
        <Header isSidebarOpen={isSidebarOpen} setSidebarOpen={setSidebarOpen} />

        {/* Super Admin Menu (conditionally rendered) */}
        <SuperAdminMenu />

        {/* Main Content with improved mobile spacing and error boundary */}
        <main className={`min-h-screen pt-4 pb-20 transition-all duration-300 ${
          isMobile
            ? 'px-3 sm:px-4'
            : 'px-4 sm:px-6 lg:px-8'
        }`}>
          <div className={`mx-auto transition-all duration-300 ${
            isMobile
              ? 'max-w-full'
              : 'max-w-7xl'
          }`}>
            <ErrorBoundary>
              {children}
            </ErrorBoundary>
          </div>
        </main>

        {/* Footer */}
        <Footer />
      </div>

      {/* Mobile Overlay with improved touch handling */}
      {isSidebarOpen && isMobile && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
          style={{ pointerEvents: 'auto' }}
          onClick={(e) => {
            e.stopPropagation();
            setSidebarOpen(false);
          }}
          onTouchStart={(e) => {
            e.stopPropagation();
            setSidebarOpen(false);
          }}
        />
      )}

      {/* Tiny modern scroll-to-top arrow */}
      <ScrollToTop />
    </div>
  );
}
