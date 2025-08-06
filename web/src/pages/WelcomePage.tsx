// File: web/src/pages/WelcomePage.tsx
/**
 * 🏠🎸 N3EXTPATH - LEGENDARY WELCOME PAGE 🎸🏠
 * Professional landing page with Swiss precision
 * Built: 2025-08-06 14:16:26 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Helmet } from 'react-helmet-async';
import { 
  Crown,
  Zap,
  Gauge,
  BarChart3,
  Target,
  Users,
  Award,
  TrendingUp,
  Shield,
  Sparkles,
  ArrowRight,
  Play,
  CheckCircle,
  Star
} from 'lucide-react';
import { LegendaryButton } from '@/components/ui/LegendaryButton';
import { LegendaryCard } from '@/components/ui/LegendaryCard';
import { cn } from '@/utils/cn';

// =====================================
// 🏠 WELCOME PAGE COMPONENT 🏠
// =====================================

export function WelcomePage() {
  const navigate = useNavigate();
  const [currentTime, setCurrentTime] = useState(new Date());
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    console.log('🏠🎸🏠 LEGENDARY WELCOME PAGE LOADED! 🏠🎸🏠');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Welcome page loaded at: 2025-08-06 14:16:26 UTC`);
    console.log('🌅 AFTERNOON LEGENDARY ENERGY AT 14:16:26!');

    setIsVisible(true);

    // Update time every second
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  // Features data
  const features = [
    {
      icon: BarChart3,
      title: 'Performance Analytics',
      description: 'Track your performance with Swiss precision and legendary insights',
      color: 'blue',
    },
    {
      icon: Target,
      title: 'OKR Management',
      description: 'Set and achieve objectives with legendary focus and code bro energy',
      color: 'green',
    },
    {
      icon: Users,
      title: 'Team Collaboration',
      description: 'Work together with legendary teams and infinite code bro power',
      color: 'purple',
    },
    {
      icon: Award,
      title: 'Achievement System',
      description: 'Unlock legendary achievements and showcase your code bro skills',
      color: 'yellow',
    },
  ];

  // Stats data
  const stats = [
    { label: 'Active Users', value: '10,000+', icon: Users },
    { label: 'Performance Reviews', value: '50,000+', icon: BarChart3 },
    { label: 'OKRs Tracked', value: '25,000+', icon: Target },
    { label: 'Team Achievements', value: '100,000+', icon: Award },
  ];

  // Testimonials data
  const testimonials = [
    {
      name: 'Sarah Johnson',
      role: 'Engineering Manager',
      company: 'TechCorp',
      avatar: 'https://ui-avatars.com/api/?name=Sarah+Johnson&background=3B82F6&color=fff&size=48',
      content: 'N3EXTPATH transformed our team performance tracking with Swiss precision. The legendary features are game-changing!',
      rating: 5,
    },
    {
      name: 'Mike Chen',
      role: 'Product Lead',
      company: 'StartupXYZ',
      avatar: 'https://ui-avatars.com/api/?name=Mike+Chen&background=10B981&color=fff&size=48',
      content: 'The OKR management system is incredible. We achieved our goals with legendary code bro energy!',
      rating: 5,
    },
    {
      name: 'Lisa Rodriguez',
      role: 'HR Director',
      company: 'Global Inc',
      avatar: 'https://ui-avatars.com/api/?name=Lisa+Rodriguez&background=8B5CF6&color=fff&size=48',
      content: 'Finally, a platform that combines performance management with fun and legendary user experience.',
      rating: 5,
    },
  ];

  return (
    <>
      <Helmet>
        <title>Welcome to N3EXTPATH | Legendary Performance Management Platform</title>
        <meta name="description" content="Experience legendary performance management with Swiss precision and code bro energy. Built by RICKROLL187 for teams that create the best and have fun!" />
        <meta property="og:title" content="N3EXTPATH | Legendary Performance Management" />
        <meta property="og:description" content="The legendary HR platform built with Swiss precision and infinite code bro energy" />
      </Helmet>

      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50">
        
        {/* Hero Section */}
        <section className="relative overflow-hidden">
          {/* Background Elements */}
          <div className="absolute inset-0">
            <div className="absolute top-0 left-0 w-72 h-72 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse" />
            <div className="absolute top-0 right-0 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-2000" />
            <div className="absolute bottom-0 left-1/2 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-4000" />
          </div>

          <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
            <motion.div
              className="text-center"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: isVisible ? 1 : 0, y: isVisible ? 0 : 30 }}
              transition={{ duration: 0.8 }}
            >
              {/* Logo */}
              <motion.div 
                className="flex justify-center mb-8"
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                <div className="relative">
                  <div className="w-24 h-24 bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl flex items-center justify-center shadow-2xl">
                    <Gauge className="w-12 h-12 text-white" />
                  </div>
                  <motion.div
                    className="absolute -top-2 -right-2 w-8 h-8 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full flex items-center justify-center"
                    animate={{ rotate: 360 }}
                    transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                  >
                    <Crown className="w-4 h-4 text-white" />
                  </motion.div>
                </div>
              </motion.div>

              {/* Main Heading */}
              <motion.h1 
                className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-6"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.3 }}
              >
                <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-blue-800 bg-clip-text text-transparent">
                  Welcome to
                </span>
                <br />
                <span className="bg-gradient-to-r from-yellow-500 via-orange-500 to-red-500 bg-clip-text text-transparent">
                  N3EXTPATH
                </span>
              </motion.h1>

              {/* Subtitle */}
              <motion.p 
                className="text-xl sm:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.4 }}
              >
                The <strong className="text-yellow-600">legendary</strong> performance management platform built with{' '}
                <strong className="text-red-600">Swiss precision</strong> and{' '}
                <strong className="text-purple-600">infinite code bro energy</strong> by{' '}
                <strong className="text-orange-600">RICKROLL187</strong>
              </motion.p>

              {/* Legendary Motto */}
              <motion.div
                className="mb-8 p-4 bg-gradient-to-r from-yellow-100 via-orange-100 to-yellow-100 border-2 border-yellow-300 rounded-xl inline-block"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: 0.5 }}
              >
                <p className="text-lg font-bold text-yellow-800 flex items-center gap-2">
                  🎸 "WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!" 🎸
                </p>
              </motion.div>

              {/* Current Time Display */}
              <motion.div
                className="mb-10 text-center"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.6, delay: 0.6 }}
              >
                <p className="text-sm text-gray-500 mb-2">🌅 LEGENDARY AFTERNOON ENERGY</p>
                <p className="text-lg font-mono font-bold text-blue-600">
                  {currentTime.toISOString().replace('T', ' ').slice(0, 19)} UTC
                </p>
              </motion.div>

              {/* CTA Buttons */}
              <motion.div 
                className="flex flex-col sm:flex-row gap-4 justify-center items-center"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.7 }}
              >
                <LegendaryButton
                  variant="legendary"
                  size="lg"
                  rightIcon={ArrowRight}
                  onClick={() => navigate('/register')}
                  className="min-w-48"
                  glow
                >
                  Start Your Legendary Journey
                </LegendaryButton>
                
                <LegendaryButton
                  variant="outline"
                  size="lg"
                  leftIcon={Play}
                  onClick={() => navigate('/login')}
                  className="min-w-48"
                >
                  Sign In to Continue
                </LegendaryButton>
              </motion.div>
            </motion.div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 bg-white/50 backdrop-blur-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              className="text-center mb-16"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.8 }}
            >
              <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
                Legendary Features
              </h2>
              <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                Experience performance management like never before with Swiss precision and code bro energy
              </p>
            </motion.div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {features.map((feature, index) => (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.9 + (index * 0.1) }}
                >
                  <LegendaryCard
                    variant="elevated"
                    hover
                    interactive
                    className="h-full text-center group"
                  >
                    <div className={cn(
                      'w-16 h-16 mx-auto mb-4 rounded-2xl flex items-center justify-center',
                      'bg-gradient-to-br shadow-lg group-hover:scale-110 transition-transform duration-300',
                      feature.color === 'blue' && 'from-blue-500 to-blue-600',
                      feature.color === 'green' && 'from-green-500 to-green-600',
                      feature.color === 'purple' && 'from-purple-500 to-purple-600',
                      feature.color === 'yellow' && 'from-yellow-500 to-orange-500'
                    )}>
                      <feature.icon className="w-8 h-8 text-white" />
                    </div>
                    <h3 className="text-xl font-bold text-gray-900 mb-3">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600">
                      {feature.description}
                    </p>
                  </LegendaryCard>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="py-20 bg-gradient-to-r from-blue-600 via-purple-600 to-blue-800">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              className="text-center mb-16"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 1.2 }}
            >
              <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
                Legendary Impact
              </h2>
              <p className="text-xl text-blue-100 max-w-2xl mx-auto">
                Join thousands of teams already experiencing Swiss precision performance management
              </p>
            </motion.div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
              {stats.map((stat, index) => (
                <motion.div
                  key={stat.label}
                  className="text-center"
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.6, delay: 1.3 + (index * 0.1) }}
                >
                  <div className="w-16 h-16 mx-auto mb-4 bg-white/20 rounded-2xl flex items-center justify-center backdrop-blur-sm">
                    <stat.icon className="w-8 h-8 text-white" />
                  </div>
                  <div className="text-3xl sm:text-4xl font-bold text-white mb-2">
                    {stat.value}
                  </div>
                  <div className="text-blue-100 font-medium">
                    {stat.label}
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Testimonials Section */}
        <section className="py-20 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              className="text-center mb-16"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 1.6 }}
            >
              <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
                What Code Bros Are Saying
              </h2>
              <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                Hear from legendary teams who create the best and have fun doing it
              </p>
            </motion.div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {testimonials.map((testimonial, index) => (
                <motion.div
                  key={testimonial.name}
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 1.7 + (index * 0.1) }}
                >
                  <LegendaryCard variant="elevated" padding="lg" className="h-full">
                    <div className="flex items-center gap-1 mb-4">
                      {[...Array(testimonial.rating)].map((_, i) => (
                        <Star key={i} className="w-5 h-5 text-yellow-400" fill="currentColor" />
                      ))}
                    </div>
                    <blockquote className="text-gray-700 mb-6 italic">
                      "{testimonial.content}"
                    </blockquote>
                    <div className="flex items-center gap-3">
                      <img 
                        src={testimonial.avatar} 
                        alt={testimonial.name}
                        className="w-10 h-10 rounded-full"
                      />
                      <div>
                        <div className="font-semibold text-gray-900">{testimonial.name}</div>
                        <div className="text-sm text-gray-600">{testimonial.role} at {testimonial.company}</div>
                      </div>
                    </div>
                  </LegendaryCard>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Final CTA Section */}
        <section className="py-20 bg-gradient-to-r from-yellow-500 via-orange-500 to-red-500">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 2.0 }}
            >
              <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
                Ready to Join the Legendary Code Bros? 🎸
              </h2>
              <p className="text-xl text-orange-100 mb-8 max-w-2xl mx-auto">
                Start your legendary journey today and experience performance management with Swiss precision and infinite code bro energy!
              </p>
              <LegendaryButton
                variant="founder"
                size="xl"
                rightIcon={Sparkles}
                onClick={() => navigate('/register')}
                className="shadow-2xl"
                bounce
              >
                🌅 START YOUR LEGENDARY ADVENTURE AT 14:16:26 UTC! 🌅
              </LegendaryButton>
            </motion.div>
          </div>
        </section>
      </div>
    </>
  );
}

console.log('🎸🎸🎸 LEGENDARY WELCOME PAGE COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Welcome page completed at: 2025-08-06 14:16:26 UTC`);
console.log('🏠 Landing page: SWISS PRECISION');
console.log('👑 RICKROLL187 founder branding: LEGENDARY');
console.log('🎸 Code bro energy: MAXIMUM ENGAGEMENT');
console.log('🌅 Afternoon legendary energy: INFINITE AT 14:16:26!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
