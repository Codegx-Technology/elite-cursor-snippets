// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Phase 4 - Multi-language support with Swahili for Kenya-first platform
// [GOAL]: Comprehensive internationalization with cultural authenticity
// [TASK]: Implement i18n system with English/Swahili support and cultural context

'use client';

import { globalCache } from './performance';

// Language types
export type Language = 'en' | 'sw';
export type LanguageDirection = 'ltr' | 'rtl';

// Translation structure
export interface Translation {
  [key: string]: string | Translation;
}

// Language configuration
export interface LanguageConfig {
  code: Language;
  name: string;
  nativeName: string;
  direction: LanguageDirection;
  flag: string;
  region: string;
  culturalContext: {
    greetings: string[];
    farewells: string[];
    expressions: string[];
  };
}

// Supported languages with cultural context
export const SUPPORTED_LANGUAGES: Record<Language, LanguageConfig> = {
  en: {
    code: 'en',
    name: 'English',
    nativeName: 'English',
    direction: 'ltr',
    flag: '🇬🇧',
    region: 'International',
    culturalContext: {
      greetings: ['Hello', 'Hi', 'Good morning', 'Good afternoon'],
      farewells: ['Goodbye', 'See you later', 'Take care', 'Farewell'],
      expressions: ['Thank you', 'You\'re welcome', 'Excuse me', 'Please']
    }
  },
  sw: {
    code: 'sw',
    name: 'Swahili',
    nativeName: 'Kiswahili',
    direction: 'ltr',
    flag: '🇰🇪',
    region: 'East Africa',
    culturalContext: {
      greetings: ['Hujambo', 'Habari', 'Salama', 'Shikamoo'],
      farewells: ['Kwaheri', 'Tutaonana', 'Safari njema', 'Haya'],
      expressions: ['Asante', 'Karibu', 'Samahani', 'Tafadhali']
    }
  }
};

