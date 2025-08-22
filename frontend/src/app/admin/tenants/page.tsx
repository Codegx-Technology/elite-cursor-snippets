"use client";

import React, { useEffect, useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import {
  Table,
  TableHeader,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { useToast } from '@/components/ui/use-toast';
import { FaEdit, FaTrash, FaPlus } from 'react-icons/fa';
import { useTenantManagement, TenantData } from '@/hooks/useTenantManagement';

export default function AdminTenantsPage() {
  const { user, isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const { tenants, loadTenants, isLoading: loadingTenants, error, deleteTenant } = useTenantManagement();
  const { toast } = useToast();

  useEffect(() => {
    if (!isLoading && (!isAuthenticated || user?.role !== 'admin')) {
      router.push('/login');
    } else if (isAuthenticated && user?.role === 'admin') {
      loadTenants();
    }
  }, [isLoading, isAuthenticated, user, router, loadTenants]);

  const handleDeleteTenant = async (tenantId: number) => {
    if (!confirm('Are you sure you want to delete this tenant?')) return;

    try {
      await deleteTenant(tenantId);
      toast({
        title: "Success",
        description: "Tenant deleted successfully.",
      });
    } catch (err: any) {
      console.error('Failed to delete tenant:', err);
      toast({
        title: "Error",
        description: err.message || 'Failed to delete tenant.',
        variant: "destructive",
      });
    }
  };

  if (isLoading || (!isAuthenticated && !loadingTenants)) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <span className="text-gray-600 font-medium">Loading authentication...</span>
        </div>
      </div>
    );
  }

  if (!isAuthenticated || user?.role !== 'admin') {
    return null; // Should have been redirected by useEffect
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Admin Tenant Management</h1>
        <Button onClick={() => router.push('/admin/tenants/create')}>
          <FaPlus className="mr-2" /> Create New Tenant
        </Button>
      </div>

      {loadingTenants ? (
        <div className="text-center py-8">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <span className="text-gray-600 font-medium">Loading tenants...</span>
        </div>
      ) : error ? (
        <div className="text-center py-8 text-red-500">{error}</div>
      ) : (
        <div className="overflow-x-auto rounded-lg shadow-md">
          <Table className="min-w-full bg-white">
            <TableHeader>
              <TableRow>
                <TableHead className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</TableHead>
                <TableHead className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</TableHead>
                <TableHead className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Active</TableHead>
                <TableHead className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Plan</TableHead>
                <TableHead className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {tenants.map((tenant) => (
                <TableRow key={tenant.id} className="border-b border-gray-200 hover:bg-gray-50">
                  <TableCell className="py-4 px-4 whitespace-nowrap text-sm font-medium text-gray-900">{tenant.id}</TableCell>
                  <TableCell className="py-4 px-4 whitespace-nowrap text-sm text-gray-700">{tenant.name}</TableCell>
                  <TableCell className="py-4 px-4 whitespace-nowrap text-sm text-gray-700">{tenant.is_active ? 'Yes' : 'No'}</TableCell>
                  <TableCell className="py-4 px-4 whitespace-nowrap text-sm text-gray-700">{tenant.plan}</TableCell>
                  <TableCell className="py-4 px-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => router.push(`/admin/tenants/${tenant.id}/edit`)}
                        title="Edit Tenant"
                      >
                        <FaEdit />
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleDeleteTenant(tenant.id)}
                        title="Delete Tenant"
                      >
                        <FaTrash />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  );
}
