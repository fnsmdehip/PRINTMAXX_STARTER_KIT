import AsyncStorage from '@react-native-async-storage/async-storage';

export interface SalahTimes {
  fajr: string;
  sunrise: string;
  dhuhr: string;
  asr: string;
  maghrib: string;
  isha: string;
}

export type SalahName = 'fajr' | 'dhuhr' | 'asr' | 'maghrib' | 'isha';

export type CalculationMethod = 'MWL' | 'ISNA' | 'Egypt' | 'Makkah' | 'Karachi';

export type Madhab = 'Shafi' | 'Hanafi';

const METHOD_CODES: Record<CalculationMethod, number> = {
  MWL: 3,
  ISNA: 2,
  Egypt: 5,
  Makkah: 4,
  Karachi: 1,
};

const MADHAB_CODES: Record<Madhab, number> = {
  Shafi: 0,
  Hanafi: 1,
};

const SALAH_CACHE_KEY = '@prayerlock_salah_times';
const SALAH_CACHE_DATE_KEY = '@prayerlock_salah_cache_date';

export const SALAH_PRAYERS: { name: SalahName; displayName: string; defaultMinutes: number }[] = [
  { name: 'fajr', displayName: 'Fajr', defaultMinutes: 3 },
  { name: 'dhuhr', displayName: 'Dhuhr', defaultMinutes: 5 },
  { name: 'asr', displayName: 'Asr', defaultMinutes: 5 },
  { name: 'maghrib', displayName: 'Maghrib', defaultMinutes: 4 },
  { name: 'isha', displayName: 'Isha', defaultMinutes: 6 },
];

export async function fetchSalahTimes(
  city: string,
  country: string,
  method: CalculationMethod = 'ISNA',
  madhab: Madhab = 'Shafi'
): Promise<SalahTimes | null> {
  try {
    const today = new Date();
    const dateStr = today.toISOString().split('T')[0];

    const cachedDate = await AsyncStorage.getItem(SALAH_CACHE_DATE_KEY);
    if (cachedDate === dateStr) {
      const cached = await AsyncStorage.getItem(SALAH_CACHE_KEY);
      if (cached) {
        return JSON.parse(cached);
      }
    }

    const methodCode = METHOD_CODES[method];
    const madhabCode = MADHAB_CODES[madhab];
    const url = `https://api.aladhan.com/v1/timingsByCity/${dateStr}?city=${encodeURIComponent(city)}&country=${encodeURIComponent(country)}&method=${methodCode}&school=${madhabCode}`;

    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`API returned ${response.status}`);
    }

    const data = await response.json();
    const timings = data.data.timings;

    const salahTimes: SalahTimes = {
      fajr: timings.Fajr,
      sunrise: timings.Sunrise,
      dhuhr: timings.Dhuhr,
      asr: timings.Asr,
      maghrib: timings.Maghrib,
      isha: timings.Isha,
    };

    await AsyncStorage.setItem(SALAH_CACHE_KEY, JSON.stringify(salahTimes));
    await AsyncStorage.setItem(SALAH_CACHE_DATE_KEY, dateStr);

    return salahTimes;
  } catch (error) {
    const cached = await AsyncStorage.getItem(SALAH_CACHE_KEY);
    if (cached) {
      return JSON.parse(cached);
    }
    return null;
  }
}

export function getNextSalah(times: SalahTimes): { name: SalahName; time: string } | null {
  const now = new Date();
  const currentMinutes = now.getHours() * 60 + now.getMinutes();

  for (const prayer of SALAH_PRAYERS) {
    const timeStr = times[prayer.name];
    const [hours, minutes] = timeStr.split(':').map(Number);
    const prayerMinutes = hours * 60 + minutes;

    if (prayerMinutes > currentMinutes) {
      return { name: prayer.name, time: timeStr };
    }
  }

  return { name: 'fajr', time: times.fajr };
}

export function getMinutesUntilSalah(salahTime: string): number {
  const now = new Date();
  const currentMinutes = now.getHours() * 60 + now.getMinutes();
  const [hours, minutes] = salahTime.split(':').map(Number);
  const targetMinutes = hours * 60 + minutes;

  if (targetMinutes > currentMinutes) {
    return targetMinutes - currentMinutes;
  }
  return (24 * 60 - currentMinutes) + targetMinutes;
}

export function formatSalahTime(time24: string): string {
  const [hours, minutes] = time24.split(':').map(Number);
  const period = hours >= 12 ? 'PM' : 'AM';
  const hours12 = hours % 12 || 12;
  return `${hours12}:${minutes.toString().padStart(2, '0')} ${period}`;
}

export function autoDetectMethod(country: string): CalculationMethod {
  const usCanada = ['US', 'CA', 'United States', 'Canada'];
  const middleEast = ['SA', 'AE', 'KW', 'QA', 'BH', 'OM', 'Saudi Arabia', 'UAE'];
  const southAsia = ['PK', 'IN', 'BD', 'Pakistan', 'India', 'Bangladesh'];
  const africa = ['EG', 'Egypt', 'Libya', 'Sudan'];

  if (usCanada.includes(country)) return 'ISNA';
  if (middleEast.includes(country)) return 'Makkah';
  if (southAsia.includes(country)) return 'Karachi';
  if (africa.includes(country)) return 'Egypt';
  return 'MWL';
}
