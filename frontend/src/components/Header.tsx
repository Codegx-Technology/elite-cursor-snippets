'use client';

import { useState } from 'react';
import {
  FaSearch,
  FaBell,
  FaUserCircle,
  FaVideo,
  FaPlus,
  FaGlobe,
  FaFlag,
  FaChevronDown
} from 'react-icons/fa';

// [SNIPPET]: thinkwithai + kenyafirst + refactorclean
// [CONTEXT]: Enterprise header with Kenya-first design and advanced functionality
// [GOAL]: Create beautiful, functional header with search, notifications, and cultural elements
// [TASK]: Implement header with proper styling, dropdowns, and Kenya-themed elements

interface HeaderProps {
  isSidebarOpen: boolean;
  setSidebarOpen: (isOpen: boolean) => void;
}

export default function Header({ isSidebarOpen, setSidebarOpen }: HeaderProps) {
  const [showNotifications, setShowNotifications] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

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
    <header
      className="bg-white shadow-lg border-b border-gray-200 px-6 py-4"
      style={{
        background: 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)'
      }}
    >
      <div className="flex items-center justify-between">
        {/* Left Section */}
        <div className="flex items-center space-x-4">
          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
            onClick={() => setSidebarOpen(!isSidebarOpen)}
          >
            <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {isSidebarOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>

          {/* Kenya Flag & Title */}
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-1">
              <FaFlag className="text-green-600" />
              <span className="text-red-600">•</span>
              <span className="text-black">•</span>
            </div>
            <div className="hidden md:block">
              <h1 className="text-xl font-bold" style={{ color: 'var(--charcoal-text)' }}>
                Shujaa Studio
              </h1>
              <p className="text-xs" style={{ color: 'var(--soft-text)' }}>
                Kenya-First AI Video Platform
              </p>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="hidden lg:flex items-center space-x-2">
            <button className="btn-primary px-4 py-2 text-sm flex items-center space-x-2">
              <FaPlus />
              <span>New Video</span>
            </button>
            <button className="btn-elite px-4 py-2 text-sm flex items-center space-x-2 text-white">
              <FaVideo />
              <span>Quick Generate</span>
            </button>
          </div>
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

        {/* Right Section */}
        <div className="flex items-center space-x-4">
          {/* Language Selector */}
          <div className="hidden md:flex items-center space-x-1 text-sm" style={{ color: 'var(--soft-text)' }}>
            <FaGlobe />
            <span>EN/SW</span>
          </div>

          {/* Notifications */}
          <div className="relative">
            <button
              className="p-2 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 relative"
              onClick={() => setShowNotifications(!showNotifications)}
            >
              <FaBell className="text-gray-600" size={20} />
              {unreadCount > 0 && (
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                  {unreadCount}
                </span>
              )}
            </button>

            {/* Notifications Dropdown */}
            {showNotifications && (
              <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
                <div className="p-4 border-b border-gray-200">
                  <h3 className="font-semibold text-gray-800">Notifications</h3>
                </div>
                <div className="max-h-64 overflow-y-auto">
                  {notifications.map((notification) => (
                    <div key={notification.id} className={`p-4 border-b border-gray-100 hover:bg-gray-50 ${notification.unread ? 'bg-blue-50' : ''}`}>
                      <p className="text-sm text-gray-800">{notification.message}</p>
                      <p className="text-xs text-gray-500 mt-1">{notification.time}</p>
                    </div>
                  ))}
                </div>
                <div className="p-3 text-center border-t border-gray-200">
                  <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                    View all notifications
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* User Menu */}
          <div className="relative">
            <button
              className="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
              onClick={() => setShowUserMenu(!showUserMenu)}
            >
              <FaUserCircle className="text-gray-600" size={24} />
              <FaChevronDown className="text-gray-400 text-xs" />
            </button>

            {/* User Dropdown */}
            {showUserMenu && (
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
                <div className="p-4 border-b border-gray-200">
                  <p className="font-semibold text-gray-800">John Kamau</p>
                  <p className="text-sm text-gray-500">john@example.com</p>
                </div>
                <div className="py-2">
                  <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Profile</a>
                  <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Settings</a>
                  <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Billing</a>
                  <hr className="my-2" />
                  <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Sign out</a>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Mobile Search */}
      <div className="md:hidden mt-4">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <FaSearch className="text-gray-400" />
          </div>
          <input
            type="text"
            className="form-input w-full pl-10 pr-4 py-2 text-sm"
            placeholder="Search..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>
    </header>
  );
}
