import { NextRequest, NextResponse } from 'next/server';

const CONVERSION_RATES: Record<string, number> = {
  simulator: 0.05,
  tycoon: 0.03,
  obby: 0.02,
  rpg: 0.04,
  horror: 0.01,
  fps: 0.03,
  social: 0.06,
  survival: 0.025,
  general: 0.03,
};

const AVG_TRANSACTION_ROBUX = 150;
const ROBLOX_DEVELOPER_SHARE = 0.70;
const DEVEX_RATE = 0.0038; // USD per Robux at DevEx

interface EstimateRequest {
  genre: string;
  expected_dau: number;
  has_gamepasses: boolean;
  has_devproducts: boolean;
  has_ads: boolean;
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const {
      genre,
      expected_dau,
      has_gamepasses,
      has_devproducts,
      has_ads,
    } = body as EstimateRequest;

    // Validate inputs
    if (!genre || typeof genre !== 'string') {
      return NextResponse.json(
        { error: 'genre is required and must be a string' },
        { status: 400 }
      );
    }

    if (
      expected_dau === undefined ||
      typeof expected_dau !== 'number' ||
      expected_dau < 0
    ) {
      return NextResponse.json(
        { error: 'expected_dau is required and must be a non-negative number' },
        { status: 400 }
      );
    }

    // Cap DAU at 1M for sanity
    const dau = Math.min(Math.floor(expected_dau), 1000000);

    const conversionRate =
      CONVERSION_RATES[genre.toLowerCase()] || CONVERSION_RATES.general;

    // Monetization multiplier
    let totalMultiplier = 0;
    const breakdownParts: Record<string, number> = {};

    if (has_gamepasses) {
      totalMultiplier += 1.0;
      breakdownParts.gamepasses = 1.0;
    }
    if (has_devproducts) {
      totalMultiplier += 0.5;
      breakdownParts.devproducts = 0.5;
    }
    if (has_ads) {
      totalMultiplier += 0.3;
      breakdownParts.ads = 0.3;
    }

    // Default to at least gamepasses if nothing selected
    if (totalMultiplier === 0) {
      totalMultiplier = 1.0;
      breakdownParts.gamepasses = 1.0;
    }

    // Monthly Robux from direct monetization
    const baseMonthlyRobux =
      dau * conversionRate * AVG_TRANSACTION_ROBUX * 30 * totalMultiplier;

    // Monthly USD from direct monetization (after Roblox cut + DevEx)
    const baseMonthlyUsd =
      baseMonthlyRobux * ROBLOX_DEVELOPER_SHARE * DEVEX_RATE;

    // Creator Rewards estimate (engagement-based payout)
    // ~2% of DAU are active spenders, ~5 Robux equivalent per active spender per day
    const creatorRewardsUsd = dau * 0.02 * 5 * 30 * DEVEX_RATE;

    // Build ranges
    const monthlyRobux = {
      low: Math.round(baseMonthlyRobux * 0.5),
      mid: Math.round(baseMonthlyRobux),
      high: Math.round(baseMonthlyRobux * 2.0),
    };

    const monthlyUsd = {
      low: round2(baseMonthlyUsd * 0.5),
      mid: round2(baseMonthlyUsd),
      high: round2(baseMonthlyUsd * 2.0),
    };

    const totalMonthlyUsd = {
      low: round2(monthlyUsd.low + creatorRewardsUsd),
      mid: round2(monthlyUsd.mid + creatorRewardsUsd),
      high: round2(monthlyUsd.high + creatorRewardsUsd),
    };

    // Calculate breakdown percentages
    const totalParts =
      Object.values(breakdownParts).reduce((a, b) => a + b, 0) +
      (creatorRewardsUsd > 0 ? 0.2 : 0);

    const breakdown: Record<string, string> = {};
    for (const [key, val] of Object.entries(breakdownParts)) {
      breakdown[key] = Math.round((val / (totalParts || 1)) * 100) + '%';
    }
    if (creatorRewardsUsd > 0) {
      breakdown.creator_rewards =
        Math.round((0.2 / (totalParts || 1)) * 100) + '%';
    }

    return NextResponse.json({
      monthly_robux: monthlyRobux,
      monthly_usd: monthlyUsd,
      creator_rewards_usd: round2(creatorRewardsUsd),
      total_monthly_usd: totalMonthlyUsd,
      breakdown,
      genre: genre.toLowerCase(),
      dau,
    });
  } catch (error) {
    console.error('[/api/estimate-revenue] Error:', error);
    return NextResponse.json(
      { error: 'Revenue estimation failed. Check your inputs.' },
      { status: 500 }
    );
  }
}

function round2(n: number): number {
  return Math.round(n * 100) / 100;
}
