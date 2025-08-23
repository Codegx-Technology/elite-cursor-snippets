
import type { Meta, StoryObj } from '@storybook/react';
import { DataTable } from './DataTable';

const meta: Meta<typeof DataTable> = {
  title: 'Components/DataTable',
  component: DataTable,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    columns: {
      control: 'object',
      description: 'Array of column definitions',
    },
    data: {
      control: 'object',
      description: 'Array of data objects',
    },
    pageSize: {
      control: { type: 'number', min: 1 },
      description: 'Number of items per page',
    },
  },
  args: {
    pageSize: 5,
  },
};

export default meta;
type Story = StoryObj<typeof DataTable>;

interface User {
  id: number;
  name: string;
  email: string;
  age: number;
  status: 'active' | 'inactive';
}

const sampleColumns = [
  {
    accessorKey: 'id',
    header: 'ID',
    enableSorting: true,
  },
  {
    accessorKey: 'name',
    header: 'Name',
    enableSorting: true,
  },
  {
    accessorKey: 'email',
    header: 'Email',
    enableSorting: true,
  },
  {
    accessorKey: 'age',
    header: 'Age',
    enableSorting: true,
  },
  {
    accessorKey: 'status',
    header: 'Status',
    cell: (row: User) => (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
        row.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
      }`}>
        {row.status}
      </span>
    ),
    enableSorting: true,
  },
];

const sampleData: User[] = [
  { id: 1, name: 'Alice Smith', email: 'alice@example.com', age: 30, status: 'active' },
  { id: 2, name: 'Bob Johnson', email: 'bob@example.com', age: 24, status: 'inactive' },
  { id: 3, name: 'Charlie Brown', email: 'charlie@example.com', age: 35, status: 'active' },
  { id: 4, name: 'Diana Prince', email: 'diana@example.com', age: 29, status: 'active' },
  { id: 5, name: 'Eve Adams', email: 'eve@example.com', age: 40, status: 'inactive' },
  { id: 6, name: 'Frank White', email: 'frank@example.com', age: 22, status: 'active' },
  { id: 7, name: 'Grace Lee', email: 'grace@example.com', age: 31, status: 'active' },
  { id: 8, name: 'Harry Kim', email: 'harry@example.com', age: 28, status: 'inactive' },
  { id: 9, name: 'Ivy Chen', email: 'ivy@example.com', age: 33, status: 'active' },
  { id: 10, name: 'Jack Ryan', email: 'jack@example.com', age: 27, status: 'active' },
  { id: 11, name: 'Karen Green', email: 'karen@example.com', age: 45, status: 'inactive' },
  { id: 12, name: 'Liam Black', email: 'liam@example.com', age: 26, status: 'active' },
];

export const Default: Story = {
  args: {
    columns: sampleColumns,
    data: sampleData,
  },
};

export const Empty: Story = {
  args: {
    columns: sampleColumns,
    data: [],
  },
};

export const CustomCellRendering: Story = {
  args: {
    columns: [
      {
        accessorKey: 'id',
        header: 'User ID',
      },
      {
        accessorKey: 'name',
        header: 'Full Name',
        cell: (row: User) => <span className="font-bold text-blue-600">{row.name.toUpperCase()}</span>,
      },
      {
        accessorKey: 'email',
        header: 'Contact Email',
      },
      {
        accessorKey: 'status',
        header: 'Account Status',
        cell: (row: User) => (
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
            row.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          }`}>
            {row.status.toUpperCase()}
          </span>
        ),
      },
    ],
    data: sampleData,
  },
};
