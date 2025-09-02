'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
// Icons replaced with inline SVGs to avoid react-icons dependency issues

// [SNIPPET]: thinkwithai + kenyafirst + refactorclean
// [CONTEXT]: Enterprise sidebar with Kenya-first design and cultural elements
// [GOAL]: Create beautiful, functional navigation with cultural authenticity
// [TASK]: Implement sidebar with Kenya colors, proper navigation states, and cultural branding

interface SidebarProps {
  isSidebarOpen: boolean;
  setSidebarOpen: (isOpen: boolean) => void;
}

export default function Sidebar({ isSidebarOpen, setSidebarOpen }: SidebarProps) {
  const pathname = usePathname();
  const lang = pathname.split('/')[1] || 'en'; // Default to 'en' if lang is not present
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    // Set client-side flag to prevent hydration mismatch
    setIsClient(true);

    // Check authentication status only on client side
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('jwt_token');
      setIsLoggedIn(!!token);
    }
  }, []);

  // Debug logging (guarded to avoid noisy prod consoles)
  if (process.env.NODE_ENV !== 'production') {
    // eslint-disable-next-line no-console
    console.log('Current pathname:', pathname);
  }

  // Navigation items based on authentication status
  const navigationItems = isLoggedIn ? [
    {
      href: `/${lang}/dashboard`,
      icon: () => <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" /></svg>,
      label: 'Dashboard',
      description: 'Overview & Analytics 📊'
    },
    {
      href: `/${lang}/video-generate`,
      icon: () => <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z" /></svg>,
      label: 'Generate Video',
      description: 'AI-Powered Creation 🎬'
    },
    {
      href: `/${lang}/projects`,
      icon: () => <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" /></svg>,
      label: 'Projects',
      description: 'Manage Your Work 📁'
    },
    {
      href: `/${lang}/gallery`,
      icon: () => <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" /></svg>,
      label: 'Gallery',
      description: 'Browse generated content'
    },
    {
      href: `/${lang}/audio-studio`,
      icon: () => <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M18 3a1 1 0 00-1.196-.98l-10 2A1 1 0 006 5v9.114A4.369 4.369 0 005 14c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V7.82l8-1.6v5.894A4.37 4.37 0 0015 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V3z" /></svg>,
      label: 'Audio Studio',
      description: 'Voice & music creation'
    },
    {
      href: `/${lang}/analytics`,
      icon: () => <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" /></svg>,
      label: 'Analytics',
      description: 'Usage insights & metrics 📊'
    },
    {
      href: `/${lang}/admin`,
      icon: () => <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M2 5a2 2 0 012-2h8a2 2 0 012 2v10a2 2 0 002 2H4a2 2 0 01-2-2V5zm3 1h6v4H5V6zm6 6H5v2h6v-2z" clipRule="evenodd" /><path d="M15 7h1a2 2 0 012 2v5.5a1.5 1.5 0 01-3 0V7z" /></svg>,
      label: 'Admin',
      description: 'Admin panel & management'
    },
    {
      href: `/${lang}/team`,
      icon: () => <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" /></svg>,
      label: 'Team',
      description: 'Collaboration tools'
    },
    {
      href: `/${lang}/pricing`,
      icon: () => <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M4 4a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2H4zm0 3v1h12V7H4zm0 3v3h12v-3H4z" clipRule="evenodd" /></svg>,
      label: 'Pricing',
      description: 'Plans & billing'
    },
    {
      href: `/${lang}/settings`,
      icon: () => <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clipRule="evenodd" /></svg>,
      label: 'Settings',
      description: 'Preferences & config'
    },
    {
      href: `/${lang}/settings/local-models`,
      icon: () => <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" /></svg>,
      label: 'Local Models',
      description: 'Manage local models'
    },
    {
      href: `/${lang}/settings/storage-management`,
      icon: () => <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z" /></svg>,
      label: 'Storage Management',
      description: 'Manage storage'
    },
    {
      href: `/${lang}/profile`,
      icon: () => <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" /></svg>,
      label: 'Profile',
      description: 'Manage your profile'
    }
  ] : [
    {
      href: `/${lang}`,
      icon: () => <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" /></svg>,
      label: 'Home',
      description: 'Welcome to Shujaa 🏠'
    },
    {
      href: `/${lang}/demo`,
      icon: () => <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z" /></svg>,
      label: 'Demo',
      description: 'See Platform in Action 🎬'
    },
    {
      href: `/${lang}/pricing`,
      icon: () => <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" /></svg>,
      label: 'Pricing',
      description: 'Plans & Features 💰'
    },
    {
      href: `/${lang}/login`,
      icon: () => <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M3 3a1 1 0 011 1v12a1 1 0 11-2 0V4a1 1 0 011-1zm7.707 3.293a1 1 0 010 1.414L9.414 9H17a1 1 0 110 2H9.414l1.293 1.293a1 1 0 01-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0z" clipRule="evenodd" /></svg>,
      label: 'Login',
      description: 'Access Your Account 🇰🇪'
    }
  ];

  const isActive = (href: string) => {
    // Handle root route and dashboard alias
    if (href === '/' && (pathname === '/' || pathname.startsWith('/dashboard'))) {
      return true;
    }
    // Mark parent as active for nested routes (e.g., /projects/123)
    if (href !== '/' && (pathname === href || pathname.startsWith(`${href}/`))) {
      return true;
    }
    return false;
  };

  return (
    <aside
      className={`fixed inset-y-0 left-0 z-50 w-72 flex flex-col transform transition-transform duration-300 ease-in-out ${
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
      } md:translate-x-0 bg-gradient-to-b from-neutral-900 to-neutral-800`}
    >
      {/* Header */}
      <div className="p-6 border-b border-gray-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-1">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
              </svg>
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 4a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm2 4V5h2v3H5zM3 13a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H4a1 1 0 01-1-1v-4zm2 4v-3h2v3H5zM11 4a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V4zm2 4V5h2v3h-2z" clipRule="evenodd" />
              </svg>
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Shujaa Studio</h1>
              <p className="text-xs text-gray-400">Kenya-First AI Video</p>
            </div>
          </div>

          <button
            onClick={() => setSidebarOpen(false)}
            className="md:hidden text-gray-400 hover:text-white focus:outline-none"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M18 3a1 1 0 00-1.196-.98l-10 2A1 1 0 006 5v9.114A4.369 4.369 0 005 14c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V7.82l8-1.6v5.894A4.37 4.37 0 0015 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V3z" />
            </svg>
          </button>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
        {!isClient ? (
          /* Loading skeleton to prevent hydration mismatch */
          Array.from({ length: 6 }).map((_, idx) => (
            <div key={idx} className="flex items-center px-4 py-3 rounded-lg">
              <div className="w-5 h-5 bg-gray-600 rounded animate-pulse mr-3"></div>
              <div className="flex-1">
                <div className="w-24 h-4 bg-gray-600 rounded animate-pulse mb-1"></div>
                <div className="w-32 h-3 bg-gray-700 rounded animate-pulse"></div>
              </div>
            </div>
          ))
        ) : (
          navigationItems.map((item, idx) => {
          const Icon = item.icon;
          const active = isActive(item.href);

          return (
            <Link
              key={`${item.href}-${idx}`}
              href={item.href}
              prefetch={true}
              className={`flex items-center px-4 py-3 rounded-lg transition-all duration-200 group cursor-pointer relative ${
                active
                  ? 'bg-gradient-to-r from-green-600 to-blue-600 text-white shadow-lg'
                  : 'text-gray-300 hover:bg-gray-700 hover:text-white'
              }`}
              style={{ pointerEvents: 'auto', zIndex: 1 }}
              aria-current={active ? 'page' : undefined}
              onClick={() => {
                // Close sidebar on mobile
                setSidebarOpen(false);
              }}
            >
              <Icon />
              <div className="flex flex-col ml-3">
                <div className={`font-medium ${active ? 'text-white' : 'text-gray-300 group-hover:text-white'}`}>
                  {item.label}
                </div>
                <div className={`text-xs ${active ? 'text-green-100' : 'text-gray-500 group-hover:text-gray-400'}`}>
                  {item.description}
                </div>
              </div>
            </Link>
          );
        })
        )}
      </nav>

      {/* Cultural Footer */}
      <div className="p-4 pb-6 border-t border-gray-700">
        <div className="bg-gradient-to-r from-green-600 via-red-600 to-black p-4 rounded-lg text-white text-center">
          <div className="flex items-center justify-center space-x-2 mb-2">
            <svg className="w-5 h-5 text-yellow-300" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM4.332 8.027a6.012 6.012 0 011.912-2.706C6.512 5.73 6.974 6 7.5 6A1.5 1.5 0 019 7.5V8a2 2 0 004 0 2 2 0 011.523-1.943A5.977 5.977 0 0116 10c0 .34-.028.675-.083 1H15a2 2 0 00-2 2v2.197A5.973 5.973 0 0110 16v-2a2 2 0 00-2-2 2 2 0 01-2-2 2 2 0 00-1.668-1.973z" clipRule="evenodd" />
            </svg>
            <span className="font-medium">Proudly Kenyan</span>
          </div>
          <p className="text-xs text-green-100">
            Empowering African storytellers worldwide
          </p>
        </div>
      </div>
    </aside>
  );
}

