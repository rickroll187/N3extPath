// File: mobile/src/navigation/LegendaryNavigation.tsx
/**
 * 🧭🎸 N3EXTPATH - LEGENDARY NAVIGATION SYSTEM 🎸🧭
 * Professional mobile navigation with Swiss precision
 * Built: 2025-08-06 01:32:02 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect } from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createDrawerNavigator } from '@react-navigation/drawer';
import { Ionicons } from '@expo/vector-icons';
import { Platform, StatusBar } from 'react-native';
import { useSelector, useDispatch } from 'react-redux';
import { useTheme } from 'react-native-paper';

// Import legendary screens
import { LegendaryWelcomeScreen } from '../screens/auth/LegendaryWelcomeScreen';
import { LegendaryLoginScreen } from '../screens/auth/LegendaryLoginScreen';
import { LegendaryRegisterScreen } from '../screens/auth/LegendaryRegisterScreen';
import { LegendaryDashboardScreen } from '../screens/dashboard/LegendaryDashboardScreen';
import { LegendaryProfileScreen } from '../screens/profile/LegendaryProfileScreen';
import { LegendaryPerformanceScreen } from '../screens/performance/LegendaryPerformanceScreen';
import { LegendaryOKRScreen } from '../screens/okr/LegendaryOKRScreen';
import { LegendaryTeamsScreen } from '../screens/teams/LegendaryTeamsScreen';
import { LegendaryNotificationsScreen } from '../screens/notifications/LegendaryNotificationsScreen';
import { LegendarySettingsScreen } from '../screens/settings/LegendarySettingsScreen';
import { LegendaryFounderScreen } from '../screens/founder/LegendaryFounderScreen';

// Import legendary components
import { LegendaryTabBar } from '../components/navigation/LegendaryTabBar';
import { LegendaryDrawerContent } from '../components/navigation/LegendaryDrawerContent';
import { LegendaryHeaderRight } from '../components/navigation/LegendaryHeaderRight';
import { LegendaryHeaderTitle } from '../components/navigation/LegendaryHeaderTitle';

// Import services and utils
import { RootState } from '../store';
import { checkAuthStatus } from '../store/slices/authSlice';
import { legendaryTheme } from '../theme/legendaryTheme';

// =====================================
// 🎸 NAVIGATION TYPE DEFINITIONS 🎸
// =====================================

export type RootStackParamList = {
  // Auth Stack
  Welcome: undefined;
  Login: undefined;
  Register: undefined;
  
  // Main App Stack
  MainApp: undefined;
  
  // Modal Screens
  Profile: { userId?: string };
  PerformanceDetails: { reviewId: string };
  OKRDetails: { okrId: string };
  TeamDetails: { teamId: string };
  NotificationDetails: { notificationId: string };
  FounderDashboard: undefined;
};

export type MainTabParamList = {
  Dashboard: undefined;
  Performance: undefined;
  OKR: undefined;
  Teams: undefined;
  Profile: undefined;
};

export type DrawerParamList = {
  MainTabs: undefined;
  Settings: undefined;
  Notifications: undefined;
  FounderDashboard: undefined;
};

// Create navigators with legendary precision
const RootStack = createNativeStackNavigator<RootStackParamList>();
const MainTabs = createBottomTabNavigator<MainTabParamList>();
const Drawer = createDrawerNavigator<DrawerParamList>();

// =====================================
// 🎸 LEGENDARY TAB NAVIGATOR 🎸
// =====================================

function LegendaryMainTabs(): JSX.Element {
  const theme = useTheme();
  const user = useSelector((state: RootState) => state.auth.user);
  const isLegendary = user?.is_legendary || false;
  const isFounder = user?.username === 'rickroll187';

  return (
    <MainTabs.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName: keyof typeof Ionicons.glyphMap;

          switch (route.name) {
            case 'Dashboard':
              iconName = focused ? 'home' : 'home-outline';
              break;
            case 'Performance':
              iconName = focused ? 'trending-up' : 'trending-up-outline';
              break;
            case 'OKR':
              iconName = focused ? 'target' : 'target-outline';
              break;
            case 'Teams':
              iconName = focused ? 'people' : 'people-outline';
              break;
            case 'Profile':
              iconName = focused ? 'person' : 'person-outline';
              break;
            default:
              iconName = 'ellipse-outline';
          }

          return (
            <Ionicons 
              name={iconName} 
              size={size} 
              color={focused ? theme.colors.primary : color}
            />
          );
        },
        tabBarActiveTintColor: theme.colors.primary,
        tabBarInactiveTintColor: theme.colors.outline,
        tabBarStyle: {
          backgroundColor: theme.colors.surface,
          borderTopColor: theme.colors.outline,
          borderTopWidth: 1,
          paddingBottom: Platform.OS === 'ios' ? 20 : 10,
          paddingTop: 10,
          height: Platform.OS === 'ios' ? 90 : 70,
        },
        tabBarLabelStyle: {
          fontSize: 12,
          fontWeight: isLegendary ? '600' : '400',
        },
        headerShown: false,
      })}
      tabBar={(props) => (
        <LegendaryTabBar 
          {...props} 
          isLegendary={isLegendary} 
          isFounder={isFounder} 
        />
      )}
    >
      <MainTabs.Screen 
        name="Dashboard" 
        component={LegendaryDashboardScreen}
        options={{
          tabBarLabel: '🎸 Dashboard',
          tabBarBadge: isLegendary ? '⭐' : undefined,
        }}
      />
      
      <MainTabs.Screen 
        name="Performance" 
        component={LegendaryPerformanceScreen}
        options={{
          tabBarLabel: '📊 Performance',
        }}
      />
      
      <MainTabs.Screen 
        name="OKR" 
        component={LegendaryOKRScreen}
        options={{
          tabBarLabel: '🎯 OKRs',
        }}
      />
      
      <MainTabs.Screen 
        name="Teams" 
        component={LegendaryTeamsScreen}
        options={{
          tabBarLabel: '👥 Teams',
        }}
      />
      
      <MainTabs.Screen 
        name="Profile" 
        component={LegendaryProfileScreen}
        options={{
          tabBarLabel: isFounder ? '👑 Profile' : '👤 Profile',
          tabBarBadge: isFounder ? '👑' : (isLegendary ? '🎸' : undefined),
        }}
      />
    </MainTabs.Navigator>
  );
}

// =====================================
// 🎸 LEGENDARY DRAWER NAVIGATOR 🎸
// =====================================

function LegendaryDrawerNavigator(): JSX.Element {
  const theme = useTheme();
  const user = useSelector((state: RootState) => state.auth.user);
  const isFounder = user?.username === 'rickroll187';
  const isLegendary = user?.is_legendary || false;

  return (
    <Drawer.Navigator
      screenOptions={{
        headerStyle: {
          backgroundColor: theme.colors.primary,
          elevation: 0,
          shadowOpacity: 0,
        },
        headerTintColor: theme.colors.onPrimary,
        headerTitleStyle: {
          fontWeight: 'bold',
          fontSize: 18,
        },
        drawerStyle: {
          backgroundColor: theme.colors.surface,
          width: 300,
        },
        drawerActiveTintColor: theme.colors.primary,
        drawerInactiveTintColor: theme.colors.onSurface,
        drawerLabelStyle: {
          fontSize: 16,
          fontWeight: isLegendary ? '600' : '400',
        },
      }}
      drawerContent={(props) => (
        <LegendaryDrawerContent 
          {...props} 
          user={user} 
          isFounder={isFounder}
          isLegendary={isLegendary}
        />
      )}
    >
      <Drawer.Screen
        name="MainTabs"
        component={LegendaryMainTabs}
        options={{
          title: '🎸 N3EXTPATH Legendary',
          drawerLabel: '🏠 Dashboard',
          drawerIcon: ({ color, size }) => (
            <Ionicons name="home-outline" size={size} color={color} />
          ),
          headerTitle: () => (
            <LegendaryHeaderTitle 
              title="N3EXTPATH"
              subtitle={isFounder ? 'Founder Edition' : (isLegendary ? 'Legendary Edition' : 'Standard')}
              isFounder={isFounder}
              isLegendary={isLegendary}
            />
          ),
          headerRight: () => (
            <LegendaryHeaderRight 
              user={user}
              isFounder={isFounder}
              isLegendary={isLegendary}
            />
          ),
        }}
      />

      <Drawer.Screen
        name="Notifications"
        component={LegendaryNotificationsScreen}
        options={{
          title: '🔔 Notifications',
          drawerLabel: '🔔 Notifications',
          drawerIcon: ({ color, size }) => (
            <Ionicons name="notifications-outline" size={size} color={color} />
          ),
        }}
      />

      <Drawer.Screen
        name="Settings"
        component={LegendarySettingsScreen}
        options={{
          title: '⚙️ Settings',
          drawerLabel: '⚙️ Settings',
          drawerIcon: ({ color, size }) => (
            <Ionicons name="settings-outline" size={size} color={color} />
          ),
        }}
      />

      {isFounder && (
        <Drawer.Screen
          name="FounderDashboard"
          component={LegendaryFounderScreen}
          options={{
            title: '👑 Founder Dashboard',
            drawerLabel: '👑 Founder Dashboard',
            drawerIcon: ({ color, size }) => (
              <Ionicons name="crown-outline" size={size} color={color} />
            ),
          }}
        />
      )}
    </Drawer.Navigator>
  );
}

// =====================================
// 🎸 MAIN LEGENDARY NAVIGATION 🎸
// =====================================

export function LegendaryNavigation(): JSX.Element {
  const dispatch = useDispatch();
  const theme = useTheme();
  const { isAuthenticated, isLoading, user } = useSelector((state: RootState) => state.auth);
  const isFounder = user?.username === 'rickroll187';

  useEffect(() => {
    // Check authentication status on app start
    dispatch(checkAuthStatus() as any);
    
    console.log('🧭 Legendary Navigation initialized!');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Navigation loaded at: ${new Date().toISOString()}`);
    
    if (isFounder) {
      console.log('👑 RICKROLL187 Founder navigation activated!');
    }
  }, [dispatch]);

  // Set status bar style based on theme
  useEffect(() => {
    if (Platform.OS === 'android') {
      StatusBar.setBackgroundColor(theme.colors.primary);
      StatusBar.setBarStyle('light-content');
    }
  }, [theme]);

  return (
    <RootStack.Navigator
      screenOptions={{
        headerShown: false,
        gestureEnabled: true,
        animation: 'slide_from_right',
      }}
    >
      {!isAuthenticated ? (
        // Auth Stack - Not authenticated
        <RootStack.Group>
          <RootStack.Screen 
            name="Welcome" 
            component={LegendaryWelcomeScreen}
            options={{
              title: '🎸 Welcome to N3EXTPATH',
              gestureEnabled: false,
            }}
          />
          <RootStack.Screen 
            name="Login" 
            component={LegendaryLoginScreen}
            options={{
              title: '🔐 Login',
              presentation: 'modal',
            }}
          />
          <RootStack.Screen 
            name="Register" 
            component={LegendaryRegisterScreen}
            options={{
              title: '📝 Register',
              presentation: 'modal',
            }}
          />
        </RootStack.Group>
      ) : (
        // Main App Stack - Authenticated
        <RootStack.Group>
          <RootStack.Screen 
            name="MainApp" 
            component={LegendaryDrawerNavigator}
            options={{
              title: isFounder ? '👑 N3EXTPATH Founder' : '🎸 N3EXTPATH Legendary',
            }}
          />
        </RootStack.Group>
      )}

      {/* Modal Screens - Available when authenticated */}
      {isAuthenticated && (
        <RootStack.Group screenOptions={{ presentation: 'modal' }}>
          <RootStack.Screen
            name="Profile"
            component={LegendaryProfileScreen}
            options={{
              title: '👤 Profile',
              headerShown: true,
              headerStyle: {
                backgroundColor: theme.colors.primary,
              },
              headerTintColor: theme.colors.onPrimary,
              headerTitleStyle: {
                fontWeight: 'bold',
              },
            }}
          />

          <RootStack.Screen
            name="PerformanceDetails"
            component={LegendaryPerformanceScreen}
            options={{
              title: '📊 Performance Details',
              headerShown: true,
              headerStyle: {
                backgroundColor: theme.colors.primary,
              },
              headerTintColor: theme.colors.onPrimary,
            }}
          />

          <RootStack.Screen
            name="OKRDetails"
            component={LegendaryOKRScreen}
            options={{
              title: '🎯 OKR Details',
              headerShown: true,
              headerStyle: {
                backgroundColor: theme.colors.primary,
              },
              headerTintColor: theme.colors.onPrimary,
            }}
          />

          <RootStack.Screen
            name="TeamDetails"
            component={LegendaryTeamsScreen}
            options={{
              title: '👥 Team Details',
              headerShown: true,
              headerStyle: {
                backgroundColor: theme.colors.primary,
              },
              headerTintColor: theme.colors.onPrimary,
            }}
          />

          <RootStack.Screen
            name="NotificationDetails"
            component={LegendaryNotificationsScreen}
            options={{
              title: '🔔 Notification Details',
              headerShown: true,
              headerStyle: {
                backgroundColor: theme.colors.primary,
              },
              headerTintColor: theme.colors.onPrimary,
            }}
          />

          {isFounder && (
            <RootStack.Screen
              name="FounderDashboard"
              component={LegendaryFounderScreen}
              options={{
                title: '👑 RICKROLL187 Founder Dashboard',
                headerShown: true,
                headerStyle: {
                  backgroundColor: theme.colors.primary,
                },
                headerTintColor: theme.colors.onPrimary,
                headerTitleStyle: {
                  fontWeight: 'bold',
                  fontSize: 18,
                },
              }}
            />
          )}
        </RootStack.Group>
      )}
    </RootStack.Navigator>
  );
}

// =====================================
// 🎸 NAVIGATION UTILITIES 🎸
// =====================================

export const navigationTheme = {
  dark: false,
  colors: {
    primary: legendaryTheme.colors.primary,
    background: legendaryTheme.colors.background,
    card: legendaryTheme.colors.surface,
    text: legendaryTheme.colors.onBackground,
    border: legendaryTheme.colors.outline,
    notification: legendaryTheme.colors.secondary,
  },
};

// =====================================
// 🎸 LEGENDARY EXPORTS 🎸
// =====================================

export default LegendaryNavigation;

export {
  type RootStackParamList,
  type MainTabParamList,
  type DrawerParamList,
  navigationTheme,
};

// =====================================
// 🎸 LEGENDARY COMPLETION MESSAGE 🎸
// =====================================

console.log('🎸🎸🎸 LEGENDARY NAVIGATION SYSTEM LOADED! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Navigation system loaded at: 2025-08-06 01:32:02 UTC`);
console.log('🧭 Stack Navigation: LEGENDARY PRECISION');
console.log('📱 Tab Navigation: SWISS PERFECTION');
console.log('🎨 Drawer Navigation: CODE BRO ENERGY');
console.log('👑 RICKROLL187 Founder Navigation: INFINITE ACCESS');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
