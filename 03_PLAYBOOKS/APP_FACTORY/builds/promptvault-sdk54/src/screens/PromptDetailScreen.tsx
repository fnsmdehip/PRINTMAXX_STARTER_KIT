import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Share,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRoute, useNavigation, RouteProp } from '@react-navigation/native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import * as Clipboard from 'expo-clipboard';
import * as Haptics from 'expo-haptics';
import Toast from '../components/Toast';
import { usePromptStore } from '../stores/promptStore';
import { useFavoriteStore } from '../stores/favoriteStore';
import { colors, spacing, borderRadius, fontSize } from '../utils/theme';

type RootStackParamList = {
  PromptDetail: { promptId: string };
};

type PromptDetailRouteProp = RouteProp<RootStackParamList, 'PromptDetail'>;

export default function PromptDetailScreen() {
  const route = useRoute<PromptDetailRouteProp>();
  const navigation = useNavigation();
  const { promptId } = route.params;

  const { getPromptById } = usePromptStore();
  const { isFavorite, toggleFavorite } = useFavoriteStore();

  const prompt = getPromptById(promptId);
  const favorite = prompt ? isFavorite(prompt.id) : false;

  const [toastVisible, setToastVisible] = useState(false);
  const [toastMessage, setToastMessage] = useState('');

  if (!prompt) {
    return (
      <SafeAreaView style={styles.container}>
        <Text style={styles.errorText}>Prompt not found</Text>
      </SafeAreaView>
    );
  }

  const categoryColor =
    colors.categoryColors[prompt.category] || colors.primary;

  const handleCopy = async () => {
    await Clipboard.setStringAsync(prompt.content);
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    setToastMessage('Copied to clipboard');
    setToastVisible(true);
  };

  const handleFavorite = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    toggleFavorite(prompt.id);
    setToastMessage(favorite ? 'Removed from favorites' : 'Added to favorites');
    setToastVisible(true);
  };

  const handleShare = async () => {
    try {
      await Share.share({
        message: `Check out this prompt from PromptVault:\n\n${prompt.title}\n\n${prompt.content}`,
      });
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <SafeAreaView style={styles.container} edges={['bottom']}>
      <Toast
        visible={toastVisible}
        message={toastMessage}
        type="success"
        onHide={() => setToastVisible(false)}
      />

      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.goBack()}
        >
          <MaterialCommunityIcons
            name="arrow-left"
            size={24}
            color={colors.text}
          />
        </TouchableOpacity>

        <View style={styles.headerActions}>
          <TouchableOpacity style={styles.actionButton} onPress={handleShare}>
            <MaterialCommunityIcons
              name="share-variant"
              size={22}
              color={colors.text}
            />
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.actionButton}
            onPress={handleFavorite}
          >
            <MaterialCommunityIcons
              name={favorite ? 'heart' : 'heart-outline'}
              size={22}
              color={favorite ? colors.error : colors.text}
            />
          </TouchableOpacity>
        </View>
      </View>

      <ScrollView
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        <View
          style={[styles.categoryBadge, { backgroundColor: categoryColor + '20' }]}
        >
          <Text style={[styles.categoryText, { color: categoryColor }]}>
            {prompt.category}
          </Text>
        </View>

        <Text style={styles.title}>{prompt.title}</Text>

        <View style={styles.tags}>
          {prompt.tags.map((tag) => (
            <View key={tag} style={styles.tag}>
              <Text style={styles.tagText}>{tag}</Text>
            </View>
          ))}
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Prompt</Text>
          <View style={styles.promptBox}>
            <Text style={styles.promptContent}>{prompt.content}</Text>
          </View>
        </View>

        {'useCases' in prompt && prompt.useCases && prompt.useCases.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Use Cases</Text>
            <View style={styles.useCases}>
              {prompt.useCases.map((useCase, index) => (
                <View key={index} style={styles.useCaseItem}>
                  <MaterialCommunityIcons
                    name="check-circle"
                    size={18}
                    color={colors.success}
                  />
                  <Text style={styles.useCaseText}>{useCase}</Text>
                </View>
              ))}
            </View>
          </View>
        )}

        {'tips' in prompt && prompt.tips && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Tips</Text>
            <View style={styles.tipsBox}>
              <MaterialCommunityIcons
                name="lightbulb-outline"
                size={20}
                color={colors.warning}
              />
              <Text style={styles.tipsText}>{prompt.tips}</Text>
            </View>
          </View>
        )}
      </ScrollView>

      <View style={styles.footer}>
        <TouchableOpacity style={styles.copyButton} onPress={handleCopy}>
          <MaterialCommunityIcons
            name="content-copy"
            size={22}
            color={colors.background}
          />
          <Text style={styles.copyButtonText}>Copy Prompt</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
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
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
  },
  backButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: colors.surface,
    justifyContent: 'center',
    alignItems: 'center',
  },
  headerActions: {
    flexDirection: 'row',
    gap: spacing.sm,
  },
  actionButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: colors.surface,
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    padding: spacing.lg,
    paddingBottom: 100,
  },
  categoryBadge: {
    alignSelf: 'flex-start',
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderRadius: borderRadius.sm,
    marginBottom: spacing.md,
  },
  categoryText: {
    fontSize: fontSize.xs,
    fontWeight: '600',
    textTransform: 'capitalize',
  },
  title: {
    fontSize: fontSize.xxl,
    fontWeight: '700',
    color: colors.text,
    marginBottom: spacing.md,
  },
  tags: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
    marginBottom: spacing.lg,
  },
  tag: {
    backgroundColor: colors.surface,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
    borderRadius: borderRadius.sm,
  },
  tagText: {
    fontSize: fontSize.sm,
    color: colors.textSecondary,
  },
  section: {
    marginBottom: spacing.lg,
  },
  sectionTitle: {
    fontSize: fontSize.sm,
    fontWeight: '600',
    color: colors.textSecondary,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
    marginBottom: spacing.sm,
  },
  promptBox: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
  },
  promptContent: {
    fontSize: fontSize.md,
    color: colors.text,
    lineHeight: 24,
    fontFamily: 'monospace',
  },
  useCases: {
    gap: spacing.sm,
  },
  useCaseItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
  },
  useCaseText: {
    fontSize: fontSize.md,
    color: colors.text,
  },
  tipsBox: {
    flexDirection: 'row',
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    gap: spacing.sm,
    alignItems: 'flex-start',
  },
  tipsText: {
    flex: 1,
    fontSize: fontSize.md,
    color: colors.textSecondary,
    lineHeight: 22,
  },
  footer: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: colors.background,
    padding: spacing.md,
    paddingBottom: spacing.lg,
    borderTopWidth: 1,
    borderTopColor: colors.surface,
  },
  copyButton: {
    flexDirection: 'row',
    backgroundColor: colors.primary,
    paddingVertical: spacing.md,
    borderRadius: borderRadius.lg,
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.sm,
  },
  copyButtonText: {
    fontSize: fontSize.lg,
    fontWeight: '600',
    color: colors.background,
  },
  errorText: {
    fontSize: fontSize.lg,
    color: colors.error,
    textAlign: 'center',
    marginTop: spacing.xl,
  },
});
