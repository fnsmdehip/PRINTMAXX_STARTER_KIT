/**
 * contentApi.ts - Content management endpoints
 */

import { apiClient } from '../ApiClient';
import type { SuccessResponse, PaginatedResponse } from '../types/ApiResponse';
import type { PagePaginationParams } from '../types/PaginatedResponse';

// ============================================================================
// Types
// ============================================================================

export type ContentStatus = 'draft' | 'published' | 'archived' | 'scheduled';
export type ContentType = 'article' | 'post' | 'video' | 'image' | 'audio';

export interface Content {
  id: string;
  type: ContentType;
  title: string;
  slug: string;
  excerpt: string | null;
  body: string;
  status: ContentStatus;
  author: {
    id: string;
    name: string;
    avatar: string | null;
  };
  coverImage: string | null;
  tags: string[];
  categories: string[];
  metadata: ContentMetadata;
  stats: ContentStats;
  publishedAt: string | null;
  scheduledAt: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface ContentMetadata {
  seo: {
    title: string | null;
    description: string | null;
    keywords: string[];
    canonicalUrl: string | null;
  };
  social: {
    ogImage: string | null;
    twitterCard: 'summary' | 'summary_large_image' | null;
  };
  reading: {
    estimatedMinutes: number;
    wordCount: number;
  };
}

export interface ContentStats {
  views: number;
  likes: number;
  comments: number;
  shares: number;
  bookmarks: number;
}

export interface ContentListItem {
  id: string;
  type: ContentType;
  title: string;
  slug: string;
  excerpt: string | null;
  coverImage: string | null;
  status: ContentStatus;
  author: {
    id: string;
    name: string;
    avatar: string | null;
  };
  stats: Pick<ContentStats, 'views' | 'likes' | 'comments'>;
  publishedAt: string | null;
  createdAt: string;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  parentId: string | null;
  contentCount: number;
}

export interface Tag {
  id: string;
  name: string;
  slug: string;
  contentCount: number;
}

export interface Comment {
  id: string;
  contentId: string;
  author: {
    id: string;
    name: string;
    avatar: string | null;
  };
  body: string;
  parentId: string | null;
  likes: number;
  replies: number;
  isLiked: boolean;
  createdAt: string;
  updatedAt: string;
}

// ============================================================================
// Request Types
// ============================================================================

export interface CreateContentRequest {
  type: ContentType;
  title: string;
  body: string;
  excerpt?: string;
  coverImage?: string;
  tags?: string[];
  categories?: string[];
  status?: ContentStatus;
  scheduledAt?: string;
  metadata?: Partial<ContentMetadata>;
}

export interface UpdateContentRequest {
  title?: string;
  body?: string;
  excerpt?: string;
  coverImage?: string;
  tags?: string[];
  categories?: string[];
  status?: ContentStatus;
  scheduledAt?: string;
  metadata?: Partial<ContentMetadata>;
}

export interface ContentFilterParams extends PagePaginationParams {
  type?: ContentType;
  status?: ContentStatus;
  authorId?: string;
  category?: string;
  tag?: string;
  search?: string;
}

export interface CreateCommentRequest {
  body: string;
  parentId?: string;
}

// ============================================================================
// Content API Class
// ============================================================================

class ContentApi {
  private readonly basePath = '/content';

  // --------------------------------------------------------------------------
  // Content CRUD
  // --------------------------------------------------------------------------

  /**
   * Get content list
   */
  async getContent(
    params?: ContentFilterParams
  ): Promise<PaginatedResponse<ContentListItem>> {
    return apiClient.get(this.basePath, { params });
  }

  /**
   * Get content by ID
   */
  async getContentById(contentId: string): Promise<Content> {
    return apiClient.get(`${this.basePath}/${contentId}`);
  }

  /**
   * Get content by slug
   */
  async getContentBySlug(slug: string): Promise<Content> {
    return apiClient.get(`${this.basePath}/slug/${slug}`);
  }