// Translation keys with nested structure
export const TRANSLATIONS: Record<Language, Translation> = {
  en: {
    common: {
      loading: 'Loading...',
      error: 'Error',
      success: 'Success',
      cancel: 'Cancel',
      save: 'Save',
      delete: 'Delete',
      edit: 'Edit',
      create: 'Create',
      back: 'Back',
      next: 'Next',
      previous: 'Previous',
      close: 'Close',
      open: 'Open',
      search: 'Search',
      filter: 'Filter',
      sort: 'Sort',
      refresh: 'Refresh'
    },
    navigation: {
      home: 'Home',
      dashboard: 'Dashboard',
      projects: 'Projects',
      gallery: 'Gallery',
      analytics: 'Analytics',
      settings: 'Settings',
      profile: 'Profile',
      team: 'Team',
      admin: 'Admin',
      generate: 'Generate Video',
      login: 'Login',
      logout: 'Logout',
      register: 'Register'
    },
    auth: {
      welcome: 'Welcome to Shujaa Studio',
      loginTitle: 'Sign in to your account',
      registerTitle: 'Create your account',
      email: 'Email address',
      password: 'Password',
      confirmPassword: 'Confirm password',
      forgotPassword: 'Forgot your password?',
      rememberMe: 'Remember me',
      signIn: 'Sign in',
      signUp: 'Sign up',
      signOut: 'Sign out',
      alreadyHaveAccount: 'Already have an account?',
      dontHaveAccount: 'Don\'t have an account?'
    },
    video: {
      create: 'Create Video',
      upload: 'Upload Video',
      processing: 'Processing video...',
      completed: 'Video processing completed',
      failed: 'Video processing failed',
      title: 'Video Title',
      description: 'Video Description',
      tags: 'Tags',
      category: 'Category',
      duration: 'Duration',
      resolution: 'Resolution',
      format: 'Format',
      size: 'File Size'
    },
    collaboration: {
      activeUsers: 'Active Users',
      comments: 'Comments',
      addComment: 'Add a comment...',
      sendComment: 'Send',
      userJoined: 'joined the session',
      userLeft: 'left the session',
      typing: 'is typing...',
      connected: 'Connected',
      disconnected: 'Disconnected',
      reconnecting: 'Reconnecting...'
    },
    ai: {
      suggestions: 'AI Suggestions',
      analyzing: 'Analyzing content...',
      generating: 'Generating suggestions...',
      confidence: 'Confidence',
      relevance: 'Kenya Relevance',
      apply: 'Apply',
      dismiss: 'Dismiss',
      feedback: 'Provide feedback',
      culturalAnalysis: 'Cultural Analysis',
      trending: 'Trending in Kenya'
    },
    cultural: {
      harambee: 'Harambee',
      karibu: 'Welcome',
      asante: 'Thank you',
      kenyaFirst: 'Kenya-First',
      heritage: 'Heritage',
      tradition: 'Tradition',
      community: 'Community',
      innovation: 'Innovation',
      excellence: 'Excellence'
    }
  },
  sw: {
    common: {
      loading: 'Inapakia...',
      error: 'Hitilafu',
      success: 'Mafanikio',
      cancel: 'Ghairi',
      save: 'Hifadhi',
      delete: 'Futa',
      edit: 'Hariri',
      create: 'Unda',
      back: 'Rudi',
      next: 'Ifuatayo',
      previous: 'Iliyotangulia',
      close: 'Funga',
      open: 'Fungua',
      search: 'Tafuta',
      filter: 'Chuja',
      sort: 'Panga',
      refresh: 'Onyesha upya'
    },
    navigation: {
      home: 'Nyumbani',
      dashboard: 'Dashibodi',
      projects: 'Miradi',
      gallery: 'Makumbusho',
      analytics: 'Uchanganuzi',
      settings: 'Mipangilio',
      profile: 'Wasifu',
      team: 'Timu',
      admin: 'Msimamizi',
      generate: 'Unda Video',
      login: 'Ingia',
      logout: 'Toka',
      register: 'Jisajili'
    },
    auth: {
      welcome: 'Karibu Shujaa Studio',
      loginTitle: 'Ingia kwenye akaunti yako',
      registerTitle: 'Unda akaunti yako',
      email: 'Anwani ya barua pepe',
      password: 'Nenosiri',
      confirmPassword: 'Thibitisha nenosiri',
      forgotPassword: 'Umesahau nenosiri lako?',
      rememberMe: 'Nikumbuke',
      signIn: 'Ingia',
      signUp: 'Jisajili',
      signOut: 'Toka',
      alreadyHaveAccount: 'Una akaunti tayari?',
      dontHaveAccount: 'Huna akaunti?'
    },
    video: {
      create: 'Unda Video',
      upload: 'Pakia Video',
      processing: 'Inachakata video...',
      completed: 'Uchakataji wa video umekamilika',
      failed: 'Uchakataji wa video umeshindwa',
      title: 'Kichwa cha Video',
      description: 'Maelezo ya Video',
      tags: 'Lebo',
      category: 'Jamii',
      duration: 'Muda',
      resolution: 'Ubora',
      format: 'Muundo',
      size: 'Ukubwa wa Faili'
    },
    collaboration: {
      activeUsers: 'Watumiaji Hai',
      comments: 'Maoni',
      addComment: 'Ongeza maoni...',
      sendComment: 'Tuma',
      userJoined: 'amejiunga na kikao',
      userLeft: 'ameondoka kwenye kikao',
      typing: 'anaandika...',
      connected: 'Imeunganishwa',
      disconnected: 'Imekatishwa',
      reconnecting: 'Inaunganisha tena...'
    },
    ai: {
      suggestions: 'Mapendekezo ya AI',
      analyzing: 'Inachambua maudhui...',
      generating: 'Inaunda mapendekezo...',
      confidence: 'Uhakika',
      relevance: 'Uhusiano wa Kenya',
      apply: 'Tumia',
      dismiss: 'Kataa',
      feedback: 'Toa maoni',
      culturalAnalysis: 'Uchanganuzi wa Kitamaduni',
      trending: 'Kinachozungumzwa Kenya'
    },
    cultural: {
      harambee: 'Harambee',
      karibu: 'Karibu',
      asante: 'Asante',
      kenyaFirst: 'Kenya-Kwanza',
      heritage: 'Urithi',
      tradition: 'Jadi',
      community: 'Jamii',
      innovation: 'Uvumbuzi',
      excellence: 'Ubora'
    }
  }
};

// I18n class for managing translations
export class I18n {
  private currentLanguage: Language = 'en';
  private fallbackLanguage: Language = 'en';
  private listeners: Set<(language: Language) => void> = new Set();

  constructor() {
    this.loadSavedLanguage();
  }

  // Load saved language from localStorage
  private loadSavedLanguage(): void {
    if (typeof window === 'undefined') return;

    const saved = localStorage.getItem('shujaa_language') as Language;
    if (saved && SUPPORTED_LANGUAGES[saved]) {
      this.currentLanguage = saved;
    } else {
      // Detect browser language
      const browserLang = navigator.language.split('-')[0] as Language;
      if (SUPPORTED_LANGUAGES[browserLang]) {
        this.currentLanguage = browserLang;
      }
    }
  }

  // Get current language
  getLanguage(): Language {
    return this.currentLanguage;
  }

  // Set language
  setLanguage(language: Language): void {
    if (!SUPPORTED_LANGUAGES[language]) {
      console.warn(`🇰🇪 Unsupported language: ${language}`);
      return;
    }

    this.currentLanguage = language;
    
    if (typeof window !== 'undefined') {
      localStorage.setItem('shujaa_language', language);
      document.documentElement.lang = language;
      document.documentElement.dir = SUPPORTED_LANGUAGES[language].direction;
    }

    this.notifyListeners();
  }

