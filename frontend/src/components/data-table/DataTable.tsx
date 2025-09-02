'use client';

// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Enterprise-grade DataTable with Kenya-first design system integration
// [GOAL]: Enhance existing DataTable with design tokens and cultural authenticity
// [TASK]: Phase 2.1a - Advanced Data Components with mobile-first responsive design

import React, { useState, useMemo } from 'react';
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from '@/components/ui/table';
import { Button, Input } from '@/components/ui/design-system';
import { colors, spacing, typography } from '@/config/designTokens';
import { cn } from '@/lib/utils';
import { FaSortUp, FaSortDown, FaSort, FaMagnifyingGlass, FaFilter } from 'react-icons/fa6';

interface ColumnDef<T> {
  accessorKey: keyof T;
  header: string | React.ReactNode;
  cell?: (row: T) => React.ReactNode;
  enableSorting?: boolean;
}

interface DataTableProps<T> {
  columns: ColumnDef<T>[];
  data: T[];
  pageSize?: number;
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  searchPlaceholder?: string;
  emptyStateMessage?: string;
  className?: string;
}

export function DataTable<T>({
  columns,
  data,
  pageSize = 10,
  variant = 'default',
  searchPlaceholder = 'Tafuta...',
  emptyStateMessage = 'Hakuna matokeo.',
  className
}: DataTableProps<T>) {
  const [sortBy, setSortBy] = useState<keyof T | null>(null);
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc');
  const [currentPage, setCurrentPage] = useState(1);

  const sortedData = useMemo(() => {
    if (!sortBy) return data;

    return [...data].sort((a, b) => {
      const aValue = a[sortBy];
      const bValue = b[sortBy];

      if (aValue === null || aValue === undefined) return sortDirection === 'asc' ? 1 : -1;
      if (bValue === null || bValue === undefined) return sortDirection === 'asc' ? -1 : 1;

      if (typeof aValue === 'string' && typeof bValue === 'string') {
        return sortDirection === 'asc'
          ? aValue.localeCompare(bValue)
          : bValue.localeCompare(aValue);
      }

      if (typeof aValue === 'number' && typeof bValue === 'number') {
        return sortDirection === 'asc' ? aValue - bValue : bValue - aValue;
      }

      // Fallback for other types, convert to string
      return sortDirection === 'asc'
        ? String(aValue).localeCompare(String(bValue))
        : String(bValue).localeCompare(String(aValue));
    });
  }, [data, sortBy, sortDirection]);

  const [searchTerm, setSearchTerm] = useState('');

  const filteredData = useMemo(() => {
    if (!searchTerm) return sortedData;

    const lowercasedSearchTerm = searchTerm.toLowerCase();
    return sortedData.filter(row =>
      columns.some(column => {
        const value = row[column.accessorKey];
        return String(value).toLowerCase().includes(lowercasedSearchTerm);
      })
    );
  }, [sortedData, searchTerm, columns]);

  const paginatedData = useMemo(() => {
    const startIndex = (currentPage - 1) * pageSize;
    const endIndex = startIndex + pageSize;
    return filteredData.slice(startIndex, endIndex); // Use filteredData here
  }, [filteredData, currentPage, pageSize]);

  const totalPages = Math.ceil(filteredData.length / pageSize); // totalPages should be based on filteredData

  const handleSort = (accessorKey: keyof T) => {
    if (sortBy === accessorKey) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(accessorKey);
      setSortDirection('asc');
    }
  };

  const getSortIcon = (accessorKey: keyof T) => {
    if (sortBy !== accessorKey) {
      return <FaSort className="ml-2 text-gray-400" />;
    }
    return sortDirection === 'asc' ? (
      <FaSortUp className="ml-2" />
    ) : (
      <FaSortDown className="ml-2" />
    );
  };

  const variantClasses = {
    default: 'border-gray-200',
    kenya: `border-[${colors.kenya.green}] border-opacity-20`,
    cultural: `border-[${colors.cultural.gold}] border-opacity-30`,
    elite: 'border-purple-200'
  };

  return (
    <div className={cn('space-y-4', className)}>
      {/* Enhanced Search with Kenya-first design */}
      <div className="relative">
        <FaSearch className={cn(
          'absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400',
          variant === 'kenya' && `text-[${colors.kenya.green}]`,
          variant === 'cultural' && `text-[${colors.cultural.gold}]`
        )} />
        <input
          type="text"
          placeholder={searchPlaceholder}
          value={searchTerm}
          onChange={(e) => {
            setSearchTerm(e.target.value);
            setCurrentPage(1);
          }}
          className={cn(
            'w-full pl-10 pr-4 py-3 border rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-1',
            variant === 'kenya' ? `border-gray-300 focus:border-[${colors.kenya.green}] focus:ring-green-500` :
            variant === 'cultural' ? `border-gray-300 focus:border-[${colors.cultural.gold}] focus:ring-yellow-500` :
            'border-gray-300 focus:border-blue-500 focus:ring-blue-500',
            'bg-white placeholder:text-gray-400'
          )}
        />
      </div>
      {/* Enhanced Table with cultural design */}
      <div className={cn(
        'rounded-lg border overflow-hidden shadow-sm',
        variantClasses[variant],
        'mobile-responsive-table'
      )}>
        <div className="overflow-x-auto">
          <Table className="min-w-full">
          <TableHeader>
            <TableRow>
              {columns.map((column) => (
                <TableHead key={String(column.accessorKey)}>
                  {column.enableSorting ? (
                    <Button
                      variant={variant === 'kenya' ? 'kenya' : variant === 'cultural' ? 'cultural' : 'secondary'}
                      size="sm"
                      onClick={() => handleSort(column.accessorKey)}
                      className="flex items-center hover:scale-105 transition-transform"
                    >
                      {column.header}
                      {getSortIcon(column.accessorKey)}
                    </Button>
                  ) : (
                    column.header
                  )}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {paginatedData.map((row, rowIndex) => (
              <TableRow key={rowIndex}>
                {columns.map((column) => (
                  <TableCell key={String(column.accessorKey)}>
                    {column.cell ? column.cell(row) : String(row[column.accessorKey])}
                  </TableCell>
                ))}
              </TableRow>
            ))}
            {paginatedData.length === 0 && (
              <TableRow>
                <TableCell colSpan={columns.length} className="h-32 text-center">
                  <div className="flex flex-col items-center space-y-2">
                    <FaFilter className={cn(
                      'text-4xl text-gray-300',
                      variant === 'kenya' && `text-[${colors.kenya.green}] opacity-30`,
                      variant === 'cultural' && `text-[${colors.cultural.gold}] opacity-30`
                    )} />
                    <p className={cn(
                      'text-gray-500',
                      `text-[${typography.fontSizes.sm}]`
                    )}>
                      {emptyStateMessage}
                    </p>
                  </div>
                </TableCell>
              </TableRow>
            )}
          </TableBody>
          </Table>
        </div>
      </div>
      {/* Enhanced Pagination with Kenya-first design */}
      <div className="flex flex-col sm:flex-row items-center justify-between space-y-2 sm:space-y-0 sm:space-x-2 py-4">
        <div className={cn(
          'text-gray-600',
          `text-[${typography.fontSizes.sm}]`
        )}>
          Onyesha {Math.min((currentPage - 1) * pageSize + 1, filteredData.length)} - {Math.min(currentPage * pageSize, filteredData.length)} ya {filteredData.length}
        </div>
        <div className="flex items-center space-x-2">
          <Button
            variant={variant === 'kenya' ? 'kenya' : variant === 'cultural' ? 'cultural' : 'secondary'}
            size="sm"
            onClick={() => setCurrentPage((prev) => Math.max(1, prev - 1))}
            disabled={currentPage === 1}
            className="min-w-[80px]"
          >
            Nyuma
          </Button>
          <span className={cn(
            'px-3 py-1 rounded-md bg-gray-100 text-gray-700 font-medium',
            `text-[${typography.fontSizes.sm}]`,
            variant === 'kenya' && 'bg-green-50 text-green-700',
            variant === 'cultural' && 'bg-yellow-50 text-yellow-700'
          )}>
            {currentPage} / {totalPages}
          </span>
          <Button
            variant={variant === 'kenya' ? 'kenya' : variant === 'cultural' ? 'cultural' : 'secondary'}
            size="sm"
            onClick={() => setCurrentPage((prev) => Math.min(totalPages, prev + 1))}
            disabled={currentPage === totalPages}
            className="min-w-[80px]"
          >
            Mbele
          </Button>
        </div>
      </div>
    </div>
  );
}

