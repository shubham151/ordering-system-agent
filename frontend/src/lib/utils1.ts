import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Utility function to merge Tailwind CSS classes
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Format order items for display
 */
export function formatOrderItems(order: {
  burgers: number;
  fries: number;
  drinks: number;
}): string {
  const items = [];
  if (order.burgers > 0) {
    items.push(`${order.burgers} burger${order.burgers !== 1 ? "s" : ""}`);
  }
  if (order.fries > 0) {
    items.push(`${order.fries} order${order.fries !== 1 ? "s" : ""} of fries`);
  }
  if (order.drinks > 0) {
    items.push(`${order.drinks} drink${order.drinks !== 1 ? "s" : ""}`);
  }
  return items.join(", ") || "Empty order";
}

/**
 * Debounce function for input handling (browser-compatible)
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: number; // Use number instead of NodeJS.Timeout for browser compatibility
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait) as unknown as number;
  };
}

/**
 * Alternative debounce using ReturnType<typeof setTimeout>
 */
export function debounceAlt<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: ReturnType<typeof setTimeout>;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

/**
 * Format relative time
 */
export function formatRelativeTime(date: Date): string {
  const now = new Date();
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  if (diffInSeconds < 60) {
    return "Just now";
  } else if (diffInSeconds < 3600) {
    const minutes = Math.floor(diffInSeconds / 60);
    return `${minutes} minute${minutes !== 1 ? "s" : ""} ago`;
  } else if (diffInSeconds < 86400) {
    const hours = Math.floor(diffInSeconds / 3600);
    return `${hours} hour${hours !== 1 ? "s" : ""} ago`;
  } else {
    const days = Math.floor(diffInSeconds / 86400);
    return `${days} day${days !== 1 ? "s" : ""} ago`;
  }
}

/**
 * Validate message input
 */
export function validateMessage(message: string): {
  isValid: boolean;
  error?: string;
} {
  const trimmed = message.trim();

  if (!trimmed) {
    return { isValid: false, error: "Message cannot be empty" };
  }

  if (trimmed.length > 500) {
    return {
      isValid: false,
      error: "Message is too long (max 500 characters)",
    };
  }

  return { isValid: true };
}

/**
 * Sleep utility for async operations
 */
export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Generate order examples for placeholder
 */
export function getOrderExamples(): string[] {
  return [
    "I want 2 burgers and 3 fries",
    "Can I get a burger and a drink?",
    "My friend and I each want fries",
    "Cancel order #3",
    "One of everything please",
    "3 burgers, 2 fries, and 4 drinks",
  ];
}

/**
 * Get random order example
 */
export function getRandomOrderExample(): string {
  const examples = getOrderExamples();
  return examples[Math.floor(Math.random() * examples.length)];
}

/**
 * Format currency (for future use)
 */
export function formatCurrency(amount: number, currency = "USD"): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: currency,
  }).format(amount);
}

/**
 * Truncate text with ellipsis
 */
export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + "...";
}

/**
 * Check if running in browser
 */
export function isBrowser(): boolean {
  return typeof window !== "undefined";
}

/**
 * Safe JSON parse with fallback
 */
export function safeJsonParse<T>(json: string, fallback: T): T {
  try {
    return JSON.parse(json);
  } catch {
    return fallback;
  }
}

/**
 * Generate unique ID
 */
export function generateId(): string {
  return Math.random().toString(36).substring(2) + Date.now().toString(36);
}

/**
 * Throttle function (alternative to debounce)
 */
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean;
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}
