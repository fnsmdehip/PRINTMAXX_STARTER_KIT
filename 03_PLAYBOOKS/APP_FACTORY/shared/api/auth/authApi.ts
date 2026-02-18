/**
 * authApi.ts - Authentication API endpoints
 */

import { apiClient } from '../ApiClient';
import { tokenManager, TokenPair } from './tokenManager';
import type { SuccessResponse } from '../types/ApiResponse';

// ============================================================================
// Types
// ============================================================================

export interface LoginRequest {
  email: string;
  password: string;
  rememberMe?: boolean;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name?: string;
  acceptedTerms: boolean;
}

export interface SocialAuthRequest {
  provider: 'google' | 'apple' | 'facebook';
  token: string;
  nonce?: string; // For Apple Sign In
}

export interface ForgotPasswordRequest {
  email: string;
}

export interface ResetPasswordRequest {
  token: string;
  password: string;
  confirmPassword: string;
}

export interface ChangePasswordRequest {
  currentPassword: string;
  newPassword: string;
}

export interface VerifyEmailRequest {
  token: string;
}

export interface RefreshTokenRequest {
  refreshToken: string;
}

export interface AuthResponse {
  user: AuthUser;
  tokens: TokenPair;
}

export interface AuthUser {
  id: string;
  email: string;
  name: string | null;
  avatar: string | null;
  emailVerified: boolean;
  createdAt: string;
}

export interface SessionInfo {
  id: string;
  device: string;
  ip: string;
  lastActive: string;
  current: boolean;
}

// ============================================================================
// Auth API Class
// ============================================================================

class AuthApi {
  private readonly basePath = '/auth';

  // --------------------------------------------------------------------------
  // Authentication
  // --------------------------------------------------------------------------

  /**
   * Login with email and password
   */
  async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>(
      `${this.basePath}/login`,
      data,
      { skipAuth: true }
    );

    await tokenManager.setTokens(response.tokens);
    return response;
  }

  /**
   * Register a new account
   */
  async register(data: RegisterRequest): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>(
      `${this.basePath}/register`,
      data,
      { skipAuth: true }
    );

    await tokenManager.setTokens(response.tokens);
    return response;
  }

  /**
   * Authenticate with social provider
   */
  async socialAuth(data: SocialAuthRequest): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>(
      `${this.basePath}/social/${data.provider}`,
      { token: data.token, nonce: data.nonce },
      { skipAuth: true }
    );

    await tokenManager.setTokens(response.tokens);
    return response;
  }

  /**
   * Logout current session
   */
  async logout(): Promise<void> {
    try {
      await apiClient.post(`${this.basePath}/logout`);
    } finally {
      // Always clear local tokens even if API call fails
      await tokenManager.clearTokens();
    }
  }

  /**
   * Logout all sessions
   */
  async logoutAll(): Promise<void> {
    try {
      await apiClient.post(`${this.basePath}/logout-all`);
    } finally {
      await tokenManager.clearTokens();
    }
  }

  // --------------------------------------------------------------------------
  // Token Management
  // --------------------------------------------------------------------------

  /**
   * Refresh access token
   */
  async refreshToken(refreshToken: string): Promise<TokenPair> {
    const response = await apiClient.post<TokenPair>(
      `${this.basePath}/refresh`,
      { refreshToken },
      { skipAuth: true }
    );

    await tokenManager.setTokens(response);
    return response;
  }

  /**
   * Verify access token is valid
   */
  async verifyToken(): Promise<{ valid: boolean; expiresIn: number }> {
    return apiClient.get(`${this.basePath}/verify`);
  }

  // --------------------------------------------------------------------------
  // Password Management
  // --------------------------------------------------------------------------

  /**
   * Request password reset email
   */
  async forgotPassword(data: ForgotPasswordRequest): Promise<SuccessResponse> {
    return apiClient.post(`${this.basePath}/forgot-password`, data, {
      skipAuth: true,
    });
  }

  /**
   * Reset password with token
   */
  async resetPassword(data: ResetPasswordRequest): Promise<SuccessResponse> {
    return apiClient.post(`${this.basePath}/reset-password`, data, {
      skipAuth: true,
    });
  }

  /**
   * Change password (authenticated)
   */
  async changePassword(data: ChangePasswordRequest): Promise<SuccessResponse> {
    return apiClient.post(`${this.basePath}/change-password`, data);
  }

  // --------------------------------------------------------------------------
  // Email Verification
  // --------------------------------------------------------------------------

  /**
   * Verify email with token
   */
  async verifyEmail(data: VerifyEmailRequest): Promise<SuccessResponse> {
    return apiClient.post(`${this.basePath}/verify-email`, data, {
      skipAuth: true,
    });
  }

  /**
   * Resend verification email
   */
  async resendVerificationEmail(): Promise<SuccessResponse> {
    return apiClient.post(`${this.basePath}/resend-verification`);
  }

  // --------------------------------------------------------------------------
  // Session Management
  // --------------------------------------------------------------------------

  /**
   * Get current user info
   */
  async getCurrentUser(): Promise<AuthUser> {
    return apiClient.get(`${this.basePath}/me`);
  }

  /**
   * Get active sessions
   */
  async getSessions(): Promise<SessionInfo[]> {
    return apiClient.get(`${this.basePath}/sessions`);
  }

  /**
   * Revoke a specific session
   */
  async revokeSession(sessionId: string): Promise<SuccessResponse> {
    return apiClient.delete(`${this.basePath}/sessions/${sessionId}`);
  }

  // --------------------------------------------------------------------------
  // Account Management
  // --------------------------------------------------------------------------

  /**
   * Delete account
   */
  async deleteAccount(password: string): Promise<SuccessResponse> {
    const response = await apiClient.post<SuccessResponse>(
      `${this.basePath}/delete-account`,
      { password }
    );

    await tokenManager.clearTokens();
    return response;
  }

  /**
   * Check if email is available
   */
  async checkEmailAvailability(email: string): Promise<{ available: boolean }> {
    return apiClient.post(
      `${this.basePath}/check-email`,
      { email },
      { skipAuth: true }
    );
  }
}

// ============================================================================
// Singleton Export
// ============================================================================

export const authApi = new AuthApi();

export default authApi;
