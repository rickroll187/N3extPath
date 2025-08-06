// File: mobile/src/screens/auth/LegendaryRegisterScreen.tsx
/**
 * 📝🎸 N3EXTPATH - LEGENDARY REGISTER SCREEN 🎸📝
 * Professional account creation with Swiss precision
 * Built: 2025-08-06 01:45:06 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  Alert,
  Animated,
  Dimensions,
} from 'react-native';
import { TextInput, Button, Checkbox, RadioButton, Card, Chip } from 'react-native-paper';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { useDispatch, useSelector } from 'react-redux';
import * as Animatable from 'react-native-animatable';
import { Formik } from 'formik';
import * as Yup from 'yup';
import { Picker } from '@react-native-picker/picker';

// Import legendary components and services
import { RootStackParamList } from '../../navigation/LegendaryNavigation';
import { RootState } from '../../store';
import { registerUser } from '../../store/slices/authSlice';
import { legendaryTheme } from '../../theme/legendaryTheme';
import { LegendaryButton } from '../../components/ui/LegendaryButton';
import { LegendaryTextInput } from '../../components/ui/LegendaryTextInput';
import { LegendaryCard } from '../../components/ui/LegendaryCard';

type RegisterScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'Register'>;

const { width, height } = Dimensions.get('window');

// =====================================
// 📋 VALIDATION SCHEMA 📋
// =====================================

const RegisterValidationSchema = Yup.object().shape({
  username: Yup.string()
    .min(3, 'Username must be at least 3 characters')
    .max(50, 'Username must be less than 50 characters')
    .matches(/^[a-zA-Z0-9_-]+$/, 'Username can only contain letters, numbers, underscores, and hyphens')
    .required('Username is required for legendary access'),
  email: Yup.string()
    .email('Please enter a valid email address')
    .required('Email is required for legendary communications'),
  password: Yup.string()
    .min(8, 'Password must be at least 8 characters')
    .matches(/(?=.*[a-z])/, 'Password must contain at least one lowercase letter')
    .matches(/(?=.*[A-Z])/, 'Password must contain at least one uppercase letter')
    .matches(/(?=.*\d)/, 'Password must contain at least one number')
    .matches(/(?=.*[!@#$%^&*])/, 'Password must contain at least one special character')
    .required('Password is required for Swiss precision security'),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref('password')], 'Passwords must match')
    .required('Please confirm your password'),
  firstName: Yup.string()
    .min(2, 'First name must be at least 2 characters')
    .max(50, 'First name must be less than 50 characters')
    .required('First name is required'),
  lastName: Yup.string()
    .min(2, 'Last name must be at least 2 characters')
    .max(50, 'Last name must be less than 50 characters')
    .required('Last name is required'),
  jobTitle: Yup.string()
    .min(2, 'Job title must be at least 2 characters')
    .max(100, 'Job title must be less than 100 characters')
    .required('Job title is required for legendary workplace setup'),
  department: Yup.string()
    .required('Department is required for team organization'),
  agreeToTerms: Yup.boolean()
    .oneOf([true], 'You must agree to the Terms and Conditions'),
  subscribeNewsletter: Yup.boolean(),
});

interface RegisterFormValues {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
  firstName: string;
  lastName: string;
  jobTitle: string;
  department: string;
  phone?: string;
  agreeToTerms: boolean;
  subscribeNewsletter: boolean;
}

// =====================================
// 🏢 DEPARTMENT OPTIONS 🏢
// =====================================

const LEGENDARY_DEPARTMENTS = [
  'Engineering',
  'Product',
  'Design',
  'Marketing',
  'Sales',
  'Human Resources',
  'Finance',
  'Operations',
  'Customer Success',
  'Data Science',
  'Quality Assurance',
  'DevOps',
  'Executive Leadership',
  'Other'
];

// =====================================
// 🎸 LEGENDARY REGISTER SCREEN 🎸
// =====================================

export function LegendaryRegisterScreen(): JSX.Element {
  const navigation = useNavigation<RegisterScreenNavigationProp>();
  const dispatch = useDispatch();
  
  // Redux state
  const { isLoading, error } = useSelector((state: RootState) => state.auth);
  
  // Local state
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);
  const [passwordStrength, setPasswordStrength] = useState(0);
  const [usernameAvailable, setUsernameAvailable] = useState<boolean | null>(null);
  
  // Animation refs
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(30)).current;
  const scaleAnim = useRef(new Animated.Value(0.9)).current;
  const progressAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    console.log('📝🎸📝 LEGENDARY REGISTER SCREEN LOADED! 📝🎸📝');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Register screen loaded at: 2025-08-06 01:45:06 UTC`);

    // Start legendary animations
    startLegendaryAnimations();
  }, []);

  useEffect(() => {
    // Update progress animation
    Animated.timing(progressAnim, {
      toValue: (currentStep - 1) / 2, // 3 steps total (0, 0.5, 1)
      duration: 300,
      useNativeDriver: false,
    }).start();
  }, [currentStep]);

  const startLegendaryAnimations = () => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 800,
        useNativeDriver: true,
      }),
      Animated.spring(slideAnim, {
        toValue: 0,
        speed: 8,
        bounciness: 6,
        useNativeDriver: true,
      }),
      Animated.spring(scaleAnim, {
        toValue: 1,
        speed: 10,
        bounciness: 8,
        useNativeDriver: true,
      }),
    ]).start();
  };

  const calculatePasswordStrength = (password: string): number => {
    let strength = 0;
    
    // Length check
    if (password.length >= 8) strength += 20;
    if (password.length >= 12) strength += 10;
    
    // Character variety checks
    if (/[a-z]/.test(password)) strength += 15;
    if (/[A-Z]/.test(password)) strength += 15;
    if (/\d/.test(password)) strength += 15;
    if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) strength += 25;
    
    return Math.min(strength, 100);
  };

  const getPasswordStrengthColor = (strength: number): string => {
    if (strength < 30) return legendaryTheme.legendary.colors.error;
    if (strength < 60) return legendaryTheme.legendary.colors.warning;
    if (strength < 80) return legendaryTheme.legendary.colors.info;
    return legendaryTheme.legendary.colors.success;
  };

  const getPasswordStrengthText = (strength: number): string => {
    if (strength < 30) return 'Weak 😟';
    if (strength < 60) return 'Fair 🙂';
    if (strength < 80) return 'Good 😊';
    return 'Strong 🎸';
  };

  const checkUsernameAvailability = async (username: string) => {
    if (username.length < 3) {
      setUsernameAvailable(null);
      return;
    }

    try {
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Mock availability check (in real app, call API)
      const unavailableUsernames = ['admin', 'root', 'user', 'test', 'rickroll187'];
      const isAvailable = !unavailableUsernames.includes(username.toLowerCase());
      
      setUsernameAvailable(isAvailable);
      
      if (username.toLowerCase() === 'rickroll187') {
        Alert.alert(
          '👑 LEGENDARY FOUNDER DETECTED',
          'The username "rickroll187" is reserved for the legendary founder!\n\n🎸 RICKROLL187 is the creator of N3EXTPATH!\n\nPlease choose a different legendary username.',
          [{ text: 'Got it!', style: 'default' }]
        );
      }
    } catch (error) {
      console.error('Error checking username availability:', error);
      setUsernameAvailable(null);
    }
  };

  const handleRegister = async (values: RegisterFormValues) => {
    try {
      console.log('🚀 Creating legendary account...');
      console.log(`Username: ${values.username}`);
      console.log(`Email: ${values.email}`);
      console.log(`Name: ${values.firstName} ${values.lastName}`);
      console.log(`Department: ${values.department}`);
      console.log(`Job Title: ${values.jobTitle}`);

      // Dispatch register action
      const result = await dispatch(registerUser({
        username: values.username,
        email: values.email,
        password: values.password,
        first_name: values.firstName,
        last_name: values.lastName,
        job_title: values.jobTitle,
        department: values.department,
        phone: values.phone,
        subscribe_newsletter: values.subscribeNewsletter,
      }) as any);

      if (result.type === 'auth/registerUser/fulfilled') {
        const user = result.payload.user;
        
        console.log('✅ Legendary account created successfully!');
        console.log(`Welcome ${user.first_name}! 🎸`);
        
        Alert.alert(
          '🎉 LEGENDARY ACCOUNT CREATED!',
          `Welcome to N3EXTPATH, ${user.first_name}! 🎸\n\nYour legendary account has been created with Swiss precision!\n\n✅ Username: ${user.username}\n✅ Email: ${user.email}\n✅ Department: ${user.department}\n✅ Job Title: ${user.job_title}\n\nYou can now login and start your legendary journey!\n\nWE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!`,
          [
            {
              text: '🚀 Login Now',
              onPress: () => navigation.navigate('Login'),
            }
          ]
        );
      }
    } catch (error: any) {
      console.error('🚨 Registration error:', error);
      Alert.alert(
        '🚨 Registration Failed',
        error.message || 'Unable to create account. Please check your information and try again.',
        [{ text: 'Try Again', style: 'default' }]
      );
    }
  };

  const handleNext = () => {
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleBack = () => {
    console.log('🔙 Going back to login');
    navigation.goBack();
  };

  const handleLoginInstead = () => {
    console.log('🔐 Navigating to login');
    navigation.navigate('Login');
  };

  const renderProgressBar = () => {
    const progressWidth = progressAnim.interpolate({
      inputRange: [0, 1],
      outputRange: ['0%', '100%'],
    });

    return (
      <View style={styles.progressContainer}>
        <Text style={styles.progressText}>
          Step {currentStep} of 3 • Creating Legendary Account
        </Text>
        <View style={styles.progressBar}>
          <Animated.View 
            style={[
              styles.progressFill, 
              { width: progressWidth }
            ]} 
          />
        </View>
      </View>
    );
  };

  const renderStep1 = (values: RegisterFormValues, errors: any, touched: any, handleChange: any, handleBlur: any, setFieldValue: any) => (
    <Animatable.View 
      animation="fadeInRight"
      key="step1"
      style={styles.stepContainer}
    >
      <Text style={styles.stepTitle}>🎸 Basic Information</Text>
      <Text style={styles.stepDescription}>
        Let's start your legendary journey with some basic details
      </Text>

      {/* Username */}
      <View style={styles.inputContainer}>
        <LegendaryTextInput
          label="👤 Username"
          value={values.username}
          onChangeText={(text) => {
            handleChange('username')(text);
            checkUsernameAvailability(text);
          }}
          onBlur={handleBlur('username')}
          error={touched.username && !!errors.username}
          mode="outlined"
          left={<TextInput.Icon icon="account" />}
          right={
            usernameAvailable === true ? (
              <TextInput.Icon icon="check" color={legendaryTheme.legendary.colors.success} />
            ) : usernameAvailable === false ? (
              <TextInput.Icon icon="close" color={legendaryTheme.legendary.colors.error} />
            ) : undefined
          }
          style={styles.input}
          autoCapitalize="none"
          autoCorrect={false}
          autoComplete="username"
        />
        
        {touched.username && errors.username && (
          <Text style={styles.errorText}>{errors.username}</Text>
        )}
        
        {usernameAvailable === false && (
          <Text style={styles.errorText}>❌ Username not available</Text>
        )}
        
        {usernameAvailable === true && (
          <Text style={styles.successText}>✅ Username available!</Text>
        )}
      </View>

      {/* Email */}
      <View style={styles.inputContainer}>
        <LegendaryTextInput
          label="📧 Email"
          value={values.email}
          onChangeText={handleChange('email')}
          onBlur={handleBlur('email')}
          error={touched.email && !!errors.email}
          mode="outlined"
          left={<TextInput.Icon icon="email" />}
          style={styles.input}
          autoCapitalize="none"
          autoCorrect={false}
          autoComplete="email"
          keyboardType="email-address"
        />
        
        {touched.email && errors.email && (
          <Text style={styles.errorText}>{errors.email}</Text>
        )}
      </View>

      {/* Password */}
      <View style={styles.inputContainer}>
        <LegendaryTextInput
          label="🔑 Password"
          value={values.password}
          onChangeText={(text) => {
            handleChange('password')(text);
            setPasswordStrength(calculatePasswordStrength(text));
          }}
          onBlur={handleBlur('password')}
          error={touched.password && !!errors.password}
          mode="outlined"
          secureTextEntry={!showPassword}
          left={<TextInput.Icon icon="lock" />}
          right={
            <TextInput.Icon 
              icon={showPassword ? "eye-off" : "eye"}
              onPress={() => setShowPassword(!showPassword)}
            />
          }
          style={styles.input}
          autoComplete="password-new"
        />
        
        {values.password && (
          <View style={styles.passwordStrengthContainer}>
            <View style={styles.passwordStrengthBar}>
              <View 
                style={[
                  styles.passwordStrengthFill,
                  {
                    width: `${passwordStrength}%`,
                    backgroundColor: getPasswordStrengthColor(passwordStrength),
                  }
                ]} 
              />
            </View>
            <Text 
              style={[
                styles.passwordStrengthText,
                { color: getPasswordStrengthColor(passwordStrength) }
              ]}
            >
              {getPasswordStrengthText(passwordStrength)}
            </Text>
          </View>
        )}
        
        {touched.password && errors.password && (
          <Text style={styles.errorText}>{errors.password}</Text>
        )}
      </View>

      {/* Confirm Password */}
      <View style={styles.inputContainer}>
        <LegendaryTextInput
          label="🔐 Confirm Password"
          value={values.confirmPassword}
          onChangeText={handleChange('confirmPassword')}
          onBlur={handleBlur('confirmPassword')}
          error={touched.confirmPassword && !!errors.confirmPassword}
          mode="outlined"
          secureTextEntry={!showConfirmPassword}
          left={<TextInput.Icon icon="lock-check" />}
          right={
            <TextInput.Icon 
              icon={showConfirmPassword ? "eye-off" : "eye"}
              onPress={() => setShowConfirmPassword(!showConfirmPassword)}
            />
          }
          style={styles.input}
          autoComplete="password-new"
        />
        
        {touched.confirmPassword && errors.confirmPassword && (
          <Text style={styles.errorText}>{errors.confirmPassword}</Text>
        )}
      </View>
    </Animatable.View>
  );

  const renderStep2 = (values: RegisterFormValues, errors: any, touched: any, handleChange: any, handleBlur: any) => (
    <Animatable.View 
      animation="fadeInRight"
      key="step2"
      style={styles.stepContainer}
    >
      <Text style={styles.stepTitle}>👤 Personal Details</Text>
      <Text style={styles.stepDescription}>
        Tell us about yourself for the legendary workplace setup
      </Text>

      {/* First Name */}
      <View style={styles.inputContainer}>
        <LegendaryTextInput
          label="👨 First Name"
          value={values.firstName}
          onChangeText={handleChange('firstName')}
          onBlur={handleBlur('firstName')}
          error={touched.firstName && !!errors.firstName}
          mode="outlined"
          left={<TextInput.Icon icon="account" />}
          style={styles.input}
          autoCapitalize="words"
          autoComplete="name-given"
        />
        
        {touched.firstName && errors.firstName && (
          <Text style={styles.errorText}>{errors.firstName}</Text>
        )}
      </View>

      {/* Last Name */}
      <View style={styles.inputContainer}>
        <LegendaryTextInput
          label="👩 Last Name"
          value={values.lastName}
          onChangeText={handleChange('lastName')}
          onBlur={handleBlur('lastName')}
          error={touched.lastName && !!errors.lastName}
          mode="outlined"
          left={<TextInput.Icon icon="account" />}
          style={styles.input}
          autoCapitalize="words"
          autoComplete="name-family"
        />
        
        {touched.lastName && errors.lastName && (
          <Text style={styles.errorText}>{errors.lastName}</Text>
        )}
      </View>

      {/* Phone (Optional) */}
      <View style={styles.inputContainer}>
        <LegendaryTextInput
          label="📱 Phone (Optional)"
          value={values.phone}
          onChangeText={handleChange('phone')}
          onBlur={handleBlur('phone')}
          mode="outlined"
          left={<TextInput.Icon icon="phone" />}
          style={styles.input}
          keyboardType="phone-pad"
          autoComplete="tel"
        />
      </View>
    </Animatable.View>
  );

  const renderStep3 = (values: RegisterFormValues, errors: any, touched: any, handleChange: any, handleBlur: any, setFieldValue: any) => (
    <Animatable.View 
      animation="fadeInRight"
      key="step3"
      style={styles.stepContainer}
    >
      <Text style={styles.stepTitle}>🏢 Work Information</Text>
      <Text style={styles.stepDescription}>
        Set up your legendary workplace profile
      </Text>

      {/* Job Title */}
      <View style={styles.inputContainer}>
        <LegendaryTextInput
          label="💼 Job Title"
          value={values.jobTitle}
          onChangeText={handleChange('jobTitle')}
          onBlur={handleBlur('jobTitle')}
          error={touched.jobTitle && !!errors.jobTitle}
          mode="outlined"
          left={<TextInput.Icon icon="briefcase" />}
          style={styles.input}
          autoCapitalize="words"
        />
        
        {touched.jobTitle && errors.jobTitle && (
          <Text style={styles.errorText}>{errors.jobTitle}</Text>
        )}
      </View>

      {/* Department */}
      <View style={styles.inputContainer}>
        <Text style={styles.pickerLabel}>🏢 Department</Text>
        <View style={styles.pickerContainer}>
          <Picker
            selectedValue={values.department}
            onValueChange={(value) => setFieldValue('department', value)}
            style={styles.picker}
          >
            <Picker.Item label="Select Department..." value="" />
            {LEGENDARY_DEPARTMENTS.map((dept) => (
              <Picker.Item key={dept} label={dept} value={dept} />
            ))}
          </Picker>
        </View>
        
        {touched.department && errors.department && (
          <Text style={styles.errorText}>{errors.department}</Text>
        )}
      </View>

      {/* Terms and Conditions */}
      <View style={styles.checkboxContainer}>
        <Checkbox
          status={values.agreeToTerms ? 'checked' : 'unchecked'}
          onPress={() => setFieldValue('agreeToTerms', !values.agreeToTerms)}
          color={legendaryTheme.colors.primary}
        />
        <Text style={styles.checkboxText}>
          I agree to the Terms and Conditions and Privacy Policy
        </Text>
      </View>
      
      {touched.agreeToTerms && errors.agreeToTerms && (
        <Text style={styles.errorText}>{errors.agreeToTerms}</Text>
      )}

      {/* Newsletter Subscription */}
      <View style={styles.checkboxContainer}>
        <Checkbox
          status={values.subscribeNewsletter ? 'checked' : 'unchecked'}
          onPress={() => setFieldValue('subscribeNewsletter', !values.subscribeNewsletter)}
          color={legendaryTheme.colors.primary}
        />
        <Text style={styles.checkboxText}>
          Subscribe to legendary updates and code bro energy newsletters
        </Text>
      </View>
    </Animatable.View>
  );

  return (
    <KeyboardAvoidingView 
      style={styles.container} 
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <LinearGradient
        colors={[
          legendaryTheme.legendary.colors.primary,
          legendaryTheme.legendary.colors.primaryVariant,
          legendaryTheme.legendary.colors.legendary,
        ]}
        style={styles.gradient}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <ScrollView 
          contentContainerStyle={styles.scrollContainer}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
        >
          {/* Header Section */}
          <Animated.View 
            style={[
              styles.header,
              {
                opacity: fadeAnim,
                transform: [
                  { translateY: slideAnim },
                  { scale: scaleAnim },
                ],
              },
            ]}
          >
            {/* Back Button */}
            <LegendaryButton
              mode="text"
              onPress={handleBack}
              style={styles.backButton}
              icon="arrow-back"
              labelStyle={styles.backButtonText}
            >
              Back
            </LegendaryButton>

            {/* Logo and Title */}
            <Animatable.View 
              animation="bounceIn" 
              delay={300}
              style={styles.logoContainer}
            >
              <Ionicons 
                name="person-add" 
                size={60} 
                color={legendaryTheme.legendary.colors.legendary} 
              />
            </Animatable.View>

            <Animatable.Text 
              animation="fadeInUp" 
              delay={500}
              style={styles.title}
            >
              📝 Join N3EXTPATH
            </Animatable.Text>

            <Animatable.Text 
              animation="fadeInUp" 
              delay={700}
              style={styles.subtitle}
            >
              Create your legendary account
            </Animatable.Text>

            {/* Progress Bar */}
            <Animatable.View 
              animation="fadeIn" 
              delay={900}
              style={styles.progressWrapper}
            >
              {renderProgressBar()}
            </Animatable.View>
          </Animated.View>

          {/* Register Form */}
          <Animated.View 
            style={[
              styles.formContainer,
              {
                opacity: fadeAnim,
                transform: [{ translateY: slideAnim }],
              },
            ]}
          >
            <LegendaryCard style={styles.formCard}>
              <Formik
                initialValues={{
                  username: '',
                  email: '',
                  password: '',
                  confirmPassword: '',
                  firstName: '',
                  lastName: '',
                  jobTitle: '',
                  department: '',
                  phone: '',
                  agreeToTerms: false,
                  subscribeNewsletter: true,
                }}
                validationSchema={RegisterValidationSchema}
                onSubmit={handleRegister}
              >
                {({ 
                  handleChange, 
                  handleBlur, 
                  handleSubmit, 
                  values, 
                  errors, 
                  touched, 
                  setFieldValue,
                  isValid
                }) => (
                  <View style={styles.form}>
                    {/* Render Current Step */}
                    {currentStep === 1 && renderStep1(values, errors, touched, handleChange, handleBlur, setFieldValue)}
                    {currentStep === 2 && renderStep2(values, errors, touched, handleChange, handleBlur)}
                    {currentStep === 3 && renderStep3(values, errors, touched, handleChange, handleBlur, setFieldValue)}

                    {/* Error Display */}
                    {error && (
                      <Animatable.View 
                        animation="shake"
                        style={styles.errorContainer}
                      >
                        <Text style={styles.errorMessage}>
                          🚨 {error}
                        </Text>
                      </Animatable.View>
                    )}

                    {/* Navigation Buttons */}
                    <View style={styles.buttonContainer}>
                      {currentStep > 1 && (
                        <LegendaryButton
                          mode="outlined"
                          onPress={handlePrevious}
                          style={styles.secondaryButton}
                          contentStyle={styles.buttonContent}
                          icon="arrow-left"
                        >
                          Previous
                        </LegendaryButton>
                      )}

                      {currentStep < 3 ? (
                        <LegendaryButton
                          mode="contained"
                          onPress={handleNext}
                          style={styles.primaryButton}
                          contentStyle={styles.buttonContent}
                          icon="arrow-right"
                          disabled={
                            currentStep === 1 && (
                              !values.username || 
                              !values.email || 
                              !values.password || 
                              !values.confirmPassword ||
                              !!errors.username ||
                              !!errors.email ||
                              !!errors.password ||
                              !!errors.confirmPassword ||
                              usernameAvailable === false
                            )
                          }
                        >
                          Next Step
                        </LegendaryButton>
                      ) : (
                        <LegendaryButton
                          mode="contained"
                          onPress={handleSubmit}
                          style={styles.primaryButton}
                          contentStyle={styles.buttonContent}
                          labelStyle={styles.registerButtonText}
                          loading={isLoading}
                          disabled={isLoading || !isValid}
                          icon="account-plus"
                        >
                          {isLoading ? 'Creating Account...' : '🎸 Create Legendary Account'}
                        </LegendaryButton>
                      )}
                    </View>

                    {/* Login Link */}
                    <View style={styles.loginContainer}>
                      <Text style={styles.loginText}>
                        Already have an account?
                      </Text>
                      <LegendaryButton
                        mode="text"
                        onPress={handleLoginInstead}
                        style={styles.loginButton}
                        labelStyle={styles.loginButtonText}
                      >
                        🔐 Login Instead
                      </LegendaryButton>
                    </View>
                  </View>
                )}
              </Formik>
            </LegendaryCard>
          </Animated.View>

          {/* Footer */}
          <Animatable.View 
            animation="fadeInUp" 
            delay={1900}
            style={styles.footer}
          >
            <Text style={styles.footerText}>
              Built with Swiss precision and infinite code bro energy
            </Text>
            <Text style={styles.footerContact}>
              👑 RICKROLL187 • letstalktech010@gmail.com
            </Text>
            <Text style={styles.footerMotto}>
              🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸
            </Text>
          </Animatable.View>
        </ScrollView>
      </LinearGradient>
    </KeyboardAvoidingView>
  );
}

