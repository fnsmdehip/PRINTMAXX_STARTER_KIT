/**
 * userApi.ts - User management endpoints
 */

import { apiClient } from '../ApiClient';
import type { SuccessResponse, PaginatedResponse } from '../types/ApiResponse';
import type { PagePaginationParams } from '../types/PaginatedResponse';

// ============================================================================
// Types
// ============================================================================

export interface User {
  id: string;
  email: string;
  name: string | null;
  avatar: string | null;
  bio: string | null;
  timezone: string;
  locale: string;
  emailVerified: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface UserProfile extends User {
  phone: string | null;
  website: string | null;
  location: string | null;
  socialLinks: {
    twitter?: string;
    linkedin?: string;
    github?: string;
  };
}

export interface UpdateProfileRequest {
  name?: string;
  bio?: string;
  timezone?: string;
  locale?: string;
  phone?: string;
  website?: string;
  location?: string;
  socialLinks?: {
    twitter?: string;
    linkedin?: string;
    github?: string;
  };
}

export interface UpdateAvatarResponse {
  avatarUrl: string;
}

export interface UserPreferences {
  notifications: {
    email: boolean;
    push: boolean;
    marketing: boolean;
    updates: boolean;
  };
  privacy: {
    profilePublic: boolean;
    showEmail: boolean;
    showActivity: boolean;
  };
  appearance: {
    theme: 'light' | 'dark' | 'system';
    fontSize: 'small' | 'medium' | 'large';
    reducedMotion: boolean;
  };
}

export interface UpdatePreferencesRequest {
  notifications?: Partial<UserPreferences['notifications']>;
  privacy?: Partial<UserPreferences['privacy']>;
  appearance?: Partial<UserPreferences['appearance']>;
}

export interface UserActivity {
  id: string;
  type: string;
  description: string;
  metadata: Record<string, unknown>;
  timestamp: string;
}

export interface UserStats {
  totalPosts: number;
  totalViews: number;
  totalLikes: number;
  totalFollowers: number;
  totalFollowing: number;
  memberSince: string;
  lastActive: string;
}

// ============================================================================
// User API Class
// ============================================================================

class UserApi {
  private readonly basePath = '/users';

  // --------------------------------------------------------------------------
  // Profile
  // --------------------------------------------------------------------------

  /**
   * Get current user profile
   */
  async getProfile(): Promise<UserProfile> {
    return apiClient.get(`${this.basePath}/me`);
  }

  /**
   * Update current user profile
   */
  async updateProfile(data: UpdateProfileRequest): Promise<UserProfile> {
    return apiClient.patch(`${this.basePath}/me`, data);
  }

  /**
   * Upload avatar
   */
  async uploadAvatar(file: FormData): Promise<UpdateAvatarResponse> {
    return apiClient.post(`${this.basePath}/me/avatar`, file, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }

  /**
   * Delete avatar
   */
  async deleteAvatar(): Promise<SuccessResponse> {
    return apiClient.delete(`${this.basePath}/me/avatar`);
  }

  // --------------------------------------------------------------------------
  // Preferences
  // --------------------------------------------------------------------------

  /**
   * Get user preferences
   */
  async getPreferences(): Promise<UserPreferences> {
    return apiClient.get(`${this.basePath}/me/preferences`);
  }

  /**
   * Update user preferences
   */
  async updatePreferences(data: UpdatePreferencesRequest): Promise<UserPreferences> {
    return apiClient.patch(`${this.basePath}/me/preferences`, data);
  }

  // --------------------------------------------------------------------------
  // Activity & Stats
  // --------------------------------------------------------------------------

  /**
   * Get user activity history
   */
  async getActivity(
    params?: PagePaginationParams
  ): Promise<PaginatedResponse<UserActivity>> {
    return apiClient.get(`${this.basePath}/me/activity`, { params });
  }

  /**
   * Get user stats
   */
  async getStats(): Promise<UserStats> {
    return apiClient.get(`${this.basePath}/me/stats`);
  }

  // --------------------------------------------------------------------------
  // Other Users
  // --------------------------------------------------------------------------

  /**
   * Get user by ID
   */
  async getUserById(userId: string): Promise<User> {
    return apiClient.get(`${this.basePath}/${userId}`);
  }

  /**
   * Get user by username
   */
  async getUserByUsername(username: string): Promise<User> {
    return apiClient.get(`${this.basePath}/username/${username}`);
  }

  /**
   * Search users
   */
  async searchUsers(
    query: string,
    params?: PagePaginationParams
  ): Promise<PaginatedResponse<User>> {
    return apiClient.get(`${this.basePath}/search`, {
      params: { q: query, ...params },
    });
  }

  // --------------------------------------------------------------------------
  // Follow/Unfollow
  // --------------------------------------------------------------------------

  /**
   * Follow a user
   */
  async followUser(userId: string): Promise<SuccessResponse> {
    return apiClient.post(`${this.basePath}/${userId}/follow`);
  }

  /**
   * Unfollow a user
   */
  async unfollowUser(userId: string): Promise<SuccessResponse> {
    return apiClient.delete(`${this.basePath}/${userId}/follow`);
  }

  /**
   * Get followers
   */
  async getFollowers(
    userId: string,
    params?: PagePaginationParams
  ): Promise<PaginatedResponse<User>> {
    return apiClient.get(`${this.basePath}/${userId}/followers`, { params });
  }

  /**
   * Get following
   */
  async getFollowing(
    userId: string,
    params?: PagePaginationParams
  ): Promise<PaginatedResponse<User>> {
    return apiClient.get(`${this.basePath}/${userId}/following`, { params });
  }

  // --------------------------------------------------------------------------
  // Block/Report
  // --------------------------------------------------------------------------

  /**
   * Block a user
   */
  async blockUser(userId: string): Promise<SuccessResponse> {
    return apiClient.post(`${this.basePath}/${userId}/block`);
  }

  /**
   * Unblock a user
   */
  async unblockUser(userId: string): Promise<SuccessResponse> {
    return apiClient.delete(`${this.basePath}/${userId}/block`);
  }

  /**
   * Get blocked users
   */
  async getBlockedUsers(
    params?: PagePaginationParams
  ): Promise<PaginatedResponse<User>> {
    return apiClient.get(`${this.basePath}/me/blocked`, { params });
  }

  /**
   * Report a user
   */
  async reportUser(
    userId: string,
    reason: string,
    details?: string
  ): Promise<SuccessResponse> {
    return apiClient.post(`${this.basePath}/${userId}/report`, {
      reason,
      details,
    });
  }

  // --------------------------------------------------------------------------
  // Data Export
  // --------------------------------------------------------------------------

  /**
   * Request data export (GDPR)
   */
  async requestDataExport(): Promise<{ requestId: string; estimatedTime: string }> {
    return apiClient.post(`${this.basePath}/me/export`);
  }

  /**
   * Get data export status
   */
  async getDataExportStatus(
    requestId: string
  ): Promise<{ status: 'pending' | 'processing' | 'ready' | 'expired'; downloadUrl?: string }> {
    return apiClient.get(`${this.basePath}/me/export/${requestId}`);
  }
}

// ============================================================================
// Singleton Export
// ============================================================================

export const userApi = new UserApi();

export default userApi;
