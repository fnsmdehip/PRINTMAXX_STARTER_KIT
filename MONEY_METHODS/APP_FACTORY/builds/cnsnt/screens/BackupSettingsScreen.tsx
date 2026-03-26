/**
 * Backup Settings Screen for cnsnt app.
 *
 * - Toggle auto-backup on/off
 * - Connect/disconnect Google Drive, Dropbox
 * - iCloud status (iOS only)
 * - Manual backup / manual restore
 * - Last backup time with health indicator
 * - Export/import .cnsnt backup files
 * - Encryption notice
 */

import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Switch,
  Pressable,
  Alert,
  ActivityIndicator,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import ErrorBoundary from '../components/ErrorBoundary';
import cloudBackup, {
  type CloudConnectionState,
  type BackupHealthStatus,
  type CloudProvider,
  type BackupInfo,
  type CnsntBackup,
} from '../services/cloudBackup';
import {
  Colors,
  Typography,
  Spacing,
  BorderRadius,
  Shadows,
  CardBorder,
  MIN_TOUCH_SIZE,
} from '../constants/theme';

interface BackupSettingsProps {
  navigation: {
    goBack: () => void;
  };
}

const HEALTH_COLORS: Record<BackupHealthStatus, string> = {
  good: Colors.success,
  warning: Colors.warning,
  critical: Colors.error,
  never: Colors.textTertiary,
};

const HEALTH_LABELS: Record<BackupHealthStatus, string> = {
  good: 'Backed up recently',
  warning: 'Backup is getting old',
  critical: 'Backup overdue',
  never: 'Never backed up',
};

