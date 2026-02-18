import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import crypto from 'crypto';
import { createUser, getUserByEmail, getUserByApiKey, createApiKey } from './db';

const JWT_SECRET = process.env.JWT_SECRET || 'change-me-in-production';

export interface AuthPayload {
  userId: number;
  email: string;
}

export function hashPassword(password: string): string {
  return bcrypt.hashSync(password, 10);
}

export function verifyPassword(password: string, hash: string): boolean {
  return bcrypt.compareSync(password, hash);
}

export function generateToken(payload: AuthPayload): string {
  return jwt.sign(payload, JWT_SECRET, { expiresIn: '30d' });
}

export function verifyToken(token: string): AuthPayload | null {
  try {
    return jwt.verify(token, JWT_SECRET) as AuthPayload;
  } catch {
    return null;
  }
}

export function generateApiKey(): string {
  return 'rmx_' + crypto.randomBytes(32).toString('hex');
}

export async function registerUser(email: string, password: string) {
  const existing = getUserByEmail(email);
  if (existing) {
    throw new Error('Email already registered');
  }

  const hash = hashPassword(password);
  const result = createUser(email, hash);
  const userId = result.lastInsertRowid as number;

  // Generate default API key
  const key = generateApiKey();
  createApiKey(userId, key, 'Default');

  const token = generateToken({ userId, email });
  return { token, apiKey: key, userId };
}

export async function loginUser(email: string, password: string) {
  const user = getUserByEmail(email);
  if (!user) {
    throw new Error('Invalid credentials');
  }

  if (!verifyPassword(password, user.password_hash as string)) {
    throw new Error('Invalid credentials');
  }

  const token = generateToken({
    userId: user.id as number,
    email: user.email as string,
  });
  return { token, userId: user.id };
}

export function authenticateRequest(
  tokenOrApiKey: string
): { userId: number; email: string } | null {
  // Try JWT token first
  const jwtPayload = verifyToken(tokenOrApiKey);
  if (jwtPayload) return jwtPayload;

  // Try API key
  if (tokenOrApiKey.startsWith('rmx_')) {
    const user = getUserByApiKey(tokenOrApiKey);
    if (user) {
      return {
        userId: user.id as number,
        email: user.email as string,
      };
    }
  }

  return null;
}
