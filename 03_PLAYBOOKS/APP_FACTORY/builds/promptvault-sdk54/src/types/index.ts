export type Category =
  | 'writing'
  | 'coding'
  | 'marketing'
  | 'analysis'
  | 'creative'
  | 'business'
  | 'productivity'
  | 'learning'
  | 'career';

export interface Prompt {
  id: string;
  title: string;
  content: string;
  category: Category;
  tags: string[];
  preview: string;
  useCases: string[];
  tips: string;
  createdAt: string;
  updatedAt: string;
  isPro?: boolean; // Premium-only prompt (Pro Alpha Prompts)
  isNew?: boolean; // Recently added (shows NEW badge)
}

export interface UserPrompt extends Omit<Prompt, 'useCases' | 'tips'> {
  userId: string;
  folderId?: string;
}

export interface Folder {
  id: string;
  name: string;
  parentId?: string;
  createdAt: string;
}

export interface SubscriptionState {
  isPro: boolean;
  expiresAt?: string;
  trialActive: boolean;
  trialEndsAt?: string;
}

export const CATEGORIES: { key: Category; label: string; icon: string }[] = [
  { key: 'writing', label: 'Writing', icon: 'pencil' },
  { key: 'coding', label: 'Coding', icon: 'code-tags' },
  { key: 'marketing', label: 'Marketing', icon: 'bullhorn' },
  { key: 'analysis', label: 'Analysis', icon: 'chart-bar' },
  { key: 'creative', label: 'Creative', icon: 'lightbulb' },
  { key: 'business', label: 'Business', icon: 'briefcase' },
  { key: 'productivity', label: 'Productivity', icon: 'clock' },
  { key: 'learning', label: 'Learning', icon: 'school' },
  { key: 'career', label: 'Career', icon: 'account-tie' },
];