  // Get translation by key
  t(key: string, params?: Record<string, string>): string {
    const translation = this.getNestedTranslation(key, this.currentLanguage) ||
                       this.getNestedTranslation(key, this.fallbackLanguage) ||
                       key;

    // Replace parameters
    if (params) {
      return Object.entries(params).reduce(
        (text, [param, value]) => text.replace(`{{${param}}}`, value),
        translation
      );
    }

    return translation;
  }

  // Get nested translation
  private getNestedTranslation(key: string, language: Language): string | null {
    const keys = key.split('.');
    let current: Translation | string | null | undefined = TRANSLATIONS[language];

    for (const k of keys) {
      if (current && typeof current === 'object' && k in current) {
        current = current[k];
      } else {
        return null;
      }
    }

    return typeof current === 'string' ? current : null;
  }

  // Get language configuration
  getLanguageConfig(language?: Language): LanguageConfig {
    return SUPPORTED_LANGUAGES[language || this.currentLanguage];
  }

  // Get all supported languages
  getSupportedLanguages(): LanguageConfig[] {
    return Object.values(SUPPORTED_LANGUAGES);
  }

  // Check if language is supported
  isLanguageSupported(language: string): boolean {
    return language in SUPPORTED_LANGUAGES;
  }

  // Get cultural greeting
  getCulturalGreeting(): string {
    const config = this.getLanguageConfig();
    const greetings = config.culturalContext.greetings;
    return greetings[Math.floor(Math.random() * greetings.length)];
  }

  // Get cultural farewell
  getCulturalFarewell(): string {
    const config = this.getLanguageConfig();
    const farewells = config.culturalContext.farewells;
    return farewells[Math.floor(Math.random() * farewells.length)];
  }

  // Format number with locale
  formatNumber(number: number): string {
    const locale = this.currentLanguage === 'sw' ? 'sw-KE' : 'en-KE';
    return new Intl.NumberFormat(locale).format(number);
  }

  // Format date with locale
  formatDate(date: Date, options?: Intl.DateTimeFormatOptions): string {
    const locale = this.currentLanguage === 'sw' ? 'sw-KE' : 'en-KE';
    return new Intl.DateTimeFormat(locale, options).format(date);
  }

  // Format currency (Kenyan Shilling)
  formatCurrency(amount: number): string {
    const locale = this.currentLanguage === 'sw' ? 'sw-KE' : 'en-KE';
    return new Intl.NumberFormat(locale, {
      style: 'currency',
      currency: 'KES'
    }).format(amount);
  }

  // Add language change listener
  onLanguageChange(callback: (language: Language) => void): () => void {
    this.listeners.add(callback);
    return () => this.listeners.delete(callback);
  }

  // Notify listeners of language change
  private notifyListeners(): void {
    this.listeners.forEach(callback => callback(this.currentLanguage));
  }

  // Get text direction
  getDirection(): LanguageDirection {
    return this.getLanguageConfig().direction;
  }

  // Check if current language is RTL
  isRTL(): boolean {
    return this.getDirection() === 'rtl';
  }

  // Get pluralization (simplified)
  plural(key: string, count: number): string {
    const singular = this.t(key);
    const plural = this.t(`${key}_plural`);
    
    return count === 1 ? singular : (plural || singular);
  }

  // Cache translations for performance
  preloadTranslations(): void {
    Object.entries(TRANSLATIONS).forEach(([lang, translations]) => {
      globalCache.set(`translations_${lang}`, translations, 3600000); // 1 hour
    });
  }
}

// Global i18n instance
export const i18n = new I18n();

// React hook for i18n
export const useI18n = () => {
  const [language, setLanguageState] = React.useState(i18n.getLanguage());

  React.useEffect(() => {
    const unsubscribe = i18n.onLanguageChange(setLanguageState);
    return unsubscribe;
  }, []);

  const setLanguage = React.useCallback((lang: Language) => {
    i18n.setLanguage(lang);
  }, []);

  const t = React.useCallback((key: string, params?: Record<string, string>) => {
    return i18n.t(key, params);
  }, [language]);

  return {
    language,
    setLanguage,
    t,
    config: i18n.getLanguageConfig(),
    supportedLanguages: i18n.getSupportedLanguages(),
    formatNumber: i18n.formatNumber.bind(i18n),
    formatDate: i18n.formatDate.bind(i18n),
    formatCurrency: i18n.formatCurrency.bind(i18n),
    getCulturalGreeting: i18n.getCulturalGreeting.bind(i18n),
    getCulturalFarewell: i18n.getCulturalFarewell.bind(i18n),
    isRTL: i18n.isRTL.bind(i18n)
  };
};

// Import React for the hook
import React from 'react';
