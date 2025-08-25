"use client";

import React, { useState } from "react";
import Link from 'next/link';
import PolicyModal from "./PolicyModal";
import { FaShieldAlt, FaCookie, FaFileContract } from 'react-icons/fa6';

export default function Footer() {
  const [open, setOpen] = useState<null | "terms" | "privacy" | "cookies">(null);

  return (
    <>
      <footer className="w-full border-t border-gray-100 bg-gray-50/50 backdrop-blur-sm relative z-20">
        <div className="mx-auto max-w-7xl px-4 py-2">
          <div className="grid grid-cols-3 items-center text-xs text-gray-500">
            {/* Left - Copyright */}
            <div className="flex items-center gap-1">
              <Link href="/" className="hover:text-gray-700 transition-colors cursor-pointer">
                © {new Date().getFullYear()} Shujaa Studio
              </Link>
            </div>

            {/* Center - Developer credit */}
            <div className="text-center">
              <a 
                href="https://codegx.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="hover:text-gray-700 transition-colors cursor-pointer"
              >
                Developed by codegx Technologies
              </a>
            </div>

            {/* Right - Policy links */}
            <nav className="flex items-center gap-3 justify-end">
              <button
                onClick={() => setOpen("terms")}
                className="hover:text-gray-700 transition-colors"
                aria-label="Terms"
              >
                Terms
              </button>
              <span>•</span>
              <button
                onClick={() => setOpen("privacy")}
                className="hover:text-gray-700 transition-colors"
                aria-label="Privacy"
              >
                Privacy
              </button>
              <span>•</span>
              <button
                onClick={() => setOpen("cookies")}
                className="hover:text-gray-700 transition-colors"
                aria-label="Cookies"
              >
                Cookies
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
