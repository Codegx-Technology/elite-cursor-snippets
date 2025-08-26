// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Phase 3 - Accessibility optimization for enterprise-grade SaaS
// [GOAL]: ARIA compliance, keyboard navigation, screen reader support
// [TASK]: Implement comprehensive accessibility features with Kenya-first considerations

'use client';

import { useEffect, useCallback, useState } from 'react';

// Accessibility preferences hook
export const useAccessibilityPreferences = () => {
  const [preferences, setPreferences] = useState({
    reduceMotion: false,
    highContrast: false,
    largeText: false,
    screenReader: false
  });

  useEffect(() => {
    // Detect system preferences
    const mediaQueries = {
      reduceMotion: window.matchMedia('(prefers-reduced-motion: reduce)'),
      highContrast: window.matchMedia('(prefers-contrast: high)'),
      largeText: window.matchMedia('(prefers-reduced-data: reduce)')
    };

    const updatePreferences = () => {
      setPreferences({
        reduceMotion: mediaQueries.reduceMotion.matches,
        highContrast: mediaQueries.highContrast.matches,
        largeText: mediaQueries.largeText.matches,
        screenReader: !!navigator.userAgent.match(/NVDA|JAWS|VoiceOver|TalkBack/)
      });
    };

    updatePreferences();

    // Listen for changes
    Object.values(mediaQueries).forEach(mq => {
      mq.addEventListener('change', updatePreferences);
    });

    return () => {
      Object.values(mediaQueries).forEach(mq => {
        mq.removeEventListener('change', updatePreferences);
      });
    };
  }, []);

  return preferences;
};

// Keyboard navigation hook
export const useKeyboardNavigation = () => {
  const [isKeyboardUser, setIsKeyboardUser] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Tab') {
        setIsKeyboardUser(true);
        document.body.classList.add('keyboard-user');
      }
    };

    const handleMouseDown = () => {
      setIsKeyboardUser(false);
      document.body.classList.remove('keyboard-user');
    };

    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('mousedown', handleMouseDown);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.removeEventListener('mousedown', handleMouseDown);
    };
  }, []);

  return { isKeyboardUser };
};

// Focus management hook
export const useFocusManagement = () => {
  const trapFocus = useCallback((element: HTMLElement) => {
    const focusableElements = element.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    const firstElement = focusableElements[0] as HTMLElement;
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Tab') {
        if (e.shiftKey) {
          if (document.activeElement === firstElement) {
            e.preventDefault();
            lastElement.focus();
          }
        } else {
          if (document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
          }
        }
      }

      // Kenya-first: Escape key support with cultural context
      if (e.key === 'Escape') {
        const closeButton = element.querySelector('[aria-label*="Close"], [aria-label*="Funga"]') as HTMLElement;
        if (closeButton) {
          closeButton.click();
        }
      }
    };

    element.addEventListener('keydown', handleKeyDown);
    firstElement?.focus();

    return () => {
      element.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  const announceLiveRegion = useCallback((message: string, priority: 'polite' | 'assertive' = 'polite') => {
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('aria-live', priority);
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.className = 'sr-only';
    
    // Kenya-first: Add cultural context to announcements
    const culturalMessage = `🇰🇪 ${message}`;
    liveRegion.textContent = culturalMessage;
    
    document.body.appendChild(liveRegion);
    
    setTimeout(() => {
      document.body.removeChild(liveRegion);
    }, 1000);
  }, []);

  return { trapFocus, announceLiveRegion };
};

// ARIA utilities
export const useAriaUtils = () => {
  const generateId = useCallback((prefix: string = 'kenya') => {
    return `${prefix}-${Math.random().toString(36).substr(2, 9)}`;
  }, []);

  const createAriaLabel = useCallback((base: string, context?: string) => {
    if (context) {
      return `${base} - ${context} 🇰🇪`;
    }
    return `${base} 🇰🇪`;
  }, []);

  const createAriaDescription = useCallback((action: string, result: string) => {
    return `${action}. ${result}. Kenya-first platform.`;
  }, []);

  return { generateId, createAriaLabel, createAriaDescription };
};

// Screen reader optimization
export const useScreenReaderOptimization = () => {
  const [isScreenReaderActive, setIsScreenReaderActive] = useState(false);

  useEffect(() => {
    // Detect screen reader usage patterns
    const detectScreenReader = () => {
      const hasScreenReader = !!(
        navigator.userAgent.match(/NVDA|JAWS|VoiceOver|TalkBack/) ||
        window.speechSynthesis ||
        document.querySelector('[aria-live]')
      );
      
      setIsScreenReaderActive(hasScreenReader);
      
      if (hasScreenReader) {
        document.body.classList.add('screen-reader-active');
        // Add Kenya-first screen reader styles
        document.body.classList.add('kenya-screen-reader');
      }
    };

    detectScreenReader();

    // Listen for screen reader specific events
    const handleFocus = (e: FocusEvent) => {
      const target = e.target as HTMLElement;
      if (target.hasAttribute('aria-describedby') || target.hasAttribute('aria-labelledby')) {
        setIsScreenReaderActive(true);
      }
    };

    document.addEventListener('focus', handleFocus, true);

    return () => {
      document.removeEventListener('focus', handleFocus, true);
    };
  }, []);

  const optimizeForScreenReader = useCallback((element: HTMLElement, description: string) => {
    if (isScreenReaderActive) {
      element.setAttribute('aria-description', `🇰🇪 ${description}`);
      element.setAttribute('role', element.tagName.toLowerCase() === 'div' ? 'region' : element.getAttribute('role') || '');
    }
  }, [isScreenReaderActive]);

  return { isScreenReaderActive, optimizeForScreenReader };
};

// Color contrast utilities
export const useColorContrast = () => {
  const checkContrast = useCallback((foreground: string, background: string) => {
    // Simplified contrast ratio calculation
    const getLuminance = (color: string) => {
      const rgb = parseInt(color.replace('#', ''), 16);
      const r = (rgb >> 16) & 0xff;
      const g = (rgb >> 8) & 0xff;
      const b = (rgb >> 0) & 0xff;
      
      return (0.299 * r + 0.587 * g + 0.114 * b) / 255;
    };

    const l1 = getLuminance(foreground);
    const l2 = getLuminance(background);
    
    const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
    
    return {
      ratio,
      isAACompliant: ratio >= 4.5,
      isAAACompliant: ratio >= 7,
      recommendation: ratio < 4.5 ? 'Improve contrast for accessibility' : 'Good contrast ratio'
    };
  }, []);

  // Kenya-first color combinations
  const kenyaColorCombinations = {
    primary: { foreground: '#FFFFFF', background: '#00A651' }, // White on Kenya Green
    secondary: { foreground: '#000000', background: '#FFD700' }, // Black on Gold
    text: { foreground: '#2D3748', background: '#FFFFFF' }, // Dark gray on white
    accent: { foreground: '#FFFFFF', background: '#E53E3E' } // White on red
  };

  const validateKenyaColors = useCallback(() => {
    const results: { [key: string]: unknown } = {};
    
    Object.entries(kenyaColorCombinations).forEach(([name, colors]) => {
      results[name] = checkContrast(colors.foreground, colors.background);
    });
    
    return results;
  }, [checkContrast]);

  return { checkContrast, validateKenyaColors, kenyaColorCombinations };
};
