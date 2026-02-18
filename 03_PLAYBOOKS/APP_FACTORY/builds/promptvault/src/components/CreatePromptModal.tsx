import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  TextInput,
  Modal,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  Alert,
} from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { Category, CATEGORIES } from '../types';
import { colors, spacing, borderRadius, fontSize } from '../utils/theme';
import { usePromptStore } from '../stores/promptStore';
import { useSubscriptionStore } from '../stores/subscriptionStore';
import Paywall from './Paywall';

interface CreatePromptModalProps {
  visible: boolean;
  onClose: () => void;
}

export default function CreatePromptModal({
  visible,
  onClose,
}: CreatePromptModalProps) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [category, setCategory] = useState<Category>('writing');
  const [tags, setTags] = useState('');
  const [paywallVisible, setPaywallVisible] = useState(false);

  const { addUserPrompt } = usePromptStore();
  const { isPro } = useSubscriptionStore();

  // Check if user has premium access for creating custom prompts
  const checkPremiumAccess = () => {
    if (!isPro) {
      setPaywallVisible(true);
      return false;
    }
    return true;
  };

  const handleSave = () => {
    // Custom prompt creation requires premium
    if (!checkPremiumAccess()) {
      return;
    }

    if (!title.trim()) {
      Alert.alert('Missing Title', 'Please enter a title for your prompt.');
      return;
    }
    if (!content.trim()) {
      Alert.alert('Missing Content', 'Please enter the prompt content.');
      return;
    }

    const tagArray = tags
      .split(',')
      .map((t) => t.trim().toLowerCase())
      .filter((t) => t.length > 0);

    addUserPrompt({
      title: title.trim(),
      content: content.trim(),
      category,
      tags: tagArray,
      preview: content.trim().substring(0, 100) + '...',
      userId: 'local-user',
    });

    // Reset form
    setTitle('');
    setContent('');
    setCategory('writing');
    setTags('');

    Alert.alert('Saved', 'Your prompt has been saved.');
    onClose();
  };

  return (
    <Modal
      visible={visible}
      animationType="slide"
      presentationStyle="pageSheet"
      onRequestClose={onClose}
    >
      <Paywall
        visible={paywallVisible}
        onClose={() => setPaywallVisible(false)}
        feature="Custom Prompts"
      />

      <KeyboardAvoidingView
        style={styles.container}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        <View style={styles.header}>
          <TouchableOpacity onPress={onClose}>
            <Text style={styles.cancelText}>Cancel</Text>
          </TouchableOpacity>
          <View style={styles.headerTitleContainer}>
            <Text style={styles.headerTitle}>New Prompt</Text>
            {!isPro && (
              <View style={styles.premiumBadge}>
                <MaterialCommunityIcons name="star-circle" size={12} color={colors.primary} />
                <Text style={styles.premiumBadgeText}>Premium</Text>
              </View>
            )}
          </View>
          <TouchableOpacity onPress={handleSave}>
            <Text style={styles.saveText}>Save</Text>
          </TouchableOpacity>
        </View>

        <ScrollView
          contentContainerStyle={styles.content}
          keyboardShouldPersistTaps="handled"
        >
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Title</Text>
            <TextInput
              style={styles.input}
              value={title}
              onChangeText={setTitle}
              placeholder="e.g., Blog Post Writer"
              placeholderTextColor={colors.textMuted}
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Category</Text>
            <ScrollView
              horizontal
              showsHorizontalScrollIndicator={false}
              style={styles.categoryScroll}
            >
              {CATEGORIES.map((cat) => (
                <TouchableOpacity
                  key={cat.key}
                  style={[
                    styles.categoryChip,
                    category === cat.key && styles.categoryChipSelected,
                  ]}
                  onPress={() => setCategory(cat.key)}
                >
                  <Text
                    style={[
                      styles.categoryChipText,
                      category === cat.key && styles.categoryChipTextSelected,
                    ]}
                  >
                    {cat.label}
                  </Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Prompt Content</Text>
            <TextInput
              style={[styles.input, styles.contentInput]}
              value={content}
              onChangeText={setContent}
              placeholder="Enter your prompt here. Use [PLACEHOLDERS] for variables."
              placeholderTextColor={colors.textMuted}
              multiline
              textAlignVertical="top"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Tags (comma separated)</Text>
            <TextInput
              style={styles.input}
              value={tags}
              onChangeText={setTags}
              placeholder="e.g., blog, writing, content"
              placeholderTextColor={colors.textMuted}
              autoCapitalize="none"
            />
          </View>

          <View style={styles.tips}>
            <MaterialCommunityIcons
              name="lightbulb-outline"
              size={20}
              color={colors.warning}
            />
            <Text style={styles.tipsText}>
              Tip: Use [BRACKETS] for variables users should fill in. Example:
              "Write about [TOPIC] for [AUDIENCE]"
            </Text>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </Modal>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.surface,
  },
  headerTitleContainer: {
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: fontSize.lg,
    fontWeight: '600',
    color: colors.text,
  },
  premiumBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: colors.primary + '20',
    paddingHorizontal: spacing.sm,
    paddingVertical: 2,
    borderRadius: borderRadius.sm,
    marginTop: 4,
  },
  premiumBadgeText: {
    fontSize: fontSize.xs,
    fontWeight: '600',
    color: colors.primary,
  },
  cancelText: {
    fontSize: fontSize.md,
    color: colors.textSecondary,
  },
  saveText: {
    fontSize: fontSize.md,
    fontWeight: '600',
    color: colors.primary,
  },
  content: {
    padding: spacing.lg,
  },
  inputGroup: {
    marginBottom: spacing.lg,
  },
  label: {
    fontSize: fontSize.sm,
    fontWeight: '600',
    color: colors.textSecondary,
    marginBottom: spacing.sm,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  input: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.md,
    padding: spacing.md,
    fontSize: fontSize.md,
    color: colors.text,
  },
  contentInput: {
    minHeight: 200,
    paddingTop: spacing.md,
  },
  categoryScroll: {
    marginHorizontal: -spacing.lg,
    paddingHorizontal: spacing.lg,
  },
  categoryChip: {
    backgroundColor: colors.surface,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: borderRadius.full,
    marginRight: spacing.sm,
  },
  categoryChipSelected: {
    backgroundColor: colors.primary,
  },
  categoryChipText: {
    fontSize: fontSize.sm,
    color: colors.textSecondary,
  },
  categoryChipTextSelected: {
    color: colors.background,
    fontWeight: '600',
  },
  tips: {
    flexDirection: 'row',
    backgroundColor: colors.surface,
    padding: spacing.md,
    borderRadius: borderRadius.md,
    gap: spacing.sm,
    alignItems: 'flex-start',
  },
  tipsText: {
    flex: 1,
    fontSize: fontSize.sm,
    color: colors.textSecondary,
    lineHeight: 20,
  },
});
