'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  FaHome,
  FaProjectDiagram,
  FaCog,
  FaVideo,
  FaImages,
  FaMusic,
  FaUsers,
  FaChartLine,
  FaFlag,
  FaMountain,
  FaGlobe,
  FaCreditCard,
  FaNewspaper,
  FaShieldAlt,
  FaDownload,
  FaBox,
  FaKey,
  FaPlug
} from 'react-icons/fa';

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

  // Debug logging (guarded to avoid noisy prod consoles)
  if (process.env.NODE_ENV !== 'production') {
    // eslint-disable-next-line no-console
    console.log('Current pathname:', pathname);
  }

  const navigationItems = [
    {
      href: '/',
      icon: FaHome,
      label: 'Dashboard',
      description: 'Overview & Stats'
    },
    {
      href: '/admin/reporting',
      icon: FaShieldAlt,
      label: 'Reporting',
      description: 'Super Admin Health'
    },
    {
      href: '/admin/users',
      icon: FaUsers,
      label: 'User Management',
      description: 'Manage users'
    },
    {
      href: '/admin/roles',
      icon: FaKey,
      label: 'Role Management',
      description: 'Manage user roles'
    },
    {
      href: '/video-generate',
      icon: FaVideo,
      label: 'Generate Video',
      description: 'Create Kenya-first content'
    },
    {
      href: '/news-generate',
      icon: FaNewspaper,
      label: 'News Videos',
      description: 'Transform news into videos'
    },
    {
      href: '/projects',
      icon: FaProjectDiagram,
      label: 'Projects',
      description: 'Manage your creations'
    },
    {
      href: '/gallery',
      icon: FaImages,
      label: 'Gallery',
      description: 'Browse generated content'
    },
    {
      href: '/audio-studio',
      icon: FaMusic,
      label: 'Audio Studio',
      description: 'Voice & music creation'
    },
    {
      href: '/admin/roles',
      icon: FaKey,
      label: 'Role Management',
      description: 'Manage user roles'
    },
    {
      href: '/admin/api-integration',
      icon: FaPlug,
      label: 'API & Integrations',
      description: 'Manage API keys and integrations'
    },
    {
      href: '/team',
      icon: FaUsers,
      label: 'Team',
      description: 'Collaboration tools'
    },
    {
      href: '/pricing',
      icon: FaCreditCard,
      label: 'Pricing',
      description: 'Plans & billing'
    },
    {
      href: '/settings',
      icon: FaCog,
      label: 'Settings',
      description: 'Preferences & config'
    },
    {
      href: '/settings/local-models',
      icon: FaDownload,
      label: 'Local Models',
      description: 'Manage local models'
    },
    {
      href: '/settings/storage-management',
      icon: FaBox,
      label: 'Storage Management',
      description: 'Manage storage'
    },
    {
      href: '/profile',
      icon: FaUsers,
      label: 'Profile',
      description: 'Manage your profile'
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
              <FaFlag className="text-2xl text-green-400" />
              <FaMountain className="text-2xl text-yellow-400" />
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
            <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
        {navigationItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.href);

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center px-4 py-3 rounded-lg transition-all duration-200 group ${
                active
                  ? 'bg-gradient-to-r from-green-600 to-blue-600 text-white shadow-lg'
                  : 'text-gray-300 hover:bg-gray-700 hover:text-white'
              }`}
              aria-current={active ? 'page' : undefined}
              onClick={() => {
                // Close sidebar immediately on mobile; Next.js handles route transitions
                setSidebarOpen(false);
              }}
            >
              <Icon className={`mr-3 text-lg ${active ? 'text-white' : 'text-gray-400 group-hover:text-white'}`} />
              <div className="flex-1">
                <div className={`font-medium ${active ? 'text-white' : 'text-gray-300 group-hover:text-white'}`}>
                  {item.label}
                </div>
                <div className={`text-xs ${active ? 'text-green-100' : 'text-gray-500 group-hover:text-gray-400'}`}>
                  {item.description}
                </div>
              </div>
            </Link>
          );
        })}
      </nav>

      {/* Cultural Footer */}
      <div className="p-4 pb-6 border-t border-gray-700">
        <div className="bg-gradient-to-r from-green-600 via-red-600 to-black p-4 rounded-lg text-white text-center">
          <div className="flex items-center justify-center space-x-2 mb-2">
            <FaGlobe className="text-yellow-300" />
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
