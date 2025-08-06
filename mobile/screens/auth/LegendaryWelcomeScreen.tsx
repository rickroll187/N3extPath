// File: mobile/src/screens/auth/LegendaryWelcomeScreen.tsx
/**
 * 🎉🎸 N3EXTPATH - LEGENDARY WELCOME SCREEN 🎸🎉
 * Professional welcome experience with Swiss precision
 * Built: 2025-08-06 01:32:02 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Dimensions,
  Animated,
  TouchableOpacity,
  ImageBackground,
  StatusBar,
  Platform,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import * as Animatable from 'react-native-animatable';

// Import legendary components and types
import { RootStackParamList } from '../../navigation/LegendaryNavigation';
import { legendaryTheme } from '../../theme/legendaryTheme';
import { LegendaryButton } from '../../components/ui/LegendaryButton';
import { LegendaryCard } from '../../components/ui/LegendaryCard';

type WelcomeScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'Welcome'>;

const { width, height } = Dimensions.get('window');

// =====================================
// 🎸 LEGENDARY WELCOME SCREEN 🎸
// =====================================

export function LegendaryWelcomeScreen(): JSX.Element {
  const navigation = useNavigation<WelcomeScreenNavigationProp>();
  
  // Animation values
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(50)).current;
  const scaleAnim = useRef(new Animated.Value(0.8)).current;
  const rotateAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    console.log('🎉🎸🎉 LEGENDARY WELCOME SCREEN LOADED! 🎉🎸🎉');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Welcome screen loaded at: ${new Date().toISOString()}`);

    // Start legendary animations
    startLegendaryAnimations();
  }, []);

  const startLegendaryAnimations = () => {
    // Parallel animations for legendary entrance
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 1000,
        useNativeDriver: true,
      }),
      Animated.spring(slideAnim, {
        toValue: 0,
        speed: 5,
        bounciness: 8,
        useNativeDriver: true,
      }),
      Animated.spring(scaleAnim, {
        toValue: 1,
        speed: 8,
        bounciness: 10,
        useNativeDriver: true,
      }),
    ]).start();

    // Continuous rotation for legendary icon
    Animated.loop(
      Animated.timing(rotateAnim, {
        toValue: 1,
        duration: 4000,
        useNativeDriver: true,
      })
    ).start();
  };

  const handleGetStarted = () => {
    console.log('🚀 User starting legendary journey!');
    navigation.navigate('Login');
  };

  const handleCreateAccount = () => {
    console.log('📝 User creating legendary account!');
    navigation.navigate('Register');
  };

  // Rotation interpolation
  const rotateInterpolate = rotateAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  return (
    <>
      <StatusBar barStyle="light-content" backgroundColor={legendaryTheme.colors.primary} />
      
      <ImageBackground
        source={{ uri: 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1000&q=80' }}
        style={styles.backgroundImage}
        blurRadius={2}
      >
        <LinearGradient
          colors={[
            'rgba(26, 26, 26, 0.9)',
            'rgba(255, 215, 0, 0.1)',
            'rgba(26, 26, 26, 0.9)',
          ]}
          style={styles.gradient}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
        >
          <View style={styles.container}>
            
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
              {/* Legendary Logo with Rotation */}
              <Animated.View
                style={[
                  styles.logoContainer,
                  {
                    transform: [{ rotate: rotateInterpolate }],
                  },
                ]}
              >
                <Ionicons 
                  name="musical-notes" 
                  size={80} 
                  color={legendaryTheme.colors.legendary} 
                />
              </Animated.View>

              {/* App Title */}
              <Animatable.Text 
                animation="fadeInUp" 
                delay={500}
                style={styles.appTitle}
              >
                N3EXTPATH
              </Animatable.Text>

              <Animatable.Text 
                animation="fadeInUp" 
                delay={700}
                style={styles.appSubtitle}
              >
                LEGENDARY
              </Animatable.Text>

              {/* Legendary Motto */}
              <Animatable.Text 
                animation="fadeInUp" 
                delay={900}
                style={styles.motto}
              >
                🎸 WE ARE CODE BROS THE CREATE THE BEST 🎸
              </Animatable.Text>
              
              <Animatable.Text 
                animation="fadeInUp" 
                delay={1100}
                style={styles.mottoSecond}
              >
                💪 AND CRACK JOKES TO HAVE FUN! 💪
              </Animatable.Text>
            </Animated.View>

            {/* Features Section */}
            <Animated.View 
              style={[
                styles.featuresContainer,
                {
                  opacity: fadeAnim,
                  transform: [{ translateY: slideAnim }],
                },
              ]}
            >
              <Animatable.Text 
                animation="fadeInLeft" 
                delay={1300}
                style={styles.featuresTitle}
              >
                🏆 Legendary Features
              </Animatable.Text>

              <View style={styles.featuresGrid}>
                <Animatable.View 
                  animation="bounceIn" 
                  delay={1500}
                  style={styles.featureItem}
                >
                  <Ionicons name="trending-up" size={24} color={legendaryTheme.colors.legendary} />
                  <Text style={styles.featureText}>📊 Performance Reviews</Text>
                </Animatable.View>

                <Animatable.View 
                  animation="bounceIn" 
                  delay={1700}
                  style={styles.featureItem}
                >
                  <Ionicons name="target" size={24} color={legendaryTheme.colors.legendary} />
                  <Text style={styles.featureText}>🎯 OKR Management</Text>
                </Animatable.View>

                <Animatable.View 
                  animation="bounceIn" 
                  delay={1900}
                  style={styles.featureItem}
                >
                  <Ionicons name="people" size={24} color={legendaryTheme.colors.legendary} />
                  <Text style={styles.featureText}>👥 Team Collaboration</Text>
                </Animatable.View>

                <Animatable.View 
                  animation="bounceIn" 
                  delay={2100}
                  style={styles.featureItem}
                >
                  <Ionicons name="analytics" size={24} color={legendaryTheme.colors.legendary} />
                  <Text style={styles.featureText}>📈 Swiss Precision Analytics</Text>
                </Animatable.View>
              </View>
            </Animated.View>

            {/* Bottom Action Section */}
            <Animated.View 
              style={[
                styles.actionsContainer,
                {
                  opacity: fadeAnim,
                  transform: [{ translateY: slideAnim }],
                },
              ]}
            >
              <LegendaryCard style={styles.actionCard}>
                <Animatable.View 
                  animation="fadeInUp" 
                  delay={2300}
                >
                  <Text style={styles.welcomeText}>
                    Welcome to the legendary HR experience! 
                  </Text>
                  <Text style={styles.descriptionText}>
                    Built with Swiss precision and infinite code bro energy by RICKROLL187
                  </Text>
                </Animatable.View>

                {/* Action Buttons */}
                <View style={styles.buttonContainer}>
                  <Animatable.View 
                    animation="bounceInLeft" 
                    delay={2500}
                    style={styles.buttonWrapper}
                  >
                    <LegendaryButton
                      mode="contained"
                      onPress={handleGetStarted}
                      style={styles.primaryButton}
                      contentStyle={styles.buttonContent}
                      labelStyle={styles.buttonLabel}
                      icon="login"
                    >
                      🚀 Get Started
                    </LegendaryButton>
                  </Animatable.View>

                  <Animatable.View 
                    animation="bounceInRight" 
                    delay={2700}
                    style={styles.buttonWrapper}
                  >
                    <LegendaryButton
                      mode="outlined"
                      onPress={handleCreateAccount}
                      style={styles.secondaryButton}
                      contentStyle={styles.buttonContent}
                      labelStyle={styles.outlinedButtonLabel}
                      icon="person-add"
                    >
                      📝 Create Account
                    </LegendaryButton>
                  </Animatable.View>
                </View>

                {/* Footer Info */}
                <Animatable.View 
                  animation="fadeIn" 
                  delay={2900}
                  style={styles.footer}
                >
                  <Text style={styles.footerText}>
                    Built by RICKROLL187 with ♥️ and 🎸
                  </Text>
                  <Text style={styles.footerContact}>
                    letstalktech010@gmail.com
                  </Text>
                </Animatable.View>
              </LegendaryCard>
            </Animated.View>
          </View>
        </LinearGradient>
      </ImageBackground>
    </>
  );
}

