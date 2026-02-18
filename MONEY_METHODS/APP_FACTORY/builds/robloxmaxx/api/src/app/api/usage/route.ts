import { NextRequest, NextResponse } from 'next/server';
import { authenticateRequest } from '@/services/auth';
import { getUserById, getDb } from '@/services/db';

export async function GET(request: NextRequest) {
  const token = request.headers.get('authorization')?.replace('Bearer ', '');

  if (!token) {
    return NextResponse.json({ error: 'No token' }, { status: 401 });
  }

  const auth = authenticateRequest(token);
  if (!auth) {
    return NextResponse.json({ error: 'Invalid token' }, { status: 401 });
  }

  const user = getUserById(auth.userId);
  if (!user) {
    return NextResponse.json({ error: 'User not found' }, { status: 404 });
  }

  // Get usage stats from usage_log (analytics only, no limits)
  const db = getDb();
  const totalActions = db.prepare(
    'SELECT COUNT(*) as count FROM usage_log WHERE user_id = ?'
  ).get(auth.userId) as { count: number } | undefined;

  const thisMonthActions = db.prepare(
    `SELECT COUNT(*) as count FROM usage_log
     WHERE user_id = ? AND created_at >= date('now', 'start of month')`
  ).get(auth.userId) as { count: number } | undefined;

  return NextResponse.json({
    plan: user.plan,
    model: 'byok',
    totalActions: totalActions?.count || 0,
    thisMonthActions: thisMonthActions?.count || 0,
    note: 'BYOK model - no action limits. You control your API costs.',
  });
}
