import {getRequestConfig} from 'next-intl/server';

export default getRequestConfig(async ({locale}) => {
  // Default to 'en' if locale is undefined or invalid
  const validLocale = locale && ['en', 'sw'].includes(locale) ? locale : 'en';
  
  return {
    messages: (await import(`./messages/${validLocale}.json`)).default
  };
});
