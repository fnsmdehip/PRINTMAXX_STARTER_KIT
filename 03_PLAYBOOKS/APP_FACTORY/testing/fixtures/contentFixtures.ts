/**
 * Content test fixtures and factory functions
 *
 * Usage:
 *   import { createPost, createCategory, POSTS } from '@testing/fixtures/contentFixtures';
 */

// ============================================================================
// Types
// ============================================================================

export interface Post {
  id: string;
  title: string;
  slug: string;
  excerpt: string;
  content: string;
  featuredImage: string | null;
  authorId: string;
  categoryId: string;
  tags: string[];
  status: 'draft' | 'published' | 'archived';
  publishedAt: Date | null;
  createdAt: Date;
  updatedAt: Date;
  readingTimeMinutes: number;
  viewCount: number;
  isPremium: boolean;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  description: string;
  parentId: string | null;
  imageUrl: string | null;
  postCount: number;
  order: number;
}

export interface Tag {
  id: string;
  name: string;
  slug: string;
  postCount: number;
}

export interface MediaItem {
  id: string;
  url: string;
  thumbnailUrl: string;
  type: 'image' | 'video' | 'audio' | 'document';
  mimeType: string;
  filename: string;
  size: number;
  width: number | null;
  height: number | null;
  duration: number | null;
  altText: string;
  uploadedAt: Date;
}

export interface Comment {
  id: string;
  postId: string;
  userId: string;
  content: string;
  parentId: string | null;
  status: 'pending' | 'approved' | 'spam' | 'deleted';
  createdAt: Date;
  updatedAt: Date;
  replyCount: number;
  likeCount: number;
}

// ============================================================================
// Factory Functions
// ============================================================================

let postIdCounter = 1;
let categoryIdCounter = 1;
let tagIdCounter = 1;
let mediaIdCounter = 1;
let commentIdCounter = 1;

const BASE_DATE = new Date('2024-01-15T10:00:00Z');

/**
 * Create a post with custom overrides
 */
export function createPost(overrides: Partial<Post> = {}): Post {
  const id = overrides.id ?? `post_${postIdCounter++}`;
  const title = overrides.title ?? `Test Post ${id}`;

  return {
    id,
    title,
    slug: overrides.slug ?? title.toLowerCase().replace(/\s+/g, '-'),
    excerpt: 'This is a test post excerpt for testing purposes.',
    content: '<p>This is the full content of the test post. It includes multiple paragraphs and formatting.</p><p>Second paragraph here.</p>',
    featuredImage: null,
    authorId: 'user_1',
    categoryId: 'category_1',
    tags: ['test', 'fixture'],
    status: 'published',
    publishedAt: BASE_DATE,
    createdAt: BASE_DATE,
    updatedAt: BASE_DATE,
    readingTimeMinutes: 3,
    viewCount: 0,
    isPremium: false,
    ...overrides,
  };
}

/**
 * Create multiple posts
 */
export function createPosts(count: number, overrides: Partial<Post> = {}): Post[] {
  return Array.from({ length: count }, (_, i) =>
    createPost({
      title: `Test Post ${i + 1}`,
      ...overrides,
    })
  );
}

/**
 * Create a draft post
 */
export function createDraftPost(overrides: Partial<Post> = {}): Post {
  return createPost({
    status: 'draft',
    publishedAt: null,
    ...overrides,
  });
}

/**
 * Create a premium post
 */
export function createPremiumPost(overrides: Partial<Post> = {}): Post {
  return createPost({
    isPremium: true,
    title: 'Premium Content',
    ...overrides,
  });
}

/**
 * Create a category with custom overrides
 */
export function createCategory(overrides: Partial<Category> = {}): Category {
  const id = overrides.id ?? `category_${categoryIdCounter++}`;
  const name = overrides.name ?? `Category ${id}`;

  return {
    id,
    name,
    slug: overrides.slug ?? name.toLowerCase().replace(/\s+/g, '-'),
    description: 'A test category for organizing content.',
    parentId: null,
    imageUrl: null,
    postCount: 0,
    order: 0,
    ...overrides,
  };
}

/**
 * Create multiple categories
 */
export function createCategories(count: number): Category[] {
  return Array.from({ length: count }, (_, i) =>
    createCategory({
      name: `Category ${i + 1}`,
      order: i,
    })
  );
}

/**
 * Create a tag
 */
export function createTag(overrides: Partial<Tag> = {}): Tag {
  const id = overrides.id ?? `tag_${tagIdCounter++}`;
  const name = overrides.name ?? `tag-${id}`;

  return {
    id,
    name,
    slug: name.toLowerCase().replace(/\s+/g, '-'),
    postCount: 0,
    ...overrides,
  };
}

/**
 * Create multiple tags
 */
export function createTags(names: string[]): Tag[] {
  return names.map((name) => createTag({ name }));
}

/**
 * Create a media item
 */
export function createMediaItem(overrides: Partial<MediaItem> = {}): MediaItem {
  const id = overrides.id ?? `media_${mediaIdCounter++}`;

  return {
    id,
    url: `https://example.com/media/${id}.jpg`,
    thumbnailUrl: `https://example.com/media/${id}_thumb.jpg`,
    type: 'image',
    mimeType: 'image/jpeg',
    filename: `image_${id}.jpg`,
    size: 102400, // 100KB
    width: 1200,
    height: 800,
    duration: null,
    altText: 'Test image',
    uploadedAt: BASE_DATE,
    ...overrides,
  };
}

/**
 * Create a video media item
 */
