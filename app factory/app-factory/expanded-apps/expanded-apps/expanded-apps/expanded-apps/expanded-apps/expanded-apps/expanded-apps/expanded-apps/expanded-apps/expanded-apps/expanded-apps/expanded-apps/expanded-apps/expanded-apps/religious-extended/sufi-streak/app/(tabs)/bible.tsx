import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Modal,
  ActivityIndicator,
  Alert,
  Animated,
  KeyboardAvoidingView,
  Platform,
  Dimensions,
  PanResponder,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import {
  BIBLE_BOOKS,
  ALL_BOOKS,
  getChapter,
  searchBible,
  BibleVerse,
} from '../../src/lib/bible';
import {
  askBibleQuestion,
  explainVerse,
  getAISettings,
  AISettings,
  GEMINI_SETUP_INSTRUCTIONS,
  saveUserAPIKey,
} from '../../src/lib/ai-helper';
import {
  saveNote,
  getNoteForVerse,
  VerseNote,
  HIGHLIGHT_COLORS,
} from '../../src/lib/notes';
import { checkIsAdFree } from '../../src/components/AdBanner';
import { useRouter } from 'expo-router';

const { width: SCREEN_WIDTH } = Dimensions.get('window');
const SWIPE_THRESHOLD = 50;

type ViewMode = 'books' | 'chapters' | 'reading' | 'search';

