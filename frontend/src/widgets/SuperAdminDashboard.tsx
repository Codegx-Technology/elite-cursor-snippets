"use client";

import React from 'react';
import Link from 'next/link';
import { FaUsers, FaBuilding, FaBoxOpen, FaCog } from 'react-icons/fa';
import Card from '@/components/Card';

interface SuperAdminDashboardProps {
  userRole: string;
}

const SuperAdminDashboard: React.FC<SuperAdminDashboardProps> = ({ userRole }) => {
  if (userRole !== 'admin') {
    return <p>You do not have access to this dashboard.</p>;
  }

  const navItems = [
    { href: '/admin/users', label: 'User Management', icon: <FaUsers /> },
    { href: '/admin/tenants', label: 'Tenant Management', icon: <FaBuilding /> },
    { href: '/admin/models', label: 'Model Management', icon: <FaBoxOpen /> },
    { href: '/admin/settings', label: 'System Settings', icon: <FaCog /> },
  ];

  return (
    <Card>
      <div className="p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Admin Controls</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {navItems.map((item) => (
            <Link href={item.href} key={item.href}>
              <div className="bg-gray-50 hover:bg-gray-100 p-6 rounded-lg shadow-sm transition-all duration-200 flex items-center space-x-4 cursor-pointer">
                <div className="text-2xl text-green-600">{item.icon}</div>
                <div>
                  <p className="font-semibold text-gray-700">{item.label}</p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </Card>
  );
};

export default SuperAdminDashboard;
