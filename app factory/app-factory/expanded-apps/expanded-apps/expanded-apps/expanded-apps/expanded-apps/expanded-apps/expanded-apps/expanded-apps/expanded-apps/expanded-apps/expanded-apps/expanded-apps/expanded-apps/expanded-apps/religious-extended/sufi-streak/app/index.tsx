import { Redirect } from 'expo-router';

export default function Index() {
  // This will redirect based on the auth state handled in _layout.tsx
  return <Redirect href="/(onboarding)" />;
}
