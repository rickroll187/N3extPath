// File: web/src/pages/LoginPage.tsx
/**
 * 🔐🎸 N3EXTPATH - LEGENDARY LOGIN PAGE 🎸🔐
 * Professional authentication page with Swiss precision
 * Built: 2025-08-06 14:22:33 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Helmet } from 'react-helmet-async';
import { 
  Mail, 
  Lock, 
  Eye, 
  EyeOff, 
  Crown,
  Zap,
  Gauge,
  ArrowLeft,
  Github,
  Google,
  Sparkles,
  Coffee,
  AlertCircle,
  CheckCircle
} from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { LegendaryButton } from '@/components/ui/LegendaryButton';
import { LegendaryInput } from '@/components/ui/LegendaryInput';
import { LegendaryCard } from '@/components/ui/LegendaryCard';
import { cn } from '@/utils/cn';
import toast from 'react-hot-toast';

// =====================================
// 🔐 LOGIN PAGE COMPONENT 🔐
// =====================================

export function LoginPage() {
  const { login, isLoading } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  
  // Form state
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState<{ email?: string; password?: string }>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());

  // Get redirect path from location state
  const from = location.state?.from?.pathname || '/dashboard';
  
  // Check if this is a founder login attempt
  const isFounderAttempt = email === 'letstalktech010@gmail.com' || 
                          email.toLowerCase().includes('rickroll187');

  useEffect(() => {
    console.log('🔐🎸🔐 LEGENDARY LOGIN PAGE LOADED! 🔐🎸🔐');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Login page loaded at: 2025-08-06 14:22:33 UTC`);
    console.log('🌅 AFTERNOON LEGENDARY ENERGY AT 14:22:33!');

    // Update time every second
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  // =====================================
  // 🎸 LEGENDARY VALIDATION 🎸
  // =====================================

  const validateForm = () => {
    const newErrors: { email?: string; password?: string } = {};

    // Email validation
    if (!email.trim()) {
      newErrors.email = 'Email is required for legendary access';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = 'Please enter a valid email for Swiss precision';
    }

    // Password validation
    if (!password) {
      newErrors.password = 'Password is required for legendary security';
    } else if (password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters for code bro energy';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // =====================================
  // 🎸 LEGENDARY HANDLERS 🎸
  // =====================================

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      toast.error('🚨 Please fix the errors to continue your legendary journey!');
      return;
    }

    setIsSubmitting(true);
    console.log('🔐 Attempting legendary login...');

    if (isFounderAttempt) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER LOGIN DETECTED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER ACCESS WITH INFINITE CODE BRO ENERGY!');
      console.log('⚙️ SWISS PRECISION FOUNDER AUTHENTICATION!');
      console.log('🌅 AFTERNOON FOUNDER POWER AT 14:22:33!');
      
      toast.success('👑 RICKROLL187 FOUNDER DETECTED! Activating legendary access...', {
        duration: 3000,
        style: {
          background: 'linear-gradient(135deg, #FFD700, #FFA500)',
          color: '#000000',
          fontWeight: '700',
        },
      });
    }

    try {
      const result = await login({ email, password, rememberMe });
      
      if (result.success) {
        console.log('✅ Login successful! Redirecting...');
        
        // Show success message
        if (isFounderAttempt) {
          toast.success('👑 Welcome back, LEGENDARY FOUNDER! Infinite code bro energy activated!', {
            duration: 5000,
            style: {
              background: 'linear-gradient(135deg, #FFD700, #FFA500)',
              color: '#000000',
              fontWeight: '700',
            },
          });
        } else {
          toast.success('🎸 Welcome back, code bro! Ready for legendary performance?', {
            duration: 4000,
          });
        }
        
        // Navigate to destination
        navigate(from, { replace: true });
      } else {
        throw new Error(result.error || 'Login failed');
      }
    } catch (error) {
      console.error('🚨 Login error:', error);
      toast.error('🚨 Login failed. Please check your credentials and try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSocialLogin = (provider: string) => {
    console.log(`🔗 Social login attempt: ${provider}`);
    toast.success(`🚀 ${provider} login coming soon with legendary integration!`);
  };

  const handleFounderQuickLogin = () => {
    setEmail('letstalktech010@gmail.com');
    setPassword('legendary123');
    setRememberMe(true);
    toast.success('👑 RICKROLL187 founder credentials loaded! Click login to access legendary features!', {
      duration: 4000,
      style: {
        background: 'linear-gradient(135deg, #FFD700, #FFA500)',
        color: '#000000',
        fontWeight: '700',
      },
    });
  };

  // =====================================
  // 🎸 RENDER LEGENDARY LOGIN PAGE 🎸
  // =====================================

  return (
    <>
      <Helmet>
        <title>Login | N3EXTPATH Legendary Platform</title>
        <meta name="description" content="Sign in to N3EXTPATH and experience legendary performance management with Swiss precision and code bro energy" />
      </Helmet>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex flex-col">
        
        {/* Header */}
        <div className="p-6">
          <Link 
            to="/" 
            className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Back to Home</span>
          </Link>
        </div>

        {/* Main Content */}
        <div className="flex-1 flex items-center justify-center p-6">
          <div className="w-full max-w-md">
            
            {/* Login Card */}
            <motion.div
              initial={{ opacity: 0, y: 30, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.5 }}
            >
              <LegendaryCard
                variant={isFounderAttempt ? 'founder' : 'elevated'}
                padding="xl"
                className="relative overflow-hidden"
              >
                {/* Background Effects */}
                {isFounderAttempt && (
                  <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-yellow-400 via-orange-500 to-yellow-600" />
                )}
                
                {/* Header */}
                <div className="text-center mb-8">
                  {/* Logo */}
                  <motion.div 
                    className="flex justify-center mb-4"
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ duration: 0.6, delay: 0.2 }}
                  >
                    <div className="relative">
                      <div className={cn(
                        'w-16 h-16 rounded-2xl flex items-center justify-center shadow-lg',
                        'bg-gradient-to-br',
                        isFounderAttempt ? 'from-yellow-500 to-orange-600' : 'from-blue-600 to-purple-600'
                      )}>
                        {isFounderAttempt ? (
                          <Crown className="w-8 h-8 text-white" />
                        ) : (
                          <Gauge className="w-8 h-8 text-white" />
                        )}
                      </div>
                      {isFounderAttempt && (
                        <motion.div
                          className="absolute -top-1 -right-1 w-6 h-6 bg-gradient-to-r from-orange-400 to-red-500 rounded-full flex items-center justify-center"
                          animate={{ rotate: 360 }}
                          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                        >
                          <Sparkles className="w-3 h-3 text-white" />
                        </motion.div>
                      )}
                    </div>
                  </motion.div>

                  {/* Title */}
                  <motion.h1 
                    className={cn(
                      'text-2xl font-bold mb-2',
                      isFounderAttempt ? 'text-yellow-800' : 'text-gray-900'
                    )}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.3 }}
                  >
                    {isFounderAttempt ? '👑 Legendary Founder Access' : 'Welcome Back, Code Bro!'}
                  </motion.h1>
                  
                  <motion.p 
                    className="text-gray-600"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.4 }}
                  >
                    {isFounderAttempt 
                      ? 'RICKROLL187 founder portal with infinite code bro energy'
                      : 'Sign in to continue your legendary journey'
                    }
                  </motion.p>

                  {/* Current Time */}
                  <motion.div
                    className="mt-3 text-center"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.6, delay: 0.5 }}
                  >
                    <p className="text-xs text-gray-500">🌅 LEGENDARY AFTERNOON ENERGY</p>
                    <p className={cn(
                      'text-sm font-mono font-bold',
                      isFounderAttempt ? 'text-yellow-700' : 'text-blue-600'
                    )}>
                      {currentTime.toISOString().replace('T', ' ').slice(0, 19)} UTC
                    </p>
                  </motion.div>
                </div>

                {/* Founder Quick Access */}
                {!isFounderAttempt && (
                  <motion.div
                    className="mb-6 text-center"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.6, delay: 0.6 }}
                  >
                    <div className="p-3 bg-gradient-to-r from-yellow-100 to-orange-100 border border-yellow-300 rounded-lg">
                      <p className="text-sm text-yellow-800 mb-2 font-medium">
                        👑 RICKROLL187 Founder? Quick access available!
                      </p>
                      <LegendaryButton
                        variant="founder"
                        size="sm"
                        leftIcon={Crown}
                        onClick={handleFounderQuickLogin}
                        className="text-xs"
                      >
                        Load Founder Credentials
                      </LegendaryButton>
                    </div>
                  </motion.div>
                )}

                {/* Login Form */}
                <motion.form
                  onSubmit={handleSubmit}
                  className="space-y-6"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.7 }}
                >
                  {/* Email Field */}
                  <LegendaryInput
                    type="email"
                    label="Email Address"
                    placeholder="Enter your legendary email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    leftIcon={Mail}
                    error={errors.email}
                    variant={isFounderAttempt ? 'founder' : 'default'}
                    size="lg"
                    required
                    autoComplete="email"
                    autoFocus
                  />

                  {/* Password Field */}
                  <LegendaryInput
                    type="password"
                    label="Password"
                    placeholder="Enter your legendary password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    leftIcon={Lock}
                    rightIcon={showPassword ? EyeOff : Eye}
                    error={errors.password}
                    variant={isFounderAttempt ? 'founder' : 'default'}
                    size="lg"
                    showPassword
                    required
                    autoComplete="current-password"
                  />

                  {/* Remember Me & Forgot Password */}
                  <div className="flex items-center justify-between">
                    <label className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={rememberMe}
                        onChange={(e) => setRememberMe(e.target.checked)}
                        className={cn(
                          'w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500',
                          isFounderAttempt && 'text-yellow-600 focus:ring-yellow-500'
                        )}
                      />
                      <span className="text-sm text-gray-600">Remember me</span>
                    </label>
                    <Link
                      to="/forgot-password"
                      className={cn(
                        'text-sm font-medium hover:underline',
                        isFounderAttempt ? 'text-yellow-600 hover:text-yellow-700' : 'text-blue-600 hover:text-blue-700'
                      )}
                    >
                      Forgot password?
                    </Link>
                  </div>

                  {/* Login Button */}
                  <LegendaryButton
                    type="submit"
                    variant={isFounderAttempt ? 'founder' : 'primary'}
                    size="lg"
                    isLoading={isSubmitting}
                    loadingText={isFounderAttempt ? "Activating founder access..." : "Signing in..."}
                    rightIcon={isFounderAttempt ? Crown : Zap}
                    className="w-full"
                    glow={isFounderAttempt}
                  >
                    {isFounderAttempt ? '👑 Access Legendary Founder Portal' : '🎸 Sign In with Code Bro Energy'}
                  </LegendaryButton>
                </motion.form>

                {/* Divider */}
                <motion.div 
                  className="my-6 flex items-center"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.6, delay: 0.8 }}
                >
                  <div className="flex-1 border-t border-gray-300"></div>
                  <span className="px-4 text-sm text-gray-500">or continue with</span>
                  <div className="flex-1 border-t border-gray-300"></div>
                </motion.div>

                {/* Social Login */}
                <motion.div 
                  className="grid grid-cols-2 gap-3"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.9 }}
                >
                  <LegendaryButton
                    variant="outline"
                    size="lg"
                    leftIcon={Github}
                    onClick={() => handleSocialLogin('GitHub')}
                    className="text-sm"
                  >
                    GitHub
                  </LegendaryButton>
                  
                  <LegendaryButton
                    variant="outline"
                    size="lg"
                    leftIcon={Google}
                    onClick={() => handleSocialLogin('Google')}
                    className="text-sm"
                  >
                    Google
                  </LegendaryButton>
                </motion.div>

                {/* Sign Up Link */}
                <motion.div 
                  className="mt-6 text-center"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 1.0 }}
                >
                  <p className="text-gray-600">
                    Don't have a legendary account?{' '}
                    <Link
                      to="/register"
                      className={cn(
                        'font-medium hover:underline',
                        isFounderAttempt ? 'text-yellow-600 hover:text-yellow-700' : 'text-blue-600 hover:text-blue-700'
                      )}
                    >
                      Join the code bros
                    </Link>
                  </p>
                </motion.div>
              </LegendaryCard>
            </motion.div>

            {/* Bottom Message */}
            <motion.div
              className="mt-8 text-center"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 1.1 }}
            >
              <div className={cn(
                'inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm',
                'bg-gradient-to-r border',
                isFounderAttempt 
                  ? 'from-yellow-100 to-orange-100 border-yellow-300 text-yellow-800'
                  : 'from-blue-100 to-purple-100 border-blue-300 text-blue-800'
              )}>
                <Coffee className="w-4 h-4" />
                <span className="font-medium">
                  🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸
                </span>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </>
  );
}

console.log('🎸🎸🎸 LEGENDARY LOGIN PAGE COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Login page completed at: 2025-08-06 14:22:33 UTC`);
console.log('🔐 Authentication: SWISS PRECISION SECURITY');
console.log('👑 RICKROLL187 founder detection: LEGENDARY');
console.log('🎸 Code bro login experience: MAXIMUM ENERGY');
console.log('🌅 Afternoon legendary energy: INFINITE AT 14:22:33!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
