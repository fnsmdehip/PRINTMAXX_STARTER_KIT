import { View, Text, StyleSheet, SafeAreaView } from 'react-native';
import { COLORS } from '../../src/utils/constants';

export default function JournalScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Journal</Text>
      </View>
      <View style={styles.content}>
        <Text style={styles.placeholder}>Journal entries will appear here</Text>
      </View>
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
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  placeholder: {
    fontSize: 16,
    color: COLORS.textSecondary,
  },
});
