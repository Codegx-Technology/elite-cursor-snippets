"use client";

import { useEffect } from "react";

declare global {
  interface Window {
    requestIdleCallback?: (callback: IdleRequestCallback, options?: IdleRequestOptions) => IdleCallbackHandle;
    cancelIdleCallback?: (handle: IdleCallbackHandle) => void;
  }
}

export default function ServiceWorkerRegistrar() {
  useEffect(() => {
    if (typeof window === "undefined") return;
    if (!("serviceWorker" in navigator)) return;

    const isProd = process.env.NODE_ENV === "production";

    const manageSW = async () => {
      try {
        const registrations = await navigator.serviceWorker.getRegistrations();
        if (!isProd) {
          // In development: ensure no SW is active to avoid caching dev chunks
          await Promise.all(registrations.map(r => r.unregister()));
          return;
        }
        // In production: ensure one is registered
        const hasActive = registrations.some(r => r.active);
        if (!hasActive) {
          await navigator.serviceWorker.register("/sw.js");
        }
      } catch (e) {
        // no-op in case of errors
      }
    };

    // Defer to idle to avoid blocking hydration
    if ((window as any).requestIdleCallback) {
      (window as any).requestIdleCallback(manageSW);
    } else {
      setTimeout(manageSW, 0);
    }
  }, []);

  return null;
}
