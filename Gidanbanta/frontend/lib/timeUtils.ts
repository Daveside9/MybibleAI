/**
 * Time Utilities for Match Scheduling
 * Handles timezone conversion and locale-aware time formatting
 */

/**
 * Detect user's timezone
 */
export function getUserTimezone(): string {
  return Intl.DateTimeFormat().resolvedOptions().timeZone;
}

/**
 * Detect user's locale
 */
export function getUserLocale(): string {
  if (typeof navigator !== 'undefined') {
    return navigator.language || 'en-US';
  }
  return 'en-US';
}

/**
 * Check if user prefers 24-hour format based on locale
 */
export function prefers24HourFormat(): boolean {
  const locale = getUserLocale();
  const testDate = new Date(2000, 0, 1, 13, 0, 0);
  const formatted = testDate.toLocaleTimeString(locale, { hour: 'numeric' });
  return formatted.includes('13');
}

/**
 * Format match time in user's local timezone
 * Automatically uses 12-hour or 24-hour format based on locale
 */
export function formatMatchTime(dateString: string): string {
  const date = new Date(dateString);
  const locale = getUserLocale();
  const use24Hour = prefers24HourFormat();
  
  return date.toLocaleTimeString(locale, {
    hour: '2-digit',
    minute: '2-digit',
    hour12: !use24Hour
  });
}

/**
 * Format match date in user's locale
 */
export function formatMatchDate(dateString: string, options?: Intl.DateTimeFormatOptions): string {
  const date = new Date(dateString);
  const locale = getUserLocale();
  
  const defaultOptions: Intl.DateTimeFormatOptions = {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    ...options
  };
  
  return date.toLocaleDateString(locale, defaultOptions);
}

/**
 * Format match date and time together
 */
export function formatMatchDateTime(dateString: string): string {
  const date = new Date(dateString);
  const locale = getUserLocale();
  const use24Hour = prefers24HourFormat();
  
  return date.toLocaleString(locale, {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: !use24Hour
  });
}

/**
 * Get relative time (e.g., "in 2 hours", "5 minutes ago")
 */
export function getRelativeTime(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = date.getTime() - now.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);
  
  if (diffMins < -60) {
    if (diffHours < -24) {
      return `${Math.abs(diffDays)} day${Math.abs(diffDays) !== 1 ? 's' : ''} ago`;
    }
    return `${Math.abs(diffHours)} hour${Math.abs(diffHours) !== 1 ? 's' : ''} ago`;
  } else if (diffMins < 0) {
    return `${Math.abs(diffMins)} minute${Math.abs(diffMins) !== 1 ? 's' : ''} ago`;
  } else if (diffMins < 60) {
    return `in ${diffMins} minute${diffMins !== 1 ? 's' : ''}`;
  } else if (diffHours < 24) {
    return `in ${diffHours} hour${diffHours !== 1 ? 's' : ''}`;
  } else {
    return `in ${diffDays} day${diffDays !== 1 ? 's' : ''}`;
  }
}

/**
 * Check if a match is happening today
 */
export function isToday(dateString: string): boolean {
  const date = new Date(dateString);
  const today = new Date();
  
  return date.getDate() === today.getDate() &&
         date.getMonth() === today.getMonth() &&
         date.getFullYear() === today.getFullYear();
}

/**
 * Check if a match is happening tomorrow
 */
export function isTomorrow(dateString: string): boolean {
  const date = new Date(dateString);
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  
  return date.getDate() === tomorrow.getDate() &&
         date.getMonth() === tomorrow.getMonth() &&
         date.getFullYear() === tomorrow.getFullYear();
}

/**
 * Get user-friendly date label (Today, Tomorrow, or formatted date)
 */
export function getFriendlyDateLabel(dateString: string): string {
  if (isToday(dateString)) {
    return 'Today';
  }
  if (isTomorrow(dateString)) {
    return 'Tomorrow';
  }
  return formatMatchDate(dateString, { weekday: 'long', month: 'long', day: 'numeric' });
}

/**
 * Convert UTC time to user's local timezone and format
 */
export function convertUTCToLocal(utcDateString: string): Date {
  return new Date(utcDateString);
}

/**
 * Get timezone abbreviation (e.g., "PST", "EST", "GMT")
 */
export function getTimezoneAbbreviation(): string {
  const date = new Date();
  const timeZoneString = date.toLocaleTimeString('en-US', { timeZoneName: 'short' });
  const parts = timeZoneString.split(' ');
  return parts[parts.length - 1];
}

/**
 * Format time with timezone info
 */
export function formatTimeWithTimezone(dateString: string): string {
  const time = formatMatchTime(dateString);
  const tz = getTimezoneAbbreviation();
  return `${time} ${tz}`;
}
