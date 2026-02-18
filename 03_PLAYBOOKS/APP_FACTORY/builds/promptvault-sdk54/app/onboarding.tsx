import { useRouter } from 'expo-router';
import OnboardingScreenComponent from '../src/screens/OnboardingScreen';
import { useOnboardingStore } from '../src/stores/onboardingStore';

export default function OnboardingScreen() {
  const router = useRouter();
  const completeOnboarding = useOnboardingStore((state) => state.completeOnboarding);

  const handleComplete = () => {
    completeOnboarding();
    router.replace('/(tabs)/home');
  };

  return <OnboardingScreenComponent onComplete={handleComplete} />;
}
