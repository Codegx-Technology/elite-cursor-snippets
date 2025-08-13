"use client";

import React, { useState } from "react";
import PolicyModal from "./PolicyModal";

export default function Footer() {
  const [open, setOpen] = useState<null | "terms" | "privacy" | "cookies">(null);

  return (
    <>
      <footer className="w-full border-t border-gray-100 bg-white/70 backdrop-blur supports-[backdrop-filter]:bg-white/50 relative z-20">
        <div className="mx-auto max-w-7xl px-3 sm:px-6 lg:px-8 py-3">
          <div className="grid grid-cols-1 sm:grid-cols-3 items-center gap-3 text-[10px] tracking-[0.2em] text-gray-500">
            {/* Left unique accent + credit */}
            <div className="flex items-center gap-2 justify-center sm:justify-start">
              {/* Unique tiny accent */}
              <span className="inline-block h-2 w-2 rounded-sm bg-gradient-to-br from-emerald-500 to-teal-600 shadow-[0_0_10px_rgba(16,185,129,0.5)]" />
              <span className="uppercase whitespace-nowrap select-none">
                MADE IN KENYA
              </span>
            </div>

            {/* Centered developer credit */}
            <div className="text-center">
              <span className="uppercase font-semibold">Developed by codegx Technologies</span>
            </div>

            {/* Right links with sleek icons */}
            <nav className="flex items-center gap-3 justify-center sm:justify-end flex-wrap">
              <button
                onClick={() => setOpen("terms")}
                className="inline-flex items-center gap-1.5 hover:text-gray-800 transition"
                aria-label="Open Terms of Service"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="h-3.5 w-3.5" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M4 19.5A2.5 2.5 0 0 0 6.5 22H18" />
                  <path d="M20 22V8a2 2 0 0 0-2-2h-7l-5 5v11" />
                </svg>
                <span className="uppercase">Terms</span>
              </button>
              <span className="text-gray-300">•</span>
              <button
                onClick={() => setOpen("privacy")}
                className="inline-flex items-center gap-1.5 hover:text-gray-800 transition"
                aria-label="Open Privacy Policy"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="h-3.5 w-3.5" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z" />
                </svg>
                <span className="uppercase">Privacy</span>
              </button>
              <span className="text-gray-300">•</span>
              <button
                onClick={() => setOpen("cookies")}
                className="inline-flex items-center gap-1.5 hover:text-gray-800 transition"
                aria-label="Open Cookies Policy"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="h-3.5 w-3.5" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M15 11v.01" />
                  <path d="M11 15v.01" />
                  <path d="M12 2a7 7 0 0 0 7 7 7 7 0 1 1-7-7Z" />
                </svg>
                <span className="uppercase">Cookies</span>
              </button>
            </nav>
          </div>
        </div>
      </footer>

      <PolicyModal open={open === "terms"} onClose={() => setOpen(null)} type="terms" />
      <PolicyModal open={open === "privacy"} onClose={() => setOpen(null)} type="privacy" />
      <PolicyModal open={open === "cookies"} onClose={() => setOpen(null)} type="cookies" />
    </>
  );
}
