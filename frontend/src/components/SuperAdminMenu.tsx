"use client";

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';

export default function SuperAdminMenu() {
  const { user, isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return null; // Or a loading spinner
  }

  if (!isAuthenticated || user?.role !== 'admin') {
    return null; // Don't render if not authenticated or not an admin
  }

  return (
    <div className="bg-gray-800 text-white p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <span className="font-bold text-lg">Super Admin Panel</span>
        <nav>
          <ul className="flex space-x-4">
            <li>
              <Link href="/admin/dashboard" className="hover:text-gray-300">
                Dashboard
              </Link>
            </li>
            <li>
              <Link href="/admin/users" className="hover:text-gray-300">
                Users
              </Link>
            </li>
            <li>
              <Link href="/admin/tenants" className="hover:text-gray-300">
                Tenants
              </Link>
            </li>
            {/* Add more admin links here */}
          </ul>
        </nav>
      </div>
    </div>
  );
}
