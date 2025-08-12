import { useState } from 'react';

export default function Header({ isSidebarOpen, setSidebarOpen }: { isSidebarOpen: boolean, setSidebarOpen: (isOpen: boolean) => void }) {
  return (
    <header className="bg-white shadow-md p-4 flex items-center justify-between">
      <h1 className="text-xl font-semibold text-charcoal-text">Shujaa Studio</h1>
      <button
        className="md:hidden p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-200"
        onClick={() => setSidebarOpen(!isSidebarOpen)}
      >
        <svg
          className="w-6 h-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          {isSidebarOpen ? (
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M6 18L18 6M6 6l12 12"
            ></path>
          ) : (
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M4 6h16M4 12h16M4 18h16"
            ></path>
          )}
        </svg>
      </button>
    </header>
  );
}