// =====================================
// 🎨 LEGENDARY STYLES 🎨
// =====================================

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  gradient: {
    flex: 1,
  },
  scrollContainer: {
    flexGrow: 1,
    paddingHorizontal: legendaryTheme.legendary.spacing.lg,
    paddingTop: Platform.OS === 'ios' ? 60 : 40,
    paddingBottom: legendaryTheme.legendary.spacing.lg,
  },
  header: {
    alignItems: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  backButton: {
    alignSelf: 'flex-start',
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  backButtonText: {
    color: legendaryTheme.legendary.colors.legendary,
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
  },
  logoContainer: {
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  title: {
    fontSize: legendaryTheme.legendary.typography.fontSize['3xl'],
    fontFamily: legendaryTheme.legendary.typography.fontFamily.legendaryBold,
    color: legendaryTheme.legendary.colors.legendary,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.sm,
    textShadowColor: 'rgba(0, 0, 0, 0.3)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
  },
  subtitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.lg,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.regular,
    color: 'rgba(255, 255, 255, 0.9)',
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
    textShadowColor: 'rgba(0, 0, 0, 0.3)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
  },
  progressWrapper: {
    width: '100%',
  },
  progressContainer: {
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  progressText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: 'rgba(255, 255, 255, 0.8)',
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  progressBar: {
    height: 4,
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    borderRadius: 2,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: legendaryTheme.legendary.colors.legendary,
    borderRadius: 2,
  },
  formContainer: {
    flex: 1,
  },
  formCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: legendaryTheme.legendary.borders.radius.xl,
    padding: legendaryTheme.legendary.spacing.lg,
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.3,
    shadowRadius: 6,
  },
  form: {
    gap: legendaryTheme.legendary.spacing.md,
  },
  stepContainer: {
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  stepTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xl,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.legendary.colors.primary,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  stepDescription: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.legendary.colors.onSurface,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  inputContainer: {
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  input: {
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
  },
  pickerLabel: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.legendary.colors.onSurface,
    marginBottom: legendaryTheme.legendary.spacing.xs,
    marginLeft: legendaryTheme.legendary.spacing.sm,
  },
  pickerContainer: {
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderRadius: legendaryTheme.legendary.borders.radius.md,
    borderWidth: 1,
    borderColor: legendaryTheme.legendary.colors.outline,
  },
  picker: {
    height: 56,
  },
  passwordStrengthContainer: {
    marginTop: legendaryTheme.legendary.spacing.xs,
    flexDirection: 'row',
    alignItems: 'center',
    gap: legendaryTheme.legendary.spacing.sm,
  },
  passwordStrengthBar: {
    flex: 1,
    height: 4,
    backgroundColor: 'rgba(0, 0, 0, 0.1)',
    borderRadius: 2,
    overflow: 'hidden',
  },
  passwordStrengthFill: {
    height: '100%',
    borderRadius: 2,
  },
  passwordStrengthText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
  },
  checkboxContainer: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  checkboxText: {
    flex: 1,
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.legendary.colors.onSurface,
    marginLeft: legendaryTheme.legendary.spacing.xs,
    lineHeight: 20,
  },
  errorText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: legendaryTheme.legendary.colors.error,
    marginTop: legendaryTheme.legendary.spacing.xs,
    marginLeft: legendaryTheme.legendary.spacing.sm,
  },
  successText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: legendaryTheme.legendary.colors.success,
    marginTop: legendaryTheme.legendary.spacing.xs,
    marginLeft: legendaryTheme.legendary.spacing.sm,
  },
  errorContainer: {
    backgroundColor: legendaryTheme.legendary.colors.errorBackground,
    borderRadius: legendaryTheme.legendary.borders.radius.md,
    padding: legendaryTheme.legendary.spacing.md,
    marginVertical: legendaryTheme.legendary.spacing.sm,
  },
  errorMessage: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.legendary.colors.error,
    textAlign: 'center',
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
  },
  buttonContainer: {
    flexDirection: 'row',
    gap: legendaryTheme.legendary.spacing.md,
    marginTop: legendaryTheme.legendary.spacing.lg,
  },
  primaryButton: {
    flex: 1,
    backgroundColor: legendaryTheme.legendary.colors.primary,
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
    elevation: 4,
  },
  secondaryButton: {
    flex: 1,
    borderColor: legendaryTheme.legendary.colors.primary,
    borderWidth: 2,
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
  },
  buttonContent: {
    height: 56,
  },
  registerButtonText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.lg,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.legendary.colors.onPrimary,
  },
  loginContainer: {
    alignItems: 'center',
    marginTop: legendaryTheme.legendary.spacing.lg,
  },
  loginText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.legendary.colors.onSurface,
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  loginButton: {
    padding: 0,
  },
  loginButtonText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.legendary.colors.primary,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
  },
  footer: {
    alignItems: 'center',
    marginTop: legendaryTheme.legendary.spacing.xl,
    paddingTop: legendaryTheme.legendary.spacing.lg,
  },
  footerText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: 'rgba(255, 255, 255, 0.7)',
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  footerContact: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: legendaryTheme.legendary.colors.legendary,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  footerMotto: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    color: 'rgba(255, 255, 255, 0.6)',
    textAlign: 'center',
    fontStyle: 'italic',
  },
});

// =====================================
// 🎸 LEGENDARY EXPORTS 🎸
// =====================================

export default LegendaryRegisterScreen;

// =====================================
// 🎸 LEGENDARY COMPLETION MESSAGE 🎸
// =====================================

console.log('🎸🎸🎸 LEGENDARY REGISTER SCREEN LOADED! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Register screen loaded at: 2025-08-06 01:45:06 UTC`);
console.log('📝 Multi-step registration: SWISS PRECISION');
console.log('🔐 Password strength meter: LEGENDARY SECURITY');
console.log('✅ Username availability: REAL-TIME VALIDATION');
console.log('👑 RICKROLL187 protection: FOUNDER RESERVED');
console.log('🏢 Department selection: PROFESSIONAL SETUP');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
