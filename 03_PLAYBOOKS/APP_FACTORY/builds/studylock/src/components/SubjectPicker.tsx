import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { COLORS, SUBJECTS } from '../utils/constants';
import { Subject } from '../types';

interface SubjectPickerProps {
  selectedSubject: Subject;
  onSelectSubject: (subject: Subject) => void;
  horizontal?: boolean;
}

export const SubjectPicker: React.FC<SubjectPickerProps> = ({
  selectedSubject,
  onSelectSubject,
  horizontal = true,
}) => {
  const renderSubject = (subject: (typeof SUBJECTS)[0]) => {
    const isSelected = selectedSubject === subject.id;

    return (
      <TouchableOpacity
        key={subject.id}
        style={[styles.chip, isSelected && styles.chipSelected]}
        onPress={() => onSelectSubject(subject.id)}
        activeOpacity={0.7}
      >
        <Text style={styles.emoji}>{subject.emoji}</Text>
        <Text style={[styles.label, isSelected && styles.labelSelected]}>
          {subject.label}
        </Text>
      </TouchableOpacity>
    );
  };

  if (horizontal) {
    return (
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.horizontalContainer}
      >
        {SUBJECTS.map(renderSubject)}
      </ScrollView>
    );
  }

  return (
    <View style={styles.gridContainer}>
      {SUBJECTS.map(renderSubject)}
    </View>
  );
};

const styles = StyleSheet.create({
  horizontalContainer: {
    paddingHorizontal: 16,
    gap: 8,
  },
  gridContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    padding: 16,
  },
  chip: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
    paddingHorizontal: 16,
    borderRadius: 20,
    backgroundColor: COLORS.surface,
    gap: 6,
  },
  chipSelected: {
    backgroundColor: COLORS.primary,
  },
  emoji: {
    fontSize: 16,
  },
  label: {
    fontSize: 14,
    fontWeight: '500',
    color: COLORS.text,
  },
  labelSelected: {
    color: COLORS.white,
  },
});

export default SubjectPicker;
