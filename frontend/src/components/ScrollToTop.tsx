"use client";

import React, { useEffect, useRef, useState } from "react";

export default function ScrollToTop() {
  // Visible by default on initial load
  const [visible, setVisible] = useState(true);
  const lastYRef = useRef(0);

  useEffect(() => {
    const onScroll = () => {
      const y = window.scrollY || 0;
      // Ignore tiny jitters to avoid flicker
      if (Math.abs(y - lastYRef.current) < 2) return;
      // Hide only when scrolling up; show when scrolling down or stationary
      setVisible(y >= lastYRef.current);
      lastYRef.current = y;
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const scrollUp = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <button
      aria-label="Scroll to top"
      onClick={scrollUp}
      className={`fixed right-3 sm:right-4 z-[100] inline-flex items-center justify-center rounded-full h-7 w-7 sm:h-8 sm:w-8 shadow-lg ring-1 ring-emerald-200/60 transition-all duration-200 border border-emerald-200 bg-white/95 hover:bg-white hover:shadow-xl bottom-[calc(env(safe-area-inset-bottom)+1rem)] sm:bottom-5 md:bottom-6 lg:bottom-6 ${
        visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-3 pointer-events-none"
      }`}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        className="h-4 w-4 text-emerald-600"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M5 15l7-7 7 7" />
      </svg>
    </button>
  );
}
