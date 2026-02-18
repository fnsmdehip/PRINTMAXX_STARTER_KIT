import { useSubscriptionStore } from '../src/stores/subscriptionStore';

// Reset store before each test
beforeEach(() => {
  useSubscriptionStore.setState({
    isPro: false,
    expiresAt: undefined,
    trialActive: false,
    trialEndsAt: undefined,
  });
});

describe('subscriptionStore', () => {
  describe('initial state', () => {
    it('should start as free user', () => {
      const state = useSubscriptionStore.getState();
      expect(state.isPro).toBe(false);
      expect(state.trialActive).toBe(false);
    });
  });

  describe('startTrial', () => {
    it('should activate trial and set isPro to true', () => {
      const { startTrial } = useSubscriptionStore.getState();

      startTrial();

      const state = useSubscriptionStore.getState();
      expect(state.isPro).toBe(true);
      expect(state.trialActive).toBe(true);
      expect(state.trialEndsAt).toBeDefined();
    });

    it('should set trial end date 7 days in future', () => {
      const { startTrial } = useSubscriptionStore.getState();
      const now = Date.now();

      startTrial();

      const state = useSubscriptionStore.getState();
      const trialEndTime = new Date(state.trialEndsAt!).getTime();
      const sevenDaysMs = 7 * 24 * 60 * 60 * 1000;

      // Allow 1 second tolerance for test execution time
      expect(trialEndTime).toBeGreaterThanOrEqual(now + sevenDaysMs - 1000);
      expect(trialEndTime).toBeLessThanOrEqual(now + sevenDaysMs + 1000);
    });
  });

  describe('endTrial', () => {
    it('should deactivate trial and remove pro status', () => {
      const { startTrial, endTrial } = useSubscriptionStore.getState();

      startTrial();
      endTrial();

      const state = useSubscriptionStore.getState();
      expect(state.isPro).toBe(false);
      expect(state.trialActive).toBe(false);
      expect(state.trialEndsAt).toBeUndefined();
    });
  });

  describe('upgradeToPro', () => {
    it('should set pro status with expiration date', () => {
      const { upgradeToPro } = useSubscriptionStore.getState();
      const expiresAt = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString();

      upgradeToPro(expiresAt);

      const state = useSubscriptionStore.getState();
      expect(state.isPro).toBe(true);
      expect(state.expiresAt).toBe(expiresAt);
      expect(state.trialActive).toBe(false);
    });

    it('should cancel trial when upgrading', () => {
      const { startTrial, upgradeToPro } = useSubscriptionStore.getState();
      const expiresAt = new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toISOString();

      startTrial();
      upgradeToPro(expiresAt);

      const state = useSubscriptionStore.getState();
      expect(state.trialActive).toBe(false);
      expect(state.trialEndsAt).toBeUndefined();
    });
  });

  describe('cancelSubscription', () => {
    it('should remove all subscription data', () => {
      const { upgradeToPro, cancelSubscription } = useSubscriptionStore.getState();
      const expiresAt = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString();

      upgradeToPro(expiresAt);
      cancelSubscription();

      const state = useSubscriptionStore.getState();
      expect(state.isPro).toBe(false);
      expect(state.expiresAt).toBeUndefined();
      expect(state.trialActive).toBe(false);
    });
  });

  describe('checkTrialStatus', () => {
    it('should expire trial when past end date', () => {
      useSubscriptionStore.setState({
        isPro: true,
        trialActive: true,
        trialEndsAt: new Date(Date.now() - 1000).toISOString(), // 1 second ago
      });

      const { checkTrialStatus } = useSubscriptionStore.getState();
      checkTrialStatus();

      const state = useSubscriptionStore.getState();
      expect(state.isPro).toBe(false);
      expect(state.trialActive).toBe(false);
    });

    it('should keep trial active when not expired', () => {
      const futureDate = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString();
      useSubscriptionStore.setState({
        isPro: true,
        trialActive: true,
        trialEndsAt: futureDate,
      });

      const { checkTrialStatus } = useSubscriptionStore.getState();
      checkTrialStatus();

      const state = useSubscriptionStore.getState();
      expect(state.isPro).toBe(true);
      expect(state.trialActive).toBe(true);
    });

    it('should expire subscription when past expiry date', () => {
      useSubscriptionStore.setState({
        isPro: true,
        expiresAt: new Date(Date.now() - 1000).toISOString(),
      });

      const { checkTrialStatus } = useSubscriptionStore.getState();
      checkTrialStatus();

      const state = useSubscriptionStore.getState();
      expect(state.isPro).toBe(false);
      expect(state.expiresAt).toBeUndefined();
    });
  });
});
