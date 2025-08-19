import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button'; // Assuming a Button component exists
import axios from 'axios';
import { motion } from 'framer-motion'; // For smooth fade-in

interface Dependency {
  name: string;
  installed_version: string;
  required_range: string;
  status: 'HEALTHY' | 'OUTDATED' | 'MISSING' | 'UNSUPPORTED';
  message: string;
}

const DependencyWatcher: React.FC = () => {
  const [dependencies, setDependencies] = useState<Dependency[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStatus = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get('/api/dependencies/status');
      setDependencies(response.data.dependencies);
    } catch (err) {
      console.error('Failed to fetch dependency status:', err);
      setError('Failed to load dependency status. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
  }, []);

  const getBadgeVariant = (status: Dependency['status']) => {
    switch (status) {
      case 'HEALTHY':
        return 'default'; // Typically green or primary
      case 'OUTDATED':
        return 'warning'; // Typically yellow or orange
      case 'MISSING':
        return 'destructive'; // Typically red
      case 'UNSUPPORTED':
        return 'secondary'; // Typically gray or light blue
      default:
        return 'outline';
    }
  };

  return (
    <Card className="rounded-2xl shadow-lg p-4">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-2xl font-bold">Dependency Health</CardTitle>
        <Button onClick={fetchStatus} disabled={loading}>
          {loading ? 'Refreshing...' : 'Refresh'}
        </Button>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="text-center py-8">Loading dependency status...</div>
        ) : error ? (
          <div className="text-center py-8 text-red-500">{error}</div>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Installed Version</TableHead>
                  <TableHead>Required Range</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Message</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {dependencies.map((dep, index) => (
                  <TableRow key={dep.name} className={index % 2 === 0 ? 'bg-gray-50' : ''}>
                    <TableCell className="font-medium">{dep.name}</TableCell>
                    <TableCell>{dep.installed_version}</TableCell>
                    <TableCell>{dep.required_range}</TableCell>
                    <TableCell>
                      <Badge variant={getBadgeVariant(dep.status)}>{dep.status}</Badge>
                    </TableCell>
                    <TableCell>{dep.message}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </motion.div>
        )}
      </CardContent>
    </Card>
  );
};

export default DependencyWatcher;
