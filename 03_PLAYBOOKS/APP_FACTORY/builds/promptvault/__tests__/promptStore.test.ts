import { usePromptStore } from '../src/stores/promptStore';

// Reset store before each test
beforeEach(() => {
  usePromptStore.setState({
    selectedCategory: null,
    searchQuery: '',
    filteredPrompts: usePromptStore.getState().prompts,
    userPrompts: [],
  });
});

describe('promptStore', () => {
  describe('initial state', () => {
    it('should have prompts loaded', () => {
      const { prompts } = usePromptStore.getState();
      expect(prompts.length).toBeGreaterThan(0);
    });

    it('should start with no category selected', () => {
      const { selectedCategory } = usePromptStore.getState();
      expect(selectedCategory).toBeNull();
    });

    it('should start with empty search query', () => {
      const { searchQuery } = usePromptStore.getState();
      expect(searchQuery).toBe('');
    });

    it('should have filteredPrompts equal to all prompts initially', () => {
      const { prompts, filteredPrompts } = usePromptStore.getState();
      expect(filteredPrompts.length).toBe(prompts.length);
    });
  });

  describe('setSelectedCategory', () => {
    it('should filter prompts by category', () => {
      const { setSelectedCategory, filteredPrompts, prompts } =
        usePromptStore.getState();

      setSelectedCategory('writing');

      const state = usePromptStore.getState();
      expect(state.selectedCategory).toBe('writing');
      expect(state.filteredPrompts.every((p) => p.category === 'writing')).toBe(
        true
      );
      expect(state.filteredPrompts.length).toBeLessThan(prompts.length);
    });

    it('should show all prompts when category is null', () => {
      const { setSelectedCategory, prompts } = usePromptStore.getState();

      setSelectedCategory('coding');
      setSelectedCategory(null);

      const state = usePromptStore.getState();
      expect(state.selectedCategory).toBeNull();
      expect(state.filteredPrompts.length).toBe(prompts.length);
    });
  });

  describe('setSearchQuery', () => {
    it('should filter prompts by search query', () => {
      const { setSearchQuery, prompts } = usePromptStore.getState();

      setSearchQuery('blog');

      const state = usePromptStore.getState();
      expect(state.searchQuery).toBe('blog');
      expect(state.filteredPrompts.length).toBeGreaterThan(0);
      expect(state.filteredPrompts.length).toBeLessThanOrEqual(prompts.length);
    });

    it('should return empty array for non-matching search', () => {
      const { setSearchQuery } = usePromptStore.getState();

      setSearchQuery('xyznonexistent123');

      const state = usePromptStore.getState();
      expect(state.filteredPrompts.length).toBe(0);
    });

    it('should combine category and search filters', () => {
      const { setSelectedCategory, setSearchQuery } = usePromptStore.getState();

      setSelectedCategory('writing');
      setSearchQuery('blog');

      const state = usePromptStore.getState();
      expect(state.filteredPrompts.every((p) => p.category === 'writing')).toBe(
        true
      );
    });
  });

  describe('getPromptById', () => {
    it('should return prompt when found', () => {
      const { getPromptById, prompts } = usePromptStore.getState();
      const firstPrompt = prompts[0];

      const found = getPromptById(firstPrompt.id);

      expect(found).toBeDefined();
      expect(found?.id).toBe(firstPrompt.id);
    });

    it('should return undefined when not found', () => {
      const { getPromptById } = usePromptStore.getState();

      const found = getPromptById('nonexistent-id');

      expect(found).toBeUndefined();
    });
  });

  describe('user prompts', () => {
    it('should add user prompt', () => {
      const { addUserPrompt } = usePromptStore.getState();

      addUserPrompt({
        title: 'Test Prompt',
        content: 'Test content',
        category: 'writing',
        tags: ['test'],
        preview: 'Test...',
        userId: 'test-user',
      });

      const state = usePromptStore.getState();
      expect(state.userPrompts.length).toBe(1);
      expect(state.userPrompts[0].title).toBe('Test Prompt');
    });

    it('should generate id and timestamps for new prompts', () => {
      const { addUserPrompt } = usePromptStore.getState();

      addUserPrompt({
        title: 'Test',
        content: 'Content',
        category: 'coding',
        tags: [],
        preview: 'Test',
        userId: 'test',
      });

      const state = usePromptStore.getState();
      expect(state.userPrompts[0].id).toMatch(/^user-\d+$/);
      expect(state.userPrompts[0].createdAt).toBeDefined();
      expect(state.userPrompts[0].updatedAt).toBeDefined();
    });

    it('should update user prompt', () => {
      const { addUserPrompt, updateUserPrompt } = usePromptStore.getState();

      addUserPrompt({
        title: 'Original',
        content: 'Content',
        category: 'coding',
        tags: [],
        preview: 'Test',
        userId: 'test',
      });

      const state1 = usePromptStore.getState();
      const promptId = state1.userPrompts[0].id;

      updateUserPrompt(promptId, { title: 'Updated' });

      const state2 = usePromptStore.getState();
      expect(state2.userPrompts[0].title).toBe('Updated');
    });

    it('should delete user prompt', () => {
      const { addUserPrompt, deleteUserPrompt } = usePromptStore.getState();

      addUserPrompt({
        title: 'To Delete',
        content: 'Content',
        category: 'coding',
        tags: [],
        preview: 'Test',
        userId: 'test',
      });

      const state1 = usePromptStore.getState();
      const promptId = state1.userPrompts[0].id;
      expect(state1.userPrompts.length).toBe(1);

      deleteUserPrompt(promptId);

      const state2 = usePromptStore.getState();
      expect(state2.userPrompts.length).toBe(0);
    });
  });
});
