import { useFavoriteStore } from '../src/stores/favoriteStore';

// Reset store before each test
beforeEach(() => {
  useFavoriteStore.setState({ favoriteIds: [] });
});

describe('favoriteStore', () => {
  describe('initial state', () => {
    it('should start with empty favorites', () => {
      const { favoriteIds } = useFavoriteStore.getState();
      expect(favoriteIds).toEqual([]);
    });
  });

  describe('addFavorite', () => {
    it('should add prompt id to favorites', () => {
      const { addFavorite } = useFavoriteStore.getState();

      addFavorite('prompt-1');

      const state = useFavoriteStore.getState();
      expect(state.favoriteIds).toContain('prompt-1');
    });

    it('should not add duplicate favorites', () => {
      const { addFavorite } = useFavoriteStore.getState();

      addFavorite('prompt-1');
      addFavorite('prompt-1');

      const state = useFavoriteStore.getState();
      expect(state.favoriteIds.length).toBe(1);
    });
  });

  describe('removeFavorite', () => {
    it('should remove prompt id from favorites', () => {
      const { addFavorite, removeFavorite } = useFavoriteStore.getState();

      addFavorite('prompt-1');
      addFavorite('prompt-2');
      removeFavorite('prompt-1');

      const state = useFavoriteStore.getState();
      expect(state.favoriteIds).not.toContain('prompt-1');
      expect(state.favoriteIds).toContain('prompt-2');
    });

    it('should handle removing non-existent favorite', () => {
      const { removeFavorite } = useFavoriteStore.getState();

      // Should not throw
      expect(() => removeFavorite('nonexistent')).not.toThrow();
    });
  });

  describe('toggleFavorite', () => {
    it('should add favorite if not present', () => {
      const { toggleFavorite } = useFavoriteStore.getState();

      toggleFavorite('prompt-1');

      const state = useFavoriteStore.getState();
      expect(state.favoriteIds).toContain('prompt-1');
    });

    it('should remove favorite if already present', () => {
      const { addFavorite, toggleFavorite } = useFavoriteStore.getState();

      addFavorite('prompt-1');
      toggleFavorite('prompt-1');

      const state = useFavoriteStore.getState();
      expect(state.favoriteIds).not.toContain('prompt-1');
    });
  });

  describe('isFavorite', () => {
    it('should return true for favorited prompts', () => {
      const { addFavorite, isFavorite } = useFavoriteStore.getState();

      addFavorite('prompt-1');

      expect(isFavorite('prompt-1')).toBe(true);
    });

    it('should return false for non-favorited prompts', () => {
      const { isFavorite } = useFavoriteStore.getState();

      expect(isFavorite('prompt-1')).toBe(false);
    });
  });

  describe('clearAllFavorites', () => {
    it('should remove all favorites', () => {
      const { addFavorite, clearAllFavorites } = useFavoriteStore.getState();

      addFavorite('prompt-1');
      addFavorite('prompt-2');
      addFavorite('prompt-3');

      clearAllFavorites();

      const state = useFavoriteStore.getState();
      expect(state.favoriteIds).toEqual([]);
    });
  });
});
