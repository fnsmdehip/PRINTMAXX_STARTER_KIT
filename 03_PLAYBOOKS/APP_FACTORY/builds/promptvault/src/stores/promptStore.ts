import { create } from 'zustand';
import Fuse from 'fuse.js';
import { Prompt, Category, UserPrompt } from '../types';
import prompts from '../data/prompts';

interface PromptState {
  prompts: Prompt[];
  userPrompts: UserPrompt[];
  selectedCategory: Category | null;
  searchQuery: string;
  filteredPrompts: Prompt[];

  // Actions
  setSelectedCategory: (category: Category | null) => void;
  setSearchQuery: (query: string) => void;
  getPromptById: (id: string) => Prompt | undefined;
  addUserPrompt: (prompt: Omit<UserPrompt, 'id' | 'createdAt' | 'updatedAt'>) => void;
  updateUserPrompt: (id: string, updates: Partial<UserPrompt>) => void;
  deleteUserPrompt: (id: string) => void;
}

const fuseOptions = {
  keys: [
    { name: 'title', weight: 0.4 },
    { name: 'tags', weight: 0.3 },
    { name: 'content', weight: 0.2 },
    { name: 'useCases', weight: 0.1 },
  ],
  threshold: 0.4,
  includeScore: true,
};

const filterPrompts = (
  allPrompts: Prompt[],
  category: Category | null,
  query: string
): Prompt[] => {
  let filtered = allPrompts;

  // Filter by category
  if (category) {
    filtered = filtered.filter((p) => p.category === category);
  }

  // Filter by search query
  if (query.trim()) {
    const fuse = new Fuse(filtered, fuseOptions);
    filtered = fuse.search(query).map((result) => result.item);
  }

  return filtered;
};

export const usePromptStore = create<PromptState>((set, get) => ({
  prompts,
  userPrompts: [],
  selectedCategory: null,
  searchQuery: '',
  filteredPrompts: prompts,

  setSelectedCategory: (category) => {
    const { prompts, searchQuery } = get();
    set({
      selectedCategory: category,
      filteredPrompts: filterPrompts(prompts, category, searchQuery),
    });
  },

  setSearchQuery: (query) => {
    const { prompts, selectedCategory } = get();
    set({
      searchQuery: query,
      filteredPrompts: filterPrompts(prompts, selectedCategory, query),
    });
  },

  getPromptById: (id) => {
    const { prompts, userPrompts } = get();
    return prompts.find((p) => p.id === id) || userPrompts.find((p) => p.id === id) as Prompt | undefined;
  },

  addUserPrompt: (prompt) => {
    const now = new Date().toISOString();
    const newPrompt: UserPrompt = {
      ...prompt,
      id: `user-${Date.now()}`,
      createdAt: now,
      updatedAt: now,
    };
    set((state) => ({
      userPrompts: [...state.userPrompts, newPrompt],
    }));
  },

  updateUserPrompt: (id, updates) => {
    set((state) => ({
      userPrompts: state.userPrompts.map((p) =>
        p.id === id ? { ...p, ...updates, updatedAt: new Date().toISOString() } : p
      ),
    }));
  },

  deleteUserPrompt: (id) => {
    set((state) => ({
      userPrompts: state.userPrompts.filter((p) => p.id !== id),
    }));
  },
}));
