import { Exercise, Routine } from '../types';

// Facial Exercises
export const EXERCISES: Exercise[] = [
  // Jawline Exercises
  {
    id: 'jaw_clench',
    name: 'Jaw Clench',
    description: 'Strengthen masseter muscles for defined jawline',
    duration: 30,
    category: 'jawline',
    instructions: [
      'Clench your jaw muscles tightly',
      'Hold for 5 seconds',
      'Release and relax',
      'Repeat 6 times',
    ],
    forGender: 'all',
  },
  {
    id: 'chin_lift',
    name: 'Chin Lift',
    description: 'Tighten neck and jawline muscles',
    duration: 45,
    category: 'jawline',
    instructions: [
      'Tilt head back looking at ceiling',
      'Push jaw forward, feeling stretch under chin',
      'Hold for 10 seconds',
      'Return to neutral',
      'Repeat 5 times',
    ],
    forGender: 'all',
  },
  {
    id: 'neck_curl',
    name: 'Neck Curl',
    description: 'Define jawline and reduce double chin',
    duration: 60,
    category: 'jawline',
    instructions: [
      'Lie on back with tongue pressed to roof of mouth',
      'Bring chin to chest, lifting head slightly',
      'Lower slowly without letting head touch ground',
      'Repeat 10-15 times',
    ],
    forGender: 'all',
  },

  // Cheekbone Exercises
  {
    id: 'cheek_puff',
    name: 'Cheek Puff',
    description: 'Tone cheek muscles for hollow look',
    duration: 30,
    category: 'cheekbones',
    instructions: [
      'Puff air into both cheeks',
      'Move air from side to side',
      'Hold each side for 5 seconds',
      'Repeat 5 times',
    ],
    forGender: 'all',
  },
  {
    id: 'fish_face',
    name: 'Fish Face',
    description: 'Define cheekbones and slim face',
    duration: 45,
    category: 'cheekbones',
    instructions: [
      'Suck cheeks in like a fish',
      'Try to smile while holding',
      'Hold for 10 seconds',
      'Relax and repeat 5 times',
    ],
    forGender: 'all',
  },
  {
    id: 'cheekbone_press',
    name: 'Cheekbone Press',
    description: 'Lift and define malar bones',
    duration: 45,
    category: 'cheekbones',
    instructions: [
      'Place fingers on cheekbones',
      'Smile wide while pushing down slightly',
      'Hold smile against resistance for 10 seconds',
      'Repeat 5 times',
    ],
    forGender: 'all',
  },

  // Neck Exercises
  {
    id: 'neck_stretch',
    name: 'Neck Stretch',
    description: 'Elongate neck and improve posture',
    duration: 60,
    category: 'neck',
    instructions: [
      'Sit or stand with shoulders back',
      'Tilt head to right, ear toward shoulder',
      'Hold 15 seconds',
      'Repeat on left side',
      'Do 3 sets each side',
    ],
    forGender: 'all',
  },
  {
    id: 'platysma_stretch',
    name: 'Platysma Stretch',
    description: 'Tighten neck and reduce turkey neck',
    duration: 45,
    category: 'neck',
    instructions: [
      'Open mouth wide, pulling corners down',
      'Tense neck muscles (platysma should be visible)',
      'Hold for 10 seconds',
      'Relax and repeat 5 times',
    ],
    forGender: 'all',
  },

  // Eye Exercises
  {
    id: 'eye_squeeze',
    name: 'Eye Squeeze',
    description: 'Reduce crow\'s feet and tighten eye area',
    duration: 30,
    category: 'eyes',
    instructions: [
      'Close eyes tightly, squeezing',
      'Hold for 5 seconds',
      'Open wide, raising eyebrows',
      'Hold for 5 seconds',
      'Repeat 6 times',
    ],
    forGender: 'all',
  },
  {
    id: 'brow_lift',
    name: 'Brow Lift',
    description: 'Lift drooping brows and open eyes',
    duration: 45,
    category: 'eyes',
    instructions: [
      'Place fingers just above eyebrows',
      'Push brows down while trying to raise them',
      'Hold resistance for 10 seconds',
      'Repeat 5 times',
    ],
    forGender: 'all',
  },

  // Forehead Exercises
  {
    id: 'forehead_smooth',
    name: 'Forehead Smooth',
    description: 'Reduce forehead lines',
    duration: 30,
    category: 'forehead',
    instructions: [
      'Place both hands on forehead, fingers spread',
      'Pull skin taut toward temples',
      'Try to raise eyebrows against resistance',
      'Hold 10 seconds, repeat 5 times',
    ],
    forGender: 'all',
  },

  // Overall Face
  {
    id: 'lion_face',
    name: 'Lion Face',
    description: 'Full face workout and tension release',
    duration: 30,
    category: 'overall',
    instructions: [
      'Inhale deeply through nose',
      'Exhale while opening mouth wide',
      'Stick tongue out toward chin',
      'Open eyes wide',
      'Hold 5 seconds, repeat 5 times',
    ],
    forGender: 'all',
  },
  {
    id: 'face_massage',
    name: 'Lymphatic Face Massage',
    description: 'Reduce puffiness and improve circulation',
    duration: 120,
    category: 'overall',
    instructions: [
      'Apply face oil or serum',
      'Using light pressure, stroke from center of face outward',
      'Move from forehead down to jawline',
      'Use upward strokes on neck toward jaw',
      'Spend 30 seconds on each area',
    ],
    forGender: 'all',
  },
];

