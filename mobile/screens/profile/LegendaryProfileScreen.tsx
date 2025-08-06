
// File: mobile/src/screens/profile/LegendaryProfileScreen.tsx
/**
 * 👤🎸 N3EXTPATH - LEGENDARY PROFILE SCREEN 🎸👤
 * Professional user profile management with Swiss precision
 * Built: 2025-08-06 01:53:06 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Image,
  TouchableOpacity,
  Alert,
  Animated,
  Dimensions,
  Platform,
} from 'react-native';
import { 
  Avatar, 
  Card, 
  Button, 
  Chip, 
  Badge, 
  Switch, 
  List, 
  Divider,
  Portal,
  Modal,
  ActivityIndicator
} from 'react-native-paper';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { useDispatch, useSelector } from 'react-redux';
import * as Animatable from 'react-native-animatable';
import * as ImagePicker from 'expo-image-picker';
import * as Sharing from 'expo-sharing';

// Import legendary components and services
import { RootStackParamList } from '../../navigation/LegendaryNavigation';
import { RootState } from '../../store';
import { updateUserProfile, logoutUser } from '../../store/slices/authSlice';
import { legendaryTheme } from '../../theme/legendaryTheme';
import { LegendaryButton } from '../../components/ui/LegendaryButton';
import { LegendaryCard } from '../../components/ui/LegendaryCard';
import { LegendaryTextInput } from '../../components/ui/LegendaryTextInput';
import { LegendaryAchievementBadge } from '../../components/profile/LegendaryAchievementBadge';
import { LegendaryStatsCard } from '../../components/profile/LegendaryStatsCard';

type ProfileScreenNavigationProp = NativeStackNavigationProp<RootStackParamList>;

const { width, height } = Dimensions.get('window');

// =====================================
// 👤 PROFILE DATA TYPES 👤
// =====================================

interface UserAchievement {
  id: string;
  title: string;
  description: string;
  icon: string;
  color: string;
  earnedAt: Date;
  isLegendary: boolean;
}

interface UserStats {
  totalProjects: number;
  completedOKRs: number;
  teamCollaborations: number;
  performanceScore: number;
  legendaryLevel: number;
  codeBroEnergy: number;
}

// =====================================
// 🎸 LEGENDARY PROFILE SCREEN 🎸
// =====================================

export function LegendaryProfileScreen(): JSX.Element {
  const navigation = useNavigation<ProfileScreenNavigationProp>();
  const dispatch = useDispatch();
  
  // Redux state
  const { user, isLoading } = useSelector((state: RootState) => state.auth);
  
  // Local state
  const [editMode, setEditMode] = useState(false);
  const [profileImage, setProfileImage] = useState<string | null>(null);
  const [showSettings, setShowSettings] = useState(false);
  const [showAchievements, setShowAchievements] = useState(false);
  const [showShareProfile, setShowShareProfile] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [notifications, setNotifications] = useState(true);
  const [publicProfile, setPublicProfile] = useState(false);
  
  // Animation refs
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(30)).current;
  const scaleAnim = useRef(new Animated.Value(0.9)).current;
  const pulseAnim = useRef(new Animated.Value(1)).current;
  const rotateAnim = useRef(new Animated.Value(0)).current;

  // Check if user is RICKROLL187 founder
  const isFounder = user?.username === 'rickroll187';
  const isLegendary = user?.is_legendary || false;
  const userName = user?.first_name || user?.username || 'User';
  const userEmail = user?.email || '';

  // Mock user stats (in real app, fetch from API)
  const [userStats, setUserStats] = useState<UserStats>({
    totalProjects: isFounder ? 25 : isLegendary ? 12 : 8,
    completedOKRs: isFounder ? 15 : isLegendary ? 8 : 5,
    teamCollaborations: isFounder ? 100 : isLegendary ? 45 : 20,
    performanceScore: isFounder ? 100 : isLegendary ? 88 : 75,
    legendaryLevel: isFounder ? 10 : isLegendary ? 7 : 4,
    codeBroEnergy: isFounder ? 10 : isLegendary ? 9 : 6,
  });

  // Mock achievements (in real app, fetch from API)
  const [achievements, setAchievements] = useState<UserAchievement[]>([
    {
      id: '1',
      title: isFounder ? '👑 Legendary Founder' : '🎸 Code Bro Master',
      description: isFounder ? 'Created the legendary N3EXTPATH platform' : 'Achieved legendary code bro status',
      icon: isFounder ? 'crown' : 'musical-notes',
      color: legendaryTheme.legendary.colors.legendary,
      earnedAt: new Date('2025-01-01'),
      isLegendary: true,
    },
    {
      id: '2',
      title: '⚙️ Swiss Precision Expert',
      description: 'Maintained 90%+ Swiss precision score for 3 months',
      icon: 'cog',
      color: legendaryTheme.legendary.colors.swissPrecision,
      earnedAt: new Date('2025-07-15'),
      isLegendary: isLegendary,
    },
    {
      id: '3',
      title: '👥 Team Collaboration Champion',
      description: 'Led 5+ successful team collaborations',
      icon: 'people',
      color: legendaryTheme.legendary.colors.success,
      earnedAt: new Date('2025-06-20'),
      isLegendary: false,
    },
    {
      id: '4',
      title: '🎯 OKR Achievement Master',
      description: 'Completed 10+ OKRs with excellent results',
      icon: 'target',
      color: legendaryTheme.legendary.colors.info,
      earnedAt: new Date('2025-05-10'),
      isLegendary: false,
    }
  ]);

  useEffect(() => {
    console.log('👤🎸👤 LEGENDARY PROFILE SCREEN LOADED! 👤🎸👤');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Profile screen loaded at: 2025-08-06 01:53:06 UTC`);
    
    if (isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER PROFILE ACTIVATED! 👑🎸👑');
      console.log('🚀 INFINITE CODE BRO ENERGY PROFILE!');
      console.log('⚙️ SWISS PRECISION FOUNDER MODE!');
    }

    // Start legendary animations
    startLegendaryAnimations();
    
    // Set up founder pulse animation
    if (isFounder) {
      startFounderAnimations();
    }

    // Request image picker permissions
    requestPermissions();
  }, []);

  const startLegendaryAnimations = () => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 1000,
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

  const startFounderAnimations = () => {
    // Pulse animation for founder
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.05,
          duration: 2000,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 2000,
          useNativeDriver: true,
        }),
      ])
    ).start();

    // Rotation animation for crown
    Animated.loop(
      Animated.timing(rotateAnim, {
        toValue: 1,
        duration: 8000,
        useNativeDriver: true,
      })
    ).start();
  };

  const requestPermissions = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission needed', 'We need camera roll permissions to update your profile photo.');
    }
  };

  const handleImagePicker = async () => {
    try {
      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [1, 1],
        quality: 0.8,
      });

      if (!result.canceled && result.assets[0]) {
        setProfileImage(result.assets[0].uri);
        console.log('📸 Profile image updated!');
        
        // In real app, upload to server
        // await dispatch(updateUserProfile({ profileImage: result.assets[0].uri }));
      }
    } catch (error) {
      console.error('Error picking image:', error);
      Alert.alert('Error', 'Failed to update profile image');
    }
  };

  const handleEditProfile = () => {
    setEditMode(!editMode);
    console.log(`✏️ Edit mode: ${!editMode}`);
  };

  const handleSaveProfile = async () => {
    try {
      console.log('💾 Saving legendary profile...');
      
      // In real app, dispatch update action
      // await dispatch(updateUserProfile(updatedData));
      
      setEditMode(false);
      
      Alert.alert(
        '✅ Profile Updated',
        isFounder 
          ? '👑 Legendary founder profile updated with infinite precision!'
          : '🎸 Your legendary profile has been updated with Swiss precision!'
      );
    } catch (error) {
      console.error('Error saving profile:', error);
      Alert.alert('Error', 'Failed to save profile changes');
    }
  };

  const handleLogout = () => {
    Alert.alert(
      '🚨 Logout Confirmation',
      isFounder 
        ? '👑 Are you sure you want to logout, legendary founder RICKROLL187?'
        : `🎸 Are you sure you want to logout, ${userName}?`,
      [
        {
          text: 'Cancel',
          style: 'cancel',
        },
        {
          text: 'Logout',
          style: 'destructive',
          onPress: () => {
            console.log('🚪 Logging out legendary user...');
            dispatch(logoutUser() as any);
          },
        },
      ]
    );
  };

  const handleShareProfile = async () => {
    try {
      const shareContent = {
        message: isFounder 
          ? `👑 Check out RICKROLL187's legendary founder profile on N3EXTPATH!\n\n🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!\n\nContact: letstalktech010@gmail.com`
          : `🎸 Check out ${userName}'s legendary profile on N3EXTPATH!\n\nSwiss Precision Score: ${userStats.performanceScore}%\nCode Bro Energy: ${userStats.codeBroEnergy}/10\n\nJoin the legendary platform!`,
      };

      if (await Sharing.isAvailableAsync()) {
        await Sharing.shareAsync('', shareContent);
        console.log('🔗 Profile shared successfully!');
      }
    } catch (error) {
      console.error('Error sharing profile:', error);
      Alert.alert('Error', 'Failed to share profile');
    }
  };

  const handleViewAchievement = (achievement: UserAchievement) => {
    Alert.alert(
      `🏆 ${achievement.title}`,
      `${achievement.description}\n\nEarned: ${achievement.earnedAt.toLocaleDateString()}\nLegendary: ${achievement.isLegendary ? 'Yes 🎸' : 'No'}`
    );
  };

  const rotateInterpolate = rotateAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  const renderProfileHeader = () => (
    <Animated.View 
      style={[
        styles.headerContainer,
        {
          opacity: fadeAnim,
          transform: [
            { translateY: slideAnim },
            { scale: isFounder ? pulseAnim : scaleAnim },
          ],
        },
      ]}
    >
      <LinearGradient
        colors={
          isFounder 
            ? [legendaryTheme.legendary.colors.legendary, legendaryTheme.legendary.colors.rickroll187]
            : isLegendary
            ? [legendaryTheme.legendary.colors.legendary, legendaryTheme.legendary.colors.swissPrecision]
            : [legendaryTheme.colors.primary, legendaryTheme.colors.primaryContainer]
        }
        style={styles.headerGradient}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        {/* Profile Image */}
        <TouchableOpacity onPress={handleImagePicker} style={styles.avatarContainer}>
          <Avatar.Image
            size={120}
            source={
              profileImage 
                ? { uri: profileImage }
                : { uri: `https://ui-avatars.com/api/?name=${userName}&background=FFD700&color=1a1a1a&size=120` }
            }
            style={styles.avatar}
          />
          <View style={styles.avatarEditIcon}>
            <Ionicons name="camera" size={20} color="#ffffff" />
          </View>
          
          {isFounder && (
            <Animated.View 
              style={[
                styles.founderCrown,
                { transform: [{ rotate: rotateInterpolate }] }
              ]}
            >
              <Ionicons name="crown" size={30} color={legendaryTheme.legendary.colors.legendary} />
            </Animated.View>
          )}
        </TouchableOpacity>

        {/* User Info */}
        <View style={styles.userInfo}>
          <Text style={styles.userName}>
            {isFounder ? '👑 RICKROLL187' : userName}
          </Text>
          <Text style={styles.userRole}>
            {isFounder 
              ? 'Legendary Founder & Chief Code Bro'
              : user?.job_title || 'Team Member'
            }
          </Text>
          <Text style={styles.userEmail}>{userEmail}</Text>
          
          {isFounder && (
            <Animatable.View 
              animation="pulse" 
              iterationCount="infinite"
              style={styles.founderBadge}
            >
              <Text style={styles.founderBadgeText}>
                🎸 WE ARE CODE BROS THE CREATE THE BEST! 🎸
              </Text>
            </Animatable.View>
          )}

          {/* Status Chips */}
          <View style={styles.statusChips}>
            {isLegendary && (
              <Chip 
                icon="star" 
                style={[styles.statusChip, { backgroundColor: legendaryTheme.legendary.colors.legendary }]}
                textStyle={styles.chipText}
              >
                Legendary
              </Chip>
            )}
            {user?.swiss_precision_certified && (
              <Chip 
                icon="precision-manufacturing" 
                style={[styles.statusChip, { backgroundColor: legendaryTheme.legendary.colors.swissPrecision }]}
                textStyle={styles.chipText}
              >
                Swiss Precision
              </Chip>
            )}
            <Chip 
              icon="musical-notes" 
              style={[styles.statusChip, { backgroundColor: legendaryTheme.legendary.colors.codeBroEnergy }]}
              textStyle={styles.chipText}
            >
              Code Bro Lv.{userStats.codeBroEnergy}
            </Chip>
          </View>
        </View>

        {/* Action Buttons */}
        <View style={styles.headerActions}>
          <LegendaryButton
            mode={editMode ? "contained" : "outlined"}
            onPress={editMode ? handleSaveProfile : handleEditProfile}
            style={[styles.actionButton, editMode && styles.saveButton]}
            icon={editMode ? "content-save" : "pencil"}
            loading={isLoading}
          >
            {editMode ? 'Save' : 'Edit'}
          </LegendaryButton>
          
          <LegendaryButton
            mode="outlined"
            onPress={() => setShowShareProfile(true)}
            style={styles.actionButton}
            icon="share"
          >
            Share
          </LegendaryButton>
        </View>
      </LinearGradient>
    </Animated.View>
  );

  const renderStatsGrid = () => (
    <Animated.View 
      style={[
        styles.statsContainer,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      <Text style={styles.sectionTitle}>
        📊 {isFounder ? 'Legendary Founder Stats' : 'Performance Stats'}
      </Text>
      
      <View style={styles.statsGrid}>
        <Animatable.View animation="bounceInLeft" delay={300}>
          <LegendaryStatsCard
            title="Projects"
            value={userStats.totalProjects}
            icon="briefcase"
            color={legendaryTheme.legendary.colors.legendary}
            subtitle="Completed"
            isFounder={isFounder}
          />
        </Animatable.View>
        
        <Animatable.View animation="bounceInRight" delay={500}>
          <LegendaryStatsCard
            title="OKRs"
            value={userStats.completedOKRs}
            icon="target"
            color={legendaryTheme.legendary.colors.swissPrecision}
            subtitle="Achieved"
            isFounder={isFounder}
          />
        </Animatable.View>
        
        <Animatable.View animation="bounceInLeft" delay={700}>
          <LegendaryStatsCard
            title="Collaborations"
            value={userStats.teamCollaborations}
            icon="people"
            color={legendaryTheme.legendary.colors.codeBroEnergy}
            subtitle="Team Projects"
            isFounder={isFounder}
          />
        </Animatable.View>
        
        <Animatable.View animation="bounceInRight" delay={900}>
          <LegendaryStatsCard
            title="Performance"
            value={userStats.performanceScore}
            icon="trending-up"
            color={legendaryTheme.legendary.colors.success}
            subtitle="Score %"
            isFounder={isFounder}
          />
        </Animatable.View>
      </View>
    </Animated.View>
  );

  const renderAchievements = () => (
    <Animated.View 
      style={[
        styles.achievementsContainer,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      <LegendaryCard style={styles.achievementsCard}>
        <View style={styles.achievementsHeader}>
          <Text style={styles.sectionTitle}>🏆 Legendary Achievements</Text>
          <Badge style={styles.achievementsBadge}>
            {achievements.length}
          </Badge>
        </View>
        
        <View style={styles.achievementsList}>
          {achievements.slice(0, 3).map((achievement, index) => (
            <Animatable.View 
              key={achievement.id}
              animation="fadeInUp"
              delay={300 + (index * 200)}
            >
              <TouchableOpacity
                onPress={() => handleViewAchievement(achievement)}
                style={styles.achievementItem}
              >
                <LegendaryAchievementBadge
                  achievement={achievement}
                  size="medium"
                />
                <View style={styles.achievementContent}>
                  <Text style={styles.achievementTitle}>{achievement.title}</Text>
                  <Text style={styles.achievementDescription} numberOfLines={2}>
                    {achievement.description}
                  </Text>
                </View>
                <Ionicons 
                  name="chevron-forward" 
                  size={20} 
                  color={legendaryTheme.colors.outline} 
                />
              </TouchableOpacity>
            </Animatable.View>
          ))}
        </View>
        
        <LegendaryButton
          mode="text"
          onPress={() => setShowAchievements(true)}
          style={styles.viewAllAchievements}
          labelStyle={styles.viewAllText}
        >
          View All Achievements →
        </LegendaryButton>
      </LegendaryCard>
    </Animated.View>
  );

  const renderSettingsSection = () => (
    <Animated.View 
      style={[
        styles.settingsContainer,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      <LegendaryCard style={styles.settingsCard}>
        <Text style={styles.sectionTitle}>⚙️ Settings & Preferences</Text>
        
        <List.Section>
          <List.Item
            title="Dark Mode"
            description="Enable dark theme"
            left={props => <List.Icon {...props} icon="theme-light-dark" />}
            right={() => (
              <Switch
                value={darkMode}
                onValueChange={setDarkMode}
                color={legendaryTheme.legendary.colors.legendary}
              />
            )}
          />
          
          <Divider />
          
          <List.Item
            title="Notifications"
            description="Receive push notifications"
            left={props => <List.Icon {...props} icon="bell" />}
            right={() => (
              <Switch
                value={notifications}
                onValueChange={setNotifications}
                color={legendaryTheme.legendary.colors.legendary}
              />
            )}
          />
          
          <Divider />
          
          <List.Item
            title="Public Profile"
            description="Make profile visible to others"
            left={props => <List.Icon {...props} icon="account-eye" />}
            right={() => (
              <Switch
                value={publicProfile}
                onValueChange={setPublicProfile}
                color={legendaryTheme.legendary.colors.legendary}
              />
            )}
          />
          
          <Divider />
          
          <List.Item
            title="Privacy & Security"
            description="Manage your privacy settings"
            left={props => <List.Icon {...props} icon="shield-account" />}
            right={props => <List.Icon {...props} icon="chevron-right" />}
            onPress={() => console.log('Privacy settings')}
          />
          
          <Divider />
          
          <List.Item
            title="Help & Support"
            description="Get help and contact support"
            left={props => <List.Icon {...props} icon="help-circle" />}
            right={props => <List.Icon {...props} icon="chevron-right" />}
            onPress={() => Alert.alert(
              '🎸 Legendary Support',
              `Contact legendary founder RICKROLL187:\n\nEmail: letstalktech010@gmail.com\n\nWE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!`,
              [{ text: 'Got it!', style: 'default' }]
            )}
          />
          
          <Divider />
          
          <List.Item
            title="About N3EXTPATH"
            description="Learn about the legendary platform"
            left={props => <List.Icon {...props} icon="information" />}
            right={props => <List.Icon {...props} icon="chevron-right" />}
            onPress={() => Alert.alert(
              '🎸 About N3EXTPATH',
              `N3EXTPATH Legendary Platform\n\nBuilt with Swiss precision and infinite code bro energy by RICKROLL187!\n\nVersion: 2.0.0\nBuilt: 2025-08-06\n\nWE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!`,
              [{ text: 'Legendary!', style: 'default' }]
            )}
          />
        </List.Section>
      </LegendaryCard>
    </Animated.View>
  );

  const renderLogoutSection = () => (
    <Animated.View 
      style={[
        styles.logoutContainer,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      <LegendaryButton
        mode="outlined"
        onPress={handleLogout}
        style={styles.logoutButton}
        labelStyle={styles.logoutButtonText}
        icon="logout"
      >
        🚪 Logout
      </LegendaryButton>
      
      <Text style={styles.versionText}>
        N3EXTPATH v2.0.0 • Built with 🎸 by RICKROLL187
      </Text>
      <Text style={styles.mottoText}>
        WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
      </Text>
    </Animated.View>
  );

  return (
    <View style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Profile Header */}
        {renderProfileHeader()}
        
        {/* Stats Grid */}
        {renderStatsGrid()}
        
        {/* Achievements */}
        {renderAchievements()}
        
        {/* Settings */}
        {renderSettingsSection()}
        
        {/* Logout Section */}
        {renderLogoutSection()}
        
        {/* Bottom Spacing */}
        <View style={styles.bottomSpacing} />
      </ScrollView>

      {/* Share Profile Modal */}
      <Portal>
        <Modal
          visible={showShareProfile}
          onDismiss={() => setShowShareProfile(false)}
          contentContainerStyle={styles.shareModal}
        >
          <View style={styles.shareContent}>
            <Text style={styles.shareTitle}>🔗 Share Profile</Text>
            <Text style={styles.shareDescription}>
              Share your legendary profile with others
            </Text>
            
            <View style={styles.shareActions}>
              <LegendaryButton
                mode="contained"
                onPress={handleShareProfile}
                style={styles.shareButton}
                icon="share"
              >
                Share Now
              </LegendaryButton>
              
              <LegendaryButton
                mode="text"
                onPress={() => setShowShareProfile(false)}
                style={styles.cancelButton}
              >
                Cancel
              </LegendaryButton>
            </View>
          </View>
        </Modal>
      </Portal>

      {/* Achievements Modal */}
      <Portal>
        <Modal
          visible={showAchievements}
          onDismiss={() => setShowAchievements(false)}
          contentContainerStyle={styles.achievementsModal}
        >
          <View style={styles.achievementsModalContent}>
            <Text style={styles.shareTitle}>🏆 All Achievements</Text>
            
            <ScrollView style={styles.achievementsModalList}>
              {achievements.map((achievement, index) => (
                <TouchableOpacity
                  key={achievement.id}
                  onPress={() => handleViewAchievement(achievement)}
                  style={styles.achievementModalItem}
                >
                  <LegendaryAchievementBadge
                    achievement={achievement}
                    size="large"
                  />
                  <View style={styles.achievementModalContent}>
                    <Text style={styles.achievementModalTitle}>{achievement.title}</Text>
                    <Text style={styles.achievementModalDescription}>
                      {achievement.description}
                    </Text>
                    <Text style={styles.achievementModalDate}>
                      Earned: {achievement.earnedAt.toLocaleDateString()}
                    </Text>
                  </View>
                </TouchableOpacity>
              ))}
            </ScrollView>
            
            <LegendaryButton
              mode="text"
              onPress={() => setShowAchievements(false)}
              style={styles.closeButton}
            >
              Close
            </LegendaryButton>
          </View>
        </Modal>
      </Portal>
    </View>
  );
}

// =====================================
// 🎨 LEGENDARY STYLES 🎨
// =====================================

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: legendaryTheme.colors.background,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    paddingBottom: legendaryTheme.legendary.spacing.xl,
  },
  headerContainer: {
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  headerGradient: {
    padding: legendaryTheme.legendary.spacing.lg,
    alignItems: 'center',
  },
  avatarContainer: {
    position: 'relative',
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  avatar: {
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.3,
    shadowRadius: 6,
  },
  avatarEditIcon: {
    position: 'absolute',
    right: 0,
    bottom: 0,
    backgroundColor: legendaryTheme.colors.primary,
    borderRadius: 20,
    width: 40,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 4,
  },
  founderCrown: {
    position: 'absolute',
    top: -10,
    right: -5,
  },
  userInfo: {
    alignItems: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  userName: {
    fontSize: legendaryTheme.legendary.typography.fontSize['2xl'],
    fontFamily: legendaryTheme.legendary.typography.fontFamily.legendaryBold,
    color: '#ffffff',
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.xs,
    textShadowColor: 'rgba(0, 0, 0, 0.3)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
  },
  userRole: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
    color: 'rgba(255, 255, 255, 0.9)',
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  userEmail: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.regular,
    color: 'rgba(255, 255, 255, 0.8)',
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  founderBadge: {
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
    paddingHorizontal: legendaryTheme.legendary.spacing.md,
    paddingVertical: legendaryTheme.legendary.spacing.xs,
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  founderBadgeText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.codeBroBold,
    color: '#ffffff',
    textAlign: 'center',
  },
  statusChips: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: legendaryTheme.legendary.spacing.sm,
    justifyContent: 'center',
  },
  statusChip: {
    elevation: 2,
  },
  chipText: {
    color: '#ffffff',
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
  },
  headerActions: {
    flexDirection: 'row',
    gap: legendaryTheme.legendary.spacing.md,
  },
  actionButton: {
    borderColor: '#ffffff',
  },
  saveButton: {
    backgroundColor: legendaryTheme.legendary.colors.success,
  },
  sectionTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xl,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.legendaryBold,
    color: legendaryTheme.colors.primary,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  statsContainer: {
    paddingHorizontal: legendaryTheme.legendary.spacing.lg,
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    gap: legendaryTheme.legendary.spacing.md,
  },
  achievementsContainer: {
    paddingHorizontal: legendaryTheme.legendary.spacing.lg,
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  achievementsCard: {
    padding: legendaryTheme.legendary.spacing.lg,
  },
  achievementsHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  achievementsBadge: {
    backgroundColor: legendaryTheme.legendary.colors.legendary,
  },
  achievementsList: {
    gap: legendaryTheme.legendary.spacing.md,
  },
  achievementItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: legendaryTheme.legendary.spacing.sm,
    gap: legendaryTheme.legendary.spacing.md,
  },
  achievementContent: {
    flex: 1,
  },
  achievementTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.onSurface,
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  achievementDescription: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.regular,
    color: legendaryTheme.colors.outline,
  },
  viewAllAchievements: {
    marginTop: legendaryTheme.legendary.spacing.md,
  },
  viewAllText: {
    color: legendaryTheme.colors.primary,
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
  },
  settingsContainer: {
    paddingHorizontal: legendaryTheme.legendary.spacing.lg,
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  settingsCard: {
    padding: legendaryTheme.legendary.spacing.lg,
  },
  logoutContainer: {
    paddingHorizontal: legendaryTheme.legendary.spacing.lg,
    alignItems: 'center',
  },
  logoutButton: {
    borderColor: legendaryTheme.legendary.colors.error,
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  logoutButtonText: {
    color: legendaryTheme.legendary.colors.error,
  },
  versionText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: legendaryTheme.colors.outline,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  mottoText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    color: legendaryTheme.colors.outline,
    textAlign: 'center',
    fontStyle: 'italic',
  },
  bottomSpacing: {
    height: legendaryTheme.legendary.spacing.xl,
  },
  shareModal: {
    backgroundColor: 'white',
    padding: legendaryTheme.legendary.spacing.lg,
    margin: legendaryTheme.legendary.spacing.lg,
    borderRadius: legendaryTheme.legendary.borders.radius.xl,
  },
  shareContent: {
    alignItems: 'center',
  },
  shareTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xl,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.primary,
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  shareDescription: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.colors.onSurface,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  shareActions: {
    gap: legendaryTheme.legendary.spacing.md,
    width: '100%',
  },
  shareButton: {
    backgroundColor: legendaryTheme.legendary.colors.legendary,
  },
  cancelButton: {
    marginTop: 0,
  },
  achievementsModal: {
    backgroundColor: 'white',
    margin: legendaryTheme.legendary.spacing.md,
    borderRadius: legendaryTheme.legendary.borders.radius.xl,
    maxHeight: height * 0.8,
  },
  achievementsModalContent: {
    padding: legendaryTheme.legendary.spacing.lg,
  },
  achievementsModalList: {
    maxHeight: height * 0.5,
    marginVertical: legendaryTheme.legendary.spacing.md,
  },
  achievementModalItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: legendaryTheme.legendary.spacing.md,
    gap: legendaryTheme.legendary.spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: legendaryTheme.colors.outline,
  },
  achievementModalContent: {
    flex: 1,
  },
  achievementModalTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.lg,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.onSurface,
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  achievementModalDescription: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.regular,
    color: legendaryTheme.colors.outline,
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  achievementModalDate: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.regular,
    color: legendaryTheme.legendary.colors.legendary,
  },
  closeButton: {
    marginTop: legendaryTheme.legendary.spacing.md,
  },
});

// =====================================
// 🎸 LEGENDARY EXPORTS 🎸
// =====================================

export default LegendaryProfileScreen;

// =====================================
// 🎸 LEGENDARY COMPLETION MESSAGE 🎸
// =====================================

console.log('🎸🎸🎸 LEGENDARY PROFILE SCREEN LOADED! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Profile screen loaded at: 2025-08-06 01:53:06 UTC`);
console.log('👤 User profile management: SWISS PRECISION');
console.log('👑 RICKROLL187 founder features: LEGENDARY');
console.log('🏆 Achievement system: MAXIMUM MOTIVATION');
console.log('⚙️ Settings & preferences: INFINITE CUSTOMIZATION');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
