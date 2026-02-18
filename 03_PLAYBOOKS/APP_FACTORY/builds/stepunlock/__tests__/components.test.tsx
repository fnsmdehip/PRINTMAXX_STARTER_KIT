import React from 'react';
import { render } from '@testing-library/react-native';
import { ProgressRing } from '../src/components/ProgressRing';
import { StreakBadge } from '../src/components/StreakBadge';
import { Button } from '../src/components/Button';
import { StreakData } from '../src/types';

describe('ProgressRing', () => {
  it('renders correctly with zero progress', () => {
    const { getByText } = render(
      <ProgressRing progress={0} steps={0} goal={5000} />
    );

    expect(getByText('0')).toBeTruthy();
    expect(getByText('/ 5,000')).toBeTruthy();
    expect(getByText('5,000 to go')).toBeTruthy();
  });

  it('renders correctly with partial progress', () => {
    const { getByText } = render(
      <ProgressRing progress={0.5} steps={2500} goal={5000} />
    );

    expect(getByText('2,500')).toBeTruthy();
    expect(getByText('2,500 to go')).toBeTruthy();
  });

  it('renders completed state correctly', () => {
    const { getByText } = render(
      <ProgressRing progress={1} steps={5000} goal={5000} />
    );

    expect(getByText('5,000')).toBeTruthy();
    expect(getByText('Goal reached!')).toBeTruthy();
  });

  it('handles over 100% progress', () => {
    const { getByText } = render(
      <ProgressRing progress={1.5} steps={7500} goal={5000} />
    );

    expect(getByText('7,500')).toBeTruthy();
    expect(getByText('Goal reached!')).toBeTruthy();
  });
});

describe('StreakBadge', () => {
  const emptyStreak: StreakData = {
    currentStreak: 0,
    longestStreak: 0,
    totalDaysCompleted: 0,
    completedDates: [],
    lastCompletedDate: null,
  };

  it('renders zero streak correctly', () => {
    const { getByText } = render(<StreakBadge streak={emptyStreak} />);

    expect(getByText('0')).toBeTruthy();
    expect(getByText('Start your streak today!')).toBeTruthy();
  });

  it('renders active streak correctly', () => {
    const streak: StreakData = {
      currentStreak: 7,
      longestStreak: 10,
      totalDaysCompleted: 50,
      completedDates: [],
      lastCompletedDate: '2025-01-15',
    };

    const { getByText } = render(<StreakBadge streak={streak} />);

    expect(getByText('7')).toBeTruthy();
    expect(getByText('10')).toBeTruthy();
    expect(getByText('50')).toBeTruthy();
  });

  it('renders compact mode', () => {
    const streak: StreakData = {
      ...emptyStreak,
      currentStreak: 5,
    };

    const { getByText, queryByText } = render(
      <StreakBadge streak={streak} compact />
    );

    expect(getByText('5')).toBeTruthy();
    // Compact mode should not show detailed stats
    expect(queryByText('Best streak')).toBeNull();
  });
});

describe('Button', () => {
  it('renders with title', () => {
    const { getByText } = render(
      <Button title="Test Button" onPress={() => {}} />
    );

    expect(getByText('Test Button')).toBeTruthy();
  });

  it('renders loading state', () => {
    const { queryByText } = render(
      <Button title="Test Button" onPress={() => {}} loading />
    );

    // Title should not be visible when loading
    expect(queryByText('Test Button')).toBeNull();
  });

  it('is disabled when disabled prop is true', () => {
    const mockOnPress = jest.fn();
    const { getByText } = render(
      <Button title="Test Button" onPress={mockOnPress} disabled />
    );

    // The button should render but be non-functional
    expect(getByText('Test Button')).toBeTruthy();
  });

  it('renders different variants', () => {
    const { rerender, getByText } = render(
      <Button title="Primary" onPress={() => {}} variant="primary" />
    );
    expect(getByText('Primary')).toBeTruthy();

    rerender(
      <Button title="Secondary" onPress={() => {}} variant="secondary" />
    );
    expect(getByText('Secondary')).toBeTruthy();

    rerender(
      <Button title="Outline" onPress={() => {}} variant="outline" />
    );
    expect(getByText('Outline')).toBeTruthy();
  });

  it('renders different sizes', () => {
    const { rerender, getByText } = render(
      <Button title="Small" onPress={() => {}} size="small" />
    );
    expect(getByText('Small')).toBeTruthy();

    rerender(<Button title="Medium" onPress={() => {}} size="medium" />);
    expect(getByText('Medium')).toBeTruthy();

    rerender(<Button title="Large" onPress={() => {}} size="large" />);
    expect(getByText('Large')).toBeTruthy();
  });
});
