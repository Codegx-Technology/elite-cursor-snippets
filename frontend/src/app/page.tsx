import { redirect } from 'next/navigation';

export default function RootPage() {
  // Redirect to the real landing page with i18n
  redirect('/en');
}
