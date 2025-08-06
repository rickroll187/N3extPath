// File: web/src/utils/cn.ts
/**
 * 🔧🎸 N3EXTPATH - LEGENDARY CLASSNAME UTILITY 🎸🔧
 * Professional class name merging with Swiss precision
 * Built: 2025-08-06 13:34:22 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * 🎸 LEGENDARY CLASS NAME MERGER
 * Combines clsx and tailwind-merge for ultimate class name handling
 * with Swiss precision and code bro energy!
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

console.log('🎸 LEGENDARY CLASSNAME UTILITY LOADED!');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`CN utility loaded at: 2025-08-06 13:34:22 UTC`);