  /**
   * Create content
   */
  async createContent(data: CreateContentRequest): Promise<Content> {
    return apiClient.post(this.basePath, data);
  }

  /**
   * Update content
   */
  async updateContent(
    contentId: string,
    data: UpdateContentRequest
  ): Promise<Content> {
    return apiClient.patch(`${this.basePath}/${contentId}`, data);
  }

  /**
   * Delete content
   */
  async deleteContent(contentId: string): Promise<SuccessResponse> {
    return apiClient.delete(`${this.basePath}/${contentId}`);
  }

  /**
   * Publish content
   */
  async publishContent(contentId: string): Promise<Content> {
    return apiClient.post(`${this.basePath}/${contentId}/publish`);
  }

  /**
   * Unpublish content
   */
  async unpublishContent(contentId: string): Promise<Content> {
    return apiClient.post(`${this.basePath}/${contentId}/unpublish`);
  }

  /**
   * Schedule content
   */
  async scheduleContent(
    contentId: string,
    scheduledAt: string
  ): Promise<Content> {
    return apiClient.post(`${this.basePath}/${contentId}/schedule`, {
      scheduledAt,
    });
  }

  /**
   * Archive content
   */
  async archiveContent(contentId: string): Promise<Content> {
    return apiClient.post(`${this.basePath}/${contentId}/archive`);
  }

  /**
   * Duplicate content
   */
  async duplicateContent(contentId: string): Promise<Content> {
    return apiClient.post(`${this.basePath}/${contentId}/duplicate`);
  }

  // --------------------------------------------------------------------------
  // User Content
  // --------------------------------------------------------------------------

  /**
   * Get current user's content
   */
  async getMyContent(
    params?: ContentFilterParams
  ): Promise<PaginatedResponse<ContentListItem>> {
    return apiClient.get(`${this.basePath}/me`, { params });
  }

  /**
   * Get user's drafts
   */
  async getMyDrafts(
    params?: PagePaginationParams
  ): Promise<PaginatedResponse<ContentListItem>> {
    return apiClient.get(`${this.basePath}/me/drafts`, { params });
  }

  /**
   * Get user's bookmarks
   */
  async getMyBookmarks(
    params?: PagePaginationParams
  ): Promise<PaginatedResponse<ContentListItem>> {
    return apiClient.get(`${this.basePath}/me/bookmarks`, { params });
  }

  // --------------------------------------------------------------------------
  // Interactions
  // --------------------------------------------------------------------------

  /**
   * Like content
   */
  async likeContent(contentId: string): Promise<{ likes: number }> {
    return apiClient.post(`${this.basePath}/${contentId}/like`);
  }

  /**
   * Unlike content
   */
  async unlikeContent(contentId: string): Promise<{ likes: number }> {
    return apiClient.delete(`${this.basePath}/${contentId}/like`);
  }

  /**
   * Bookmark content
   */
  async bookmarkContent(contentId: string): Promise<SuccessResponse> {
    return apiClient.post(`${this.basePath}/${contentId}/bookmark`);
  }

  /**
   * Remove bookmark
   */
  async removeBookmark(contentId: string): Promise<SuccessResponse> {
    return apiClient.delete(`${this.basePath}/${contentId}/bookmark`);
  }

  /**
   * Share content (track share)
   */
  async trackShare(
    contentId: string,
    platform: string
  ): Promise<{ shares: number }> {
    return apiClient.post(`${this.basePath}/${contentId}/share`, { platform });
  }

  /**
   * Report content
   */
  async reportContent(
    contentId: string,
    reason: string,
    details?: string
  ): Promise<SuccessResponse> {
    return apiClient.post(`${this.basePath}/${contentId}/report`, {
      reason,
      details,
    });
  }

  // --------------------------------------------------------------------------
  // Comments
  // --------------------------------------------------------------------------

  /**
   * Get comments for content
   */
  async getComments(
    contentId: string,
    params?: PagePaginationParams
  ): Promise<PaginatedResponse<Comment>> {
    return apiClient.get(`${this.basePath}/${contentId}/comments`, { params });
  }

