import React from 'react';
import DependencyWatcher from '@/admin/components/DependencyWatcher';
import LoadingStates from '@/components/ui/LoadingStates';
import ErrorStates from '@/components/ui/ErrorStates';
import Card from '@/components/Card';

const AdminDashboard: React.FC = () => {
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6">Admin Dashboard</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Other admin components can go here */}
        <DependencyWatcher />
      </div>
    </div>
  );
};

export default AdminDashboard;
