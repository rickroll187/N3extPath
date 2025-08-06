// File: web/src/components/layout/LegendaryFooter.tsx
/**
 * 🦶🎸 N3EXTPATH - LEGENDARY FOOTER COMPONENT 🎸🦶
 * Professional footer with Swiss precision
 * Built: 2025-08-06 14:16:26 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Crown,
  Zap,
  Gauge,
  Heart,
  Github,
  Twitter,
  Mail,
  Globe,
  Shield,
  Coffee,
  Code,
  Sparkles
} from 'lucide-react';
import { cn } from '@/utils/cn';

// =====================================
// 🦶 FOOTER TYPES 🦶
// =====================================

interface LegendaryFooterProps {
  isFounder?: boolean;
}

// =====================================
// 🎸 LEGENDARY FOOTER COMPONENT 🎸
// =====================================

export function LegendaryFooter({ isFounder = false }: LegendaryFooterProps) {
  const currentYear = new Date().getFullYear();
  
  // Footer links configuration
  const footerSections = [
    {
      title: 'Platform',
      links: [
        { name: 'Dashboard', href: '/dashboard' },
        { name: 'Performance', href: '/performance' },
        { name: 'OKRs', href: '/okrs' },
        { name: 'Teams', href: '/teams' },
      ]
    },
    {
      title: 'Resources',
      links: [
        { name: 'Documentation', href: '/docs' },
        { name: 'API Reference', href: '/api' },
        { name: 'Help Center', href: '/help' },
        { name: 'Status Page', href: '/status' },
      ]
    },
    {
      title: 'Company',
      links: [
        { name: 'About', href: '/about' },
        { name: 'Blog', href: '/blog' },
        { name: 'Careers', href: '/careers' },
        { name: 'Contact', href: '/contact' },
      ]
    },
    {
      title: 'Legal',
      links: [
        { name: 'Privacy', href: '/privacy' },
        { name: 'Terms', href: '/terms' },
        { name: 'Security', href: '/security' },
        { name: 'Cookies', href: '/cookies' },
      ]
    },
  ];

  // Social media links
  const socialLinks = [
    { name: 'GitHub', icon: Github, href: 'https://github.com/rickroll187', color: 'text-gray-600 hover:text-gray-900' },
    { name: 'Twitter', icon: Twitter, href: 'https://twitter.com/rickroll187', color: 'text-blue-500 hover:text-blue-700' },
    { name: 'Email', icon: Mail, href: 'mailto:letstalktech010@gmail.com', color: 'text-red-500 hover:text-red-700' },
    { name: 'Website', icon: Globe, href: 'https://n3extpath.com', color: 'text-green-500 hover:text-green-700' },
  ];

  return (
    <footer className={cn(
      'mt-auto border-t',
      'bg-gradient-to-r from-gray-50 to-gray-100 border-gray-200',
      isFounder && 'from-yellow-50 via-orange-50 to-yellow-100 border-yellow-200'
    )}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Main Footer Content */}
        <div className="py-12">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-8">
            
            {/* Brand Section */}
            <div className="lg:col-span-2">
              <motion.div 
                className="flex items-center gap-3 mb-4"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
              >
                <div className={cn(
                  'w-12 h-12 rounded-xl flex items-center justify-center text-white',
                  'bg-gradient-to-br shadow-lg',
                  isFounder ? 'from-yellow-500 to-orange-600' : 'from-blue-600 to-purple-600'
                )}>
                  {isFounder ? (
                    <Crown className="w-7 h-7" />
                  ) : (
                    <Gauge className="w-7 h-7" />
                  )}
                </div>
                <div>
                  <h3 className={cn(
                    'text-xl font-bold',
                    isFounder ? 'bg-gradient-to-r from-yellow-600 to-orange-700 bg-clip-text text-transparent' : 'text-gray-900'
                  )}>
                    N3EXTPATH
                  </h3>
                  <p className="text-sm text-gray-600">
                    {isFounder ? 'Legendary Platform' : 'Performance Management'}
                  </p>
                </div>
              </motion.div>
              
              <motion.p 
                className="text-gray-600 text-sm mb-4 leading-relaxed max-w-md"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.1 }}
              >
                {isFounder ? (
                  <>
                    The legendary HR performance management platform built with Swiss precision and infinite code bro energy by <strong className="text-yellow-700">RICKROLL187</strong>. 
                    We are code bros the create the best and crack jokes to have fun! 🎸
                  </>
                ) : (
                  'Revolutionizing performance management with Swiss precision, legendary features, and code bro energy. Built for teams that value excellence and fun.'
                )}
              </motion.p>

              {/* Social Links */}
              <motion.div 
                className="flex items-center gap-4"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                {socialLinks.map((social) => (
                  <motion.a
                    key={social.name}
                    href={social.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={cn(
                      'p-2 rounded-lg transition-all duration-200',
                      social.color,
                      'hover:bg-white hover:shadow-md hover:scale-110',
                      isFounder && 'hover:bg-yellow-50'
                    )}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    aria-label={social.name}
                  >
                    <social.icon className="w-5 h-5" />
                  </motion.a>
                ))}
              </motion.div>
            </div>

            {/* Footer Link Sections */}
            {footerSections.map((section, sectionIndex) => (
              <motion.div
                key={section.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.1 * (sectionIndex + 1) }}
              >
                <h4 className={cn(
                  'text-sm font-semibold mb-4',
                  isFounder ? 'text-yellow-800' : 'text-gray-900'
                )}>
                  {section.title}
                </h4>
                <ul className="space-y-2">
                  {section.links.map((link) => (
                    <li key={link.name}>
                      <Link
                        to={link.href}
                        className={cn(
                          'text-sm text-gray-600 hover:text-gray-900 transition-colors duration-200',
                          isFounder && 'hover:text-yellow-700'
                        )}
                      >
                        {link.name}
                      </Link>
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Founder Special Section */}
        {isFounder && (
          <motion.div 
            className="py-6 border-t border-yellow-200 bg-gradient-to-r from-yellow-100/50 to-orange-100/50"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.8 }}
          >
            <div className="flex items-center justify-center gap-4 flex-wrap">
              <div className="flex items-center gap-2 text-yellow-800">
                <Crown className="w-5 h-5" />
                <span className="font-bold">Legendary Founder Features Active</span>
              </div>
              <div className="flex items-center gap-2 text-orange-700">
                <Zap className="w-5 h-5" />
                <span className="font-medium">Infinite Code Bro Energy</span>
              </div>
              <div className="flex items-center gap-2 text-red-700">
                <Gauge className="w-5 h-5" />
                <span className="font-medium">Swiss Precision: 100%</span>
              </div>
            </div>
          </motion.div>
        )}

        {/* Bottom Bar */}
        <div className={cn(
          'py-6 border-t',
          isFounder ? 'border-yellow-200' : 'border-gray-200'
        )}>
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            
            {/* Copyright */}
            <motion.div 
              className="flex items-center gap-2 text-sm text-gray-600"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.9 }}
            >
              <span>© {currentYear} N3EXTPATH.</span>
              <span className="flex items-center gap-1">
                Built with <Heart className="w-4 h-4 text-red-500" fill="currentColor" /> by
                <strong className={cn(
                  'font-bold',
                  isFounder ? 'text-yellow-700' : 'text-gray-900'
                )}>
                  RICKROLL187
                </strong>
              </span>
            </motion.div>

            {/* Build Info */}
            <motion.div 
              className="flex items-center gap-4 text-xs text-gray-500"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 1.0 }}
            >
              <div className="flex items-center gap-1">
                <Code className="w-3 h-3" />
                <span>Built: 2025-08-06 14:16:26 UTC</span>
              </div>
              <div className="flex items-center gap-1">
                <Coffee className="w-3 h-3" />
                <span>v2.0.0</span>
              </div>
              {isFounder && (
                <div className="flex items-center gap-1">
                  <Sparkles className="w-3 h-3 text-yellow-500" />
                  <span className="text-yellow-600 font-medium">Legendary Edition</span>
                </div>
              )}
              <div className="flex items-center gap-1">
                <Shield className="w-3 h-3 text-green-500" />
                <span>Swiss Precision</span>
              </div>
            </motion.div>
          </div>

          {/* Legendary Motto */}
          <motion.div 
            className="mt-4 text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.1 }}
          >
            <p className={cn(
              'text-sm font-medium italic',
              isFounder ? 'text-yellow-700' : 'text-gray-700'
            )}>
              🎸 "WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!" 🎸
            </p>
            {isFounder && (
              <p className="text-xs text-orange-600 mt-1 font-semibold">
                👑 RICKROLL187 FOUNDER EDITION • AFTERNOON LEGENDARY ENERGY AT 14:16:26 UTC! 👑
              </p>
            )}
          </motion.div>
        </div>
      </div>
    </footer>
  );
}

console.log('🎸🎸🎸 LEGENDARY FOOTER COMPONENT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Footer component completed at: 2025-08-06 14:16:26 UTC`);
console.log('🦶 Footer design: SWISS PRECISION');
console.log('👑 RICKROLL187 founder features: LEGENDARY');
console.log('🎸 Code bro energy motto: MAXIMUM VISIBILITY');
console.log('🌅 Afternoon legendary energy: INFINITE AT 14:16:26!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