const BackupSettingsScreen: React.FC<BackupSettingsProps> = ({ navigation }) => {
  const [loading, setLoading] = useState(true);
  const [autoBackupEnabled, setAutoBackupEnabled] = useState(false);
  const [connections, setConnections] = useState<CloudConnectionState>({
    icloud: { connected: false, lastBackup: null },
    gdrive: { connected: false, lastBackup: null, email: null },
    dropbox: { connected: false, lastBackup: null, email: null },
  });
  const [lastBackupTime, setLastBackupTime] = useState<string | null>(null);
  const [healthStatus, setHealthStatus] = useState<BackupHealthStatus>('never');
  const [backingUp, setBackingUp] = useState(false);
  const [restoring, setRestoring] = useState(false);
  const [connectingProvider, setConnectingProvider] = useState<CloudProvider | null>(null);

  const gdriveConfigured = cloudBackup.isOAuthConfigured('gdrive');
  const dropboxConfigured = cloudBackup.isOAuthConfigured('dropbox');

  const loadState = useCallback(async () => {
    try {
      const [autoEnabled, connState, lastTime] = await Promise.all([
        cloudBackup.isAutoBackupEnabled(),
        cloudBackup.getConnectionState(),
        cloudBackup.getLastBackupTime(),
      ]);

      setAutoBackupEnabled(autoEnabled);
      setConnections(connState);
      setLastBackupTime(lastTime);
      setHealthStatus(cloudBackup.getBackupHealthStatus(lastTime));
    } catch {
      Alert.alert('Error', 'Failed to load backup settings.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadState();
  }, [loadState]);

  const handleAutoBackupToggle = async (value: boolean) => {
    await cloudBackup.setAutoBackupEnabled(value);
    setAutoBackupEnabled(value);
  };

  const handleConnectGDrive = async () => {
    setConnectingProvider('gdrive');
    try {
      const success = await cloudBackup.connectProvider('gdrive');
      if (success) {
        Alert.alert('Connected', 'Google Drive connected for backup.');
        await loadState();
      } else {
        Alert.alert('Cancelled', 'Google Drive connection was cancelled.');
      }
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Connection failed.';
      Alert.alert('Error', msg);
    } finally {
      setConnectingProvider(null);
    }
  };

  const handleDisconnectGDrive = () => {
    Alert.alert(
      'Disconnect Google Drive',
      'Your existing backups in Google Drive will not be deleted, but new auto-backups will stop.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Disconnect',
          style: 'destructive',
          onPress: async () => {
            await cloudBackup.disconnectProvider('gdrive');
            await loadState();
          },
        },
      ]
    );
  };

  const handleConnectDropbox = async () => {
    setConnectingProvider('dropbox');
    try {
      const success = await cloudBackup.connectProvider('dropbox');
      if (success) {
        Alert.alert('Connected', 'Dropbox connected for backup.');
        await loadState();
      } else {
        Alert.alert('Cancelled', 'Dropbox connection was cancelled.');
      }
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Connection failed.';
      Alert.alert('Error', msg);
    } finally {
      setConnectingProvider(null);
    }
  };

  const handleDisconnectDropbox = () => {
    Alert.alert(
      'Disconnect Dropbox',
      'Your existing backups in Dropbox will not be deleted, but new auto-backups will stop.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Disconnect',
          style: 'destructive',
          onPress: async () => {
            await cloudBackup.disconnectProvider('dropbox');
            await loadState();
          },
        },
      ]
    );
  };

  const handleManualBackup = async () => {
    const connectedProviders: string[] = [];
    if (connections.icloud.connected) connectedProviders.push('iCloud');
    if (connections.gdrive.connected) connectedProviders.push('Google Drive');
    if (connections.dropbox.connected) connectedProviders.push('Dropbox');

    if (connectedProviders.length === 0) {
      Alert.alert(
        'No Cloud Connected',
        'Connect a cloud service first, or use "Export Backup File" to save locally.',
      );
      return;
    }

    setBackingUp(true);
    try {
      const results = await cloudBackup.backupToAll();
      await loadState();

      const providers = results.map((r) => {
        switch (r.provider) {
          case 'icloud': return 'iCloud';
          case 'gdrive': return 'Google Drive';
          case 'dropbox': return 'Dropbox';
          default: return r.provider;
        }
      });

      Alert.alert(
        'Backup Complete',
        `${results[0]?.recordCount || 0} records backed up to: ${providers.join(', ')}.`
      );
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Backup failed.';
      Alert.alert('Backup Failed', msg);
    } finally {
      setBackingUp(false);
    }
  };

  const handleExportFile = async () => {
    setBackingUp(true);
    try {
      const info = await cloudBackup.local.exportBackup();
      Alert.alert(
        'Export Ready',
        `Backup file with ${info.recordCount} records is ready to share.`
      );
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Export failed.';
      Alert.alert('Export Failed', msg);
    } finally {
      setBackingUp(false);
    }
  };

  const handleRestoreFromCloud = async (provider: CloudProvider) => {
    setRestoring(true);
    try {
      let backups: BackupInfo[];

      switch (provider) {
        case 'icloud':
          backups = await cloudBackup.icloud.listBackups();
          break;
        case 'gdrive':
          backups = await cloudBackup.gdrive.listBackups();
          break;
        case 'dropbox':
          backups = await cloudBackup.dropbox.listBackups();
          break;
        default:
          setRestoring(false);
          return;
      }

      if (backups.length === 0) {
        Alert.alert('No Backups Found', `No backup files were found in ${providerLabel(provider)}.`);
        setRestoring(false);
        return;
      }

      // Use the most recent backup
      const latest = backups[0];

      Alert.alert(
        'Restore Backup',
        `Found backup from ${cloudBackup.formatRelativeTime(latest.timestamp)}. How would you like to restore?`,
        [
          { text: 'Cancel', style: 'cancel', onPress: () => setRestoring(false) },
          {
            text: 'Merge (keep existing)',
            onPress: () => executeRestore(provider, latest, 'merge'),
          },
          {
            text: 'Replace all',
            style: 'destructive',
            onPress: () => {
              Alert.alert(
                'Confirm Replace',
                'This will delete all current records and replace them with the backup. Continue?',
                [
                  { text: 'Cancel', style: 'cancel', onPress: () => setRestoring(false) },
                  {
                    text: 'Replace',
                    style: 'destructive',
                    onPress: () => executeRestore(provider, latest, 'replace'),
                  },
                ]
              );
            },
          },
        ]
      );
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Restore failed.';
      Alert.alert('Restore Failed', msg);
      setRestoring(false);
    }
  };

  const executeRestore = async (
    provider: CloudProvider,
    backupInfo: BackupInfo,
    mode: 'replace' | 'merge'
  ) => {
    try {
      let backup: CnsntBackup;

      switch (provider) {
        case 'icloud':
          backup = await cloudBackup.icloud.restore(backupInfo.filename);
          break;
        case 'gdrive':
          backup = await cloudBackup.gdrive.restore(backupInfo.filename);
          break;
        case 'dropbox':
          backup = await cloudBackup.dropbox.restore(backupInfo.filename);
          break;
        default:
          throw new Error('Unknown provider');
      }

      const data = await cloudBackup.restoreFromBackup(backup);
      const result = await cloudBackup.applyRestore(data, mode);

      Alert.alert(
        'Restore Complete',
        `Imported: ${result.imported} records${result.skipped > 0 ? `, skipped ${result.skipped} duplicates` : ''}.`
      );

      await loadState();
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Restore failed.';
      Alert.alert('Restore Failed', msg);
    } finally {
      setRestoring(false);
    }
  };

  const handleRestoreMenu = () => {
    const options: Array<{ label: string; provider: CloudProvider; connected: boolean }> = [];

    if (connections.icloud.connected) {
      options.push({ label: 'From iCloud', provider: 'icloud', connected: true });
    }
    if (connections.gdrive.connected) {
      options.push({ label: 'From Google Drive', provider: 'gdrive', connected: true });
    }
    if (connections.dropbox.connected) {
      options.push({ label: 'From Dropbox', provider: 'dropbox', connected: true });
    }

    if (options.length === 0) {
      Alert.alert(
        'No Cloud Connected',
        'Connect a cloud service to restore from cloud backups. You can back up to Google Drive, iCloud, or Dropbox from the settings above.'
      );
      return;
    }

    Alert.alert(
      'Restore From',
      'Select backup source:',
      [
        ...options.map((opt) => ({
          text: opt.label,
          onPress: () => handleRestoreFromCloud(opt.provider),
        })),
        { text: 'Cancel', style: 'cancel' as const },
      ]
    );
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={Colors.primary} />
      </SafeAreaView>
    );
  }

  return (
    <ErrorBoundary>
      <SafeAreaView style={styles.container} edges={['left', 'right']}>
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
        >
          {/* Backup Health */}
          <View style={styles.healthCard}>
            <View style={styles.healthHeader}>
              <View style={[styles.healthDot, { backgroundColor: HEALTH_COLORS[healthStatus] }]} />
              <Text style={[styles.healthLabel, { color: HEALTH_COLORS[healthStatus] }]}>
                {HEALTH_LABELS[healthStatus]}
              </Text>
            </View>
            {lastBackupTime ? (
              <Text style={styles.healthDetail}>
                Last backup: {cloudBackup.formatRelativeTime(lastBackupTime)}
              </Text>
            ) : (
              <Text style={styles.healthDetail}>
                No backups yet. Create one to protect your data.
              </Text>
            )}
          </View>

          {/* Encryption Notice */}
          <View style={styles.encryptionNotice}>
            <Ionicons name="lock-closed" size={16} color={Colors.success} />
            <Text style={styles.encryptionText}>
              All backups are encrypted on your device before upload. Your cloud provider cannot read your data.
            </Text>
          </View>

          {/* Auto-Backup */}
          <Text style={styles.sectionTitle}>Auto-Backup</Text>
          <View style={styles.settingsGroup}>
            <View style={styles.settingRow}>
              <View style={styles.settingIconContainer}>
                <Ionicons name="sync" size={18} color={Colors.primary} />
              </View>
              <View style={styles.settingInfo}>
                <Text style={styles.settingLabel}>Auto-Backup</Text>
                <Text style={styles.settingDescription}>
                  Back up after every record change (max 1/hour)
                </Text>
              </View>
              <Switch
                value={autoBackupEnabled}
                onValueChange={handleAutoBackupToggle}
                trackColor={{ false: Colors.border, true: Colors.primaryMuted }}
                thumbColor={autoBackupEnabled ? Colors.primary : Colors.surfaceElevated}
              />
            </View>
          </View>

          {/* Cloud Services */}
          <Text style={styles.sectionTitle}>Cloud Services</Text>
          <View style={styles.settingsGroup}>
            {/* iCloud */}
            {Platform.OS === 'ios' && (
              <View style={styles.providerRow}>
                <View style={[styles.providerIcon, { backgroundColor: '#E8F4FD' }]}>
                  <Ionicons name="cloud" size={18} color="#007AFF" />
                </View>
                <View style={styles.providerInfo}>
                  <Text style={styles.providerName}>iCloud</Text>
                  <Text style={styles.providerStatus}>
                    {connections.icloud.connected
                      ? connections.icloud.lastBackup
                        ? `Last: ${cloudBackup.formatRelativeTime(connections.icloud.lastBackup)}`
                        : 'Available'
                      : 'Not available'}
                  </Text>
                </View>
                <View
                  style={[
                    styles.statusDot,
                    {
                      backgroundColor: connections.icloud.connected
                        ? Colors.success
                        : Colors.textTertiary,
                    },
                  ]}
                />
              </View>
            )}

            {/* Google Drive */}
            <View style={styles.providerRow}>
              <View style={[styles.providerIcon, { backgroundColor: gdriveConfigured ? '#FFF3E0' : '#F3F4F6' }]}>
                <Ionicons name="logo-google" size={18} color={gdriveConfigured ? '#EA4335' : Colors.textTertiary} />
              </View>
              <View style={styles.providerInfo}>
                <Text style={[styles.providerName, !gdriveConfigured && { color: Colors.textTertiary }]}>
                  Google Drive
                </Text>
                <Text style={styles.providerStatus}>
                  {!gdriveConfigured
                    ? 'Credentials not configured'
                    : connections.gdrive.connected
                      ? connections.gdrive.email || 'Connected'
                      : 'Not connected'}
                </Text>
                {connections.gdrive.lastBackup && gdriveConfigured && (
                  <Text style={styles.providerLastBackup}>
                    Last: {cloudBackup.formatRelativeTime(connections.gdrive.lastBackup)}
                  </Text>
                )}
              </View>
              {gdriveConfigured ? (
                connectingProvider === 'gdrive' ? (
                  <ActivityIndicator size="small" color={Colors.primary} />
                ) : connections.gdrive.connected ? (
                  <Pressable
                    style={styles.disconnectButton}
                    onPress={handleDisconnectGDrive}
                    hitSlop={8}
                  >
                    <Text style={styles.disconnectText}>Disconnect</Text>
                  </Pressable>
                ) : (
                  <Pressable
                    style={styles.connectButton}
                    onPress={handleConnectGDrive}
                    hitSlop={8}
                  >
                    <Text style={styles.connectText}>Connect</Text>
                  </Pressable>
                )
              ) : null}
            </View>

            {/* Dropbox */}
            <View style={[styles.providerRow, { borderBottomWidth: 0 }]}>
              <View style={[styles.providerIcon, { backgroundColor: dropboxConfigured ? '#E8F0FE' : '#F3F4F6' }]}>
                <Ionicons name="cube" size={18} color={dropboxConfigured ? '#0061FF' : Colors.textTertiary} />
              </View>
              <View style={styles.providerInfo}>
                <Text style={[styles.providerName, !dropboxConfigured && { color: Colors.textTertiary }]}>
                  Dropbox
                </Text>
                <Text style={styles.providerStatus}>
                  {!dropboxConfigured
                    ? 'Credentials not configured'
                    : connections.dropbox.connected
                      ? connections.dropbox.email || 'Connected'
                      : 'Not connected'}
                </Text>
                {connections.dropbox.lastBackup && dropboxConfigured && (
                  <Text style={styles.providerLastBackup}>
                    Last: {cloudBackup.formatRelativeTime(connections.dropbox.lastBackup)}
                  </Text>
                )}
              </View>
              {dropboxConfigured ? (
                connectingProvider === 'dropbox' ? (
                  <ActivityIndicator size="small" color={Colors.primary} />
                ) : connections.dropbox.connected ? (
                  <Pressable
                    style={styles.disconnectButton}
                    onPress={handleDisconnectDropbox}
                    hitSlop={8}
                  >
                    <Text style={styles.disconnectText}>Disconnect</Text>
                  </Pressable>
                ) : (
                  <Pressable
                    style={styles.connectButton}
                    onPress={handleConnectDropbox}
                    hitSlop={8}
                  >
                    <Text style={styles.connectText}>Connect</Text>
                  </Pressable>
                )
              ) : null}
            </View>

            {/* OAuth credentials note */}
            {(!gdriveConfigured || !dropboxConfigured) && (
              <View style={[styles.providerRow, { borderBottomWidth: 0, opacity: 0.7 }]}>
                <View style={[styles.settingIconContainer, { backgroundColor: Colors.surfaceElevated }]}>
                  <Ionicons name="information-circle-outline" size={18} color={Colors.textTertiary} />
                </View>
                <Text style={styles.infoText}>
                  Configure Google Drive / Dropbox credentials in .env to enable cloud backup. iCloud and local export are always available.
                </Text>
              </View>
            )}
          </View>

          {/* Manual Actions */}
          <Text style={styles.sectionTitle}>Manual Backup & Restore</Text>
          <View style={styles.settingsGroup}>
            {/* Backup to cloud */}
            <Pressable
              style={styles.actionRow}
              onPress={handleManualBackup}
              disabled={backingUp || restoring}
            >
              <View style={[styles.settingIconContainer, { backgroundColor: Colors.successLight }]}>
                <Ionicons name="cloud-upload" size={18} color={Colors.success} />
              </View>
              <Text style={styles.actionText}>
                {backingUp ? 'Backing up...' : 'Backup to Cloud Now'}
              </Text>
              {backingUp && (
                <ActivityIndicator
                  size="small"
                  color={Colors.primary}
                  style={{ marginLeft: 'auto' }}
                />
              )}
            </Pressable>

            {/* Restore from cloud */}
            <Pressable
              style={styles.actionRow}
              onPress={handleRestoreMenu}
              disabled={backingUp || restoring}
            >
              <View style={[styles.settingIconContainer, { backgroundColor: Colors.primaryLight }]}>
                <Ionicons name="cloud-download" size={18} color={Colors.primary} />
              </View>
              <Text style={styles.actionText}>
                {restoring ? 'Restoring...' : 'Restore from Cloud'}
              </Text>
              {restoring && (
                <ActivityIndicator
                  size="small"
                  color={Colors.primary}
                  style={{ marginLeft: 'auto' }}
                />
              )}
            </Pressable>

            {/* Export .cnsnt file */}
            <Pressable
              style={styles.actionRow}
              onPress={handleExportFile}
              disabled={backingUp || restoring}
            >
              <View style={[styles.settingIconContainer, { backgroundColor: Colors.warningLight }]}>
                <Ionicons name="share" size={18} color={Colors.warning} />
              </View>
              <Text style={styles.actionText}>Export Backup File (.cnsnt)</Text>
            </Pressable>

            {/* Info row */}
            <View style={[styles.actionRow, { borderBottomWidth: 0, opacity: 0.6 }]}>
              <View style={[styles.settingIconContainer, { backgroundColor: Colors.surfaceElevated }]}>
                <Ionicons name="information-circle" size={18} color={Colors.textTertiary} />
              </View>
              <Text style={styles.infoText}>
                Export creates an encrypted .cnsnt file you can save anywhere via AirDrop, email, or Files.
              </Text>
            </View>
          </View>

          {/* Bottom spacer */}
          <View style={{ height: Spacing.xxxl * 2 }} />
        </ScrollView>
      </SafeAreaView>
    </ErrorBoundary>
  );
};

