// File: frontend/src/components/Auth/LoginForm.tsx
/**
 * 🔐🎸 N3EXTPATH - LEGENDARY LOGIN FORM 🎸🔐
 * Professional authentication with Swiss precision security
 * Built: 2025-08-05 18:29:42 UTC by RICKROLL187
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'react-toastify';
import { 
  loginUser, 
  selectAuth, 
  selectIsAuthenticated, 
  selectIsLegendaryUser 
} from '../../store/store';
import { AppDispatch } from '../../store/store';

// Validation Schema
const loginValidationSchema = Yup.object({
  username: Yup.string()
    .min(3, 'Username must be at least 3 characters')
    .max(50, 'Username must be less than 50 characters')
    .required('Username is required'),
  password: Yup.string()
    .min(6, 'Password must be at least 6 characters')
    .required('Password is required'),
  remember_me: Yup.boolean()
});

interface LoginFormData {
  username: string;
  password: string;
  remember_me: boolean;
}

const LoginForm: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const location = useLocation();
  
  const { isLoading, error } = useSelector(selectAuth);
  const isAuthenticated = useSelector(selectIsAuthenticated);
  const isLegendary = useSelector(selectIsLegendaryUser);
  
  const [showPassword, setShowPassword] = useState(false);
  const [isRickroll187Mode, setIsRickroll187Mode] = useState(false);
  const [legendaryAnimations, setLegendaryAnimations] = useState(false);

  // Check if user is trying to access legendary features
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    if (params.get('legendary') === 'true' || params.get('rickroll187') === 'true') {
      setIsRickroll187Mode(true);
      setLegendaryAnimations(true);
      toast.info('🎸 Legendary login mode activated! 🎸');
    }
  }, [location]);

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      const from = (location.state as any)?.from?.pathname || 
                   (isLegendary ? '/legendary-dashboard' : '/dashboard');
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, isLegendary, navigate, location]);

  const handleSubmit = async (values: LoginFormData) => {
    try {
      const result = await dispatch(loginUser({
        username: values.username,
        password: values.password,
        remember_me: values.remember_me
      }));

      if (loginUser.fulfilled.match(result)) {
        const user = result.payload.user;
        
        if (user.is_legendary) {
          toast.success('🎸 LEGENDARY FOUNDER LOGIN SUCCESSFUL! Welcome back, RICKROLL187! 🎸');
          setLegendaryAnimations(true);
          
          // Add some legendary flair
          setTimeout(() => {
            navigate('/legendary-dashboard');
          }, 1500);
        } else {
          toast.success(`Welcome back, ${user.first_name}!`);
          const from = (location.state as any)?.from?.pathname || '/dashboard';
          navigate(from, { replace: true });
        }
      } else {
        // Error is handled by Redux and API service
      }
    } catch (error: any) {
      toast.error(error.message || 'Login failed');
    }
  };

  const handleRickroll187Click = () => {
    setIsRickroll187Mode(!isRickroll187Mode);
    setLegendaryAnimations(!legendaryAnimations);
    
    if (!isRickroll187Mode) {
      toast.success('🎸 LEGENDARY MODE ACTIVATED! RICKROLL187 special features enabled! 🎸');
    } else {
      toast.info('Legendary mode deactivated');
    }
  };

  const legendaryVariants = {
    hidden: { opacity: 0, scale: 0.8, rotateY: -180 },
    visible: { 
      opacity: 1, 
      scale: 1, 
      rotateY: 0,
      transition: { 
        type: "spring", 
        stiffness: 100, 
        damping: 12,
        duration: 0.8
      }
    },
    exit: { 
      opacity: 0, 
      scale: 0.8, 
      rotateY: 180,
      transition: { duration: 0.5 }
    }
  };

  const inputVariants = {
    focus: { 
      scale: 1.02, 
      borderColor: isRickroll187Mode ? '#FFD700' : '#3B82F6',
      boxShadow: isRickroll187Mode ? 
        '0 0 20px rgba(255, 215, 0, 0.5)' : 
        '0 0 10px rgba(59, 130, 246, 0.3)'
    },
    blur: { 
      scale: 1, 
      borderColor: '#D1D5DB',
      boxShadow: 'none'
    }
  };

  return (
    <div className={`min-h-screen flex items-center justify-center ${
      isRickroll187Mode 
        ? 'bg-gradient-to-br from-yellow-400 via-red-500 to-pink-500' 
        : 'bg-gradient-to-br from-blue-50 to-indigo-100'
    }`}>
      <AnimatePresence>
        <motion.div
          key="login-container"
          variants={legendaryVariants}
          initial="hidden"
          animate="visible"
          exit="exit"
          className={`max-w-md w-full space-y-8 p-8 ${
            isRickroll187Mode 
              ? 'bg-black bg-opacity-20 backdrop-blur-lg border border-yellow-300' 
              : 'bg-white'
          } rounded-xl shadow-2xl`}
        >
          {/* Header */}
          <div className="text-center">
            <motion.div
              animate={legendaryAnimations ? { rotate: [0, 360] } : {}}
              transition={{ duration: 2, repeat: legendaryAnimations ? Infinity : 0 }}
              className="mx-auto h-16 w-16 flex items-center justify-center rounded-full text-4xl"
            >
              {isRickroll187Mode ? '🎸' : '🔐'}
            </motion.div>
            
            <motion.h2 
              className={`mt-6 text-3xl font-extrabold ${
                isRickroll187Mode ? 'text-yellow-300' : 'text-gray-900'
              }`}
              animate={legendaryAnimations ? { scale: [1, 1.05, 1] } : {}}
              transition={{ duration: 2, repeat: legendaryAnimations ? Infinity : 0 }}
            >
              {isRickroll187Mode ? '🎸 LEGENDARY LOGIN 🎸' : 'Sign in to N3EXTPATH'}
            </motion.h2>
            
            {isRickroll187Mode && (
              <motion.p 
                className="mt-2 text-sm text-yellow-200"
                animate={{ opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 1.5, repeat: Infinity }}
              >
                Welcome back, legendary founder RICKROLL187!
              </motion.p>
            )}
            
            <p className={`mt-2 text-sm ${
              isRickroll187Mode ? 'text-yellow-100' : 'text-gray-600'
            }`}>
              Or{' '}
              <Link 
                to="/register" 
                className={`font-medium ${
                  isRickroll187Mode 
                    ? 'text-yellow-300 hover:text-yellow-100' 
                    : 'text-indigo-600 hover:text-indigo-500'
                }`}
              >
                create a new account
              </Link>
            </p>
          </div>

          {/* Login Form */}
          <Formik
            initialValues={{
              username: isRickroll187Mode ? 'rickroll187' : '',
              password: '',
              remember_me: false
            }}
            validationSchema={loginValidationSchema}
            onSubmit={handleSubmit}
          >
            {({ isSubmitting, setFieldValue, values }) => (
              <Form className="mt-8 space-y-6">
                {/* Username Field */}
                <div>
                  <label htmlFor="username" className={`block text-sm font-medium ${
                    isRickroll187Mode ? 'text-yellow-200' : 'text-gray-700'
                  }`}>
                    Username
                  </label>
                  <motion.div
                    whileFocus="focus"
                    whileBlur="blur"
                    variants={inputVariants}
                  >
                    <Field
                      id="username"
                      name="username"
                      type="text"
                      autoComplete="username"
                      className={`mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 sm:text-sm ${
                        isRickroll187Mode
                          ? 'bg-black bg-opacity-30 border-yellow-300 text-yellow-100 placeholder-yellow-200 focus:ring-yellow-300'
                          : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500 focus:ring-indigo-500 focus:border-indigo-500'
                      }`}
                      placeholder="Enter your username"
                    />
                  </motion.div>
                  <ErrorMessage 
                    name="username" 
                    component="div" 
                    className="mt-1 text-sm text-red-400"
                  />
                </div>

                {/* Password Field */}
                <div>
                  <label htmlFor="password" className={`block text-sm font-medium ${
                    isRickroll187Mode ? 'text-yellow-200' : 'text-gray-700'
                  }`}>
                    Password
                  </label>
                  <motion.div 
                    className="mt-1 relative"
                    whileFocus="focus"
                    whileBlur="blur"
                    variants={inputVariants}
                  >
                    <Field
                      id="password"
                      name="password"
                      type={showPassword ? 'text' : 'password'}
                      autoComplete="current-password"
                      className={`block w-full px-3 py-2 pr-10 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 sm:text-sm ${
                        isRickroll187Mode
                          ? 'bg-black bg-opacity-30 border-yellow-300 text-yellow-100 placeholder-yellow-200 focus:ring-yellow-300'
                          : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500 focus:ring-indigo-500 focus:border-indigo-500'
                      }`}
                      placeholder="Enter your password"
                    />
                    <button
                      type="button"
                      className={`absolute inset-y-0 right-0 pr-3 flex items-center ${
                        isRickroll187Mode ? 'text-yellow-300 hover:text-yellow-100' : 'text-gray-400 hover:text-gray-600'
                      }`}
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      {showPassword ? '🙈' : '👁️'}
                    </button>
                  </motion.div>
                  <ErrorMessage 
                    name="password" 
                    component="div" 
                    className="mt-1 text-sm text-red-400"
                  />
                </div>

                {/* Remember Me & Forgot Password */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <Field
                      id="remember_me"
                      name="remember_me"
                      type="checkbox"
                      className={`h-4 w-4 rounded border-gray-300 ${
                        isRickroll187Mode
                          ? 'text-yellow-600 focus:ring-yellow-500'
                          : 'text-indigo-600 focus:ring-indigo-500'
                      }`}
                    />
                    <label htmlFor="remember_me" className={`ml-2 block text-sm ${
                      isRickroll187Mode ? 'text-yellow-200' : 'text-gray-900'
                    }`}>
                      Remember me
                    </label>
                  </div>

                  <div className="text-sm">
                    <Link
                      to="/forgot-password"
                      className={`font-medium ${
                        isRickroll187Mode
                          ? 'text-yellow-300 hover:text-yellow-100'
                          : 'text-indigo-600 hover:text-indigo-500'
                      }`}
                    >
                      Forgot your password?
                    </Link>
                  </div>
                </div>

                {/* Error Display */}
                <AnimatePresence>
                  {error && (
                    <motion.div
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      className="bg-red-50 border border-red-200 rounded-md p-3"
                    >
                      <p className="text-sm text-red-600">{error}</p>
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Submit Button */}
                <motion.button
                  type="submit"
                  disabled={isSubmitting || isLoading}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className={`group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed ${
                    isRickroll187Mode
                      ? 'bg-gradient-to-r from-yellow-600 to-red-600 hover:from-yellow-500 hover:to-red-500 focus:ring-yellow-500'
                      : 'bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500'
                  }`}
                  animate={legendaryAnimations && values.username === 'rickroll187' ? 
                    { boxShadow: ['0 0 0 rgba(255,215,0,0)', '0 0 20px rgba(255,215,0,0.8)', '0 0 0 rgba(255,215,0,0)'] } : 
                    {}
                  }
                  transition={{ duration: 1.5, repeat: legendaryAnimations ? Infinity : 0 }}
                >
                  {isSubmitting || isLoading ? (
                    <>
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      {isRickroll187Mode ? 'Authenticating legendary status...' : 'Signing in...'}
                    </>
                  ) : (
                    <>
                      <span className="absolute left-0 inset-y-0 flex items-center pl-3">
                        {isRickroll187Mode ? '🎸' : '🔐'}
                      </span>
                      {isRickroll187Mode ? '🎸 LEGENDARY LOGIN 🎸' : 'Sign in'}
                    </>
                  )}
                </motion.button>

                {/* Legendary Easter Egg */}
                <div className="text-center">
                  <button
                    type="button"
                    onClick={handleRickroll187Click}
                    className={`text-xs ${
                      isRickroll187Mode ? 'text-yellow-300' : 'text-gray-400'
                    } hover:underline`}
                  >
                    {isRickroll187Mode ? '🎸 Legendary Mode Active 🎸' : 'Activate Legendary Mode'}
                  </button>
                </div>
              </Form>
            )}
          </Formik>

          {/* Swiss Precision Footer */}
          <div className="text-center">
            <p className={`text-xs ${
              isRickroll187Mode ? 'text-yellow-200' : 'text-gray-500'
            }`}>
              {isRickroll187Mode ? 
                '🎸 Built with legendary Swiss precision by RICKROLL187 🎸' :
                'Built with Swiss precision by N3EXTPATH'
              }
            </p>
            {isRickroll187Mode && (
              <motion.p 
                className="text-xs text-yellow-300 mt-1"
                animate={{ opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
              </motion.p>
            )}
          </div>
        </motion.div>
      </AnimatePresence>

      {/* Legendary Background Animation */}
      {legendaryAnimations && (
        <div className="fixed inset-0 pointer-events-none">
          {[...Array(20)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute text-4xl"
              initial={{
                x: Math.random() * window.innerWidth,
                y: Math.random() * window.innerHeight,
                opacity: 0
              }}
              animate={{
                y: -100,
                opacity: [0, 1, 0],
                rotate: 360
              }}
              transition={{
                duration: 3,
                repeat: Infinity,
                delay: i * 0.2
              }}
            >
              🎸
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
};

export default LoginForm;

// Legendary startup message
if (process.env.NODE_ENV === 'development') {
  console.log('🎸🎸🎸 LEGENDARY LOGIN FORM LOADED! 🎸🎸🎸');
  console.log('Professional authentication with Swiss precision!');
  console.log('Special RICKROLL187 legendary mode included!');
  console.log('Built with maximum code bro energy!');
  console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
  console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
}
