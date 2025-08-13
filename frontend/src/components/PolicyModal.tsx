"use client";

import React from "react";

type PolicyType = "terms" | "privacy" | "cookies";

export default function PolicyModal({
  open,
  onClose,
  type,
}: {
  open: boolean;
  onClose: () => void;
  type: PolicyType;
}) {
  if (!open) return null;

  const titles: Record<PolicyType, string> = {
    terms: "Terms of Service",
    privacy: "Privacy Policy",
    cookies: "Cookies Policy",
  };

  return (
    <div
      className="fixed inset-0 z-[100] flex items-end sm:items-center justify-center"
      aria-modal="true"
      role="dialog"
    >
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Sheet / Modal */}
      <div className="relative w-full sm:max-w-2xl sm:rounded-2xl bg-white shadow-2xl border border-gray-100 overflow-hidden animate-in fade-in zoom-in duration-150">
        <div className="flex items-center justify-between px-4 sm:px-6 py-3 border-b border-gray-100">
          <h3 className="text-sm font-semibold tracking-wide text-gray-700">
            {titles[type]}
          </h3>
          <button
            aria-label="Close"
            onClick={onClose}
            className="inline-flex h-8 w-8 items-center justify-center rounded-full hover:bg-gray-100"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              className="h-4 w-4 text-gray-500"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M18 6L6 18" />
              <path d="M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div className="px-4 sm:px-6 py-4 max-h-[70vh] overflow-y-auto text-sm leading-6 text-gray-600">
          {/* Placeholder copy - can be replaced with real policies */}
          <p className="mb-3">
            This {titles[type].toLowerCase()} outlines how Shujaa Studio provides
            services to users in a modern, privacy-respecting, Kenya-first way.
          </p>
          <p className="mb-3">
            We value transparency and security. Please review this document to
            understand your rights and responsibilities when using our platform.
          </p>
          <p className="mb-3">
            If you have questions, contact us via the in-app support or our
            official channels.
          </p>
        </div>
        <div className="px-4 sm:px-6 py-3 border-t border-gray-100 flex items-center justify-end gap-2">
          <button
            onClick={onClose}
            className="px-3 py-1.5 text-xs font-medium rounded-md bg-gray-900 text-white hover:bg-black transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
