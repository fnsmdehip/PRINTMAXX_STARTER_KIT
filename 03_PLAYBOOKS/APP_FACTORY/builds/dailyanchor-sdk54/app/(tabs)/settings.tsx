import { View, Text, StyleSheet, SafeAreaView, ScrollView } from 'react-native';
import { COLORS } from '../../src/utils/constants';
import { MoreApps } from '../../src/components/common/MoreApps';

export default function SettingsScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Settings</Text>
      </View>
      <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
        <View style={styles.content}>
          <Text style={styles.placeholder}>Settings will appear here</Text>
        </View>

        {/* More Apps */}
        <MoreApps />

        <Text style={styles.version}>DailyAnchor v1.0.0</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    padding: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: '800',
    color: COLORS.text,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
    paddingTop: 0,
    paddingBottom: 40,
  },
  content: {
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 40,
  },
  placeholder: {
    fontSize: 16,
    color: COLORS.textSecondary,
  },
  version: {
    fontSize: 13,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginTop: 20,
  },
});
