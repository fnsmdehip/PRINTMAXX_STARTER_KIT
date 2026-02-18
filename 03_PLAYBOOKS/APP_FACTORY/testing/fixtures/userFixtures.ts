/**
 * User test fixtures and factory functions
 *
 * Usage:
 *   import { createUser, USERS } from '@testing/fixtures/userFixtures';
 *
 *   // Use static fixture
 *   const user = USERS.free;
 *
 *   // Create custom user
 *   const customUser = createUser({ email: 'custom@test.com' });
 */

// ============================================================================
// Types
// ============================================================================

export interface User {
  id: string;
  email: string;
  displayName: string | null;
  avatarUrl: string | null;
  createdAt: Date;
  updatedAt: Date;
  isEmailVerified: boolean;
  preferences: UserPreferences;
  onboardingCompleted: boolean;
  lastActiveAt: Date;
}

export interface UserPreferences {
  notificationsEnabled: boolean;
  emailDigest: 'daily' | 'weekly' | 'never';
  theme: 'light' | 'dark' | 'system';
  language: string;
}

// ============================================================================
// Default Values
// ============================================================================

const DEFAULT_PREFERENCES: UserPreferences = {
  notificationsEnabled: true,
  emailDigest: 'weekly',
  theme: 'system',
  language: 'en',
};

const BASE_DATE = new Date('2024-01-15T10:00:00Z');

// ============================================================================
// Factory Functions
// ============================================================================

let userIdCounter = 1;

/**
 * Create a user with custom overrides
 */
export function createUser(overrides: Partial<User> = {}): User {
  const id = overrides.id ?? `user_${userIdCounter++}`;

  return {
    id,
    email: `user${id}@test.com`,
    displayName: null,
    avatarUrl: null,
    createdAt: BASE_DATE,
    updatedAt: BASE_DATE,
    isEmailVerified: true,
    preferences: { ...DEFAULT_PREFERENCES },
    onboardingCompleted: true,
    lastActiveAt: BASE_DATE,
    ...overrides,
    // Merge nested preferences
    ...(overrides.preferences && {
      preferences: { ...DEFAULT_PREFERENCES, ...overrides.preferences },
    }),
  };
}

/**
 * Create multiple users
 */
export function createUsers(count: number, overrides: Partial<User> = {}): User[] {
  return Array.from({ length: count }, () => createUser(overrides));
}

/**
 * Create a new user who hasn't completed onboarding
 */
export function createNewUser(overrides: Partial<User> = {}): User {
  return createUser({
    onboardingCompleted: false,
    isEmailVerified: false,
    displayName: null,
    ...overrides,
  });
}

/**
 * Create an anonymous/guest user
 */
export function createAnonymousUser(): User {
  return createUser({
    id: 'anonymous',
    email: '',
    displayName: 'Guest',
    isEmailVerified: false,
    onboardingCompleted: false,
  });
}

// ============================================================================
// Static Fixtures
// ============================================================================

export const USERS = {
  /**
   * Free tier user with default settings
   */
  free: createUser({
    id: 'user_free',
    email: 'free@test.com',
    displayName: 'Free User',
    onboardingCompleted: true,
  }),

  /**
   * Pro tier user
   */
  pro: createUser({
    id: 'user_pro',
    email: 'pro@test.com',
    displayName: 'Pro User',
    onboardingCompleted: true,
  }),

  /**
   * Premium tier user
   */
  premium: createUser({
    id: 'user_premium',
    email: 'premium@test.com',
    displayName: 'Premium User',
    onboardingCompleted: true,
  }),

  /**
   * New user who hasn't completed onboarding
   */
  new: createNewUser({
    id: 'user_new',
    email: 'new@test.com',
  }),

  /**
   * User with notifications disabled
   */
  noNotifications: createUser({
    id: 'user_no_notifs',
    email: 'quiet@test.com',
    displayName: 'Quiet User',
    preferences: {
      ...DEFAULT_PREFERENCES,
      notificationsEnabled: false,
      emailDigest: 'never',
    },
  }),

  /**
   * User preferring dark mode
   */
  darkMode: createUser({
    id: 'user_dark',
    email: 'dark@test.com',
    displayName: 'Dark Mode User',
    preferences: {
      ...DEFAULT_PREFERENCES,
      theme: 'dark',
    },
  }),

  /**
   * Unverified user
   */
  unverified: createUser({
    id: 'user_unverified',
    email: 'unverified@test.com',
    isEmailVerified: false,
  }),

  /**
   * Long-time user with lots of activity
   */
  veteran: createUser({
    id: 'user_veteran',
    email: 'veteran@test.com',
    displayName: 'Veteran User',
    createdAt: new Date('2022-01-01T00:00:00Z'),
    lastActiveAt: new Date(),
  }),
} as const;

// ============================================================================
// Auth Related Fixtures
// ============================================================================

export interface AuthCredentials {
  email: string;
  password: string;
}

export const VALID_CREDENTIALS: AuthCredentials = {
  email: 'test@example.com',
  password: 'Password123!',
};

export const INVALID_CREDENTIALS: AuthCredentials = {
  email: 'invalid@example.com',
  password: 'wrongpassword',
};

export interface AuthSession {
  accessToken: string;
  refreshToken: string;
  expiresAt: number;
  user: User;
}

export function createAuthSession(user: User = USERS.free): AuthSession {
  return {
    accessToken: `access_token_${user.id}`,
    refreshToken: `refresh_token_${user.id}`,
    expiresAt: Date.now() + 3600 * 1000, // 1 hour from now
    user,
  };
}

export function createExpiredSession(user: User = USERS.free): AuthSession {
  return {
    ...createAuthSession(user),
    expiresAt: Date.now() - 1000, // Expired 1 second ago
  };
}

// ============================================================================
// Reset Counter (for test isolation)
// ============================================================================

export function resetUserIdCounter(): void {
  userIdCounter = 1;
}