export function createVideoMedia(overrides: Partial<MediaItem> = {}): MediaItem {
  const id = overrides.id ?? `media_${mediaIdCounter++}`;

  return createMediaItem({
    id,
    url: `https://example.com/media/${id}.mp4`,
    thumbnailUrl: `https://example.com/media/${id}_thumb.jpg`,
    type: 'video',
    mimeType: 'video/mp4',
    filename: `video_${id}.mp4`,
    size: 10485760, // 10MB
    width: 1920,
    height: 1080,
    duration: 120, // 2 minutes
    ...overrides,
  });
}

/**
 * Create a comment
 */
export function createComment(overrides: Partial<Comment> = {}): Comment {
  const id = overrides.id ?? `comment_${commentIdCounter++}`;

  return {
    id,
    postId: 'post_1',
    userId: 'user_1',
    content: 'This is a test comment.',
    parentId: null,
    status: 'approved',
    createdAt: BASE_DATE,
    updatedAt: BASE_DATE,
    replyCount: 0,
    likeCount: 0,
    ...overrides,
  };
}

/**
 * Create a comment thread (parent with replies)
 */
export function createCommentThread(
  replyCount: number = 3,
  overrides: Partial<Comment> = {}
): Comment[] {
  const parent = createComment(overrides);
  const replies = Array.from({ length: replyCount }, (_, i) =>
    createComment({
      parentId: parent.id,
      content: `Reply ${i + 1} to the parent comment.`,
      userId: `user_${i + 2}`,
    })
  );

  return [parent, ...replies];
}

// ============================================================================
// Static Fixtures
// ============================================================================

export const CATEGORIES = {
  tutorials: createCategory({
    id: 'category_tutorials',
    name: 'Tutorials',
    description: 'Step-by-step guides and how-tos',
    postCount: 15,
    order: 0,
  }),
  news: createCategory({
    id: 'category_news',
    name: 'News',
    description: 'Latest updates and announcements',
    postCount: 8,
    order: 1,
  }),
  tips: createCategory({
    id: 'category_tips',
    name: 'Tips & Tricks',
    description: 'Quick tips to improve your workflow',
    postCount: 12,
    order: 2,
  }),
  premium: createCategory({
    id: 'category_premium',
    name: 'Premium Content',
    description: 'Exclusive content for subscribers',
    postCount: 5,
    order: 3,
  }),
} as const;

export const TAGS = {
  beginner: createTag({ id: 'tag_beginner', name: 'beginner', postCount: 10 }),
  advanced: createTag({ id: 'tag_advanced', name: 'advanced', postCount: 5 }),
  featured: createTag({ id: 'tag_featured', name: 'featured', postCount: 3 }),
  trending: createTag({ id: 'tag_trending', name: 'trending', postCount: 7 }),
} as const;

export const POSTS = {
  published: createPost({
    id: 'post_published',
    title: 'Getting Started Guide',
    slug: 'getting-started-guide',
    categoryId: CATEGORIES.tutorials.id,
    tags: ['beginner', 'featured'],
    viewCount: 1250,
  }),
  draft: createDraftPost({
    id: 'post_draft',
    title: 'Upcoming Feature Preview',
    slug: 'upcoming-feature-preview',
  }),
  premium: createPremiumPost({
    id: 'post_premium',
    title: 'Advanced Techniques',
    slug: 'advanced-techniques',
    categoryId: CATEGORIES.premium.id,
    tags: ['advanced'],
  }),
  popular: createPost({
    id: 'post_popular',
    title: 'Most Popular Post',
    slug: 'most-popular-post',
    viewCount: 15000,
    tags: ['trending', 'featured'],
  }),
  longForm: createPost({
    id: 'post_long',
    title: 'Comprehensive Guide to Everything',
    slug: 'comprehensive-guide',
    content: '<p>'.repeat(50) + 'Long content...</p>'.repeat(50),
    readingTimeMinutes: 25,
  }),
  archived: createPost({
    id: 'post_archived',
    title: 'Archived Post',
    slug: 'archived-post',
    status: 'archived',
  }),
} as const;

export const MEDIA = {
  featuredImage: createMediaItem({
    id: 'media_featured',
    altText: 'Featured article image',
    width: 1200,
    height: 630,
  }),
  thumbnail: createMediaItem({
    id: 'media_thumb',
    altText: 'Thumbnail image',
    width: 300,
    height: 200,
    size: 25600,
  }),
  video: createVideoMedia({
    id: 'media_video',
    duration: 300,
  }),
  avatar: createMediaItem({
    id: 'media_avatar',
    altText: 'User avatar',
    width: 200,
    height: 200,
    size: 15360,
  }),
} as const;

// ============================================================================
// Feed/List Response Mocks
// ============================================================================

export interface PaginatedResponse<T> {
  data: T[];
  meta: {
    total: number;
    page: number;
    perPage: number;
    totalPages: number;
    hasMore: boolean;
  };
}

export function createPaginatedPosts(
  page: number = 1,
  perPage: number = 10,
  total: number = 50
): PaginatedResponse<Post> {
  const totalPages = Math.ceil(total / perPage);
  const startIndex = (page - 1) * perPage;
  const posts = createPosts(Math.min(perPage, total - startIndex));

  return {
    data: posts,
    meta: {
      total,
      page,
      perPage,
      totalPages,
      hasMore: page < totalPages,
    },
  };
}

export function createEmptyPaginatedResponse<T>(): PaginatedResponse<T> {
  return {
    data: [],
    meta: {
      total: 0,
      page: 1,
      perPage: 10,
      totalPages: 0,
      hasMore: false,
    },
  };
}

// ============================================================================
// Reset Counters
// ============================================================================

export function resetContentIdCounters(): void {
  postIdCounter = 1;
  categoryIdCounter = 1;
  tagIdCounter = 1;
  mediaIdCounter = 1;
  commentIdCounter = 1;
}
