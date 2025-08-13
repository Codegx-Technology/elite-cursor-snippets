"use client";

// [SNIPPET]: surgicalfix + uxfix + hydrateguard
// [CONTEXT]: Client bootstrapping for SW and viewport adjustments without SSR side-effects
// [GOAL]: Prevent hydration mismatches by moving DOM mutations to client effect

import { useEffect } from "react";

export default function ClientBoot() {
  useEffect(() => {
    // Register service worker for PWA functionality
    if (typeof navigator !== "undefined" && "serviceWorker" in navigator) {
      const onLoad = () => {
        navigator.serviceWorker
          .register("/sw.js")
          .then((registration) => {
            if (process.env.NODE_ENV === "development") {
              console.log("SW registered: ", registration);
            }
          })
          .catch((err) => {
            if (process.env.NODE_ENV === "development") {
              console.log("SW registration failed: ", err);
            }
          });
      };
      window.addEventListener("load", onLoad, { once: true });
      return () => window.removeEventListener("load", onLoad);
    }
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
