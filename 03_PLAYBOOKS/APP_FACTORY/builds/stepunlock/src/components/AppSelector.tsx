import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';
import { COLORS, DEFAULT_BLOCKED_APPS } from '../utils/constants';
import { BlockedApp } from '../types';
import { getBlockableApps } from '../services/blockerService';

interface Props {
  selectedApps: BlockedApp[];
  onSelectionChange: (apps: BlockedApp[]) => void;
}

export function AppSelector({ selectedApps, onSelectionChange }: Props) {
  const [availableApps, setAvailableApps] = useState<BlockedApp[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadApps();
  }, []);

  const loadApps = async () => {
    setIsLoading(true);
    try {
      const apps = await getBlockableApps();
      // If native module returns empty, use defaults
      setAvailableApps(apps.length > 0 ? apps : DEFAULT_BLOCKED_APPS);
    } catch {
      setAvailableApps(DEFAULT_BLOCKED_APPS);
    }
    setIsLoading(false);
  };

  const toggleApp = (app: BlockedApp) => {
    const isSelected = selectedApps.some((a) => a.id === app.id);
    if (isSelected) {
      onSelectionChange(selectedApps.filter((a) => a.id !== app.id));
    } else {
      onSelectionChange([...selectedApps, app]);
    }
  };

  const isSelected = (app: BlockedApp) =>
    selectedApps.some((a) => a.id === app.id);

  const renderApp = ({ item }: { item: BlockedApp }) => (
    <TouchableOpacity
      style={[styles.appItem, isSelected(item) && styles.appItemSelected]}
      onPress={() => toggleApp(item)}
    >
      <View style={styles.appInfo}>
        <View style={styles.appIcon}>
          <Text style={styles.appIconText}>{item.name.charAt(0)}</Text>
        </View>
        <Text style={styles.appName}>{item.name}</Text>
      </View>
      <View
        style={[
          styles.checkbox,
          isSelected(item) && styles.checkboxSelected,
        ]}
      >
        {isSelected(item) && <Text style={styles.checkmark}>✓</Text>}
      </View>
    </TouchableOpacity>
  );

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
        <Text style={styles.loadingText}>Loading apps...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Apps to block</Text>
      <Text style={styles.subtitle}>
        Select apps you want blocked until you hit your step goal
      </Text>

      <View style={styles.selectionInfo}>
        <Text style={styles.selectionCount}>
          {selectedApps.length} app{selectedApps.length !== 1 ? 's' : ''} selected
        </Text>
      </View>

      <FlatList
        data={availableApps}
        renderItem={renderApp}
        keyExtractor={(item) => item.id}
        style={styles.list}
        showsVerticalScrollIndicator={false}
      />

      <TouchableOpacity
        style={styles.selectAllButton}
        onPress={() => {
          if (selectedApps.length === availableApps.length) {
            onSelectionChange([]);
          } else {
            onSelectionChange([...availableApps]);
          }
        }}
      >
        <Text style={styles.selectAllText}>
          {selectedApps.length === availableApps.length
            ? 'Deselect all'
            : 'Select all'}
        </Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 12,
    fontSize: 16,
    color: COLORS.textSecondary,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 16,
  },
  selectionInfo: {
    marginBottom: 12,
  },
  selectionCount: {
    fontSize: 14,
    color: COLORS.primary,
    fontWeight: '500',
  },
  list: {
    flex: 1,
  },
  appItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 12,
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    marginBottom: 8,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  appItemSelected: {
    borderColor: COLORS.primary,
    backgroundColor: '#E8F5E9',
  },
  appInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  appIcon: {
    width: 40,
    height: 40,
    borderRadius: 10,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  appIconText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: COLORS.surface,
  },
  appName: {
    fontSize: 16,
    color: COLORS.text,
  },
  checkbox: {
    width: 24,
    height: 24,
    borderRadius: 6,
    borderWidth: 2,
    borderColor: COLORS.border,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkboxSelected: {
    backgroundColor: COLORS.primary,
    borderColor: COLORS.primary,
  },
  checkmark: {
    color: COLORS.surface,
    fontSize: 14,
    fontWeight: 'bold',
  },
  selectAllButton: {
    padding: 12,
    alignItems: 'center',
  },
  selectAllText: {
    fontSize: 14,
    color: COLORS.primary,
    fontWeight: '500',
  },
});
