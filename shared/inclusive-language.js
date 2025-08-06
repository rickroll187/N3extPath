// File: shared/constants/inclusive-language.js
/**
 * 🌈🎸 N3EXTPATH - INCLUSIVE LANGUAGE CONSTANTS 🎸🌈
 * Universal inclusivity with infinite respect for all
 * Built: 2025-08-06 18:08:08 UTC by RICKROLL187
 * BIAS ELIMINATION - WELCOMING ALL CODE CREATORS!
 */

// Inclusive terminology replacements
const INCLUSIVE_TERMS = {
  // Gender-neutral alternatives
  'code bro': 'code creator', // More inclusive than "bro"
  'legendary': 'exceptional', // Less hierarchical
  'infinite energy': 'high engagement', // More ability-inclusive
  
  // Cultural neutrality
  'swiss precision': 'meticulous quality',
  'legendary founder': 'platform founder',
  
  // Achievement language
  'legendary user': 'highly engaged user',
  'legendary team': 'high-performing team',
  'legendary okr': 'exceptional objective'
};

// Inclusive user roles and descriptions
const INCLUSIVE_ROLES = {
  founder: {
    name: 'Platform Founder',
    description: 'Platform creator with full administrative access',
    pronouns_neutral: true
  },
  admin: {
    name: 'Administrator', 
    description: 'System administrator with management privileges',
    pronouns_neutral: true
  },
  moderator: {
    name: 'Community Moderator',
    description: 'Community guide helping maintain positive environment',
    pronouns_neutral: true
  },
  user: {
    name: 'Team Member',
    description: 'Valued contributor to the platform community',
    pronouns_neutral: true
  }
};

// Inclusive achievement system
const INCLUSIVE_ACHIEVEMENTS = {
  // Remove hierarchical "legendary" system
  // Replace with skill-based recognition
  achievements: {
    'okr-completer': {
      name: 'Goal Achiever',
      description: 'Completed multiple objectives successfully',
      criteria: 'Complete 5 OKRs with >90% progress'
    },
    'team-collaborator': {
      name: 'Team Collaborator', 
      description: 'Active contributor to team success',
      criteria: 'Participate in 10+ team discussions'
    },
    'mentor': {
      name: 'Community Mentor',
      description: 'Helps others achieve their goals',
      criteria: 'Help 5+ team members with their OKRs'
    },
    'innovator': {
      name: 'Creative Problem Solver',
      description: 'Brings fresh perspectives to challenges',
      criteria: 'Suggest improvements that get implemented'
    }
  }
};

// Accessibility constants
const ACCESSIBILITY_STANDARDS = {
  contrast_ratios: {
    normal_text: 4.5, // WCAG AA standard
    large_text: 3.0,
    ui_components: 3.0
  },
  font_sizes: {
    minimum: 16, // Never go below 16px
    comfortable: 18,
    large: 24
  },
  keyboard_navigation: true,
  screen_reader_support: true,
  reduced_motion_support: true
};

// Inclusive notification messages
const INCLUSIVE_MESSAGES = {
  welcome: "Welcome to N3EXTPATH! We're excited to have you join our inclusive community of creators.",
  achievement: "Congratulations on your achievement! Your contributions make our community stronger.",
  team_invite: "You've been invited to collaborate with an amazing team. Welcome aboard!",
  okr_complete: "Objective completed! Your dedication and hard work paid off.",
  error_generic: "Something went wrong, but don't worry - we're here to help you succeed."
};

// Cultural sensitivity guidelines
const CULTURAL_SENSITIVITY = {
  avoid_cultural_supremacy: [
    'Avoid implying any culture/country is superior',
    'Use neutral quality descriptors instead of cultural references',
    'Respect diverse working styles and approaches'
  ],
  time_zone_inclusive: [
    'Never assume user timezone',
    'Provide clear UTC timestamps', 
    'Accommodate different working hours globally'
  ],
  language_inclusive: [
    'Use simple, clear English that translates well',
    'Avoid idioms and cultural-specific references',
    'Provide context for technical terms'
  ]
};

// Bias detection patterns
const BIAS_PATTERNS = {
  gender_bias: [
    /\b(his|her|he|she)\b/gi, // Use "their" instead
    /\b(guys|girls|ladies|gentlemen)\b/gi, // Use "everyone" or "team"
    /\b(manpower|mankind)\b/gi // Use "workforce" or "humanity"
  ],
  cultural_bias: [
    /\b(oriental|exotic|primitive)\b/gi,
    /\b(first world|third world)\b/gi, // Use "developed/developing"
    /\b(normal|typical)\b/gi // These can be exclusionary
  ],
  ability_bias: [
    /\b(crazy|insane|lame|dumb|blind to)\b/gi,
    /\b(sanity check)\b/gi, // Use "logic check"
    /\b(see|hear|walk through)\b/gi // Context dependent
  ]
};

module.exports = {
  INCLUSIVE_TERMS,
  INCLUSIVE_ROLES, 
  INCLUSIVE_ACHIEVEMENTS,
  ACCESSIBILITY_STANDARDS,
  INCLUSIVE_MESSAGES,
  CULTURAL_SENSITIVITY,
  BIAS_PATTERNS
};

console.log('🌈🎸🌈 INCLUSIVE LANGUAGE CONSTANTS LOADED! 🌈🎸🌈');
console.log('🌍 UNIVERSAL INCLUSIVITY FOR ALL CODE CREATORS ACTIVATED!');
console.log('Built with infinite respect by RICKROLL187 at 18:08:08 UTC!');
console.log('💙 WELCOMING ALL IDENTITIES, CULTURES, AND ABILITIES! 💙');
