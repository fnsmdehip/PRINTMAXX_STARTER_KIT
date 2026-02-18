// Timer utility functions

export const formatTime = (seconds: number): string => {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
};

export const formatTimeWithHours = (seconds: number): string => {
  const hours = Math.floor(seconds / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;

  if (hours > 0) {
    return `${hours}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }

  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
};

export const formatMinutes = (minutes: number): string => {
  if (minutes < 60) {
    return `${minutes}m`;
  }

  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;

  if (mins === 0) {
    return `${hours}h`;
  }

  return `${hours}h ${mins}m`;
};

export const formatHoursDecimal = (minutes: number): string => {
  const hours = minutes / 60;
  return hours.toFixed(1);
};

export const minutesToSeconds = (minutes: number): number => minutes * 60;

export const secondsToMinutes = (seconds: number): number => Math.floor(seconds / 60);

export const calculateProgress = (remaining: number, total: number): number => {
  if (total === 0) return 0;
  return ((total - remaining) / total) * 100;
};

export const calculateTimeProgress = (remaining: number, total: number): number => {
  if (total === 0) return 1;
  return remaining / total;
};

export const getProgressColor = (progress: number): string => {
  // Returns color based on timer progress
  if (progress < 0.25) return '#10B981'; // Green - just started
  if (progress < 0.5) return '#0066FF'; // Blue - making progress
  if (progress < 0.75) return '#F59E0B'; // Yellow - more than halfway
  return '#EF4444'; // Red - almost done
};

export const isSessionOverdue = (remaining: number): boolean => {
  return remaining <= 0;
};

export const getMotivationalMessage = (progress: number): string => {
  if (progress < 0.1) return 'Great start! Keep it up!';
  if (progress < 0.25) return 'You\'re doing amazing!';
  if (progress < 0.5) return 'Keep pushing, you\'re making progress!';
  if (progress < 0.75) return 'Halfway there! Stay focused!';
  if (progress < 0.9) return 'Almost done! You\'ve got this!';
  return 'Final stretch! Finish strong!';
};

export const getStreakMessage = (streak: number): string => {
  if (streak === 0) return 'Start your streak today!';
  if (streak === 1) return 'First day! Keep going!';
  if (streak < 7) return `${streak} days strong!`;
  if (streak < 14) return `One week+! Incredible!`;
  if (streak < 30) return `${streak} days! You\'re unstoppable!`;
  if (streak < 60) return `${streak} day streak! Amazing dedication!`;
  if (streak < 100) return `${streak} days! You\'re a study machine!`;
  return `${streak} days! Legendary focus!`;
};

// Date helpers
export const getTodayDateString = (): string => {
  return new Date().toISOString().split('T')[0];
};

export const getYesterdayDateString = (): string => {
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  return yesterday.toISOString().split('T')[0];
};

export const formatDate = (date: Date | string): string => {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
  });
};

export const formatDateFull = (date: Date | string): string => {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
    year: 'numeric',
  });
};

export const getDayOfWeek = (date: Date | string): string => {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString('en-US', { weekday: 'short' });
};

export const isToday = (date: Date | string): boolean => {
  const d = typeof date === 'string' ? new Date(date) : date;
  const today = new Date();
  return d.toISOString().split('T')[0] === today.toISOString().split('T')[0];
};

export const isYesterday = (date: Date | string): boolean => {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toISOString().split('T')[0] === getYesterdayDateString();
};

export const getRelativeDateLabel = (date: Date | string): string => {
  if (isToday(date)) return 'Today';
  if (isYesterday(date)) return 'Yesterday';
  return formatDate(date);
};

// Week data for charts
export const getLast7Days = (): string[] => {
  const days: string[] = [];
  const today = new Date();

  for (let i = 6; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    days.push(date.toISOString().split('T')[0]);
  }

  return days;
};
