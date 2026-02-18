// FemFit Exercise Library - Women-focused selection
export type MuscleGroup =
  | 'glutes'
  | 'legs'
  | 'arms'
  | 'back'
  | 'chest'
  | 'shoulders'
  | 'core';

export interface Exercise {
  id: string;
  name: string;
  category: MuscleGroup;
  muscles: string[];
  description: string;
  tips: string[];
  equipment: string[];
  videoUrl?: string; // YouTube tutorial link
  affiliateProducts?: AffiliateProduct[];
}

export interface AffiliateProduct {
  name: string;
  type: 'equipment' | 'supplement' | 'apparel';
  url: string; // Affiliate link
  price?: string;
}

export const exercises: Exercise[] = [
  // GLUTES (12)
  {
    id: 'hip-thrust',
    name: 'Hip Thrust',
    category: 'glutes',
    muscles: ['Glutes', 'Hamstrings'],
    description: 'Barbell hip thrust targeting the glutes. Great for building strength and shape.',
    tips: [
      'Keep chin tucked throughout movement',
      'Drive through heels',
      'Squeeze glutes hard at the top',
      'Pause at top for 1-2 seconds',
    ],
    equipment: ['Barbell', 'Bench'],
    videoUrl: 'https://www.youtube.com/watch?v=SEdqd1n0cvg', // Bret Contreras - The Glute Guy
    affiliateProducts: [
      { name: 'Hip Thrust Pad', type: 'equipment', url: 'AFFILIATE_LINK_PLACEHOLDER', price: '$29.99' },
      { name: 'Resistance Bands Set', type: 'equipment', url: 'AFFILIATE_LINK_PLACEHOLDER', price: '$19.99' },
    ],
  },
  {
    id: 'glute-bridge',
    name: 'Glute Bridge',
    category: 'glutes',
    muscles: ['Glutes', 'Hamstrings'],
    description: 'Floor-based glute activation exercise. Perfect for warm-ups or high reps.',
    tips: [
      'Press lower back into floor at start',
      'Squeeze glutes at top',
      'Control the descent',
    ],
    equipment: ['None'],
    videoUrl: 'https://www.youtube.com/watch?v=OUgsJ8-Vi0E',
    affiliateProducts: [
      { name: 'Exercise Mat', type: 'equipment', url: 'AFFILIATE_LINK_PLACEHOLDER', price: '$24.99' },
      { name: 'Booty Bands (3-Pack)', type: 'equipment', url: 'AFFILIATE_LINK_PLACEHOLDER', price: '$14.99' },
    ],
  },
  {
    id: 'cable-kickback',
    name: 'Cable Kickback',
    category: 'glutes',
    muscles: ['Glutes'],
    description: 'Isolation exercise for glute focus using cable machine.',
    tips: [
      'Keep core tight',
      'Dont swing - control the movement',
      'Squeeze at full extension',
    ],
    equipment: ['Cable Machine', 'Ankle Strap'],
    videoUrl: 'https://www.youtube.com/watch?v=KxI7i8TJdKs',
    affiliateProducts: [
      { name: 'Ankle Straps (Pair)', type: 'equipment', url: 'AFFILIATE_LINK_PLACEHOLDER', price: '$12.99' },
    ],
  },
  {
    id: 'rdl',
    name: 'Romanian Deadlift',
    category: 'glutes',
    muscles: ['Glutes', 'Hamstrings', 'Lower Back'],
    description: 'Hinge movement targeting posterior chain. Great for hamstrings and glutes.',
    tips: [
      'Keep bar close to legs',
      'Push hips back, slight knee bend',
      'Feel stretch in hamstrings',
      'Squeeze glutes to stand',
    ],
    equipment: ['Barbell', 'Dumbbells'],
    videoUrl: 'https://www.youtube.com/watch?v=JCXUYuzwNrM',
    affiliateProducts: [
      { name: 'Lifting Straps', type: 'equipment', url: 'AFFILIATE_LINK_PLACEHOLDER', price: '$9.99' },
    ],
  },
  {
    id: 'sumo-deadlift',
    name: 'Sumo Deadlift',
    category: 'glutes',
    muscles: ['Glutes', 'Inner Thighs', 'Quads'],
    description: 'Wide stance deadlift variation that targets glutes and inner thighs.',
    tips: [
      'Toes pointed out 45 degrees',
      'Push knees out over toes',
      'Keep chest up',
    ],
    equipment: ['Barbell'],
    videoUrl: 'https://www.youtube.com/watch?v=y1SD3bO2S0s',
  },
  {
    id: 'bulgarian-split-squat',
    name: 'Bulgarian Split Squat',
    category: 'glutes',
    muscles: ['Glutes', 'Quads', 'Hamstrings'],
    description: 'Single leg squat with rear foot elevated. Excellent for glute development.',
    tips: [
      'Lean torso slightly forward for more glute',
      'Keep front knee stable',
      'Control the descent',
    ],
    equipment: ['Bench', 'Dumbbells'],
    videoUrl: 'https://www.youtube.com/watch?v=2C-uNgKwPLE',
    affiliateProducts: [
      { name: 'Adjustable Dumbbells', type: 'equipment', url: 'AFFILIATE_LINK_PLACEHOLDER', price: '$149.99' },
    ],
  },
  {
    id: 'step-up',
    name: 'Step Up',
    category: 'glutes',
    muscles: ['Glutes', 'Quads'],
    description: 'Step onto elevated surface focusing on driving through front leg.',
    tips: [
      'Dont push off back foot',
      'Drive through heel of working leg',
      'Control the step down',
    ],
    equipment: ['Bench', 'Dumbbells'],
    videoUrl: 'https://www.youtube.com/watch?v=WCFCdxzFBa4',
  },
  {
    id: 'fire-hydrant',
    name: 'Fire Hydrant',
    category: 'glutes',
    muscles: ['Glute Medius', 'Glutes'],
    description: 'Quadruped hip abduction exercise targeting side glutes.',
    tips: [
      'Keep core engaged',
      'Lift from the hip, not back',
      'Pause at top',
    ],
    equipment: ['None', 'Resistance Band'],
    videoUrl: 'https://www.youtube.com/watch?v=La3xYT8MGks',
    affiliateProducts: [
      { name: 'Fabric Resistance Bands', type: 'equipment', url: 'AFFILIATE_LINK_PLACEHOLDER', price: '$16.99' },
    ],
  },
  {
    id: 'donkey-kick',
    name: 'Donkey Kick',
    category: 'glutes',
    muscles: ['Glutes'],
    description: 'Quadruped kickback targeting glutes.',
    tips: [
      'Keep core tight',
      'Dont arch lower back',
      'Squeeze glute at top',
    ],
    equipment: ['None', 'Resistance Band'],
    videoUrl: 'https://www.youtube.com/watch?v=9z0lG0-BDWQ',
  },
  {
    id: 'frog-pump',
    name: 'Frog Pump',
    category: 'glutes',
    muscles: ['Glutes'],
    description: 'Glute bridge variation with feet together, knees out.',
    tips: [
      'Keep soles of feet together',
      'Push knees out',
      'High reps work well',
    ],
    equipment: ['None'],
    videoUrl: 'https://www.youtube.com/watch?v=Jml6Fe0Gfxw',
  },
  {
    id: 'cable-pull-through',
    name: 'Cable Pull Through',
    category: 'glutes',
    muscles: ['Glutes', 'Hamstrings'],
    description: 'Hip hinge using cable for constant tension on glutes.',
    tips: [
      'Hinge at hips',
      'Keep arms straight',
      'Squeeze glutes to stand',
    ],
    equipment: ['Cable Machine'],
    videoUrl: 'https://www.youtube.com/watch?v=MzFI6pS3R24',
  },
  {
    id: 'banded-walk',
    name: 'Banded Walk',
    category: 'glutes',
    muscles: ['Glute Medius', 'Glutes'],
    description: 'Lateral walking with resistance band for glute activation.',
    tips: [
      'Keep tension in band',
      'Stay low in squat position',
      'Dont let knees cave',
    ],
    equipment: ['Resistance Band'],
    videoUrl: 'https://www.youtube.com/watch?v=R_6cj1WzXm0',
  },

  // LEGS (10)
  {
    id: 'squat',
    name: 'Squat',
    category: 'legs',
    muscles: ['Quads', 'Glutes', 'Hamstrings'],
    description: 'Fundamental lower body exercise. Barbell back squat.',
    tips: [
      'Keep chest up',
      'Knees track over toes',
      'Depth to parallel or below',
      'Drive through full foot',
    ],
    equipment: ['Barbell', 'Squat Rack'],
    videoUrl: 'https://www.youtube.com/watch?v=bEv6CCg2BC8',
    affiliateProducts: [
      { name: 'Weightlifting Belt', type: 'equipment', url: 'AFFILIATE_LINK_PLACEHOLDER', price: '$39.99' },
      { name: 'Knee Sleeves', type: 'equipment', url: 'AFFILIATE_LINK_PLACEHOLDER', price: '$29.99' },
    ],
  },
  {
    id: 'goblet-squat',
    name: 'Goblet Squat',
    category: 'legs',
    muscles: ['Quads', 'Glutes', 'Core'],
    description: 'Front-loaded squat holding dumbbell or kettlebell at chest.',
    tips: [
      'Hold weight at chest',
      'Elbows between knees at bottom',
      'Keep core tight',
    ],
    equipment: ['Dumbbell', 'Kettlebell'],
    videoUrl: 'https://www.youtube.com/watch?v=MeIiIdhvXT4',
  },
  {
    id: 'leg-press',
    name: 'Leg Press',
    category: 'legs',
    muscles: ['Quads', 'Glutes', 'Hamstrings'],
    description: 'Machine press for leg development with back support.',
    tips: [
      'Dont lock out knees',
      'Control the descent',
      'Foot placement affects muscle emphasis',
    ],
    equipment: ['Leg Press Machine'],
    videoUrl: 'https://www.youtube.com/watch?v=IZxyjW7MPJQ',
  },
  {
    id: 'leg-curl',
    name: 'Leg Curl',
    category: 'legs',
    muscles: ['Hamstrings'],
    description: 'Isolation exercise for hamstrings using curl machine.',
    tips: [
      'Dont lift hips off pad',
      'Control both directions',
      'Full range of motion',
    ],
    equipment: ['Leg Curl Machine'],
    videoUrl: 'https://www.youtube.com/watch?v=1Tq3QdYUuHs',
  },
  {
    id: 'leg-extension',
    name: 'Leg Extension',
    category: 'legs',
    muscles: ['Quads'],
    description: 'Quad isolation using extension machine.',
    tips: [
      'Squeeze at top',
      'Dont use momentum',
      'Control the negative',
    ],
    equipment: ['Leg Extension Machine'],
    videoUrl: 'https://www.youtube.com/watch?v=YyvSfVjQeL0',
  },
  {
    id: 'calf-raise',
    name: 'Calf Raise',
    category: 'legs',
    muscles: ['Calves'],
    description: 'Standing or seated calf raise for lower leg development.',
    tips: [
      'Full stretch at bottom',
      'Pause at top',
      'Slow and controlled',
    ],
    equipment: ['Calf Raise Machine', 'Smith Machine'],
    videoUrl: 'https://www.youtube.com/watch?v=-M4-G8p8fmc',
  },
  {
    id: 'lunge',
    name: 'Lunge',
    category: 'legs',
    muscles: ['Quads', 'Glutes', 'Hamstrings'],
    description: 'Alternating forward lunges for leg strength.',
    tips: [
      'Step far enough forward',
      'Keep torso upright',
      'Front knee over ankle',
    ],
    equipment: ['Dumbbells', 'None'],
    videoUrl: 'https://www.youtube.com/watch?v=QOVaHwm-Q6U',
  },
  {
    id: 'walking-lunge',
    name: 'Walking Lunge',
    category: 'legs',
    muscles: ['Quads', 'Glutes', 'Hamstrings'],
    description: 'Continuous forward lunging motion.',
    tips: [
      'Take controlled steps',
      'Drive through front heel',
      'Keep balance',
    ],
    equipment: ['Dumbbells', 'None'],
    videoUrl: 'https://www.youtube.com/watch?v=L8fvypPrzzs',
  },
  {
    id: 'wall-sit',
    name: 'Wall Sit',
    category: 'legs',
    muscles: ['Quads', 'Glutes'],
    description: 'Isometric hold against wall in squat position.',
    tips: [
      'Thighs parallel to floor',
      'Back flat against wall',
      'Hold for time',
    ],
    equipment: ['Wall'],
    videoUrl: 'https://www.youtube.com/watch?v=y-wV4Venusw',
  },
  {
    id: 'good-morning',
    name: 'Good Morning',
    category: 'legs',
    muscles: ['Hamstrings', 'Glutes', 'Lower Back'],
    description: 'Hip hinge with bar on back for posterior chain.',
    tips: [
      'Slight knee bend',
      'Push hips back',
      'Feel hamstring stretch',
    ],
    equipment: ['Barbell'],
    videoUrl: 'https://www.youtube.com/watch?v=vKPGe8zb2S4',
  },

  // ARMS (8)
  {
    id: 'bicep-curl',
    name: 'Bicep Curl',
    category: 'arms',
    muscles: ['Biceps'],
    description: 'Standard dumbbell curl for bicep development.',
    tips: [
      'Keep elbows at sides',
      'Dont swing',
      'Squeeze at top',
    ],
    equipment: ['Dumbbells', 'Barbell'],
    videoUrl: 'https://www.youtube.com/watch?v=ykJmrZ5v0Oo',
  },
  {
    id: 'hammer-curl',
    name: 'Hammer Curl',
    category: 'arms',
    muscles: ['Biceps', 'Forearms'],
    description: 'Neutral grip curl targeting biceps and forearms.',
    tips: [
      'Thumbs up grip',
      'Control the movement',
      'Keep elbows stable',
    ],
    equipment: ['Dumbbells'],
    videoUrl: 'https://www.youtube.com/watch?v=zC3nLlEvin4',
  },
  {
    id: 'tricep-pushdown',
    name: 'Tricep Pushdown',
    category: 'arms',
    muscles: ['Triceps'],
    description: 'Cable pushdown for tricep isolation.',
    tips: [
      'Keep elbows at sides',
      'Full extension at bottom',
      'Control the negative',
    ],
    equipment: ['Cable Machine'],
    videoUrl: 'https://www.youtube.com/watch?v=2-LAMcpzODU',
  },
  {
    id: 'tricep-dip',
    name: 'Tricep Dip',
    category: 'arms',
    muscles: ['Triceps', 'Chest', 'Shoulders'],
    description: 'Bodyweight dip on bench or parallel bars.',
    tips: [
      'Keep elbows close to body',
      'Lower with control',
      'Dont go too deep',
    ],
    equipment: ['Bench', 'Dip Station'],
    videoUrl: 'https://www.youtube.com/watch?v=6kALZikXxLc',
  },
  {
    id: 'overhead-tricep-extension',
    name: 'Overhead Tricep Extension',
    category: 'arms',
    muscles: ['Triceps'],
    description: 'Overhead extension for long head of tricep.',
    tips: [
      'Keep elbows pointed up',
      'Full stretch at bottom',
      'Dont flare elbows',
    ],
    equipment: ['Dumbbell', 'Cable'],
    videoUrl: 'https://www.youtube.com/watch?v=_gsUck-7M74',
  },
  {
    id: 'concentration-curl',
    name: 'Concentration Curl',
    category: 'arms',
    muscles: ['Biceps'],
    description: 'Seated single arm curl for bicep peak.',
    tips: [
      'Elbow braced on inner thigh',
      'Isolate the bicep',
      'Squeeze at top',
    ],
    equipment: ['Dumbbell'],
    videoUrl: 'https://www.youtube.com/watch?v=Jvj2wV0vOYU',
  },
  {
    id: 'cable-curl',
    name: 'Cable Curl',
    category: 'arms',
    muscles: ['Biceps'],
    description: 'Constant tension curl using cable machine.',
    tips: [
      'Keep tension throughout',
      'Dont lean back',
      'Control both directions',
    ],
    equipment: ['Cable Machine'],
    videoUrl: 'https://www.youtube.com/watch?v=NFzTWp2qpiE',
  },
  {
    id: 'skull-crusher',
    name: 'Skull Crusher',
    category: 'arms',
    muscles: ['Triceps'],
    description: 'Lying tricep extension with bar or dumbbells.',
    tips: [
      'Lower to forehead or behind head',
      'Keep elbows in',
      'Control the weight',
    ],
    equipment: ['Barbell', 'Dumbbells'],
    videoUrl: 'https://www.youtube.com/watch?v=d_KZxkY_0cM',
  },

  // BACK (6)
  {
    id: 'lat-pulldown',
    name: 'Lat Pulldown',
    category: 'back',
    muscles: ['Lats', 'Biceps', 'Rear Delts'],
    description: 'Cable pulldown targeting the lats.',
    tips: [
      'Pull to upper chest',
      'Squeeze shoulder blades',
      'Control the negative',
    ],
    equipment: ['Cable Machine'],
    videoUrl: 'https://www.youtube.com/watch?v=CAwf7n6Luuc',
  },
  {
    id: 'seated-row',
    name: 'Seated Row',
    category: 'back',
    muscles: ['Lats', 'Rhomboids', 'Biceps'],
    description: 'Cable row for mid-back development.',
    tips: [
      'Pull to stomach',
      'Squeeze at end',
      'Dont lean too far back',
    ],
    equipment: ['Cable Machine'],
    videoUrl: 'https://www.youtube.com/watch?v=GZbfZ033f74',
  },
  {
    id: 'bent-over-row',
    name: 'Bent Over Row',
    category: 'back',
    muscles: ['Lats', 'Rhomboids', 'Biceps'],
    description: 'Free weight row in bent over position.',
    tips: [
      'Keep back flat',
      'Pull to hip',
      'Control the weight',
    ],
    equipment: ['Barbell', 'Dumbbells'],
    videoUrl: 'https://www.youtube.com/watch?v=FWJR5Ve8bnQ',
  },
  {
    id: 'face-pull',
    name: 'Face Pull',
    category: 'back',
    muscles: ['Rear Delts', 'Rhomboids', 'Rotator Cuff'],
    description: 'Cable exercise for rear delts and upper back.',
    tips: [
      'Pull to face level',
      'Elbows high',
      'Squeeze shoulder blades',
    ],
    equipment: ['Cable Machine', 'Rope Attachment'],
    videoUrl: 'https://www.youtube.com/watch?v=rep-qVOkqgk',
  },
  {
    id: 'single-arm-row',
    name: 'Single Arm Row',
    category: 'back',
    muscles: ['Lats', 'Rhomboids', 'Biceps'],
    description: 'Dumbbell row with one arm at a time.',
    tips: [
      'Keep back flat',
      'Pull to hip',
      'Full stretch at bottom',
    ],
    equipment: ['Dumbbell', 'Bench'],
    videoUrl: 'https://www.youtube.com/watch?v=roCP6wCXPqo',
  },
  {
    id: 'pull-up',
    name: 'Pull Up',
    category: 'back',
    muscles: ['Lats', 'Biceps', 'Core'],
    description: 'Bodyweight pulling movement. Use assisted if needed.',
    tips: [
      'Full hang at bottom',
      'Chin over bar at top',
      'Control the descent',
    ],
    equipment: ['Pull Up Bar', 'Assisted Machine'],
    videoUrl: 'https://www.youtube.com/watch?v=eGo4IYlbE5g',
  },

  // CHEST (4)
  {
    id: 'bench-press',
    name: 'Bench Press',
    category: 'chest',
    muscles: ['Chest', 'Shoulders', 'Triceps'],
    description: 'Fundamental pushing exercise for chest.',
    tips: [
      'Feet flat on floor',
      'Arch upper back slightly',
      'Touch chest, press up',
    ],
    equipment: ['Barbell', 'Bench'],
    videoUrl: 'https://www.youtube.com/watch?v=4Y2ZdHCOXok',
    affiliateProducts: [
      { name: 'Wrist Wraps', type: 'equipment', url: 'AFFILIATE_LINK_PLACEHOLDER', price: '$15.99' },
    ],
  },
  {
    id: 'incline-press',
    name: 'Incline Press',
    category: 'chest',
    muscles: ['Upper Chest', 'Shoulders', 'Triceps'],
    description: 'Angled bench press for upper chest emphasis.',
    tips: [
      'Bench at 30-45 degrees',
      'Press up and slightly back',
      'Control the weight',
    ],
    equipment: ['Barbell', 'Dumbbells', 'Bench'],
    videoUrl: 'https://www.youtube.com/watch?v=SrqOu55lrYU',
  },
  {
    id: 'chest-fly',
    name: 'Chest Fly',
    category: 'chest',
    muscles: ['Chest'],
    description: 'Isolation movement for chest stretch and squeeze.',
    tips: [
      'Slight bend in elbows',
      'Feel stretch at bottom',
      'Squeeze chest at top',
    ],
    equipment: ['Dumbbells', 'Cable Machine'],
    videoUrl: 'https://www.youtube.com/watch?v=eozdVDA78K0',
  },
  {
    id: 'push-up',
    name: 'Push Up',
    category: 'chest',
    muscles: ['Chest', 'Shoulders', 'Triceps', 'Core'],
    description: 'Bodyweight pushing exercise.',
    tips: [
      'Body in straight line',
      'Chest to floor',
      'Full lockout at top',
    ],
    equipment: ['None'],
    videoUrl: 'https://www.youtube.com/watch?v=IODxDxX7oi4',
  },

  // SHOULDERS (5)
  {
    id: 'shoulder-press',
    name: 'Shoulder Press',
    category: 'shoulders',
    muscles: ['Shoulders', 'Triceps'],
    description: 'Overhead pressing movement for shoulder development.',
    tips: [
      'Keep core tight',
      'Press straight up',
      'Dont arch lower back',
    ],
    equipment: ['Dumbbells', 'Barbell'],
    videoUrl: 'https://www.youtube.com/watch?v=qEwKCR5JCog',
  },
  {
    id: 'lateral-raise',
    name: 'Lateral Raise',
    category: 'shoulders',
    muscles: ['Side Delts'],
    description: 'Side raise for lateral delt development.',
    tips: [
      'Slight bend in elbows',
      'Raise to shoulder height',
      'Control the weight',
    ],
    equipment: ['Dumbbells', 'Cable'],
    videoUrl: 'https://www.youtube.com/watch?v=3VcKaXpzqRo',
  },
  {
    id: 'front-raise',
    name: 'Front Raise',
    category: 'shoulders',
    muscles: ['Front Delts'],
    description: 'Front raise for anterior deltoid.',
    tips: [
      'Raise to eye level',
      'Dont swing',
      'Alternate or together',
    ],
    equipment: ['Dumbbells', 'Barbell'],
    videoUrl: 'https://www.youtube.com/watch?v=-t7fuZ0KhDA',
  },
  {
    id: 'rear-delt-fly',
    name: 'Rear Delt Fly',
    category: 'shoulders',
    muscles: ['Rear Delts'],
    description: 'Bent over fly for rear deltoid development.',
    tips: [
      'Bend at hips',
      'Elbows slightly bent',
      'Squeeze at top',
    ],
    equipment: ['Dumbbells', 'Cable'],
    videoUrl: 'https://www.youtube.com/watch?v=EA7u4Q_8HQ0',
  },
  {
    id: 'arnold-press',
    name: 'Arnold Press',
    category: 'shoulders',
    muscles: ['Shoulders'],
    description: 'Rotating press hitting all three heads of deltoid.',
    tips: [
      'Start palms facing you',
      'Rotate as you press',
      'Full rotation at top',
    ],
    equipment: ['Dumbbells'],
    videoUrl: 'https://www.youtube.com/watch?v=6Z15_WdXmVw',
  },

  // CORE (5)
  {
    id: 'plank',
    name: 'Plank',
    category: 'core',
    muscles: ['Core', 'Shoulders'],
    description: 'Isometric hold for core stability.',
    tips: [
      'Body in straight line',
      'Dont let hips sag',
      'Squeeze glutes and core',
    ],
    equipment: ['None'],
    videoUrl: 'https://www.youtube.com/watch?v=pSHjTRCQxIw',
    affiliateProducts: [
      { name: 'Exercise Mat', type: 'equipment', url: 'AFFILIATE_LINK_PLACEHOLDER', price: '$24.99' },
    ],
  },
  {
    id: 'crunch',
    name: 'Crunch',
    category: 'core',
    muscles: ['Abs'],
    description: 'Basic ab crunch for rectus abdominis.',
    tips: [
      'Curl shoulders off floor',
      'Dont pull on neck',
      'Exhale at top',
    ],
    equipment: ['None'],
    videoUrl: 'https://www.youtube.com/watch?v=5ER5Of4MOPI',
  },
  {
    id: 'russian-twist',
    name: 'Russian Twist',
    category: 'core',
    muscles: ['Obliques', 'Abs'],
    description: 'Seated rotation for obliques.',
    tips: [
      'Lean back slightly',
      'Rotate from core, not arms',
      'Touch floor each side',
    ],
    equipment: ['None', 'Medicine Ball'],
    videoUrl: 'https://www.youtube.com/watch?v=wkD8rjkodUI',
  },
  {
    id: 'leg-raise',
    name: 'Leg Raise',
    category: 'core',
    muscles: ['Lower Abs', 'Hip Flexors'],
    description: 'Lying or hanging leg raise for lower abs.',
    tips: [
      'Keep legs straight or slightly bent',
      'Control the descent',
      'Press lower back into floor',
    ],
    equipment: ['None', 'Pull Up Bar'],
    videoUrl: 'https://www.youtube.com/watch?v=JB2oyawG9KI',
  },
  {
    id: 'dead-bug',
    name: 'Dead Bug',
    category: 'core',
    muscles: ['Core', 'Abs'],
    description: 'Anti-extension exercise for core stability.',
    tips: [
      'Keep lower back pressed down',
      'Move opposite arm and leg',
      'Breathe throughout',
    ],
    equipment: ['None'],
    videoUrl: 'https://www.youtube.com/watch?v=I5xbsA71v1A',
  },
];

// Grouped by category for easy access
export const exercisesByCategory = exercises.reduce((acc, exercise) => {
  if (!acc[exercise.category]) {
    acc[exercise.category] = [];
  }
  acc[exercise.category].push(exercise);
  return acc;
}, {} as Record<MuscleGroup, Exercise[]>);

export const categoryLabels: Record<MuscleGroup, string> = {
  glutes: 'Glutes',
  legs: 'Legs',
  arms: 'Arms',
  back: 'Back',
  chest: 'Chest',
  shoulders: 'Shoulders',
  core: 'Core',
};

export const categoryColors: Record<MuscleGroup, string> = {
  glutes: '#FF7B7B',
  legs: '#B8A9C9',
  arms: '#98D7C2',
  back: '#FFB366',
  chest: '#7BC47F',
  shoulders: '#FF9999',
  core: '#99D6FF',
};