export default function BibleScreen() {
  const router = useRouter();
  const [viewMode, setViewMode] = useState<ViewMode>('books');
  const [selectedBook, setSelectedBook] = useState<typeof ALL_BOOKS[0] | null>(null);
  const [selectedChapter, setSelectedChapter] = useState<number>(1);
  const [verses, setVerses] = useState<BibleVerse[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<BibleVerse[]>([]);
  const [isPremium, setIsPremium] = useState(false);
  
  // AI Helper
  const [showAIModal, setShowAIModal] = useState(false);
  const [selectedVerse, setSelectedVerse] = useState<BibleVerse | null>(null);
  const [aiResponse, setAIResponse] = useState<string>('');
  const [aiLoading, setAILoading] = useState(false);
  const [aiQuestion, setAIQuestion] = useState('');
  const [aiSettings, setAISettings] = useState<AISettings | null>(null);
  
  // Notes
  const [showNoteModal, setShowNoteModal] = useState(false);
  const [noteText, setNoteText] = useState('');
  const [existingNote, setExistingNote] = useState<VerseNote | null>(null);
  
  // API Key setup
  const [showAPIKeyModal, setShowAPIKeyModal] = useState(false);
  const [apiKeyInput, setApiKeyInput] = useState('');
  
  // Animation for page transitions
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(0)).current;
  const scrollViewRef = useRef<ScrollView>(null);

  // Swipe gesture for chapter navigation
  const panResponder = useRef(
    PanResponder.create({
      onMoveShouldSetPanResponder: (_, gestureState) => {
        return Math.abs(gestureState.dx) > 20 && Math.abs(gestureState.dy) < 50;
      },
      onPanResponderRelease: (_, gestureState) => {
        if (gestureState.dx > SWIPE_THRESHOLD && selectedBook) {
          // Swipe right - previous chapter
          goToPrevChapter();
        } else if (gestureState.dx < -SWIPE_THRESHOLD && selectedBook) {
          // Swipe left - next chapter
          goToNextChapter();
        }
      },
    })
  ).current;

  useEffect(() => {
    loadSettings();
    Animated.timing(fadeAnim, { toValue: 1, duration: 300, useNativeDriver: true }).start();
  }, []);

  const loadSettings = async () => {
    const settings = await getAISettings();
    setAISettings(settings);
    const premium = await checkIsAdFree();
    setIsPremium(premium);
  };

  // Chapter navigation
  const goToPrevChapter = async () => {
    if (!selectedBook || isLoading) return;
    if (selectedChapter > 1) {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
      animatePageTurn('right');
      await loadChapter(selectedChapter - 1);
    }
  };

  const goToNextChapter = async () => {
    if (!selectedBook || isLoading) return;
    if (selectedChapter < selectedBook.chapters) {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
      animatePageTurn('left');
      await loadChapter(selectedChapter + 1);
    }
  };

  const animatePageTurn = (direction: 'left' | 'right') => {
    const toValue = direction === 'left' ? -SCREEN_WIDTH : SCREEN_WIDTH;
    Animated.sequence([
      Animated.timing(slideAnim, { toValue, duration: 150, useNativeDriver: true }),
      Animated.timing(slideAnim, { toValue: 0, duration: 0, useNativeDriver: true }),
    ]).start();
  };

  const loadChapter = async (chapter: number) => {
    setIsLoading(true);
    setSelectedChapter(chapter);
    scrollViewRef.current?.scrollTo({ y: 0, animated: false });
    
    if (selectedBook) {
      const data = await getChapter(selectedBook.name, chapter);
      if (data?.verses) {
        setVerses(data.verses);
      }
    }
    setIsLoading(false);
  };

  const handleBookSelect = (book: typeof ALL_BOOKS[0]) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    setSelectedBook(book);
    setViewMode('chapters');
  };

  const handleChapterSelect = async (chapter: number) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    setViewMode('reading');
    await loadChapter(chapter);
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    setIsLoading(true);
    setViewMode('search');
    
    const results = await searchBible(searchQuery);
    setSearchResults(results);
    setIsLoading(false);
  };

  const handleVersePress = (verse: BibleVerse) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    setSelectedVerse(verse);
    
    Alert.alert(
      `${verse.book_name} ${verse.chapter}:${verse.verse}`,
      verse.text,
      [
        { text: 'Cancel', style: 'cancel' },
        { text: '📝 Add Note', onPress: () => openNoteModal(verse) },
        { text: '🤖 Ask AI', onPress: () => openAIModal(verse) },
      ]
    );
  };

  const openAIModal = async (verse: BibleVerse) => {
    // AI is premium-only feature
    if (!isPremium) {
      Alert.alert(
        '✨ Premium Feature',
        'AI Bible Helper is available for premium members. Upgrade to unlock unlimited AI-powered Bible study!',
        [
          { text: 'Maybe Later', style: 'cancel' },
          { text: 'Upgrade Now', onPress: () => router.push('/paywall') },
        ]
      );
      return;
    }
    
    setSelectedVerse(verse);
    setAIResponse('');
    setAIQuestion('');
    
    // Check if AI is configured
    const settings = await getAISettings();
    if (settings.provider === 'none') {
      setShowAPIKeyModal(true);
      return;
    }
    
    setShowAIModal(true);
  };

  const handleAskAI = async () => {
    if (!selectedVerse || !aiQuestion.trim()) return;
    
    setAILoading(true);
    const reference = `${selectedVerse.book_name} ${selectedVerse.chapter}:${selectedVerse.verse}`;
    
    const result = await askBibleQuestion(aiQuestion, {
      verse: selectedVerse.text,
      reference,
    });
    
    if (result.success) {
      setAIResponse(result.response || '');
    } else {
      Alert.alert('Error', result.error || 'Failed to get AI response');
    }
    setAILoading(false);
  };

  const handleQuickExplain = async () => {
    if (!selectedVerse) return;
    
    setAILoading(true);
    const reference = `${selectedVerse.book_name} ${selectedVerse.chapter}:${selectedVerse.verse}`;
    
    const result = await explainVerse(selectedVerse.text, reference);
    
    if (result.success) {
      setAIResponse(result.response || '');
    } else {
      Alert.alert('Error', result.error || 'Failed to get explanation');
    }
    setAILoading(false);
  };

  const openNoteModal = async (verse: BibleVerse) => {
    setSelectedVerse(verse);
    const reference = `${verse.book_name} ${verse.chapter}:${verse.verse}`;
    const existing = await getNoteForVerse(reference);
    setExistingNote(existing);
    setNoteText(existing?.note || '');
    setShowNoteModal(true);
  };

  const handleSaveNote = async () => {
    if (!selectedVerse || !noteText.trim()) return;
    
    const reference = `${selectedVerse.book_name} ${selectedVerse.chapter}:${selectedVerse.verse}`;
    await saveNote(reference, selectedVerse.text, noteText);
    
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    setShowNoteModal(false);
    Alert.alert('Saved!', 'Your note has been saved.');
  };

  const handleSaveAPIKey = async () => {
    if (!apiKeyInput.trim()) return;
    
    const success = await saveUserAPIKey(apiKeyInput);
    if (success) {
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      setShowAPIKeyModal(false);
      loadAISettings();
      Alert.alert('Success!', 'Your API key has been saved. You can now use the AI helper!');
    } else {
      Alert.alert('Error', 'Failed to save API key');
    }
  };

  const goBack = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    if (viewMode === 'reading') {
      setViewMode('chapters');
    } else if (viewMode === 'chapters' || viewMode === 'search') {
      setViewMode('books');
      setSelectedBook(null);
    }
  };

  // Render premium book selection
  const renderBooks = () => (
    <View style={styles.booksContainer}>
      {/* Header */}
      <View style={styles.booksHeader}>
        <Text style={styles.booksTitle}>Holy Bible</Text>
        <Text style={styles.booksSubtitle}>King James Version</Text>
        <View style={styles.booksStats}>
          <Text style={styles.booksStatsText}>66 Books • 1,189 Chapters • 31,102 Verses</Text>
        </View>
      </View>

      <ScrollView
        contentContainerStyle={styles.booksScrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Old Testament */}
        <View style={styles.testamentSection}>
          <View style={styles.testamentHeader}>
            <Ionicons name="book-outline" size={20} color="#e94560" />
            <Text style={styles.testamentTitle}>Old Testament</Text>
            <Text style={styles.testamentCount}>39 Books</Text>
          </View>
          <View style={styles.bookGrid}>
            {BIBLE_BOOKS.oldTestament.map((book, index) => (
              <TouchableOpacity
                key={book.id}
                style={[styles.bookCard, { backgroundColor: getBookColor(index) }]}
                onPress={() => handleBookSelect(book)}
                activeOpacity={0.8}
              >
                <View style={styles.bookCardContent}>
                  <Text style={styles.bookName}>{book.name}</Text>
                  <View style={styles.bookMeta}>
                    <Text style={styles.bookChapters}>{book.chapters} chapters</Text>
                    <Ionicons name="chevron-forward" size={14} color="#ffffff60" />
                  </View>
                </View>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* New Testament */}
        <View style={styles.testamentSection}>
          <View style={styles.testamentHeader}>
            <Ionicons name="heart" size={20} color="#4ade80" />
            <Text style={styles.testamentTitle}>New Testament</Text>
            <Text style={styles.testamentCount}>27 Books</Text>
          </View>
          <View style={styles.bookGrid}>
            {BIBLE_BOOKS.newTestament.map((book, index) => (
              <TouchableOpacity
                key={book.id}
                style={[styles.bookCard, { backgroundColor: getBookColor(index + 39) }]}
                onPress={() => handleBookSelect(book)}
                activeOpacity={0.8}
              >
                <View style={styles.bookCardContent}>
                  <Text style={styles.bookName}>{book.name}</Text>
                  <View style={styles.bookMeta}>
                    <Text style={styles.bookChapters}>{book.chapters} chapters</Text>
                    <Ionicons name="chevron-forward" size={14} color="#ffffff60" />
                  </View>
                </View>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Premium Feature Note */}
        <View style={styles.premiumNote}>
          <Ionicons name="diamond" size={16} color="#e94560" />
          <Text style={styles.premiumNoteText}>
            Premium Bible experience with AI study helper and advanced features
          </Text>
        </View>
      </ScrollView>
    </View>
  );

  // Generate book card colors
  const getBookColor = (index: number) => {
    const colors = [
      '#e9456020', '#4ade8020', '#60a5fa20', '#fbbf2420',
      '#f472b620', '#8b5cf620', '#06b6d420', '#ec489920'
    ];
    return colors[index % colors.length];
  };

  // Render premium chapter selection
  const renderChapters = () => (
    <View style={styles.chaptersContainer}>
      {/* Header */}
      <View style={styles.chaptersHeader}>
        <TouchableOpacity
          style={styles.chaptersBackButton}
          onPress={() => setViewMode('books')}
          activeOpacity={0.7}
        >
          <Ionicons name="arrow-back" size={20} color="#ffffff" />
        </TouchableOpacity>
        <View style={styles.chaptersHeaderContent}>
          <Text style={styles.chaptersBookTitle}>{selectedBook?.name}</Text>
          <Text style={styles.chaptersBookMeta}>
            {selectedBook?.chapters} chapters • {getTestamentName()}
          </Text>
        </View>
      </View>

      {/* Chapter Grid */}
      <ScrollView
        contentContainerStyle={styles.chaptersScrollContent}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.chaptersGrid}>
          {Array.from({ length: selectedBook?.chapters || 0 }, (_, i) => i + 1).map((chapter) => (
            <TouchableOpacity
              key={chapter}
              style={[
                styles.chapterCard,
                chapter === selectedChapter && styles.chapterCardSelected,
              ]}
              onPress={() => handleChapterSelect(chapter)}
              activeOpacity={0.8}
            >
              <Text
                style={[
                  styles.chapterNumber,
                  chapter === selectedChapter && styles.chapterNumberSelected,
                ]}
              >
                {chapter}
              </Text>
              {chapter === selectedChapter && (
                <View style={styles.chapterSelectedIndicator}>
                  <Ionicons name="checkmark" size={12} color="#ffffff" />
                </View>
              )}
            </TouchableOpacity>
          ))}
        </View>

        {/* Quick Actions */}
        <View style={styles.chaptersActions}>
          <TouchableOpacity
            style={styles.chaptersActionButton}
            onPress={() => {
              if (selectedBook) {
                Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
                handleChapterSelect(1);
              }
            }}
            activeOpacity={0.7}
          >
            <Ionicons name="play-skip-back" size={18} color="#e94560" />
            <Text style={styles.chaptersActionText}>Start from Beginning</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.chaptersActionButton}
            onPress={() => {
              if (selectedBook) {
                Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
                handleChapterSelect(Math.floor((selectedBook.chapters || 1) / 2));
              }
            }}
            activeOpacity={0.7}
          >
            <Ionicons name="locate" size={18} color="#4ade80" />
            <Text style={styles.chaptersActionText}>Jump to Middle</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.chaptersActionButton}
            onPress={() => {
              if (selectedBook) {
                Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
                handleChapterSelect(selectedBook.chapters);
              }
            }}
            activeOpacity={0.7}
          >
            <Ionicons name="play-skip-forward" size={18} color="#60a5fa" />
            <Text style={styles.chaptersActionText}>Go to End</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </View>
  );

  // Get testament name
  const getTestamentName = () => {
    if (!selectedBook) return '';
    return BIBLE_BOOKS.oldTestament.find(b => b.id === selectedBook.id)
      ? 'Old Testament'
      : 'New Testament';
  };

  // Render reading view with premium page-turn animations
  const renderReading = () => (
    <View style={{ flex: 1 }}>
      {/* Premium Chapter Navigation */}
      <View style={styles.premiumNav}>
        {/* Book Selector */}
        <TouchableOpacity
          style={styles.bookSelector}
          onPress={() => setViewMode('chapters')}
          activeOpacity={0.7}
        >
          <Ionicons name="book" size={16} color="#e94560" />
          <Text style={styles.bookSelectorText} numberOfLines={1}>
            {selectedBook?.name}
          </Text>
          <Ionicons name="chevron-down" size={14} color="#ffffff60" />
        </TouchableOpacity>

        {/* Chapter Navigation */}
        <View style={styles.chapterControls}>
          <TouchableOpacity
            style={[styles.chapterControl, selectedChapter <= 1 && styles.chapterControlDisabled]}
            onPress={goToPrevChapter}
            disabled={selectedChapter <= 1 || isLoading}
            activeOpacity={0.7}
          >
            <Ionicons
              name="chevron-back"
              size={20}
              color={selectedChapter <= 1 ? '#ffffff30' : '#e94560'}
            />
          </TouchableOpacity>

          <View style={styles.chapterDisplay}>
            <Text style={styles.chapterDisplayText}>
              {selectedChapter}
            </Text>
            <Text style={styles.chapterTotalText}>
              of {selectedBook?.chapters}
            </Text>
          </View>

          <TouchableOpacity
            style={[styles.chapterControl, selectedChapter >= (selectedBook?.chapters || 1) && styles.chapterControlDisabled]}
            onPress={goToNextChapter}
            disabled={selectedChapter >= (selectedBook?.chapters || 1) || isLoading}
            activeOpacity={0.7}
          >
            <Ionicons
              name="chevron-forward"
              size={20}
              color={selectedChapter >= (selectedBook?.chapters || 1) ? '#ffffff30' : '#e94560'}
            />
          </TouchableOpacity>
        </View>
      </View>

      {/* Page-Turn Animation Container */}
      <View style={styles.pageContainer} {...panResponder.panHandlers}>
        <Animated.View
          style={[
            styles.pageContent,
            {
              transform: [{ translateX: slideAnim }],
              opacity: slideAnim.interpolate({
                inputRange: [-SCREEN_WIDTH, 0, SCREEN_WIDTH],
                outputRange: [0.7, 1, 0.7],
              }),
            },
          ]}
        >
          {isLoading ? (
            <View style={styles.loadingContainer}>
              <ActivityIndicator size="large" color="#e94560" />
              <Text style={styles.loadingText}>Loading chapter...</Text>
            </View>
          ) : (
            <ScrollView
              ref={scrollViewRef}
              contentContainerStyle={styles.versesContainer}
              showsVerticalScrollIndicator={false}
              bounces={false}
            >
              {/* Chapter Header */}
              <View style={styles.chapterHeader}>
                <Text style={styles.chapterTitle}>
                  {selectedBook?.name} Chapter {selectedChapter}
                </Text>
                <View style={styles.chapterStats}>
                  <Text style={styles.chapterStatsText}>
                    {verses.length} verses
                  </Text>
                </View>
              </View>

              {/* Verses */}
              {verses.map((verse, index) => (
                <TouchableOpacity
                  key={`${verse.chapter}-${verse.verse}`}
                  style={[
                    styles.verseItem,
                    index === verses.length - 1 && styles.lastVerse,
                  ]}
                  onPress={() => handleVersePress(verse)}
                  activeOpacity={0.6}
                  delayPressIn={0}
                >
                  <View style={styles.verseNumberContainer}>
                    <Text style={styles.verseNumber}>{verse.verse}</Text>
                  </View>
                  <Text style={styles.verseContent}>{verse.text}</Text>
                </TouchableOpacity>
              ))}

              {/* Page Footer */}
              <View style={styles.pageFooter}>
                <Text style={styles.pageFooterText}>
                  {selectedBook?.name} {selectedChapter}
                </Text>
                <View style={styles.pageNumber}>
                  <Text style={styles.pageNumberText}>
                    {selectedChapter}/{selectedBook?.chapters}
                  </Text>
                </View>
              </View>
            </ScrollView>
          )}
        </Animated.View>

        {/* Page Turn Effects */}
        {slideAnim.interpolate({
          inputRange: [-SCREEN_WIDTH, 0, SCREEN_WIDTH],
          outputRange: [-1, 0, 1],
        }).__getValue() !== 0 && (
          <View style={styles.pageShadow} />
        )}
      </View>

      {/* Bottom Navigation Bar */}
      <View style={styles.bottomBar}>
        <TouchableOpacity
          style={[styles.bottomBarButton, selectedChapter <= 1 && styles.bottomBarButtonDisabled]}
          onPress={goToPrevChapter}
          disabled={selectedChapter <= 1 || isLoading}
          activeOpacity={0.7}
        >
          <Ionicons
            name="arrow-back"
            size={20}
            color={selectedChapter <= 1 ? '#ffffff30' : '#e94560'}
          />
          <Text style={[styles.bottomBarButtonText, selectedChapter <= 1 && styles.bottomBarButtonTextDisabled]}>
            Previous
          </Text>
        </TouchableOpacity>

        <View style={styles.bottomBarCenter}>
          <Text style={styles.bottomBarTitle}>
            {selectedBook?.name} {selectedChapter}
          </Text>
          <Text style={styles.bottomBarSubtitle}>
            {verses.length} verses
          </Text>
        </View>

        <TouchableOpacity
          style={[styles.bottomBarButton, selectedChapter >= (selectedBook?.chapters || 1) && styles.bottomBarButtonDisabled]}
          onPress={goToNextChapter}
          disabled={selectedChapter >= (selectedBook?.chapters || 1) || isLoading}
          activeOpacity={0.7}
        >
          <Text style={[styles.bottomBarButtonText, selectedChapter >= (selectedBook?.chapters || 1) && styles.bottomBarButtonTextDisabled]}>
            Next
          </Text>
          <Ionicons
            name="arrow-forward"
            size={20}
            color={selectedChapter >= (selectedBook?.chapters || 1) ? '#ffffff30' : '#e94560'}
          />
        </TouchableOpacity>
      </View>

      {/* Premium Features Hint */}
      <View style={styles.premiumHint}>
        <Ionicons name="diamond" size={12} color="#e94560" />
        <Text style={styles.premiumHintText}>Premium Reading Experience</Text>
      </View>
    </View>
  );

  // Render search results
  const renderSearchResults = () => (
    <ScrollView contentContainerStyle={styles.searchResults}>
      {isLoading ? (
        <ActivityIndicator size="large" color="#e94560" style={{ marginTop: 50 }} />
      ) : searchResults.length === 0 ? (
        <Text style={styles.noResults}>No results found. Try different keywords.</Text>
      ) : (
        searchResults.map((verse, index) => (
          <TouchableOpacity
            key={index}
            style={styles.searchResultCard}
            onPress={() => handleVersePress(verse)}
            activeOpacity={0.7}
          >
            <Text style={styles.searchResultRef}>
              {verse.book_name} {verse.chapter}:{verse.verse}
            </Text>
            <Text style={styles.searchResultText}>{verse.text}</Text>
          </TouchableOpacity>
        ))
      )}
    </ScrollView>
  );

  return (
    <LinearGradient
      colors={['#1a1a2e', '#0f0f23', '#1a1a2e']}
      style={styles.container}
    >
      <Animated.View style={[styles.content, { opacity: fadeAnim }]}>
        {/* Header */}
        <View style={styles.header}>
          {viewMode !== 'books' && (
            <TouchableOpacity style={styles.backButton} onPress={goBack}>
              <Ionicons name="chevron-back" size={24} color="#ffffff" />
            </TouchableOpacity>
          )}
          <Text style={styles.title}>
            {viewMode === 'books' && 'Bible'}
            {viewMode === 'chapters' && selectedBook?.name}
            {viewMode === 'reading' && `${selectedBook?.name} ${selectedChapter}`}
            {viewMode === 'search' && 'Search Results'}
          </Text>
          <TouchableOpacity 
            style={styles.aiButton}
            onPress={() => aiSettings?.provider !== 'none' ? null : setShowAPIKeyModal(true)}
          >
            <Ionicons 
              name="sparkles" 
              size={22} 
              color={aiSettings?.provider !== 'none' ? '#4ade80' : '#ffffff50'} 
            />
          </TouchableOpacity>
        </View>

        {/* Search Bar */}
        {viewMode === 'books' && (
          <View style={styles.searchContainer}>
            <Ionicons name="search" size={20} color="#ffffff50" />
            <TextInput
              style={styles.searchInput}
              placeholder="Search verses..."
              placeholderTextColor="#ffffff40"
              value={searchQuery}
              onChangeText={setSearchQuery}
              onSubmitEditing={handleSearch}
              returnKeyType="search"
            />
            {searchQuery.length > 0 && (
              <TouchableOpacity onPress={() => setSearchQuery('')}>
                <Ionicons name="close-circle" size={20} color="#ffffff50" />
              </TouchableOpacity>
            )}
          </View>
        )}

        {/* Content */}
        {viewMode === 'books' && renderBooks()}
        {viewMode === 'chapters' && renderChapters()}
        {viewMode === 'reading' && renderReading()}
        {viewMode === 'search' && renderSearchResults()}

        {/* AI Helper Modal */}
        <Modal visible={showAIModal} animationType="slide" transparent>
          <KeyboardAvoidingView 
            behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            style={styles.modalOverlay}
          >
            <View style={styles.modalContent}>
              <View style={styles.modalHeader}>
                <Text style={styles.modalTitle}>🤖 AI Bible Helper</Text>
                <TouchableOpacity onPress={() => setShowAIModal(false)}>
                  <Ionicons name="close" size={24} color="#ffffff" />
                </TouchableOpacity>
              </View>
              
              {selectedVerse && (
                <View style={styles.selectedVerseBox}>
                  <Text style={styles.selectedVerseRef}>
                    {selectedVerse.book_name} {selectedVerse.chapter}:{selectedVerse.verse}
                  </Text>
                  <Text style={styles.selectedVerseText} numberOfLines={3}>
                    "{selectedVerse.text}"
                  </Text>
                </View>
              )}

              <TouchableOpacity 
                style={styles.quickButton}
                onPress={handleQuickExplain}
                disabled={aiLoading}
              >
                <Text style={styles.quickButtonText}>✨ Quick Explanation</Text>
              </TouchableOpacity>

              <TextInput
                style={styles.aiInput}
                placeholder="Ask a question about this verse..."
                placeholderTextColor="#ffffff40"
                value={aiQuestion}
                onChangeText={setAIQuestion}
                multiline
              />

              <TouchableOpacity 
                style={[styles.askButton, (!aiQuestion.trim() || aiLoading) && styles.askButtonDisabled]}
                onPress={handleAskAI}
                disabled={!aiQuestion.trim() || aiLoading}
              >
                {aiLoading ? (
                  <ActivityIndicator color="#ffffff" size="small" />
                ) : (
                  <Text style={styles.askButtonText}>Ask AI</Text>
                )}
              </TouchableOpacity>

              {aiResponse && (
                <ScrollView style={styles.aiResponseBox}>
                  <Text style={styles.aiResponseText}>{aiResponse}</Text>
                </ScrollView>
              )}
            </View>
          </KeyboardAvoidingView>
        </Modal>

        {/* Note Modal */}
        <Modal visible={showNoteModal} animationType="slide" transparent>
          <KeyboardAvoidingView 
            behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            style={styles.modalOverlay}
          >
            <View style={styles.modalContent}>
              <View style={styles.modalHeader}>
                <Text style={styles.modalTitle}>📝 Verse Note</Text>
                <TouchableOpacity onPress={() => setShowNoteModal(false)}>
                  <Ionicons name="close" size={24} color="#ffffff" />
                </TouchableOpacity>
              </View>
              
              {selectedVerse && (
                <View style={styles.selectedVerseBox}>
                  <Text style={styles.selectedVerseRef}>
                    {selectedVerse.book_name} {selectedVerse.chapter}:{selectedVerse.verse}
                  </Text>
                  <Text style={styles.selectedVerseText} numberOfLines={2}>
                    "{selectedVerse.text}"
                  </Text>
                </View>
              )}

              <TextInput
                style={styles.noteInput}
                placeholder="Write your thoughts, reflections, or prayers..."
                placeholderTextColor="#ffffff40"
                value={noteText}
                onChangeText={setNoteText}
                multiline
                textAlignVertical="top"
              />

              <TouchableOpacity 
                style={[styles.saveNoteButton, !noteText.trim() && styles.saveNoteButtonDisabled]}
                onPress={handleSaveNote}
                disabled={!noteText.trim()}
              >
                <Ionicons name="checkmark" size={20} color="#ffffff" />
                <Text style={styles.saveNoteText}>Save Note</Text>
              </TouchableOpacity>
            </View>
          </KeyboardAvoidingView>
        </Modal>

        {/* API Key Setup Modal */}
        <Modal visible={showAPIKeyModal} animationType="slide" transparent>
          <KeyboardAvoidingView 
            behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            style={styles.modalOverlay}
          >
            <View style={styles.modalContent}>
              <View style={styles.modalHeader}>
                <Text style={styles.modalTitle}>🔑 Set Up AI Helper</Text>
                <TouchableOpacity onPress={() => setShowAPIKeyModal(false)}>
                  <Ionicons name="close" size={24} color="#ffffff" />
                </TouchableOpacity>
              </View>

              <ScrollView style={styles.setupInstructions}>
                <Text style={styles.setupText}>
                  To use the AI Bible helper, you need a free Google Gemini API key:
                </Text>
                <Text style={styles.setupStep}>1. Go to makersuite.google.com/app/apikey</Text>
                <Text style={styles.setupStep}>2. Sign in with your Google account</Text>
                <Text style={styles.setupStep}>3. Click "Create API Key"</Text>
                <Text style={styles.setupStep}>4. Copy and paste it below</Text>
                <Text style={styles.setupNote}>
                  💡 It's free! 60 requests per minute included.
                </Text>
              </ScrollView>

              <TextInput
                style={styles.apiKeyInput}
                placeholder="Paste your Gemini API key here..."
                placeholderTextColor="#ffffff40"
                value={apiKeyInput}
                onChangeText={setApiKeyInput}
                autoCapitalize="none"
                autoCorrect={false}
              />

              <TouchableOpacity 
                style={[styles.saveKeyButton, !apiKeyInput.trim() && styles.saveKeyButtonDisabled]}
                onPress={handleSaveAPIKey}
                disabled={!apiKeyInput.trim()}
              >
                <Text style={styles.saveKeyText}>Save API Key</Text>
              </TouchableOpacity>

              <Text style={styles.privacyNote}>
                🔒 Your key is stored locally and never shared.
              </Text>
            </View>
          </KeyboardAvoidingView>
        </Modal>
      </Animated.View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    flex: 1,
    paddingTop: 60,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    marginBottom: 16,
  },
  backButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#ffffff10',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  title: {
    flex: 1,
    fontSize: 28,
    fontWeight: '800',
    color: '#ffffff',
  },
  aiButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#ffffff10',
    justifyContent: 'center',
    alignItems: 'center',
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ffffff10',
    marginHorizontal: 20,
    marginBottom: 20,
    paddingHorizontal: 16,
    borderRadius: 14,
    height: 50,
  },
  searchInput: {
    flex: 1,
    color: '#ffffff',
    fontSize: 16,
    marginLeft: 12,
  },
  booksContainer: {
    flex: 1,
  },
  booksHeader: {
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 40,
    paddingBottom: 24,
  },
  booksTitle: {
    color: '#ffffff',
    fontSize: 28,
    fontWeight: '800',
    marginBottom: 4,
  },
  booksSubtitle: {
    color: '#ffffff60',
    fontSize: 16,
    marginBottom: 12,
  },
  booksStats: {
    backgroundColor: '#ffffff08',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  booksStatsText: {
    color: '#ffffff80',
    fontSize: 12,
    fontWeight: '500',
  },
  booksScrollContent: {
    paddingHorizontal: 20,
    paddingBottom: 120,
  },
  testamentSection: {
    marginBottom: 32,
  },
  testamentHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
    gap: 8,
  },
  testamentTitle: {
    color: '#ffffff',
    fontSize: 18,
    fontWeight: '700',
    flex: 1,
  },
  testamentCount: {
    color: '#ffffff60',
    fontSize: 12,
    fontWeight: '600',
    backgroundColor: '#ffffff10',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  bookGrid: {
    gap: 12,
  },
  bookCard: {
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: '#ffffff08',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  bookCardContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  bookName: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '700',
    flex: 1,
  },
  bookMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  bookChapters: {
    color: '#ffffff60',
    fontSize: 12,
    fontWeight: '500',
  },
  premiumNote: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: '#e9456020',
    padding: 16,
    borderRadius: 16,
    marginTop: 20,
    borderWidth: 1,
    borderColor: '#e9456030',
  },
  premiumNoteText: {
    color: '#e94560',
    fontSize: 14,
    fontWeight: '600',
    flex: 1,
  },
  chaptersContainer: {
    flex: 1,
  },
  chaptersHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 50,
    paddingBottom: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#ffffff08',
  },
  chaptersBackButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#ffffff10',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  chaptersHeaderContent: {
    flex: 1,
  },
  chaptersBookTitle: {
    color: '#ffffff',
    fontSize: 24,
    fontWeight: '800',
    marginBottom: 2,
  },
  chaptersBookMeta: {
    color: '#ffffff60',
    fontSize: 14,
    fontWeight: '500',
  },
  chaptersScrollContent: {
    paddingHorizontal: 20,
    paddingTop: 20,
    paddingBottom: 120,
  },
  chaptersGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
    marginBottom: 32,
  },
  chapterCard: {
    width: 70,
    height: 70,
    backgroundColor: '#ffffff08',
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#ffffff08',
    position: 'relative',
  },
  chapterCardSelected: {
    backgroundColor: '#e9456020',
    borderColor: '#e94560',
  },
  chapterNumber: {
    color: '#ffffff',
    fontSize: 22,
    fontWeight: '700',
  },
  chapterNumberSelected: {
    color: '#e94560',
  },
  chapterSelectedIndicator: {
    position: 'absolute',
    top: 4,
    right: 4,
    width: 20,
    height: 20,
    borderRadius: 10,
    backgroundColor: '#e94560',
    justifyContent: 'center',
    alignItems: 'center',
  },
  chaptersActions: {
    gap: 12,
  },
  chaptersActionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ffffff08',
    paddingVertical: 14,
    paddingHorizontal: 16,
    borderRadius: 14,
    gap: 10,
  },
  chaptersActionText: {
    color: '#ffffff',
    fontSize: 15,
    fontWeight: '600',
    flex: 1,
  },
  premiumNav: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 16,
    backgroundColor: '#ffffff03',
    borderBottomWidth: 1,
    borderBottomColor: '#ffffff06',
  },
  bookSelector: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ffffff08',
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 20,
    gap: 6,
    flex: 1,
    marginRight: 16,
  },
  bookSelectorText: {
    color: '#ffffff',
    fontSize: 15,
    fontWeight: '600',
    flex: 1,
  },
  chapterControls: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  chapterControl: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#ffffff08',
    justifyContent: 'center',
    alignItems: 'center',
  },
  chapterControlDisabled: {
    backgroundColor: '#ffffff05',
  },
  chapterDisplay: {
    alignItems: 'center',
    minWidth: 60,
  },
  chapterDisplayText: {
    color: '#e94560',
    fontSize: 18,
    fontWeight: '800',
  },
  chapterTotalText: {
    color: '#ffffff60',
    fontSize: 10,
    fontWeight: '600',
    marginTop: 2,
  },
  pageContainer: {
    flex: 1,
    backgroundColor: '#ffffff02',
  },
  pageContent: {
    flex: 1,
    backgroundColor: '#1a1a2e',
    borderRadius: 12,
    margin: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 6,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    color: '#ffffff60',
    fontSize: 14,
    marginTop: 12,
  },
  versesContainer: {
    paddingHorizontal: 24,
    paddingTop: 20,
    paddingBottom: 80,
  },
  chapterHeader: {
    alignItems: 'center',
    marginBottom: 24,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#ffffff08',
  },
  chapterTitle: {
    color: '#ffffff',
    fontSize: 20,
    fontWeight: '700',
    marginBottom: 4,
  },
  chapterStats: {
    backgroundColor: '#e9456020',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
  },
  chapterStatsText: {
    color: '#e94560',
    fontSize: 12,
    fontWeight: '600',
  },
  verseItem: {
    flexDirection: 'row',
    marginBottom: 16,
    paddingVertical: 4,
    alignItems: 'flex-start',
  },
  lastVerse: {
    marginBottom: 24,
  },
  verseNumberContainer: {
    width: 32,
    height: 24,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  verseNumber: {
    color: '#e94560',
    fontSize: 13,
    fontWeight: '700',
    opacity: 0.8,
  },
  verseContent: {
    flex: 1,
    color: '#ffffff',
    fontSize: 17,
    lineHeight: 26,
    fontFamily: Platform.OS === 'ios' ? 'Georgia' : 'serif',
  },
  pageFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 24,
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: '#ffffff06',
  },
  pageFooterText: {
    color: '#ffffff60',
    fontSize: 14,
    fontWeight: '500',
  },
  pageNumber: {
    backgroundColor: '#e9456020',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
  },
  pageNumberText: {
    color: '#e94560',
    fontSize: 12,
    fontWeight: '700',
  },
  pageShadow: {
    position: 'absolute',
    top: 16,
    left: 16,
    right: 16,
    bottom: 16,
    backgroundColor: 'rgba(0,0,0,0.1)',
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 3,
  },
  bottomBar: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 16,
    backgroundColor: '#ffffff05',
    borderTopWidth: 1,
    borderTopColor: '#ffffff08',
  },
  bottomBarButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 16,
  },
  bottomBarButtonDisabled: {
    opacity: 0.4,
  },
  bottomBarButtonText: {
    color: '#e94560',
    fontSize: 14,
    fontWeight: '600',
  },
  bottomBarButtonTextDisabled: {
    color: '#ffffff30',
  },
  bottomBarCenter: {
    flex: 1,
    alignItems: 'center',
  },
  bottomBarTitle: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '700',
  },
  bottomBarSubtitle: {
    color: '#ffffff60',
    fontSize: 12,
    marginTop: 2,
  },
  premiumHint: {
    position: 'absolute',
    bottom: 8,
    right: 16,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: '#e9456020',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  premiumHintText: {
    color: '#e94560',
    fontSize: 11,
    fontWeight: '600',
  },
  searchResults: {
    paddingHorizontal: 20,
    paddingBottom: 120,
  },
  noResults: {
    color: '#ffffff60',
    fontSize: 16,
    textAlign: 'center',
    marginTop: 40,
  },
  searchResultCard: {
    backgroundColor: '#ffffff08',
    borderRadius: 14,
    padding: 16,
    marginBottom: 12,
  },
  searchResultRef: {
    color: '#e94560',
    fontSize: 14,
    fontWeight: '700',
    marginBottom: 8,
  },
  searchResultText: {
    color: '#ffffff',
    fontSize: 15,
    lineHeight: 22,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.8)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: '#1a1a2e',
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    padding: 24,
    maxHeight: '85%',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  modalTitle: {
    color: '#ffffff',
    fontSize: 20,
    fontWeight: '700',
  },
  selectedVerseBox: {
    backgroundColor: '#ffffff08',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  selectedVerseRef: {
    color: '#e94560',
    fontSize: 14,
    fontWeight: '700',
    marginBottom: 8,
  },
  selectedVerseText: {
    color: '#ffffff80',
    fontSize: 15,
    fontStyle: 'italic',
    lineHeight: 22,
  },
  quickButton: {
    backgroundColor: '#e9456020',
    borderRadius: 12,
    padding: 14,
    alignItems: 'center',
    marginBottom: 16,
  },
  quickButtonText: {
    color: '#e94560',
    fontSize: 16,
    fontWeight: '600',
  },
  aiInput: {
    backgroundColor: '#ffffff08',
    borderRadius: 12,
    padding: 16,
    color: '#ffffff',
    fontSize: 16,
    minHeight: 80,
    marginBottom: 16,
  },
  askButton: {
    backgroundColor: '#e94560',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
  },
  askButtonDisabled: {
    opacity: 0.5,
  },
  askButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '700',
  },
  aiResponseBox: {
    backgroundColor: '#4ade8015',
    borderRadius: 12,
    padding: 16,
    marginTop: 16,
    maxHeight: 200,
  },
  aiResponseText: {
    color: '#ffffff',
    fontSize: 15,
    lineHeight: 24,
  },
  noteInput: {
    backgroundColor: '#ffffff08',
    borderRadius: 12,
    padding: 16,
    color: '#ffffff',
    fontSize: 16,
    minHeight: 150,
    marginBottom: 16,
  },
  saveNoteButton: {
    backgroundColor: '#4ade80',
    borderRadius: 12,
    padding: 16,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 8,
  },
  saveNoteButtonDisabled: {
    opacity: 0.5,
  },
  saveNoteText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '700',
  },
  setupInstructions: {
    maxHeight: 200,
    marginBottom: 16,
  },
  setupText: {
    color: '#ffffff',
    fontSize: 15,
    lineHeight: 22,
    marginBottom: 16,
  },
  setupStep: {
    color: '#ffffff80',
    fontSize: 14,
    lineHeight: 24,
    marginLeft: 8,
  },
  setupNote: {
    color: '#4ade80',
    fontSize: 14,
    marginTop: 12,
  },
  apiKeyInput: {
    backgroundColor: '#ffffff08',
    borderRadius: 12,
    padding: 16,
    color: '#ffffff',
    fontSize: 14,
    marginBottom: 16,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  saveKeyButton: {
    backgroundColor: '#e94560',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    marginBottom: 12,
  },
  saveKeyButtonDisabled: {
    opacity: 0.5,
  },
  saveKeyText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '700',
  },
  privacyNote: {
    color: '#ffffff40',
    fontSize: 12,
    textAlign: 'center',
  },
});
