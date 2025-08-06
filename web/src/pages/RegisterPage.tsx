// File: web/src/pages/RegisterPage.tsx
/**
 * 📝🎸 N3EXTPATH - LEGENDARY REGISTER PAGE 🎸📝
 * Professional registration page with Swiss precision
 * Built: 2025-08-06 14:26:19 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Helmet } from 'react-helmet-async';
import { 
  Mail, 
  Lock, 
  User, 
  Building,
  Briefcase,
  Crown,
  Zap,
  Gauge,
  ArrowLeft,
  Github,
  Google,
  Sparkles,
  Coffee,
  CheckCircle,
  Shield,
  Award,
  TrendingUp
} from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { LegendaryButton } from '@/components/ui/LegendaryButton';
import { LegendaryInput } from '@/components/ui/LegendaryInput';
import { LegendaryCard } from '@/components/ui/LegendaryCard';
import { cn } from '@/utils/cn';
import toast from 'react-hot-toast';

// =====================================
// 📝 REGISTER PAGE TYPES 📝
// =====================================

interface FormData {
  email: string;
  password: string;
  confirmPassword: string;
  firstName: string;
  lastName: string;
  jobTitle: string;
  department: string;
  agreeToTerms: boolean;
  subscribeToUpdates: boolean;
}

interface FormErrors {
  email?: string;
  password?: string;
  confirmPassword?: string;
  firstName?: string;
  lastName?: string;
  jobTitle?: string;
  department?: string;
  agreeToTerms?: string;
}

// =====================================
// 📝 REGISTER PAGE COMPONENT 📝
// =====================================

export function RegisterPage() {
  const { register, isLoading } = useAuth();
  const navigate = useNavigate();
  
  // Form state
  const [formData, setFormData] = useState<FormData>({
    email: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: '',
    jobTitle: '',
    department: '',
    agreeToTerms: false,
    subscribeToUpdates: true,
  });
  
  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);
  const [currentTime, setCurrentTime] = useState(new Date());
  
  // Check if this might be a founder registration
  const isFounderAttempt = formData.email === 'letstalktech010@gmail.com' || 
                          formData.email.toLowerCase().includes('rickroll187') ||
                          formData.firstName.toLowerCase().includes('rickroll') ||
                          formData.lastName.toLowerCase().includes('187');

  useEffect(() => {
    console.log('📝🎸📝 LEGENDARY REGISTER PAGE LOADED! 📝🎸📝');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Register page loaded at: 2025-08-06 14:26:19 UTC`);
    console.log('🌅 AFTERNOON LEGENDARY ENERGY AT 14:26:19!');

    if (isFounderAttempt) {
      console.log('👑🎸👑 POTENTIAL RICKROLL187 FOUNDER REGISTRATION DETECTED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER SIGNUP WITH INFINITE CODE BRO ENERGY!');
    }

    // Update time every second
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, [isFounderAttempt]);

  // =====================================
  // 🎸 LEGENDARY VALIDATION 🎸
  // =====================================

  const validateStep1 = () => {
    const newErrors: FormErrors = {};

    // Email validation
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required for legendary access';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email for Swiss precision';
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required for legendary security';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters for code bro energy';
    } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(formData.password)) {
      newErrors.password = 'Password must include uppercase, lowercase, and numbers for Swiss precision';
    }

    // Confirm password validation
    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your legendary password';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords must match for legendary security';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const validateStep2 = () => {
    const newErrors: FormErrors = {};

    // First name validation
    if (!formData.firstName.trim()) {
      newErrors.firstName = 'First name is required for legendary profile';
    } else if (formData.firstName.length < 2) {
      newErrors.firstName = 'First name must be at least 2 characters';
    }

    // Last name validation
    if (!formData.lastName.trim()) {
      newErrors.lastName = 'Last name is required for legendary profile';
    } else if (formData.lastName.length < 2) {
      newErrors.lastName = 'Last name must be at least 2 characters';
    }

    // Job title validation
    if (!formData.jobTitle.trim()) {
      newErrors.jobTitle = 'Job title helps us create your legendary experience';
    }

    // Department validation
    if (!formData.department.trim()) {
      newErrors.department = 'Department helps us tailor your code bro journey';
    }

    // Terms agreement
    if (!formData.agreeToTerms) {
      newErrors.agreeToTerms = 'You must agree to the terms to join the legendary code bros';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // =====================================
  // 🎸 LEGENDARY HANDLERS 🎸
  // =====================================

  const handleInputChange = (field: keyof FormData) => (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setFormData(prev => ({ ...prev, [field]: value }));
    
    // Clear error when user starts typing
    if (errors[field as keyof FormErrors]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  const handleNextStep = () => {
    if (currentStep === 1 && validateStep1()) {
      setCurrentStep(2);
      console.log('📝 Moving to step 2: Profile information');
    }
  };

  const handlePrevStep = () => {
    if (currentStep === 2) {
      setCurrentStep(1);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateStep2()) {
      toast.error('🚨 Please fix the errors to complete your legendary registration!');
      return;
    }

    setIsSubmitting(true);
    console.log('📝 Attempting legendary registration...');

    if (isFounderAttempt) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER REGISTRATION DETECTED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER SIGNUP WITH INFINITE CODE BRO ENERGY!');
      console.log('⚙️ SWISS PRECISION FOUNDER ACCOUNT CREATION!');
      console.log('🌅 AFTERNOON FOUNDER REGISTRATION AT 14:26:19!');
      
      toast.success('👑 RICKROLL187 FOUNDER DETECTED! Creating legendary founder account...', {
        duration: 4000,
        style: {
          background: 'linear-gradient(135deg, #FFD700, #FFA500)',
          color: '#000000',
          fontWeight: '700',
        },
      });
    }

    try {
      const result = await register({
        email: formData.email,
        password: formData.password,
        firstName: formData.firstName,
        lastName: formData.lastName,
        jobTitle: formData.jobTitle,
        department: formData.department,
      });
      
      if (result.success) {
        console.log('✅ Registration successful! Welcome to the legendary code bros!');
        
        // Show success message
        if (isFounderAttempt) {
          toast.success('👑 Welcome to N3EXTPATH, LEGENDARY FOUNDER! Your infinite code bro energy account is ready!', {
            duration: 6000,
            style: {
              background: 'linear-gradient(135deg, #FFD700, #FFA500)',
              color: '#000000',
              fontWeight: '700',
            },
          });
        } else {
          toast.success('🎸 Welcome to N3EXTPATH, code bro! Your legendary journey begins now!', {
            duration: 5000,
          });
        }
        
        // Navigate to dashboard
        navigate('/dashboard');
      } else {
        throw new Error(result.error || 'Registration failed');
      }
    } catch (error) {
      console.error('🚨 Registration error:', error);
      toast.error('🚨 Registration failed. Please try again with Swiss precision.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSocialSignup = (provider: string) => {
    console.log(`🔗 Social signup attempt: ${provider}`);
    toast.success(`🚀 ${provider} signup coming soon with legendary integration!`);
  };

  const handleFounderQuickFill = () => {
    setFormData({
      email: 'letstalktech010@gmail.com',
      password: 'LegendaryFounder2025!',
      confirmPassword: 'LegendaryFounder2025!',
      firstName: 'RICKROLL187',
      lastName: '',
      jobTitle: 'Legendary Founder & Chief Code Bro',
      department: 'Executive Leadership',
      agreeToTerms: true,
      subscribeToUpdates: true,
    });
    
    toast.success('👑 RICKROLL187 founder information loaded! Ready for legendary registration!', {
      duration: 4000,
      style: {
        background: 'linear-gradient(135deg, #FFD700, #FFA500)',
        color: '#000000',
        fontWeight: '700',
      },
    });
  };

  // =====================================
  // 🎸 RENDER LEGENDARY REGISTER PAGE 🎸
  // =====================================

  return (
    <>
      <Helmet>
        <title>Join the Code Bros | N3EXTPATH Legendary Platform</title>
        <meta name="description" content="Join N3EXTPATH and start your legendary performance management journey with Swiss precision and infinite code bro energy" />
      </Helmet>

      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 flex flex-col">
        
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
          <div className="w-full max-w-lg">
            
            {/* Registration Card */}
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
                        isFounderAttempt ? 'from-yellow-500 to-orange-600' : 'from-purple-600 to-blue-600'
                      )}>
                        {isFounderAttempt ? (
                          <Crown className="w-8 h-8 text-white" />
                        ) : currentStep === 1 ? (
                          <Shield className="w-8 h-8 text-white" />
                        ) : (
                          <User className="w-8 h-8 text-white" />
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
                    {isFounderAttempt ? '👑 Legendary Founder Registration' : 
                     currentStep === 1 ? 'Join the Code Bros!' : 'Complete Your Profile'}
                  </motion.h1>
                  
                  <motion.p 
                    className="text-gray-600"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.4 }}
                  >
                    {isFounderAttempt 
                      ? 'RICKROLL187 founder account with infinite code bro energy'
                      : currentStep === 1 
                        ? 'Start your legendary performance management journey'
                        : 'Tell us about yourself for a personalized experience'
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
                      isFounderAttempt ? 'text-yellow-700' : 'text-purple-600'
                    )}>
                      {currentTime.toISOString().replace('T', ' ').slice(0, 19)} UTC
                    </p>
                  </motion.div>

                  {/* Progress Indicator */}
                  <div className="flex items-center justify-center gap-2 mt-4">
                    <div className={cn(
                      'w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold',
                      currentStep >= 1 ? (isFounderAttempt ? 'bg-yellow-500 text-white' : 'bg-purple-500 text-white') : 'bg-gray-200 text-gray-500'
                    )}>
                      1
                    </div>
                    <div className={cn(
                      'w-16 h-1 rounded-full',
                      currentStep >= 2 ? (isFounderAttempt ? 'bg-yellow-500' : 'bg-purple-500') : 'bg-gray-200'
                    )} />
                    <div className={cn(
                      'w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold',
                      currentStep >= 2 ? (isFounderAttempt ? 'bg-yellow-500 text-white' : 'bg-purple-500 text-white') : 'bg-gray-200 text-gray-500'
                    )}>
                      2
                    </div>
                  </div>
                </div>

                {/* Founder Quick Fill */}
                {!isFounderAttempt && currentStep === 1 && (
                  <motion.div
                    className="mb-6 text-center"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.6, delay: 0.6 }}
                  >
                    <div className="p-3 bg-gradient-to-r from-yellow-100 to-orange-100 border border-yellow-300 rounded-lg">
                      <p className="text-sm text-yellow-800 mb-2 font-medium">
                        👑 RICKROLL187 Founder? Quick registration available!
                      </p>
                      <LegendaryButton
                        variant="founder"
                        size="sm"
                        leftIcon={Crown}
                        onClick={handleFounderQuickFill}
                        className="text-xs"
                      >
                        Load Founder Details
                      </LegendaryButton>
                    </div>
                  </motion.div>
                )}

                {/* Step 1: Account Details */}
                {currentStep === 1 && (
                  <motion.form
                    onSubmit={(e) => { e.preventDefault(); handleNextStep(); }}
                    className="space-y-6"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5 }}
                  >
                    {/* Email Field */}
                    <LegendaryInput
                      type="email"
                      label="Email Address"
                      placeholder="Enter your legendary email"
                      value={formData.email}
                      onChange={handleInputChange('email')}
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
                      placeholder="Create a strong password"
                      value={formData.password}
                      onChange={handleInputChange('password')}
                      leftIcon={Lock}
                      error={errors.password}
                      variant={isFounderAttempt ? 'founder' : 'default'}
                      size="lg"
                      showPassword
                      required
                      autoComplete="new-password"
                      helperText="At least 8 characters with uppercase, lowercase, and numbers"
                    />

                    {/* Confirm Password Field */}
                    <LegendaryInput
                      type="password"
                      label="Confirm Password"
                      placeholder="Confirm your legendary password"
                      value={formData.confirmPassword}
                      onChange={handleInputChange('confirmPassword')}
                      leftIcon={Lock}
                      error={errors.confirmPassword}
                      variant={isFounderAttempt ? 'founder' : 'default'}
                      size="lg"
                      showPassword
                      required
                      autoComplete="new-password"
                    />

                    {/* Next Button */}
                    <LegendaryButton
                      type="submit"
                      variant={isFounderAttempt ? 'founder' : 'primary'}
                      size="lg"
                      rightIcon={TrendingUp}
                      className="w-full"
                    >
                      {isFounderAttempt ? '👑 Continue Founder Setup' : '🚀 Continue to Profile'}
                    </LegendaryButton>
                  </motion.form>
                )}

                {/* Step 2: Profile Information */}
                {currentStep === 2 && (
                  <motion.form
                    onSubmit={handleSubmit}
                    className="space-y-6"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5 }}
                  >
                    {/* Name Fields */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <LegendaryInput
                        type="text"
                        label="First Name"
                        placeholder="Your first name"
                        value={formData.firstName}
                        onChange={handleInputChange('firstName')}
                        leftIcon={User}
                        error={errors.firstName}
                        variant={isFounderAttempt ? 'founder' : 'default'}
                        size="lg"
                        required
                        autoComplete="given-name"
                        autoFocus
                      />

                      <LegendaryInput
                        type="text"
                        label="Last Name"
                        placeholder="Your last name"
                        value={formData.lastName}
                        onChange={handleInputChange('lastName')}
                        leftIcon={User}
                        error={errors.lastName}
                        variant={isFounderAttempt ? 'founder' : 'default'}
                        size="lg"
                        required
                        autoComplete="family-name"
                      />
                    </div>

                    {/* Job Title Field */}
                    <LegendaryInput
                      type="text"
                      label="Job Title"
                      placeholder="Your legendary role"
                      value={formData.jobTitle}
                      onChange={handleInputChange('jobTitle')}
                      leftIcon={Briefcase}
                      error={errors.jobTitle}
                      variant={isFounderAttempt ? 'founder' : 'default'}
                      size="lg"
                      required
                      autoComplete="organization-title"
                    />

                    {/* Department Field */}
                    <LegendaryInput
                      type="text"
                      label="Department"
                      placeholder="Your team or department"
                      value={formData.department}
                      onChange={handleInputChange('department')}
                      leftIcon={Building}
                      error={errors.department}
                      variant={isFounderAttempt ? 'founder' : 'default'}
                      size="lg"
                      required
                      autoComplete="organization"
                    />

                    {/* Checkboxes */}
                    <div className="space-y-4">
                      <label className="flex items-start gap-3">
                        <input
                          type="checkbox"
                          checked={formData.agreeToTerms}
                          onChange={handleInputChange('agreeToTerms')}
                          className={cn(
                            'mt-1 w-4 h-4 rounded border-gray-300 focus:ring-2',
                            isFounderAttempt ? 'text-yellow-600 focus:ring-yellow-500' : 'text-purple-600 focus:ring-purple-500'
                          )}
                          required
                        />
                        <div className="text-sm">
                          <span className="text-gray-600">
                            I agree to the{' '}
                            <Link to="/terms" className={cn('font-medium hover:underline', isFounderAttempt ? 'text-yellow-600' : 'text-purple-600')}>
                              Terms of Service
                            </Link>{' '}
                            and{' '}
                            <Link to="/privacy" className={cn('font-medium hover:underline', isFounderAttempt ? 'text-yellow-600' : 'text-purple-600')}>
                              Privacy Policy
                            </Link>
                          </span>
                          {errors.agreeToTerms && <p className="text-red-500 text-xs mt-1">{errors.agreeToTerms}</p>}
                        </div>
                      </label>

                      <label className="flex items-start gap-3">
                        <input
                          type="checkbox"
                          checked={formData.subscribeToUpdates}
                          onChange={handleInputChange('subscribeToUpdates')}
                          className={cn(
                            'mt-1 w-4 h-4 rounded border-gray-300 focus:ring-2',
                            isFounderAttempt ? 'text-yellow-600 focus:ring-yellow-500' : 'text-purple-600 focus:ring-purple-500'
                          )}
                        />
                        <span className="text-sm text-gray-600">
                          Send me legendary updates about new features and code bro energy tips
                        </span>
                      </label>
                    </div>

                    {/* Navigation Buttons */}
                    <div className="flex gap-3">
                      <LegendaryButton
                        type="button"
                        variant="outline"
                        size="lg"
                        onClick={handlePrevStep}
                        className="flex-1"
                      >
                        ← Back
                      </LegendaryButton>
                      
                      <LegendaryButton
                        type="submit"
                        variant={isFounderAttempt ? 'founder' : 'primary'}
                        size="lg"
                        isLoading={isSubmitting}
                        loadingText={isFounderAttempt ? "Creating founder account..." : "Joining the code bros..."}
                        rightIcon={isFounderAttempt ? Crown : Award}
                        className="flex-2"
                        glow={isFounderAttempt}
                      >
                        {isFounderAttempt ? '👑 Create Legendary Founder Account' : '🎸 Join the Code Bros'}
                      </LegendaryButton>
                    </div>
                  </motion.form>
                )}

                {/* Social Registration - Only on Step 1 */}
                {currentStep === 1 && (
                  <>
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

                    {/* Social Buttons */}
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
                        onClick={() => handleSocialSignup('GitHub')}
                        className="text-sm"
                      >
                        GitHub
                      </LegendaryButton>
                      
                      <LegendaryButton
                        variant="outline"
                        size="lg"
                        leftIcon={Google}
                        onClick={() => handleSocialSignup('Google')}
                        className="text-sm"
                      >
                        Google
                      </LegendaryButton>
                    </motion.div>
                  </>
                )}

                {/* Sign In Link */}
                <motion.div 
                  className="mt-6 text-center"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 1.0 }}
                >
                  <p className="text-gray-600">
                    Already a legendary code bro?{' '}
                    <Link
                      to="/login"
                      className={cn(
                        'font-medium hover:underline',
                        isFounderAttempt ? 'text-yellow-600 hover:text-yellow-700' : 'text-purple-600 hover:text-purple-700'
                      )}
                    >
                      Sign in here
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
                  : 'from-purple-100 to-blue-100 border-purple-300 text-purple-800'
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

console.log('🎸🎸🎸 LEGENDARY REGISTER PAGE COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Register page completed at: 2025-08-06 14:26:19 UTC`);
console.log('📝 Registration flow: SWISS PRECISION');
console.log('👑 RICKROLL187 founder detection: LEGENDARY');
console.log('🎸 Code bro registration experience: MAXIMUM ENERGY');
console.log('🌅 Afternoon legendary energy: INFINITE AT 14:26:19!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