  /**
   * Create comment
   */
  async createComment(
    contentId: string,
    data: CreateCommentRequest
  ): Promise<Comment> {
    return apiClient.post(`${this.basePath}/${contentId}/comments`, data);
  }

  /**
   * Update comment
   */
  async updateComment(
    contentId: string,
    commentId: string,
    body: string
  ): Promise<Comment> {
    return apiClient.patch(
      `${this.basePath}/${contentId}/comments/${commentId}`,
      { body }
    );
  }

  /**
   * Delete comment
   */
  async deleteComment(
    contentId: string,
    commentId: string
  ): Promise<SuccessResponse> {
    return apiClient.delete(
      `${this.basePath}/${contentId}/comments/${commentId}`
    );
  }

  /**
   * Like comment
   */
  async likeComment(
    contentId: string,
    commentId: string
  ): Promise<{ likes: number }> {
    return apiClient.post(
      `${this.basePath}/${contentId}/comments/${commentId}/like`
    );
  }

  /**
   * Unlike comment
   */
  async unlikeComment(
    contentId: string,
    commentId: string
  ): Promise<{ likes: number }> {
    return apiClient.delete(
      `${this.basePath}/${contentId}/comments/${commentId}/like`
    );
  }

  // --------------------------------------------------------------------------
  // Categories & Tags
  // --------------------------------------------------------------------------

  /**
   * Get categories
   */
  async getCategories(): Promise<Category[]> {
    return apiClient.get(`${this.basePath}/categories`, { skipAuth: true });
  }

  /**
   * Get tags
   */
  async getTags(params?: { limit?: number }): Promise<Tag[]> {
    return apiClient.get(`${this.basePath}/tags`, {
      params,
      skipAuth: true,
    });
  }

  /**
   * Get popular tags
   */
  async getPopularTags(limit: number = 20): Promise<Tag[]> {
    return apiClient.get(`${this.basePath}/tags/popular`, {
      params: { limit },
      skipAuth: true,
    });
  }

  // --------------------------------------------------------------------------
  // Search & Discovery
  // --------------------------------------------------------------------------

  /**
   * Search content
   */
  async searchContent(
    query: string,
    params?: ContentFilterParams
  ): Promise<PaginatedResponse<ContentListItem>> {
    return apiClient.get(`${this.basePath}/search`, {
      params: { q: query, ...params },
      skipAuth: true,
    });
  }

  /**
   * Get trending content
   */
  async getTrendingContent(
    params?: { period?: 'day' | 'week' | 'month'; limit?: number }
  ): Promise<ContentListItem[]> {
    return apiClient.get(`${this.basePath}/trending`, {
      params,
      skipAuth: true,
    });
  }

  /**
   * Get featured content
   */
  async getFeaturedContent(limit: number = 5): Promise<ContentListItem[]> {
    return apiClient.get(`${this.basePath}/featured`, {
      params: { limit },
      skipAuth: true,
    });
  }

  /**
   * Get related content
   */
  async getRelatedContent(
    contentId: string,
    limit: number = 5
  ): Promise<ContentListItem[]> {
    return apiClient.get(`${this.basePath}/${contentId}/related`, {
      params: { limit },
      skipAuth: true,
    });
  }

  // --------------------------------------------------------------------------
  // Media Upload
  // --------------------------------------------------------------------------

  /**
   * Get upload URL for media
   */
  async getUploadUrl(
    filename: string,
    contentType: string
  ): Promise<{ uploadUrl: string; fileUrl: string }> {
    return apiClient.post(`${this.basePath}/upload-url`, {
      filename,
      contentType,
    });
  }

  /**
   * Upload media directly
   */
  async uploadMedia(
    file: FormData
  ): Promise<{ url: string; thumbnailUrl?: string }> {
    return apiClient.post(`${this.basePath}/upload`, file, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }
}

// ============================================================================
// Singleton Export
// ============================================================================

export const contentApi = new ContentApi();

export default contentApi;
