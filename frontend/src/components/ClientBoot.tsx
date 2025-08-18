"use client";

// [SNIPPET]: surgicalfix + uxfix + hydrateguard
// [CONTEXT]: Client bootstrapping for SW and viewport adjustments without SSR side-effects
// [GOAL]: Prevent hydration mismatches by moving DOM mutations to client effect

import { useEffect } from "react";

export default function ClientBoot() {
  useEffect(() => {
    if (typeof navigator === "undefined" || !("serviceWorker" in navigator)) return;

    // In development, unregister all service workers to avoid caching issues
    if (process.env.NODE_ENV === "development") {
      navigator.serviceWorker.getRegistrations?.().then((regs) => {
        regs.forEach((reg) => reg.unregister());
      }).catch(() => {});
      return;
    }

    // In production, register the service worker
    const onLoad = () => {
      navigator.serviceWorker
        .register("/sw.js")
        .catch(() => {});
    };
    window.addEventListener("load", onLoad, { once: true });
    return () => window.removeEventListener("load", onLoad);
  }, []);

  useEffect(() => {
    // Prevent zoom on iOS when focusing inputs (no-op handler to enable delegation)
    const handler = () => {};
    document.addEventListener("touchstart", handler, true);
    return () => document.removeEventListener("touchstart", handler, true);
  }, []);

  useEffect(() => {
    // Ensure viewport meta exists
    const hasViewport = document.querySelector('meta[name="viewport"]');
    if (!hasViewport) {
      const viewport = document.createElement("meta");
      viewport.name = "viewport";
      viewport.content = "width=device-width, initial-scale=1, maximum-scale=5, user-scalable=yes";
      document.head.appendChild(viewport);
    }
  }, []);

  return null;
}