function providerLabel(provider: CloudProvider): string {
  switch (provider) {
    case 'icloud': return 'iCloud';
    case 'gdrive': return 'Google Drive';
    case 'dropbox': return 'Dropbox';
    case 'local': return 'Local';
    default: return provider;
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  loadingContainer: {
    flex: 1,
    backgroundColor: Colors.background,
    justifyContent: 'center',
    alignItems: 'center',
  },
  scrollContent: {
    padding: Spacing.lg,
  },

  // Health card
  healthCard: {
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.xl,
    padding: Spacing.xl,
    marginBottom: Spacing.lg,
    ...CardBorder,
    ...Shadows.card,
  },
  healthHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: Spacing.sm,
  },
  healthDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    marginRight: Spacing.sm,
  },
  healthLabel: {
    ...Typography.label,
    fontWeight: '600',
  },
  healthDetail: {
    ...Typography.caption,
    color: Colors.textSecondary,
    marginLeft: 18,
  },

  // Encryption notice
  encryptionNotice: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    backgroundColor: Colors.successLight,
    borderRadius: BorderRadius.md,
    padding: Spacing.md,
    marginBottom: Spacing.xl,
    gap: Spacing.sm,
  },
  encryptionText: {
    ...Typography.caption,
    color: '#065F46',
    flex: 1,
    lineHeight: 18,
  },

  // Section
  sectionTitle: {
    ...Typography.overline,
    color: Colors.textTertiary,
    marginTop: Spacing.lg,
    marginBottom: Spacing.md,
  },

  // Settings group
  settingsGroup: {
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.lg,
    ...CardBorder,
    ...Shadows.card,
    overflow: 'hidden',
  },
  settingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: Spacing.lg,
    borderBottomWidth: 1,
    borderBottomColor: Colors.divider,
    minHeight: MIN_TOUCH_SIZE,
  },
  settingIconContainer: {
    width: 36,
    height: 36,
    borderRadius: 10,
    backgroundColor: Colors.surfaceElevated,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: Spacing.md,
  },
  settingInfo: {
    flex: 1,
    marginRight: Spacing.md,
  },
  settingLabel: {
    ...Typography.body,
    color: Colors.textPrimary,
    fontWeight: '500',
  },
  settingDescription: {
    ...Typography.caption,
    color: Colors.textTertiary,
    marginTop: 2,
  },

  // Provider rows
  providerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: Spacing.lg,
    borderBottomWidth: 1,
    borderBottomColor: Colors.divider,
    minHeight: MIN_TOUCH_SIZE,
  },
  providerIcon: {
    width: 36,
    height: 36,
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: Spacing.md,
  },
  providerInfo: {
    flex: 1,
    marginRight: Spacing.md,
  },
  providerName: {
    ...Typography.body,
    color: Colors.textPrimary,
    fontWeight: '500',
  },
  providerStatus: {
    ...Typography.caption,
    color: Colors.textTertiary,
    marginTop: 1,
  },
  providerLastBackup: {
    ...Typography.caption,
    color: Colors.textTertiary,
    marginTop: 1,
    fontSize: 11,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  connectButton: {
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
    borderRadius: BorderRadius.round,
    backgroundColor: Colors.primaryLight,
    minHeight: MIN_TOUCH_SIZE,
    justifyContent: 'center',
  },
  connectText: {
    ...Typography.caption,
    color: Colors.primary,
    fontWeight: '600',
  },
  disconnectButton: {
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
    borderRadius: BorderRadius.round,
    backgroundColor: Colors.errorLight,
    minHeight: MIN_TOUCH_SIZE,
    justifyContent: 'center',
  },
  disconnectText: {
    ...Typography.caption,
    color: Colors.error,
    fontWeight: '600',
  },

  // Action rows
  actionRow: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: Spacing.lg,
    borderBottomWidth: 1,
    borderBottomColor: Colors.divider,
    minHeight: MIN_TOUCH_SIZE,
  },
  actionText: {
    ...Typography.body,
    color: Colors.primary,
    fontWeight: '500',
  },
  infoText: {
    ...Typography.caption,
    color: Colors.textTertiary,
    flex: 1,
    lineHeight: 18,
  },
});

export default BackupSettingsScreen;