// =====================================
// 🎨 LEGENDARY STYLES 🎨
// =====================================

const styles = StyleSheet.create({
  backgroundImage: {
    flex: 1,
    width,
    height,
  },
  gradient: {
    flex: 1,
  },
  container: {
    flex: 1,
    paddingHorizontal: legendaryTheme.legendary.spacing.lg,
    paddingTop: Platform.OS === 'ios' ? 60 : 40,
    paddingBottom: legendaryTheme.legendary.spacing.lg,
  },
  header: {
    alignItems: 'center',
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  logoContainer: {
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  appTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.legendary,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.legendaryBold,
    color: legendaryTheme.legendary.colors.legendary,
    textAlign: 'center',
    letterSpacing: 2,
    textShadowColor: 'rgba(0, 0, 0, 0.3)',
    textShadowOffset: { width: 2, height: 2 },
    textShadowRadius: 4,
  },
  appSubtitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize['2xl'],
    fontFamily: legendaryTheme.legendary.typography.fontFamily.legendaryBold,
    color: legendaryTheme.legendary.colors.swissPrecision,
    textAlign: 'center',
    letterSpacing: 4,
    marginBottom: legendaryTheme.legendary.spacing.lg,
    textShadowColor: 'rgba(0, 0, 0, 0.3)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
  },
  motto: {
    fontSize: legendaryTheme.legendary.typography.fontSize.lg,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.codeBroBold,
    color: legendaryTheme.legendary.colors.codeBroEnergy,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.sm,
    textShadowColor: 'rgba(0, 0, 0, 0.3)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
  },
  mottoSecond: {
    fontSize: legendaryTheme.legendary.typography.fontSize.lg,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.codeBroBold,
    color: legendaryTheme.legendary.colors.codeBroEnergy,
    textAlign: 'center',
    textShadowColor: 'rgba(0, 0, 0, 0.3)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
  },
  featuresContainer: {
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  featuresTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xl,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.swissPrecisionBold,
    color: legendaryTheme.legendary.colors.legendary,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
    textShadowColor: 'rgba(0, 0, 0, 0.3)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
  },
  featuresGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  featureItem: {
    width: '48%',
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
    padding: legendaryTheme.legendary.spacing.md,
    marginBottom: legendaryTheme.legendary.spacing.md,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: 'rgba(255, 215, 0, 0.3)',
  },
  featureText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
    color: '#ffffff',
    textAlign: 'center',
    marginTop: legendaryTheme.legendary.spacing.xs,
  },
  actionsContainer: {
    flex: 1,
    justifyContent: 'flex-end',
  },
  actionCard: {
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
  welcomeText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xl,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.legendary.colors.primary,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  descriptionText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.regular,
    color: legendaryTheme.legendary.colors.onSurface,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
    lineHeight: 22,
  },
  buttonContainer: {
    gap: legendaryTheme.legendary.spacing.md,
  },
  buttonWrapper: {
    width: '100%',
  },
  primaryButton: {
    backgroundColor: legendaryTheme.legendary.colors.legendary,
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
    elevation: 4,
  },
  secondaryButton: {
    borderColor: legendaryTheme.legendary.colors.legendary,
    borderWidth: 2,
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
  },
  buttonContent: {
    height: 56,
  },
  buttonLabel: {
    fontSize: legendaryTheme.legendary.typography.fontSize.lg,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.legendary.colors.primary,
  },
  outlinedButtonLabel: {
    fontSize: legendaryTheme.legendary.typography.fontSize.lg,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.legendary.colors.legendary,
  },
  footer: {
    marginTop: legendaryTheme.legendary.spacing.lg,
    alignItems: 'center',
  },
  footerText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
    color: legendaryTheme.legendary.colors.onSurface,
    textAlign: 'center',
  },
  footerContact: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.regular,
    color: legendaryTheme.legendary.colors.legendary,
    textAlign: 'center',
    marginTop: legendaryTheme.legendary.spacing.xs,
  },
});

// =====================================
// 🎸 LEGENDARY EXPORTS 🎸
// =====================================

export default LegendaryWelcomeScreen;

// =====================================
// 🎸 LEGENDARY COMPLETION MESSAGE 🎸
// =====================================

console.log('🎸🎸🎸 LEGENDARY WELCOME SCREEN LOADED! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Welcome screen loaded at: 2025-08-06 01:32:02 UTC`);
console.log('🎉 Legendary animations: INFINITE ENERGY');
console.log('🎨 Swiss precision design: MAXIMUM BEAUTY');
console.log('💪 Code bro energy: WELCOME EXPERIENCE');
console.log('👑 RICKROLL187 branding: FOUNDER APPROVED');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
