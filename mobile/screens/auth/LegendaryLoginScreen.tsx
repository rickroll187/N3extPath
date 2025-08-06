// File: mobile/src/screens/auth/LegendaryLoginScreen.tsx
/**
 * 🔐🎸 N3EXTPATH - LEGENDARY LOGIN SCREEN 🎸🔐
 * Professional authentication with Swiss precision
 * Built: 2025-08-06 01:37:48 UTC by RICKROLL187
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
import { TextInput, Button, Checkbox, Card, ActivityIndicator } from 'react-native-paper';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { useDispatch, useSelector } from 'react-redux';
import * as Animatable from 'react-native-animatable';
import { Formik } from 'formik';
import * as Yup from 'yup';

// Import legendary components and services
import { RootStackParamList } from '../../navigation/LegendaryNavigation';
import { RootState } from '../../store';
import { loginUser } from '../../store/slices/authSlice';
import { legendaryTheme } from '../../theme/legendaryTheme';
import { LegendaryButton } from '../../components/ui/LegendaryButton';
import { LegendaryTextInput } from '../../components/ui/LegendaryTextInput';
import { LegendaryCard } from '../../components/ui/LegendaryCard';

type LoginScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'Login'>;

const { width, height } = Dimensions.get('window');

// =====================================
// 📋 VALIDATION SCHEMA 📋
// =====================================

const LoginValidationSchema = Yup.object().shape({
  username: Yup.string()
    .min(3, 'Username must be at least 3 characters')
    .max(50, 'Username must be less than 50 characters')
    .required('Username is required for legendary access'),
  password: Yup.string()
    .min(8, 'Password must be at least 8 characters')
    .required('Password is required for Swiss precision security'),
});

interface LoginFormValues {
  username: string;
  password: string;
  rememberMe: boolean;
}

// =====================================
// 🎸 LEGENDARY LOGIN SCREEN 🎸
// =====================================

export function LegendaryLoginScreen(): JSX.Element {
  const navigation = useNavigation<LoginScreenNavigationProp>();
  const dispatch = useDispatch();
  
  // Redux state
  const { isLoading, error } = useSelector((state: RootState) => state.auth);
  
  // Local state
  const [showPassword, setShowPassword] = useState(false);
  const [isRickroll187, setIsRickroll187] = useState(false);
  
  // Animation refs
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(30)).current;
  const scaleAnim = useRef(new Animated.Value(0.9)).current;

  useEffect(() => {
    console.log('🔐🎸🔐 LEGENDARY LOGIN SCREEN LOADED! 🔐🎸🔐');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Login screen loaded at: ${new Date().toISOString()}`);

    // Start legendary animations
    startLegendaryAnimations();
  }, []);

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

  const handleLogin = async (values: LoginFormValues) => {
    try {
      console.log('🚀 Attempting legendary login...');
      console.log(`Username: ${values.username}`);
      console.log(`Remember me: ${values.rememberMe}`);
      
      // Check if this is RICKROLL187 founder
      if (values.username.toLowerCase() === 'rickroll187') {
        setIsRickroll187(true);
        console.log('👑 RICKROLL187 FOUNDER LOGIN DETECTED!');
        console.log('🎸 LEGENDARY FOUNDER ACCESS INITIATED!');
      }

      // Dispatch login action
      const result = await dispatch(loginUser({
        username: values.username,
        password: values.password,
        rememberMe: values.rememberMe,
      }) as any);

      if (result.type === 'auth/loginUser/fulfilled') {
        const user = result.payload.user;
        
        if (user.username === 'rickroll187') {
          console.log('👑🎸👑 LEGENDARY FOUNDER RICKROLL187 LOGGED IN! 👑🎸👑');
          console.log('🚀 INFINITE CODE BRO ENERGY ACTIVATED!');
          console.log('⚙️ SWISS PRECISION MODE: MAXIMUM!');
          console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
          
          Alert.alert(
            '👑 LEGENDARY FOUNDER ACCESS',
            '🎸 Welcome back RICKROLL187!\n\nLegendary Founder privileges activated!\n\n⚙️ Swiss Precision: MAXIMUM\n💪 Code Bro Energy: INFINITE\n🏆 Platform Status: LEGENDARY\n\nWE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!',
            [{ text: '🚀 Enter Legendary Platform', style: 'default' }]
          );
        } else if (user.is_legendary) {
          console.log('🎸 Legendary user logged in!');
          Alert.alert(
            '🎸 LEGENDARY ACCESS GRANTED',
            `Welcome back ${user.first_name}!\n\nLegendary user privileges activated!\n\n⚙️ Swiss Precision: HIGH\n💪 Code Bro Energy: MAXIMUM`,
            [{ text: '🚀 Continue', style: 'default' }]
          );
        } else {
          console.log('✅ Standard user logged in successfully!');
        }
      }
    } catch (error: any) {
      console.error('🚨 Login error:', error);
      Alert.alert(
        '🚨 Login Failed',
        error.message || 'Unable to authenticate. Please check your credentials and try again.',
        [{ text: 'Try Again', style: 'default' }]
      );
    }
  };

  const handleForgotPassword = () => {
    console.log('🔑 Forgot password requested');
    Alert.alert(
      '🔑 Password Recovery',
      'Password recovery feature coming soon!\n\nFor immediate assistance, contact:\nletstalktech010@gmail.com\n\nBuilt with Swiss precision by RICKROLL187!',
      [{ text: 'OK', style: 'default' }]
    );
  };

  const handleCreateAccount = () => {
    console.log('📝 Navigating to registration');
    navigation.navigate('Register');
  };

  const handleBack = () => {
    console.log('🔙 Going back to welcome');
    navigation.goBack();
  };

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
                name="lock-closed" 
                size={60} 
                color={legendaryTheme.legendary.colors.legendary} 
              />
            </Animatable.View>

            <Animatable.Text 
              animation="fadeInUp" 
              delay={500}
              style={styles.title}
            >
              🔐 Legendary Login
            </Animatable.Text>

            <Animatable.Text 
              animation="fadeInUp" 
              delay={700}
              style={styles.subtitle}
            >
              Access your legendary workspace
            </Animatable.Text>

            {isRickroll187 && (
              <Animatable.View 
                animation="pulse" 
                iterationCount="infinite"
                style={styles.founderBadge}
              >
                <Text style={styles.founderBadgeText}>
                  👑 FOUNDER ACCESS DETECTED 👑
                </Text>
              </Animatable.View>
            )}
          </Animated.View>

          {/* Login Form */}
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
                  password: '',
                  rememberMe: false,
                }}
                validationSchema={LoginValidationSchema}
                onSubmit={handleLogin}
              >
                {({ 
                  handleChange, 
                  handleBlur, 
                  handleSubmit, 
                  values, 
                  errors, 
                  touched, 
                  setFieldValue 
                }) => (
                  <View style={styles.form}>
                    {/* Username Input */}
                    <Animatable.View 
                      animation="fadeInLeft" 
                      delay={900}
                      style={styles.inputContainer}
                    >
                      <LegendaryTextInput
                        label="👤 Username"
                        value={values.username}
                        onChangeText={(text) => {
                          handleChange('username')(text);
                          // Check for RICKROLL187
                          if (text.toLowerCase() === 'rickroll187') {
                            setIsRickroll187(true);
                          } else {
                            setIsRickroll187(false);
                          }
                        }}
                        onBlur={handleBlur('username')}
                        error={touched.username && !!errors.username}
                        mode="outlined"
                        left={<TextInput.Icon icon="account" />}
                        style={[
                          styles.input,
                          isRickroll187 && styles.founderInput
                        ]}
                        theme={{
                          colors: {
                            primary: isRickroll187 
                              ? legendaryTheme.legendary.colors.legendary
                              : legendaryTheme.colors.primary,
                          },
                        }}
                        autoCapitalize="none"
                        autoCorrect={false}
                        autoComplete="username"
                      />
                      
                      {touched.username && errors.username && (
                        <Text style={styles.errorText}>{errors.username}</Text>
                      )}
                    </Animatable.View>

                    {/* Password Input */}
                    <Animatable.View 
                      animation="fadeInRight" 
                      delay={1100}
                      style={styles.inputContainer}
                    >
                      <LegendaryTextInput
                        label="🔑 Password"
                        value={values.password}
                        onChangeText={handleChange('password')}
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
                        style={[
                          styles.input,
                          isRickroll187 && styles.founderInput
                        ]}
                        theme={{
                          colors: {
                            primary: isRickroll187 
                              ? legendaryTheme.legendary.colors.legendary
                              : legendaryTheme.colors.primary,
                          },
                        }}
                        autoComplete="password"
                      />
                      
                      {touched.password && errors.password && (
                        <Text style={styles.errorText}>{errors.password}</Text>
                      )}
                    </Animatable.View>

                    {/* Remember Me & Forgot Password */}
                    <Animatable.View 
                      animation="fadeInUp" 
                      delay={1300}
                      style={styles.optionsContainer}
                    >
                      <View style={styles.rememberMeContainer}>
                        <Checkbox
                          status={values.rememberMe ? 'checked' : 'unchecked'}
                          onPress={() => setFieldValue('rememberMe', !values.rememberMe)}
                          color={isRickroll187 
                            ? legendaryTheme.legendary.colors.legendary
                            : legendaryTheme.colors.primary
                          }
                        />
                        <Text style={styles.rememberMeText}>Remember me</Text>
                      </View>

                      <LegendaryButton
                        mode="text"
                        onPress={handleForgotPassword}
                        style={styles.forgotPasswordButton}
                        labelStyle={styles.forgotPasswordText}
                      >
                        Forgot Password?
                      </LegendaryButton>
                    </Animatable.View>

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

                    {/* Login Button */}
                    <Animatable.View 
                      animation="bounceIn" 
                      delay={1500}
                      style={styles.loginButtonContainer}
                    >
                      <LegendaryButton
                        mode="contained"
                        onPress={handleSubmit}
                        style={[
                          styles.loginButton,
                          isRickroll187 && styles.founderLoginButton
                        ]}
                        contentStyle={styles.loginButtonContent}
                        labelStyle={[
                          styles.loginButtonText,
                          isRickroll187 && styles.founderLoginButtonText
                        ]}
                        loading={isLoading}
                        disabled={isLoading}
                        icon={isRickroll187 ? "crown" : "login"}
                      >
                        {isLoading 
                          ? 'Authenticating...' 
                          : isRickroll187 
                            ? '👑 Enter Legendary Platform' 
                            : '🚀 Login'
                        }
                      </LegendaryButton>
                    </Animatable.View>

                    {/* Create Account Link */}
                    <Animatable.View 
                      animation="fadeIn" 
                      delay={1700}
                      style={styles.createAccountContainer}
                    >
                      <Text style={styles.createAccountText}>
                        Don't have an account yet?
                      </Text>
                      <LegendaryButton
                        mode="text"
                        onPress={handleCreateAccount}
                        style={styles.createAccountButton}
                        labelStyle={styles.createAccountButtonText}
                      >
                        📝 Create Legendary Account
                      </LegendaryButton>
                    </Animatable.View>
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
    marginBottom: legendaryTheme.legendary.spacing.xl,
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
    textShadowColor: 'rgba(0, 0, 0, 0.3)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
  },
  founderBadge: {
    backgroundColor: legendaryTheme.legendary.colors.legendary,
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
    paddingHorizontal: legendaryTheme.legendary.spacing.lg,
    paddingVertical: legendaryTheme.legendary.spacing.sm,
    marginTop: legendaryTheme.legendary.spacing.md,
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  founderBadgeText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.legendary.colors.primary,
    textAlign: 'center',
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
    gap: legendaryTheme.legendary.spacing.lg,
  },
  inputContainer: {
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  input: {
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
  },
  founderInput: {
    backgroundColor: 'rgba(255, 215, 0, 0.1)',
    borderColor: legendaryTheme.legendary.colors.legendary,
    borderWidth: 2,
  },
  errorText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: legendaryTheme.legendary.colors.error,
    marginTop: legendaryTheme.legendary.spacing.xs,
    marginLeft: legendaryTheme.legendary.spacing.md,
  },
  optionsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  rememberMeContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  rememberMeText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.legendary.colors.onSurface,
    marginLeft: legendaryTheme.legendary.spacing.xs,
  },
  forgotPasswordButton: {
    padding: 0,
  },
  forgotPasswordText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: legendaryTheme.legendary.colors.primary,
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
  loginButtonContainer: {
    marginTop: legendaryTheme.legendary.spacing.md,
  },
  loginButton: {
    backgroundColor: legendaryTheme.legendary.colors.primary,
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
    elevation: 4,
  },
  founderLoginButton: {
    backgroundColor: legendaryTheme.legendary.colors.legendary,
  },
  loginButtonContent: {
    height: 56,
  },
  loginButtonText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.lg,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.legendary.colors.onPrimary,
  },
  founderLoginButtonText: {
    color: legendaryTheme.legendary.colors.primary,
  },
  createAccountContainer: {
    alignItems: 'center',
    marginTop: legendaryTheme.legendary.spacing.md,
  },
  createAccountText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.legendary.colors.onSurface,
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  createAccountButton: {
    padding: 0,
  },
  createAccountButtonText: {
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

export default LegendaryLoginScreen;

// =====================================
// 🎸 LEGENDARY COMPLETION MESSAGE 🎸
// =====================================

console.log('🎸🎸🎸 LEGENDARY LOGIN SCREEN LOADED! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Login screen loaded at: 2025-08-06 01:37:48 UTC`);
console.log('🔐 Authentication forms: SWISS PRECISION');
console.log('👑 RICKROLL187 founder detection: LEGENDARY');
console.log('🎨 Legendary animations: INFINITE ENERGY');
console.log('⚙️ Form validation: MAXIMUM SECURITY');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
