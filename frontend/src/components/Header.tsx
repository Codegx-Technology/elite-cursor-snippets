'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
// Icons replaced with inline SVGs to avoid react-icons dependency issues
import LoadingStates from '@/components/ui/LoadingStates';
import ErrorStates from '@/components/ui/ErrorStates';
import { useAuth } from '@/context/AuthContext';
import DevAutoLogin from '@/components/DevAutoLogin';

// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + refactorintent
// [CONTEXT]: Enterprise header with Kenya-first design and mobile-first responsiveness
// [GOAL]: Create beautiful, functional header with search, notifications, and cultural elements
// [TASK]: Implement header with proper mobile optimization, touch-friendly interactions

interface HeaderProps {
  isSidebarOpen: boolean;
  setSidebarOpen: (isOpen: boolean) => void;
}

export default function Header({ isSidebarOpen, setSidebarOpen }: HeaderProps) {
  const { logout } = useAuth();
  const [showNotifications, setShowNotifications] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showDevMode, setShowDevMode] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState<{ name: string; email: string } | null>(null);
  const [isClient, setIsClient] = useState(false);
  const [showSuperAdminLogin, setShowSuperAdminLogin] = useState(false);
  const [superAdminCredentials, setSuperAdminCredentials] = useState({ username: '', password: '' });
  const router = useRouter();

  // Superadmin login function
  const handleSuperAdminLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/superadmin/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username: superAdminCredentials.username,
          password: superAdminCredentials.password,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('jwt_token', data.access_token);
        setShowSuperAdminLogin(false);
        setSuperAdminCredentials({ username: '', password: '' });
        router.push('/admin/dashboard');
      } else {
        alert('Invalid superadmin credentials');
      }
    } catch (error) {
      console.error('Superadmin login error:', error);
      alert('Login failed. Please try again.');
    }
  };

  useEffect(() => {
    // Set client-side flag to prevent hydration mismatch
    setIsClient(true);

    // Check authentication status only on client side
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('jwt_token');
      if (token) {
        setIsLoggedIn(true);
        // Mock user data - in real app, fetch from API
        setUser({ name: 'John Kamau', email: 'john@example.com' });
      }
    }
  }, []);

  const handleLogout = () => {
    setShowUserMenu(false);
    logout();
  };

  const notifications = [
    {
      id: 1,
      type: 'success',
      message: 'Kenya Tourism video generated successfully',
      time: '2 min ago',
      unread: true
    },
    {
      id: 2,
      type: 'info',
      message: 'New cultural preset available: Coastal Beauty',
      time: '1 hour ago',
      unread: true
    },
    {
      id: 3,
      type: 'warning',
      message: 'Storage usage at 85%',
      time: '3 hours ago',
      unread: false
    }
  ];

  const unreadCount = notifications.filter(n => n.unread).length;

  return (
    <header className="sticky top-0 z-40 bg-white shadow-lg border-b border-gray-200 px-3 sm:px-4 lg:px-6 py-3 sm:py-4"
    >
      <div className="flex items-center justify-between">
        {/* Left Section */}
        <div className="flex items-center space-x-2 sm:space-x-4">
          {/* Mobile Menu Button - Fixed hamburger icon */}
          <button
            className="md:hidden p-3 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200 text-gray-700"
            onClick={() => setSidebarOpen(!isSidebarOpen)}
            aria-label={isSidebarOpen ? 'Close menu' : 'Open menu'}
          >
            {isSidebarOpen ? (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            ) : (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            )}
          </button>

          {/* Kenya Flag & Title - Mobile optimized */}
          <div className="flex items-center space-x-2 sm:space-x-3">
            <div className="flex items-center space-x-1">
              <svg className="w-5 h-5 text-gray-700" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" />
              </svg>
              <span className="text-red-600 text-sm">•</span>
              <span className="text-black text-sm">•</span>
            </div>
            <div className="hidden sm:block">
              <h1 className="text-lg sm:text-xl font-bold text-gray-900">
                Shujaa Studio
              </h1>
              <p className="text-xs hidden md:block text-gray-600">
                Kenya-First AI Video Platform
              </p>
            </div>
            {/* Mobile-only compact title */}
            <div className="sm:hidden">
              <h1 className="text-lg font-bold text-gray-900">
                Shujaa
              </h1>
            </div>
          </div>

          {/* Quick Actions - Only show if logged in */}
          {isLoggedIn && (
            <div className="hidden lg:flex items-center space-x-2">
              <Link href="/generate" className="btn-primary px-4 py-2 text-sm flex items-center space-x-2 hover:no-underline">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 01-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
                </svg>
                <span>New Video</span>
              </Link>
              <Link href="/video-generate" className="btn-elite px-4 py-2 text-sm flex items-center space-x-2 text-white hover:no-underline">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 0010 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                </svg>
                <span>Quick Generate</span>
              </Link>
            </div>
          )}
        </div>

        {/* Center Section - Search */}
        <div className="hidden md:flex flex-1 max-w-md mx-8">
          <div className="relative w-full">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
              </svg>
            </div>
            <input
              type="text"
              className="form-input w-full pl-10 pr-12 py-2 text-sm"
              placeholder="Search projects, videos, or templates..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            {/* Superadmin Gear Icon */}
            <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
              <button
                onClick={() => setShowSuperAdminLogin(true)}
                className="text-gray-400 hover:text-gray-600 transition-colors duration-200"
                title="Superadmin Access"
              >
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clipRule="evenodd" />
                </svg>
              </button>
            </div>

            {/* Dev Mode Icon - Only show in development */}
            {process.env.NODE_ENV === 'development' && (
              <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                <div className="relative">
                  <button
                    onClick={() => setShowDevMode(!showDevMode)}
                    className="p-1 rounded-full hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
                    title="Dev Mode - Quick Login"
                  >
                    <svg className="w-4 h-4 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clipRule="evenodd" />
                    </svg>
                  </button>

                  {/* Dev Mode Popup */}
                  {showDevMode && (
                    <div className="absolute right-0 top-full mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
                      <div className="p-4">
                        <DevAutoLogin />
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Right Section - Mobile optimized */}
        <div className="flex items-center space-x-2 sm:space-x-4">
          {/* Language Selector */}
          <div className="hidden lg:flex items-center space-x-1 text-sm text-gray-600">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M5 3a2 2 0 00-2 2v10a2 2 0 110 4h2a2 2 0 110-4V5a2 2 0 012-2zm8 0a2 2 0 110 4h2a2 2 0 110-4V5a2 2 0 012-2zm-1 11h.01" clipRule="evenodd" />
            </svg>
            <span>EN/SW</span>
          </div>

          {/* Notifications - Only show if logged in */}
          {isLoggedIn && (
            <div className="relative">
              <button
                className="p-3 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 relative transition-colors duration-200 text-gray-700"
                onClick={() => setShowNotifications(!showNotifications)}
                aria-label="Notifications"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" />
                </svg>
                {unreadCount > 0 && (
                  <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center font-medium">
                    {unreadCount}
                  </span>
                )}
              </button>

              {/* Notifications Dropdown - Mobile responsive */}
              {showNotifications && (
                <div className="absolute right-0 mt-2 w-80 sm:w-96 bg-white rounded-lg shadow-lg border border-gray-200 z-50 max-w-[calc(100vw-2rem)]">
                  <div className="p-4 border-b border-gray-200">
                    <h3 className="font-semibold text-gray-800">Notifications 🇰🇪</h3>
                  </div>
                  <div className="max-h-64 overflow-y-auto">
                    {notifications.map((notification) => (
                      <div key={notification.id} className={`p-4 border-b border-gray-100 hover:bg-gray-50 transition-colors duration-200 ${notification.unread ? 'bg-blue-50' : ''}`}>
                        <p className="text-sm text-gray-800 leading-relaxed">{notification.message}</p>
                        <p className="text-xs text-gray-500 mt-1">{notification.time}</p>
                      </div>
                    ))}
                  </div>
                  <div className="p-3 text-center border-t border-gray-200">
                    <button className="text-blue-600 hover:text-blue-800 text-sm font-medium transition-colors duration-200">
                      View all notifications
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Authentication Section - Only render after client hydration */}
          {isClient && isLoggedIn ? (
            /* User Menu - Mobile optimized */
            <div className="relative">
              <button
                className="flex items-center space-x-1 sm:space-x-2 p-2 sm:p-3 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200 text-gray-700"
                onClick={() => setShowUserMenu(!showUserMenu)}
                aria-label="User menu"
              >
                <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 0010 16a5.986 5.986 0 004.546-2.084A5 5 0 0010 11z" clipRule="evenodd" />
                </svg>
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>

              {/* User Dropdown - Mobile responsive */}
              {showUserMenu && (
                <div className="absolute right-0 mt-2 w-48 sm:w-56 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
                  <div className="p-4 border-b border-gray-200">
                    <p className="font-semibold text-gray-800">{user?.name || 'User'}</p>
                    <p className="text-sm text-gray-500 truncate">{user?.email || 'user@example.com'}</p>
                  </div>
                  <div className="py-2">
                    <Link href="/profile" className="block px-4 py-3 text-sm text-gray-700 hover:bg-gray-100 transition-colors duration-200">Profile</Link>
                    <Link href="/settings" className="block px-4 py-3 text-sm text-gray-700 hover:bg-gray-100 transition-colors duration-200">Settings</Link>
                    <Link href="/pricing" className="block px-4 py-3 text-sm text-gray-700 hover:bg-gray-100 transition-colors duration-200">Billing</Link>
                    <hr className="my-2" />
                    <button 
                      onClick={handleLogout}
                      className="w-full text-left px-4 py-3 text-sm text-gray-700 hover:bg-gray-100 transition-colors duration-200 flex items-center space-x-2"
                    >
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clipRule="evenodd" />
                      </svg>
                      <span>Sign out</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          ) : isClient ? (
            /* Login/Register buttons when logged out */
            <div className="flex items-center space-x-2">
              <Link href="/login" className="btn-primary px-4 py-2 text-sm hover:no-underline">
                Login 🇰🇪
              </Link>
              <Link href="/register" className="btn-elite px-4 py-2 text-sm text-white hover:no-underline hidden sm:block">
                Register
              </Link>
            </div>
          ) : (
            /* Loading placeholder to prevent hydration mismatch */
            <div className="flex items-center space-x-2">
              <div className="w-16 h-8 bg-gray-200 rounded animate-pulse"></div>
              <div className="w-20 h-8 bg-gray-200 rounded animate-pulse hidden sm:block"></div>
            </div>
          )}
        </div>
      </div>

      {/* Mobile Search - Only show if logged in and client-side */}
      {isClient && isLoggedIn && (
        <div className="md:hidden mt-3 sm:mt-4">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg className="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
              </svg>
            </div>
            <input
              type="text"
              className="form-input w-full pl-10 pr-4 py-3 text-base"
              placeholder="Search projects, videos..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{ fontSize: '16px' }} // Prevents zoom on iOS
            />
          </div>
        </div>
      )}

      {/* Superadmin Login Modal */}
      {showSuperAdminLogin && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-96 max-w-md mx-4">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-gray-900">🇰🇪 Superadmin Access</h3>
              <button
                onClick={() => {
                  setShowSuperAdminLogin(false);
                  setSuperAdminCredentials({ username: '', password: '' });
                }}
                className="text-gray-400 hover:text-gray-600"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <form onSubmit={handleSuperAdminLogin} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
                <input
                  type="text"
                  value={superAdminCredentials.username}
                  onChange={(e) => setSuperAdminCredentials(prev => ({ ...prev, username: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                  placeholder="Enter superadmin username"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                <input
                  type="password"
                  value={superAdminCredentials.password}
                  onChange={(e) => setSuperAdminCredentials(prev => ({ ...prev, password: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                  placeholder="Enter superadmin password"
                  required
                />
              </div>

              <div className="flex space-x-3 pt-2">
                <button
                  type="button"
                  onClick={() => {
                    setShowSuperAdminLogin(false);
                    setSuperAdminCredentials({ username: '', password: '' });
                  }}
                  className="flex-1 px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
                >
                  Login
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </header>
  );
}

