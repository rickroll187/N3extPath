// File: mobile/App.tsx
/**
 * 🎸🎸🎸 N3EXTPATH - LEGENDARY MOBILE APP V2.0 🎸🎸🎸
 * Professional mobile experience with Swiss precision
 * Built: 2025-08-06 01:24:40 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect, useState } from 'react';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { NavigationContainer } from '@react-navigation/native';
import { Provider as ReduxProvider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import * as SplashScreen from 'expo-splash-screen';
import * as Font from 'expo-font';
import { LogBox, Platform } from 'react-native';
import { Provider as PaperProvider } from 'react-native-paper';

// Import legendary components and services
import { store, persistor } from './src/store';
import { LegendaryThemeProvider } from './src/theme/LegendaryThemeProvider';
import { NotificationService } from './src/services/NotificationService';
import { AuthService } from './src/services/AuthService';
import { LegendarySplashScreen } from './src/components/LegendarySplashScreen';
import { LegendaryNavigation } from './src/navigation/LegendaryNavigation';
import { LegendaryErrorBoundary } from './src/components/LegendaryErrorBoundary';
import { legendaryTheme } from './src/theme/legendaryTheme';

// Configure logging for legendary development
LogBox.ignoreLogs([
  'Non-serializable values were found in the navigation state',
  'Remote debugger', // Common React Native warnings
]);

// Keep the splash screen visible while we fetch resources
SplashScreen.preventAutoHideAsync();

/**
 * 🎸 LEGENDARY MOBILE APPLICATION 🎸
 * Main entry point with Swiss precision initialization
 */
export default function LegendaryApp(): JSX.Element {
  const [isReady, setIsReady] = useState(false);
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    async function prepareLegendaryApp() {
      try {
        console.log('🎸🎸🎸 STARTING N3EXTPATH LEGENDARY MOBILE! 🎸🎸🎸');
        console.log('Built with Swiss precision by RICKROLL187!');
        console.log('Email: letstalktech010@gmail.com');
        console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
        console.log(`Starting at: ${new Date().toISOString()}`);

        // Load legendary fonts
        await loadLegendaryFonts();
        console.log('✅ Legendary fonts loaded with Swiss precision!');

        // Initialize notification service
        await NotificationService.initialize();
        console.log('✅ Notification service initialized with legendary power!');

        // Initialize auth service
        await AuthService.initialize();
        console.log('✅ Auth service ready for legendary users!');

        // Perform legendary health checks
        await performLegendaryHealthCheck();
        console.log('✅ Legendary health check passed!');

        console.log('🚀 N3EXTPATH Legendary Mobile ready with infinite code bro energy!');

      } catch (error) {
        console.error('🚨 Error preparing legendary app:', error);
        setHasError(true);
      } finally {
        setIsReady(true);
        // Hide the splash screen once everything is ready
        await SplashScreen.hideAsync();
      }
    }

    prepareLegendaryApp();
  }, []);

  // Load legendary fonts with Swiss precision
  const loadLegendaryFonts = async () => {
    await Font.loadAsync({
      'Legendary-Regular': require('./assets/fonts/Legendary-Regular.ttf'),
      'Legendary-Bold': require('./assets/fonts/Legendary-Bold.ttf'),
      'SwissPrecision-Regular': require('./assets/fonts/SwissPrecision-Regular.ttf'),
      'SwissPrecision-Bold': require('./assets/fonts/SwissPrecision-Bold.ttf'),
      'CodeBro-Regular': require('./assets/fonts/CodeBro-Regular.ttf'),
      'CodeBro-Bold': require('./assets/fonts/CodeBro-Bold.ttf'),
    });
  };

  // Perform legendary health checks
  const performLegendaryHealthCheck = async () => {
    // Check device compatibility
    const platformCheck = Platform.OS === 'ios' || Platform.OS === 'android';
    if (!platformCheck) {
      throw new Error('🚨 Platform not supported for legendary experience!');
    }

    // Simulate API connectivity check
    await new Promise(resolve => setTimeout(resolve, 1000));

    console.log('🏥 Legendary health check completed with Swiss precision!');
  };

  // Handle error state with legendary precision
  if (hasError) {
    return (
      <LegendaryErrorBoundary
        error="Failed to initialize legendary mobile app"
        onRetry={() => {
          setHasError(false);
          setIsReady(false);
        }}
      />
    );
  }

  // Show legendary splash screen while loading
  if (!isReady) {
    return (
      <LegendarySplashScreen 
        message="Loading legendary features with Swiss precision..."
        founder="RICKROLL187"
        email="letstalktech010@gmail.com"
      />
    );
  }

  // Main legendary application
  return (
    <SafeAreaProvider>
      <ReduxProvider store={store}>
        <PersistGate loading={<LegendarySplashScreen message="Restoring legendary session..." />} persistor={persistor}>
          <PaperProvider theme={legendaryTheme}>
            <LegendaryThemeProvider>
              <LegendaryErrorBoundary>
                <NavigationContainer>
                  <LegendaryNavigation />
                  <StatusBar style="auto" backgroundColor={legendaryTheme.colors.primary} />
                </NavigationContainer>
              </LegendaryErrorBoundary>
            </LegendaryThemeProvider>
          </PaperProvider>
        </PersistGate>
      </ReduxProvider>
    </SafeAreaProvider>
  );
}
