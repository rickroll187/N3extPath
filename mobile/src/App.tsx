// File: mobile/src/App.tsx
/**
 * 📱🎸 N3EXTPATH - LEGENDARY MOBILE APP 🎸📱
 * Professional React Native mobile application
 * Built: 2025-08-05 16:42:20 UTC by RICKROLL187
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useState, useEffect } from 'react';
import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  View,
  Alert,
  Dimensions,
  Platform,
  TouchableOpacity,
  Image,
  Animated,
  RefreshControl,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Icon from 'react-native-vector-icons/MaterialIcons';
import LinearGradient from 'react-native-linear-gradient';

// Import screens
import DashboardScreen from './screens/DashboardScreen';
import OKRScreen from './screens/OKRScreen';
import PerformanceScreen from './screens/PerformanceScreen';
import ChatScreen from './screens/ChatScreen';
import ProfileScreen from './screens/ProfileScreen';

const Tab = createBottomTabNavigator();
const { width, height } = Dimensions.get('window');

interface User {
  user_id: string;
  username: string;
  first_name: string;
  last_name: string;
  role: string;
  department: string;
  is_legendary?: boolean;
}

const LegendaryMobileApp: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [currentTime, setCurrentTime] = useState(new Date());
  const fadeAnim = new Animated.Value(0);

  useEffect(() => {
    // Update time every second (Swiss precision!)
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    // Initialize app
    initializeApp();

    // Fade in animation
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 1000,
      useNativeDriver: true,
    }).start();

    return () => {
      clearInterval(timer);
    };
  }, []);

  const initializeApp = async () => {
    try {
      setLoading(true);
      
      // Check for stored user data
      const storedUser = await AsyncStorage.getItem('user_data');
      
      if (storedUser) {
        const userData = JSON.parse(storedUser);
        setUser(userData);
      } else {
        // Mock login for demo - in real app would show login screen
        const mockUser: User = {
          user_id: 'rickroll187',
          username: 'rickroll187',
          first_name: 'RICKROLL187',
          last_name: 'Legendary Founder',
          role: 'founder',
          department: 'legendary',
          is_legendary: true
        };
        
        setUser(mockUser);
        await AsyncStorage.setItem('user_data', JSON.stringify(mockUser));
      }
      
      // Show legendary welcome for RICKROLL187
      if (user?.username === 'rickroll187') {
        setTimeout(() => {
          Alert.alert(
            '🎸 LEGENDARY FOUNDER DETECTED! 🎸',
            'Welcome back, RICKROLL187! Your legendary mobile app is ready to rock and roll with Swiss precision!',
            [{ text: 'LET\'S GO!', style: 'default' }]
          );
        }, 1500);
      }
      
    } catch (error) {
      console.error('App initialization error:', error);
      Alert.alert('Error', 'Failed to initialize app. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getTabBarIcon = (route: any, focused: boolean, color: string, size: number) => {
    let iconName = 'dashboard';

    if (route.name === 'Dashboard') {
      iconName = focused ? 'dashboard' : 'dashboard';
    } else if (route.name === 'OKRs') {
      iconName = focused ? 'track-changes' : 'track-changes';
    } else if (route.name === 'Performance') {
      iconName = focused ? 'trending-up' : 'trending-up';
    } else if (route.name === 'Chat') {
      iconName = focused ? 'chat' : 'chat-bubble-outline';
    } else if (route.name === 'Profile') {
      iconName = focused ? 'person' : 'person-outline';
    }

    // Special legendary icon for RICKROLL187
    if (user?.username === 'rickroll187' && route.name === 'Profile') {
      iconName = focused ? 'star' : 'star-border';
    }

    return <Icon name={iconName} size={size} color={color} />;
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.loadingContainer}>
        <StatusBar barStyle="light-content" backgroundColor="#667eea" />
        <LinearGradient
          colors={['#667eea', '#764ba2']}
          style={styles.loadingGradient}
        >
          <Animated.View style={[styles.loadingContent, { opacity: fadeAnim }]}>
            <Image
              source={require('../assets/legendary-logo.png')}
              style={styles.loadingLogo}
              resizeMode="contain"
            />
            <Text style={styles.loadingTitle}>🎸 N3EXTPATH 🎸</Text>
            <Text style={styles.loadingSubtitle}>Professional HR Platform</Text>
            <Text style={styles.loadingTime}>
              {currentTime.toLocaleString('en-US', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                timeZoneName: 'short'
              })}
            </Text>
            <Text style={styles.legendaryMessage}>
              WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
            </Text>
            
            {/* Loading animation */}
            <View style={styles.loadingDots}>
              {[0, 1, 2].map((index) => (
                <Animated.View
                  key={index}
                  style={[
                    styles.loadingDot,
                    {
                      opacity: fadeAnim,
                      transform: [{
                        scale: fadeAnim.interpolate({
                          inputRange: [0, 1],
                          outputRange: [0.5, 1.2]
                        })
                      }]
                    }
                  ]}
                />
              ))}
            </View>
          </Animated.View>
        </LinearGradient>
      </SafeAreaView>
    );
  }

  return (
    <NavigationContainer>
      <StatusBar barStyle="light-content" backgroundColor="#667eea" />
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ focused, color, size }) => 
            getTabBarIcon(route, focused, color, size),
          tabBarActiveTintColor: user?.username === 'rickroll187' ? '#FFD700' : '#667eea',
          tabBarInactiveTintColor: '#8e8e93',
          tabBarStyle: {
            backgroundColor: '#ffffff',
            borderTopWidth: 1,
            borderTopColor: '#e1e1e1',
            paddingBottom: Platform.OS === 'ios' ? 20 : 5,
            height: Platform.OS === 'ios' ? 90 : 60,
            elevation: 8,
            shadowColor: '#000',
            shadowOffset: {
              width: 0,
              height: -2,
            },
            shadowOpacity: 0.1,
            shadowRadius: 3.84,
          },
          tabBarLabelStyle: {
            fontSize: 12,
            fontWeight: '600',
            marginTop: 2,
          },
          headerStyle: {
            backgroundColor: user?.username === 'rickroll187' ? '#FFD700' : '#667eea',
            elevation: 4,
            shadowOpacity: 0.3,
          },
          headerTintColor: user?.username === 'rickroll187' ? '#000' : '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
            fontSize: 18,
          },
        })}
      >
        <Tab.Screen 
          name="Dashboard" 
          component={DashboardScreen}
          options={{
            title: user?.username === 'rickroll187' ? '🎸 Legendary Dashboard' : 'Dashboard'
          }}
          initialParams={{ user }}
        />
        <Tab.Screen 
          name="OKRs" 
          component={OKRScreen}
          options={{
            title: user?.username === 'rickroll187' ? '🎯 Legendary Goals' : 'OKRs'
          }}
          initialParams={{ user }}
        />
        <Tab.Screen 
          name="Performance" 
          component={PerformanceScreen}
          options={{
            title: user?.username === 'rickroll187' ? '🏆 Legendary Performance' : 'Performance'
          }}
          initialParams={{ user }}
        />
        <Tab.Screen 
          name="Chat" 
          component={ChatScreen}
          options={{
            title: user?.username === 'rickroll187' ? '💬 Legendary Chat' : 'Team Chat'
          }}
          initialParams={{ user }}
        />
        <Tab.Screen 
          name="Profile" 
          component={ProfileScreen}
          options={{
            title: user?.username === 'rickroll187' ? '👑 Legendary Profile' : 'Profile'
          }}
          initialParams={{ user }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
};

const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
  },
  loadingGradient: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingContent: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 40,
  },
  loadingLogo: {
    width: 120,
    height: 120,
    marginBottom: 20,
  },
  loadingTitle: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 8,
    textAlign: 'center',
  },
  loadingSubtitle: {
    fontSize: 18,
    color: '#ffffff',
    marginBottom: 20,
    textAlign: 'center',
    opacity: 0.9,
  },
  loadingTime: {
    fontSize: 14,
    color: '#ffffff',
    marginBottom: 20,
    textAlign: 'center',
    opacity: 0.8,
    fontFamily: Platform.OS === 'ios' ? 'Courier' : 'monospace',
  },
  legendaryMessage: {
    fontSize: 16,
    color: '#FFD700',
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 40,
    paddingHorizontal: 20,
  },
  loadingDots: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: '#ffffff',
    marginHorizontal: 4,
  },
});

export default LegendaryMobileApp;
