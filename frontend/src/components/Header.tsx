'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import {
  FaSearch,
  FaBell,
  FaUserCircle,
  FaVideo,
  FaPlus,
  FaGlobe,
  FaFlag,
  FaChevronDown,
  FaSignOutAlt
} from 'react-icons/fa';
import LoadingStates from '@/components/ui/LoadingStates';
import ErrorStates from '@/components/ui/ErrorStates';
import { useAuth } from '@/context/AuthContext';

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
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState<{ name: string; email: string } | null>(null);
  const router = useRouter();

  useEffect(() => {
    // Check authentication status
    const token = localStorage.getItem('jwt_token');
    if (token) {
      setIsLoggedIn(true);
      // Mock user data - in real app, fetch from API
      setUser({ name: 'John Kamau', email: 'john@example.com' });
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
          {/* Mobile Menu Button - Improved touch target */}
          <button
            className="md:hidden p-3 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
            onClick={() => setSidebarOpen(!isSidebarOpen)}
            aria-label={isSidebarOpen ? 'Close menu' : 'Open menu'}
          >
            <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {isSidebarOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>

          {/* Kenya Flag & Title - Mobile optimized */}
          <div className="flex items-center space-x-2 sm:space-x-3">
            <div className="flex items-center space-x-1">
              <FaFlag className="text-green-600 text-lg sm:text-xl" />
              <span className="text-red-600 text-sm">•</span>
              <span className="text-black text-sm">•</span>
            </div>
            <div className="hidden sm:block">
              <h1 className="text-lg sm:text-xl font-bold" style={{ color: 'var(--charcoal-text)' }}>
                Shujaa Studio
              </h1>
              <p className="text-xs hidden md:block" style={{ color: 'var(--soft-text)' }}>
                Kenya-First AI Video Platform
              </p>
            </div>
            {/* Mobile-only compact title */}
            <div className="sm:hidden">
              <h1 className="text-lg font-bold" style={{ color: 'var(--charcoal-text)' }}>
                Shujaa
              </h1>
            </div>
          </div>

          {/* Quick Actions - Only show if logged in */}
          {isLoggedIn && (
            <div className="hidden lg:flex items-center space-x-2">
              <Link href="/generate" className="btn-primary px-4 py-2 text-sm flex items-center space-x-2 hover:no-underline">
                <FaPlus />
                <span>New Video</span>
              </Link>
              <Link href="/video-generate" className="btn-elite px-4 py-2 text-sm flex items-center space-x-2 text-white hover:no-underline">
                <FaVideo />
                <span>Quick Generate</span>
              </Link>
            </div>
          )}
        </div>

        {/* Center Section - Search */}
        <div className="hidden md:flex flex-1 max-w-md mx-8">
          <div className="relative w-full">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <FaSearch className="text-gray-400" />
            </div>
            <input
              type="text"
              className="form-input w-full pl-10 pr-4 py-2 text-sm"
              placeholder="Search projects, videos, or templates..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>

        {/* Right Section - Mobile optimized */}
        <div className="flex items-center space-x-2 sm:space-x-4">
          {/* Language Selector */}
          <div className="hidden lg:flex items-center space-x-1 text-sm" style={{ color: 'var(--soft-text)' }}>
            <FaGlobe />
            <span>EN/SW</span>
          </div>

          {/* Notifications - Only show if logged in */}
          {isLoggedIn && (
            <div className="relative">
              <button
                className="p-3 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 relative transition-colors duration-200"
                onClick={() => setShowNotifications(!showNotifications)}
                aria-label="Notifications"
              >
                <FaBell className="text-gray-600" size={18} />
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

          {/* Authentication Section */}
          {isLoggedIn ? (
            /* User Menu - Mobile optimized */
            <div className="relative">
              <button
                className="flex items-center space-x-1 sm:space-x-2 p-2 sm:p-3 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
                onClick={() => setShowUserMenu(!showUserMenu)}
                aria-label="User menu"
              >
                <FaUserCircle className="text-gray-600" size={20} />
                <FaChevronDown className="text-gray-400 text-xs hidden sm:block" />
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
                      <FaSignOutAlt className="text-gray-500" />
                      <span>Sign out</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          ) : (
            /* Login/Register buttons when logged out */
            <div className="flex items-center space-x-2">
              <Link href="/login" className="btn-primary px-4 py-2 text-sm hover:no-underline">
                Login 🇰🇪
              </Link>
              <Link href="/register" className="btn-elite px-4 py-2 text-sm text-white hover:no-underline hidden sm:block">
                Register
              </Link>
            </div>
          )}
        </div>
      </div>

      {/* Mobile Search - Only show if logged in */}
      {isLoggedIn && (
        <div className="md:hidden mt-3 sm:mt-4">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <FaSearch className="text-gray-400" />
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
    </header>
  );
}
