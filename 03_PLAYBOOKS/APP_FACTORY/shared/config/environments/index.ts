/**
 * Environment configuration index
 *
 * Exports environment detection and environment-specific configs
 */

export type Environment = 'development' | 'staging' | 'production';

/**
 * Detect current environment
 *
 * Priority:
 * 1. Explicit APP_ENV environment variable
 * 2. React Native __DEV__ global
 * 3. NODE_ENV environment variable
 * 4. Default to development
 */
export function getEnvironment(): Environment {
  // Check explicit APP_ENV first (set via react-native-config)
  const appEnv = process.env.APP_ENV as Environment | undefined;
  if (appEnv && isValidEnvironment(appEnv)) {
    return appEnv;
  }

  // Check React Native __DEV__ global
  if (typeof __DEV__ !== 'undefined') {
    return __DEV__ ? 'development' : 'production';
  }

  // Check NODE_ENV
  const nodeEnv = process.env.NODE_ENV;
  if (nodeEnv === 'production') {
    return 'production';
  }
  if (nodeEnv === 'staging' || nodeEnv === 'test') {
    return 'staging';
  }

  // Default to development
  return 'development';
}

/**
 * Validate environment string
 */
function isValidEnvironment(env: string): env is Environment {
  return ['development', 'staging', 'production'].includes(env);
}

/**
 * Re-export environment-specific configs
 */
export { developmentConfig } from './development';
export { stagingConfig } from './staging';
export { productionConfig } from './production';

/**
 * Get config for a specific environment
 */
export function getEnvironmentConfig(env: Environment) {
  switch (env) {
    case 'development':
      return require('./development').developmentConfig;
    case 'staging':
      return require('./staging').stagingConfig;
    case 'production':
      return require('./production').productionConfig;
    default:
      return require('./development').developmentConfig;
  }
}