// Pre-built Routines
export const ROUTINES: Routine[] = [
  {
    id: 'morning_skincare',
    name: 'Morning Skincare',
    type: 'morning_skincare',
    description: 'Complete morning skincare routine',
    exercises: [],
    totalDuration: 300, // 5 minutes
    forGender: 'all',
  },
  {
    id: 'evening_skincare',
    name: 'Evening Skincare',
    type: 'evening_skincare',
    description: 'Complete evening skincare routine with double cleanse',
    exercises: [],
    totalDuration: 420, // 7 minutes
    forGender: 'all',
  },
  {
    id: 'mewing_practice',
    name: 'Mewing Practice',
    type: 'mewing',
    description: 'Guided mewing session with posture check',
    exercises: [],
    totalDuration: 300, // 5 minutes
    forGender: 'all',
  },
  {
    id: 'quick_jawline',
    name: 'Quick Jawline',
    type: 'facial_exercises',
    description: '5-minute jawline focused workout',
    exercises: EXERCISES.filter((e) => e.category === 'jawline'),
    totalDuration: 135,
    forGender: 'all',
  },
  {
    id: 'full_face',
    name: 'Full Face Workout',
    type: 'facial_exercises',
    description: 'Complete facial exercise routine',
    exercises: EXERCISES.filter((e) => e.category !== 'overall'),
    totalDuration: 420,
    forGender: 'all',
  },
  {
    id: 'debloat_morning',
    name: 'Morning Debloat',
    type: 'debloating',
    description: 'Quick routine to reduce morning puffiness',
    exercises: [
      EXERCISES.find((e) => e.id === 'face_massage')!,
      EXERCISES.find((e) => e.id === 'neck_stretch')!,
      EXERCISES.find((e) => e.id === 'lion_face')!,
    ],
    totalDuration: 210,
    forGender: 'all',
  },
  {
    id: 'male_jawline',
    name: 'Masculine Jawline',
    type: 'facial_exercises',
    description: 'Exercises focused on masculine jaw definition',
    exercises: [
      EXERCISES.find((e) => e.id === 'jaw_clench')!,
      EXERCISES.find((e) => e.id === 'chin_lift')!,
      EXERCISES.find((e) => e.id === 'neck_curl')!,
      EXERCISES.find((e) => e.id === 'platysma_stretch')!,
    ],
    totalDuration: 180,
    forGender: 'male',
  },
  {
    id: 'feminine_glow',
    name: 'Feminine Glow',
    type: 'facial_exercises',
    description: 'Softer exercises for feminine facial features',
    exercises: [
      EXERCISES.find((e) => e.id === 'cheek_puff')!,
      EXERCISES.find((e) => e.id === 'cheekbone_press')!,
      EXERCISES.find((e) => e.id === 'brow_lift')!,
      EXERCISES.find((e) => e.id === 'face_massage')!,
    ],
    totalDuration: 240,
    forGender: 'female',
  },
  {
    id: 'posture_check',
    name: 'Posture Reset',
    type: 'posture',
    description: 'Quick posture correction routine',
    exercises: [
      EXERCISES.find((e) => e.id === 'neck_stretch')!,
    ],
    totalDuration: 60,
    forGender: 'all',
  },
];

/**
 * Get routines filtered by gender
 */
export function getRoutinesForGender(gender: 'male' | 'female' | 'other'): Routine[] {
  return ROUTINES.filter(
    (routine) => routine.forGender === 'all' || routine.forGender === gender
  );
}

/**
 * Get exercise by ID
 */
export function getExerciseById(id: string): Exercise | undefined {
  return EXERCISES.find((e) => e.id === id);
}

/**
 * Get routine by ID
 */
export function getRoutineById(id: string): Routine | undefined {
  return ROUTINES.find((r) => r.id === id);
}
