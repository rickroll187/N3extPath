// File: mobile/src/screens/teams/LegendaryTeamsScreen.tsx
/**
 * 👥🎸 N3EXTPATH - LEGENDARY TEAMS SCREEN 🎸👥
 * Professional team collaboration with Swiss precision
 * Built: 2025-08-06 02:17:58 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  TouchableOpacity,
  Alert,
  Animated,
  Dimensions,
  Image,
} from 'react-native';
import { 
  Card, 
  Button, 
  Chip, 
  Badge, 
  Avatar,
  List,
  Portal,
  Modal,
  FAB,
  Searchbar,
  Menu,
  Divider,
  ProgressBar
} from 'react-native-paper';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation, useFocusEffect } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { useDispatch, useSelector } from 'react-redux';
import * as Animatable from 'react-native-animatable';
import { BarChart, PieChart, LineChart } from 'react-native-chart-kit';

// Import legendary components and services
import { RootStackParamList } from '../../navigation/LegendaryNavigation';
import { RootState } from '../../store';
import { fetchTeamsData, joinTeam, createTeam } from '../../store/slices/teamsSlice';
import { legendaryTheme } from '../../theme/legendaryTheme';
import { LegendaryButton } from '../../components/ui/LegendaryButton';
import { LegendaryCard } from '../../components/ui/LegendaryCard';

type TeamsScreenNavigationProp = NativeStackNavigationProp<RootStackParamList>;

const { width, height } = Dimensions.get('window');

// =====================================
// 👥 TEAMS DATA TYPES 👥
// =====================================

interface TeamMember {
  id: string;
  username: string;
  firstName: string;
  lastName: string;
  email: string;
  jobTitle: string;
  department: string;
  role: 'owner' | 'admin' | 'member';
  isLegendary: boolean;
  isFounder: boolean;
  swissPrecisionScore: number;
  codeBroEnergy: number;
  profileImage?: string;
  lastActive: Date;
  joinedAt: Date;
}

interface Team {
  id: string;
  name: string;
  description: string;
  type: 'project' | 'department' | 'cross_functional' | 'legendary';
  status: 'active' | 'completed' | 'on_hold' | 'archived';
  privacy: 'public' | 'private' | 'invitation_only';
  memberCount: number;
  maxMembers?: number;
  owner: TeamMember;
  admins: TeamMember[];
  members: TeamMember[];
  isLegendary: boolean;
  swissPrecisionMode: boolean;
  codeBroEnergyGoal: boolean;
  averagePerformance: number;
  averageSwissPrecision: number;
  averageCodeBroEnergy: number;
  projectsCount: number;
  okrsCount: number;
  completedTasks: number;
  totalTasks: number;
  createdAt: Date;
  lastActivity: Date;
  tags: string[];
  achievements: string[];
  teamImage?: string;
}

interface TeamsOverview {
  totalTeams: number;
  myTeams: number;
  managedTeams: number;
  legendaryTeams: number;
  averageTeamPerformance: number;
  totalCollaborations: number;
  activeProjects: number;
}

// =====================================
// 🎸 LEGENDARY TEAMS SCREEN 🎸
// =====================================

export function LegendaryTeamsScreen(): JSX.Element {
  const navigation = useNavigation<TeamsScreenNavigationProp>();
  const dispatch = useDispatch();
  
  // Redux state
  const { user } = useSelector((state: RootState) => state.auth);
  const { teamsData, isLoading } = useSelector((state: RootState) => state.teams);
  
  // Local state
  const [refreshing, setRefreshing] = useState(false);
  const [selectedTab, setSelectedTab] = useState('my_teams');
  const [searchQuery, setSearchQuery] = useState('');
  const [showTeamModal, setShowTeamModal] = useState(false);
  const [selectedTeam, setSelectedTeam] = useState<Team | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showJoinModal, setShowJoinModal] = useState(false);
  const [filterMenuVisible, setFilterMenuVisible] = useState(false);
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [sortMenuVisible, setSortMenuVisible] = useState(false);
  const [selectedSort, setSelectedSort] = useState('recent');
  
  // Animation refs
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(30)).current;
  const scaleAnim = useRef(new Animated.Value(0.9)).current;
  const pulseAnim = useRef(new Animated.Value(1)).current;

  // Check if user is RICKROLL187 founder
  const isFounder = user?.username === 'rickroll187';
  const isLegendary = user?.is_legendary || false;
  const userName = user?.first_name || user?.username || 'User';

  // Mock teams overview (in real app, fetch from API)
  const [teamsOverview, setTeamsOverview] = useState<TeamsOverview>({
    totalTeams: isFounder ? 15 : isLegendary ? 8 : 5,
    myTeams: isFounder ? 12 : isLegendary ? 6 : 4,
    managedTeams: isFounder ? 8 : isLegendary ? 3 : 2,
    legendaryTeams: isFounder ? 15 : isLegendary ? 5 : 2,
    averageTeamPerformance: isFounder ? 95.8 : isLegendary ? 87.2 : 78.5,
    totalCollaborations: isFounder ? 150 : isLegendary ? 75 : 35,
    activeProjects: isFounder ? 25 : isLegendary ? 12 : 8,
  });

  // Mock teams data (in real app, fetch from API)
  const [teams, setTeams] = useState<Team[]>([
    {
      id: '1',
      name: isFounder ? '👑 N3EXTPATH Legendary Core Team' : '🎸 Frontend Legends',
      description: isFounder 
        ? 'The legendary founding team building N3EXTPATH with infinite Swiss precision and code bro energy'
        : 'Building legendary user interfaces with Swiss precision and maximum code bro energy',
      type: isFounder ? 'legendary' : 'project',
      status: 'active',
      privacy: isFounder ? 'invitation_only' : 'public',
      memberCount: isFounder ? 8 : 6,
      maxMembers: isFounder ? 10 : 8,
      owner: {
        id: isFounder ? 'founder' : 'lead1',
        username: isFounder ? 'rickroll187' : 'team_lead',
        firstName: isFounder ? 'RICKROLL187' : 'Sarah',
        lastName: isFounder ? '' : 'Johnson',
        email: isFounder ? 'letstalktech010@gmail.com' : 'sarah.johnson@company.com',
        jobTitle: isFounder ? 'Legendary Founder & Chief Code Bro' : 'Senior Frontend Developer',
        department: isFounder ? 'Executive Leadership' : 'Engineering',
        role: 'owner',
        isLegendary: true,
        isFounder: isFounder,
        swissPrecisionScore: isFounder ? 100 : 92,
        codeBroEnergy: isFounder ? 10 : 9,
        lastActive: new Date(),
        joinedAt: new Date('2025-01-01'),
      },
      admins: [],
      members: [
        {
          id: 'member1',
          username: 'alex_dev',
          firstName: 'Alex',
          lastName: 'Chen',
          email: 'alex.chen@company.com',
          jobTitle: 'Full Stack Developer',
          department: 'Engineering',
          role: 'member',
          isLegendary: isLegendary,
          isFounder: false,
          swissPrecisionScore: isFounder ? 95 : 85,
          codeBroEnergy: isFounder ? 9 : 7,
          lastActive: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
          joinedAt: new Date('2025-02-15'),
        },
        {
          id: 'member2',
          username: 'maria_ux',
          firstName: 'Maria',
          lastName: 'Rodriguez',
          email: 'maria.rodriguez@company.com',
          jobTitle: 'UX Designer',
          department: 'Design',
          role: 'member',
          isLegendary: isLegendary,
          isFounder: false,
          swissPrecisionScore: isFounder ? 98 : 88,
          codeBroEnergy: isFounder ? 8 : 8,
          lastActive: new Date(Date.now() - 30 * 60 * 1000), // 30 minutes ago
          joinedAt: new Date('2025-03-01'),
        },
      ],
      isLegendary: true,
      swissPrecisionMode: true,
      codeBroEnergyGoal: true,
      averagePerformance: isFounder ? 97.5 : 88.2,
      averageSwissPrecision: isFounder ? 98.2 : 89.5,
      averageCodeBroEnergy: isFounder ? 9.5 : 8.2,
      projectsCount: isFounder ? 15 : 8,
      okrsCount: isFounder ? 12 : 5,
      completedTasks: isFounder ? 245 : 156,
      totalTasks: isFounder ? 280 : 180,
      createdAt: new Date('2025-01-01'),
      lastActivity: new Date(),
      tags: ['legendary', 'swiss-precision', 'code-bro-energy', isFounder ? 'founder-team' : 'frontend'],
      achievements: [
        isFounder ? '👑 Legendary Platform Creation' : '🎸 Legendary UI Development',
        isFounder ? '⚙️ Swiss Precision Architecture' : '⚙️ Swiss Precision Components',
        isFounder ? '💪 Infinite Code Bro Energy' : '💪 Maximum Code Bro Energy',
      ],
    },
    {
      id: '2',
      name: isFounder ? '🚀 Platform Innovation Squad' : '⚙️ Backend Precision Team',
      description: isFounder 
        ? 'Innovation team pushing legendary boundaries with Swiss precision technology'
        : 'Building robust backend systems with Swiss precision and legendary reliability',
      type: 'project',
      status: 'active',
      privacy: 'public',
      memberCount: isFounder ? 6 : 5,
      maxMembers: 8,
      owner: {
        id: 'owner2',
        username: isFounder ? 'innovation_lead' : 'backend_lead',
        firstName: isFounder ? 'James' : 'David',
        lastName: isFounder ? 'Mitchell' : 'Thompson',
        email: isFounder ? 'james.mitchell@company.com' : 'david.thompson@company.com',
        jobTitle: isFounder ? 'Chief Innovation Officer' : 'Senior Backend Developer',
        department: 'Engineering',
        role: 'owner',
        isLegendary: isLegendary,
        isFounder: false,
        swissPrecisionScore: isFounder ? 94 : 87,
        codeBroEnergy: isFounder ? 9 : 8,
        lastActive: new Date(Date.now() - 60 * 60 * 1000), // 1 hour ago
        joinedAt: new Date('2025-02-01'),
      },
      admins: [],
      members: [],
      isLegendary: isLegendary,
      swissPrecisionMode: true,
      codeBroEnergyGoal: true,
      averagePerformance: isFounder ? 92.8 : 84.5,
      averageSwissPrecision: isFounder ? 94.2 : 86.8,
      averageCodeBroEnergy: isFounder ? 8.8 : 7.8,
      projectsCount: isFounder ? 10 : 6,
      okrsCount: isFounder ? 8 : 4,
      completedTasks: isFounder ? 189 : 124,
      totalTasks: isFounder ? 220 : 150,
      createdAt: new Date('2025-02-01'),
      lastActivity: new Date(Date.now() - 60 * 60 * 1000),
      tags: ['innovation', 'swiss-precision', isFounder ? 'legendary' : 'backend', 'api'],
      achievements: [
        isFounder ? '🚀 Innovation Excellence' : '⚙️ System Architecture Excellence',
        '📊 Performance Optimization',
        '🔒 Security Implementation',
      ],
    },
    {
      id: '3',
      name: isFounder ? '🎸 Global Code Bro Alliance' : '👥 Cross-Platform Team',
      description: isFounder 
        ? 'Worldwide alliance of legendary code bros spreading Swiss precision and infinite energy'
        : 'Cross-platform development team building legendary mobile and web experiences',
      type: isFounder ? 'legendary' : 'cross_functional',
      status: 'active',
      privacy: isFounder ? 'public' : 'public',
      memberCount: isFounder ? 25 : 7,
      maxMembers: isFounder ? 50 : 10,
      owner: {
        id: 'owner3',
        username: isFounder ? 'global_coordinator' : 'crossplatform_lead',
        firstName: isFounder ? 'Elena' : 'Michael',
        lastName: isFounder ? 'Volkov' : 'Park',
        email: isFounder ? 'elena.volkov@company.com' : 'michael.park@company.com',
        jobTitle: isFounder ? 'Global Code Bro Coordinator' : 'Cross-Platform Lead',
        department: isFounder ? 'Global Operations' : 'Engineering',
        role: 'owner',
        isLegendary: true,
        isFounder: false,
        swissPrecisionScore: isFounder ? 96 : 89,
        codeBroEnergy: isFounder ? 10 : 8,
        lastActive: new Date(Date.now() - 15 * 60 * 1000), // 15 minutes ago
        joinedAt: new Date('2025-01-15'),
      },
      admins: [],
      members: [],
      isLegendary: true,
      swissPrecisionMode: true,
      codeBroEnergyGoal: true,
      averagePerformance: isFounder ? 94.5 : 86.2,
      averageSwissPrecision: isFounder ? 95.8 : 88.5,
      averageCodeBroEnergy: isFounder ? 9.2 : 8.5,
      projectsCount: isFounder ? 20 : 9,
      okrsCount: isFounder ? 15 : 6,
      completedTasks: isFounder ? 320 : 178,
      totalTasks: isFounder ? 380 : 210,
      createdAt: new Date('2025-01-15'),
      lastActivity: new Date(Date.now() - 15 * 60 * 1000),
      tags: [isFounder ? 'global' : 'cross-platform', 'legendary', 'code-bro-alliance', 'collaboration'],
      achievements: [
        isFounder ? '🌍 Global Code Bro Network' : '📱 Cross-Platform Excellence',
        isFounder ? '⚙️ International Swiss Precision' : '⚙️ Multi-Platform Swiss Precision',
        isFounder ? '🎸 Legendary Community Building' : '🎸 Team Collaboration Excellence',
      ],
    },
  ]);

  useEffect(() => {
    console.log('👥🎸👥 LEGENDARY TEAMS SCREEN LOADED! 👥🎸👥');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Teams screen loaded at: 2025-08-06 02:17:58 UTC`);
    
    if (isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER TEAMS MASTERY ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY TEAM LEADERSHIP WITH INFINITE CODE BRO ENERGY!');
      console.log('⚙️ SWISS PRECISION TEAM MANAGEMENT!');
    }

    // Start legendary animations
    startLegendaryAnimations();
    
    // Set up founder pulse animation
    if (isFounder) {
      startFounderAnimations();
    }

    // Load teams data
    loadTeamsData();
  }, []);

  useFocusEffect(
    useCallback(() => {
      loadTeamsData();
    }, [])
  );

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
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.02,
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
  };

  const loadTeamsData = async () => {
    try {
      console.log('👥 Loading legendary teams data...');
      
      // Dispatch teams data fetch
      // await dispatch(fetchTeamsData() as any);
      
      console.log('✅ Teams data loaded with Swiss precision!');
      
    } catch (error) {
      console.error('🚨 Error loading teams data:', error);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    console.log('🔄 Refreshing legendary teams data...');
    
    try {
      await loadTeamsData();
      
      if (isFounder) {
        console.log('👑 RICKROLL187 teams data refreshed with infinite power!');
      }
    } catch (error) {
      console.error('🚨 Error refreshing teams data:', error);
    } finally {
      setRefreshing(false);
    }
  };

  const handleTeamPress = (team: Team) => {
    setSelectedTeam(team);
    setShowTeamModal(true);
    console.log(`👥 Viewing team: ${team.name}`);
  };

  const handleCreateTeam = () => {
    console.log('📝 Creating new legendary team...');
    setShowCreateModal(true);
  };

  const handleJoinTeam = () => {
    console.log('🚀 Joining legendary team...');
    setShowJoinModal(true);
  };

  const handleJoinTeamAction = async (teamId: string) => {
    try {
      console.log(`🤝 Joining team: ${teamId}`);
      
      // In real app, dispatch join team action
      // await dispatch(joinTeam({ teamId }) as any);
      
      Alert.alert(
        '✅ Team Joined',
        isFounder 
          ? '👑 Welcome to the legendary team! Your infinite code bro energy will inspire everyone!'
          : '🎸 Welcome to the team! Get ready for legendary collaboration with Swiss precision!'
      );
      
    } catch (error) {
      console.error('🚨 Error joining team:', error);
      Alert.alert('Error', 'Failed to join team');
    }
  };

  const getTeamTypeColor = (type: string): string => {
    switch (type) {
      case 'legendary': return legendaryTheme.legendary.colors.legendary;
      case 'project': return legendaryTheme.legendary.colors.info;
      case 'department': return legendaryTheme.legendary.colors.swissPrecision;
      case 'cross_functional': return legendaryTheme.legendary.colors.codeBroEnergy;
      default: return legendaryTheme.colors.outline;
    }
  };

  const getTeamStatusColor = (status: string): string => {
    switch (status) {
      case 'active': return legendaryTheme.legendary.colors.success;
      case 'completed': return legendaryTheme.legendary.colors.legendary;
      case 'on_hold': return legendaryTheme.legendary.colors.warning;
      case 'archived': return legendaryTheme.colors.outline;
      default: return legendaryTheme.colors.outline;
    }
  };

  const getPerformanceColor = (score: number): string => {
    if (score >= 95) return legendaryTheme.legendary.colors.legendary;
    if (score >= 85) return legendaryTheme.legendary.colors.success;
    if (score >= 75) return legendaryTheme.legendary.colors.info;
    if (score >= 65) return legendaryTheme.legendary.colors.warning;
    return legendaryTheme.legendary.colors.error;
  };

  const filteredTeams = teams.filter(team => {
    const matchesTab = 
      selectedTab === 'all' ||
      (selectedTab === 'my_teams' && (team.owner.username === user?.username || team.members.some(m => m.username === user?.username))) ||
      (selectedTab === 'managed' && team.owner.username === user?.username) ||
      (selectedTab === 'available' && team.privacy === 'public');
      
    const matchesFilter = 
      selectedFilter === 'all' ||
      (selectedFilter === 'legendary' && team.isLegendary) ||
      (selectedFilter === 'swiss_precision' && team.swissPrecisionMode) ||
      (selectedFilter === 'code_bro' && team.codeBroEnergyGoal) ||
      (selectedFilter === 'type' && team.type === 'legendary');
      
    const matchesSearch = 
      team.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      team.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      team.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));
    
    return matchesTab && matchesFilter && matchesSearch;
  });

  const sortedTeams = [...filteredTeams].sort((a, b) => {
    switch (selectedSort) {
      case 'recent':
        return b.lastActivity.getTime() - a.lastActivity.getTime();
      case 'name':
        return a.name.localeCompare(b.name);
      case 'performance':
        return b.averagePerformance - a.averagePerformance;
      case 'members':
        return b.memberCount - a.memberCount;
      default:
        return 0;
    }
  });

  const renderTeamsHeader = () => (
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
        <View style={styles.headerContent}>
          <Animatable.View 
            animation={isFounder ? "pulse" : "fadeIn"}
            iterationCount={isFounder ? "infinite" : 1}
            style={styles.headerIcon}
          >
            <Ionicons 
              name={isFounder ? "crown" : isLegendary ? "people" : "people-outline"} 
              size={50} 
              color="#ffffff" 
            />
          </Animatable.View>
          
          <Text style={styles.headerTitle}>
            {isFounder ? '👑 Legendary Team Empire' : '👥 Your Teams'}
          </Text>
          
          <Text style={styles.headerSubtitle}>
            {isFounder 
              ? 'Infinite Teams • Swiss Precision Leadership'
              : isLegendary 
              ? 'Legendary Collaboration • Swiss Precision Teams'
              : 'Building legendary teamwork with Swiss precision'
            }
          </Text>

          {/* Teams Summary Stats */}
          <View style={styles.summaryStats}>
            <View style={styles.summaryStatItem}>
              <Text style={styles.summaryStatValue}>{teamsOverview.myTeams}</Text>
              <Text style={styles.summaryStatLabel}>My Teams</Text>
            </View>
            <View style={styles.summaryStatDivider} />
            <View style={styles.summaryStatItem}>
              <Text style={styles.summaryStatValue}>{teamsOverview.managedTeams}</Text>
              <Text style={styles.summaryStatLabel}>Managed</Text>
            </View>
            <View style={styles.summaryStatDivider} />
            <View style={styles.summaryStatItem}>
              <Text style={styles.summaryStatValue}>{teamsOverview.averageTeamPerformance.toFixed(0)}%</Text>
              <Text style={styles.summaryStatLabel}>Avg Performance</Text>
            </View>
          </View>

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
        </View>
      </LinearGradient>
    </Animated.View>
  );

  const renderTeamsChart = () => {
    const chartData = [
      {
        name: 'Legendary',
        population: teamsOverview.legendaryTeams,
        color: legendaryTheme.legendary.colors.legendary,
        legendFontColor: '#7F7F7F',
        legendFontSize: 12,
      },
      {
        name: 'Regular',
        population: teamsOverview.totalTeams - teamsOverview.legendaryTeams,
        color: legendaryTheme.colors.primary,
        legendFontColor: '#7F7F7F',
        legendFontSize: 12,
      },
    ];

    return (
      <Animated.View 
        style={[
          styles.chartContainer,
          {
            opacity: fadeAnim,
            transform: [{ translateY: slideAnim }],
          },
        ]}
      >
        <LegendaryCard style={styles.chartCard}>
          <Text style={styles.sectionTitle}>
            📊 {isFounder ? 'Legendary Team Empire Overview' : 'Team Overview'}
          </Text>
          
          <PieChart
            data={chartData}
            width={width - 60}
            height={200}
            chartConfig={{
              color: (opacity = 1) => `rgba(26, 26, 26, ${opacity})`,
            }}
            accessor="population"
            backgroundColor="transparent"
            paddingLeft="15"
            absolute
            style={styles.chart}
          />
          
          <View style={styles.chartStats}>
            <View style={styles.chartStatItem}>
              <Text style={styles.chartStatValue}>{teamsOverview.totalTeams}</Text>
              <Text style={styles.chartStatLabel}>Total Teams</Text>
            </View>
            <View style={styles.chartStatItem}>
              <Text style={styles.chartStatValue}>{teamsOverview.activeProjects}</Text>
              <Text style={styles.chartStatLabel}>Active Projects</Text>
            </View>
            <View style={styles.chartStatItem}>
              <Text style={styles.chartStatValue}>{teamsOverview.totalCollaborations}</Text>
              <Text style={styles.chartStatLabel}>Collaborations</Text>
            </View>
          </View>
        </LegendaryCard>
      </Animated.View>
    );
  };

  const renderTabsAndFilters = () => (
    <Animated.View 
      style={[
        styles.filtersContainer,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      {/* Search Bar */}
      <Searchbar
        placeholder="Search legendary teams..."
        onChangeText={setSearchQuery}
        value={searchQuery}
        style={styles.searchBar}
        iconColor={legendaryTheme.legendary.colors.legendary}
      />

      {/* Tabs */}
      <View style={styles.tabsContainer}>
        {[
          { key: 'my_teams', label: 'My Teams' },
          { key: 'managed', label: 'Managed' },
          { key: 'available', label: 'Available' },
          { key: 'all', label: 'All' }
        ].map((tab) => (
          <TouchableOpacity
            key={tab.key}
            onPress={() => setSelectedTab(tab.key)}
            style={[
              styles.tabButton,
              selectedTab === tab.key && styles.activeTabButton,
            ]}
          >
            <Text style={[
              styles.tabButtonText,
              selectedTab === tab.key && styles.activeTabButtonText,
            ]}>
              {tab.label}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Filter and Sort Controls */}
      <View style={styles.controlsContainer}>
        {/* Filter Menu */}
        <Menu
          visible={filterMenuVisible}
          onDismiss={() => setFilterMenuVisible(false)}
          anchor={
            <TouchableOpacity
              onPress={() => setFilterMenuVisible(true)}
              style={styles.controlButton}
            >
              <Ionicons name="filter" size={20} color={legendaryTheme.colors.primary} />
              <Text style={styles.controlButtonText}>Filter</Text>
            </TouchableOpacity>
          }
        >
          <Menu.Item onPress={() => { setSelectedFilter('all'); setFilterMenuVisible(false); }} title="All Teams" />
          <Menu.Item onPress={() => { setSelectedFilter('legendary'); setFilterMenuVisible(false); }} title="🎸 Legendary" />
          <Menu.Item onPress={() => { setSelectedFilter('swiss_precision'); setFilterMenuVisible(false); }} title="⚙️ Swiss Precision" />
          <Menu.Item onPress={() => { setSelectedFilter('code_bro'); setFilterMenuVisible(false); }} title="💪 Code Bro Energy" />
        </Menu>

        {/* Sort Menu */}
        <Menu
          visible={sortMenuVisible}
          onDismiss={() => setSortMenuVisible(false)}
          anchor={
            <TouchableOpacity
              onPress={() => setSortMenuVisible(true)}
              style={styles.controlButton}
            >
              <Ionicons name="swap-vertical" size={20} color={legendaryTheme.colors.primary} />
              <Text style={styles.controlButtonText}>Sort</Text>
            </TouchableOpacity>
          }
        >
          <Menu.Item onPress={() => { setSelectedSort('recent'); setSortMenuVisible(false); }} title="Recent Activity" />
          <Menu.Item onPress={() => { setSelectedSort('name'); setSortMenuVisible(false); }} title="Name" />
          <Menu.Item onPress={() => { setSelectedSort('performance'); setSortMenuVisible(false); }} title="Performance" />
          <Menu.Item onPress={() => { setSelectedSort('members'); setSortMenuVisible(false); }} title="Team Size" />
        </Menu>
      </View>
    </Animated.View>
  );

  const renderTeamsList = () => (
    <Animated.View 
      style={[
        styles.teamsListContainer,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      <View style={styles.teamsListHeader}>
        <Text style={styles.sectionTitle}>
          {selectedTab === 'my_teams' ? '👥 My Teams' : 
           selectedTab === 'managed' ? '👑 Managed Teams' : 
           selectedTab === 'available' ? '🌟 Available Teams' : 
           '📋 All Teams'}
        </Text>
        <Badge style={styles.teamsCountBadge}>
          {sortedTeams.length}
        </Badge>
      </View>
      
      <View style={styles.teamsList}>
        {sortedTeams.map((team, index) => (
          <Animatable.View 
            key={team.id}
            animation="fadeInUp"
            delay={300 + (index * 100)}
          >
            <TouchableOpacity
              onPress={() => handleTeamPress(team)}
              style={styles.teamCard}
            >
              <LegendaryCard style={[
                styles.teamCardContent,
                team.isLegendary && styles.legendaryTeamCard,
                isFounder && team.type === 'legendary' && styles.founderTeamCard
              ]}>
                {/* Team Header */}
                <View style={styles.teamCardHeader}>
                  <View style={styles.teamImageContainer}>
                    {team.teamImage ? (
                      <Image source={{ uri: team.teamImage }} style={styles.teamImage} />
                    ) : (
                      <View style={[
                        styles.teamImagePlaceholder,
                        { backgroundColor: getTeamTypeColor(team.type) }
                      ]}>
                        <Ionicons 
                          name={team.type === 'legendary' ? "crown" : "people"} 
                          size={24} 
                          color="#ffffff" 
                        />
                      </View>
                    )}
                  </View>
                  
                  <View style={styles.teamMainInfo}>
                    <Text style={styles.teamName} numberOfLines={1}>
                      {team.name}
                    </Text>
                    <Text style={styles.teamDescription} numberOfLines={2}>
                      {team.description}
                    </Text>
                    <View style={styles.teamMeta}>
                      <Text style={styles.teamMembers}>
                        {team.memberCount} members
                      </Text>
                      <Text style={styles.teamType}>
                        • {team.type.replace('_', ' ')}
                      </Text>
                    </View>
                  </View>
                  
                  <View style={styles.teamBadges}>
                    <Chip 
                      style={[
                        styles.statusChip,
                        { backgroundColor: getTeamStatusColor(team.status) }
                      ]}
                      textStyle={styles.statusChipText}
                    >
                      {team.status}
                    </Chip>
                  </View>
                </View>

                {/* Performance Metrics */}
                <View style={styles.teamMetrics}>
                  <View style={styles.metricItem}>
                    <Text style={styles.metricLabel}>Performance</Text>
                    <Text style={[
                      styles.metricValue,
                      { color: getPerformanceColor(team.averagePerformance) }
                    ]}>
                      {team.averagePerformance.toFixed(1)}%
                    </Text>
                  </View>
                  <View style={styles.metricItem}>
                    <Text style={styles.metricLabel}>Swiss Precision</Text>
                    <Text style={[
                      styles.metricValue,
                      { color: getPerformanceColor(team.averageSwissPrecision) }
                    ]}>
                      {team.averageSwissPrecision.toFixed(1)}%
                    </Text>
                  </View>
                  <View style={styles.metricItem}>
                    <Text style={styles.metricLabel}>Code Bro Energy</Text>
                    <Text style={[
                      styles.metricValue,
                      { color: getPerformanceColor(team.averageCodeBroEnergy * 10) }
                    ]}>
                      {team.averageCodeBroEnergy.toFixed(1)}/10
                    </Text>
                  </View>
                </View>

                {/* Progress Bar */}
                <View style={styles.teamProgress}>
                  <View style={styles.progressHeader}>
                    <Text style={styles.progressLabel}>Project Progress</Text>
                    <Text style={styles.progressValue}>
                      {Math.round((team.completedTasks / team.totalTasks) * 100)}%
                    </Text>
                  </View>
                  <ProgressBar
                    progress={team.completedTasks / team.totalTasks}
                    color={getPerformanceColor(team.averagePerformance)}
                    style={styles.progressBar}
                  />
                  <Text style={styles.progressDetails}>
                    {team.completedTasks} / {team.totalTasks} tasks completed
                  </Text>
                </View>

                {/* Team Members Preview */}
                <View style={styles.membersPreview}>
                  <Text style={styles.membersLabel}>Team Members</Text>
                  <View style={styles.membersAvatars}>
                    <Avatar.Image
                      size={32}
                      source={{ 
                        uri: `https://ui-avatars.com/api/?name=${team.owner.firstName}+${team.owner.lastName}&background=${team.owner.isFounder ? 'FFD700' : team.owner.isLegendary ? '1E90FF' : '6c757d'}&color=fff&size=32`
                      }}
                      style={[
                        styles.memberAvatar,
                        team.owner.isFounder && styles.founderAvatar,
                        team.owner.isLegendary && styles.legendaryAvatar
                      ]}
                    />
                    {team.members.slice(0, 3).map((member) => (
                      <Avatar.Image
                        key={member.id}
                        size={32}
                        source={{ 
                          uri: `https://ui-avatars.com/api/?name=${member.firstName}+${member.lastName}&background=${member.isLegendary ? '1E90FF' : '6c757d'}&color=fff&size=32`
                        }}
                        style={[
                          styles.memberAvatar,
                          member.isLegendary && styles.legendaryAvatar
                        ]}
                      />
                    ))}
                    {team.memberCount > 4 && (
                      <View style={styles.moreMembers}>
                        <Text style={styles.moreMembersText}>
                          +{team.memberCount - 4}
                        </Text>
                      </View>
                    )}
                  </View>
                </View>

                {/* Special Badges */}
                <View style={styles.specialBadges}>
                  {team.isLegendary && (
                    <Chip 
                      style={[styles.specialChip, { backgroundColor: legendaryTheme.legendary.colors.legendary }]}
                      textStyle={styles.specialChipText}
                      icon="star"
                    >
                      Legendary
                    </Chip>
                  )}
                  {team.swissPrecisionMode && (
                    <Chip 
                      style={[styles.specialChip, { backgroundColor: legendaryTheme.legendary.colors.swissPrecision }]}
                      textStyle={styles.specialChipText}
                      icon="precision-manufacturing"
                    >
                      Swiss Precision
                    </Chip>
                  )}
                  {team.codeBroEnergyGoal && (
                    <Chip 
                      style={[styles.specialChip, { backgroundColor: legendaryTheme.legendary.colors.codeBroEnergy }]}
                      textStyle={styles.specialChipText}
                      icon="musical-notes"
                    >
                      Code Bro Energy
                    </Chip>
                  )}
                </View>

                {/* Last Activity */}
                <View style={styles.teamFooter}>
                  <Text style={styles.lastActivity}>
                    Last activity: {team.lastActivity.toLocaleString()}
                  </Text>
                  <Ionicons name="chevron-forward" size={20} color={legendaryTheme.colors.outline} />
                </View>
              </LegendaryCard>
            </TouchableOpacity>
          </Animatable.View>
        ))}
      </View>

      {sortedTeams.length === 0 && (
        <Animatable.View 
          animation="fadeIn"
          style={styles.emptyState}
        >
          <Ionicons 
            name="people" 
            size={80} 
            color={legendaryTheme.colors.outline} 
          />
          <Text style={styles.emptyStateTitle}>
            No Teams Found
          </Text>
          <Text style={styles.emptyStateDescription}>
            {searchQuery 
              ? 'Try adjusting your search or filter criteria'
              : selectedTab === 'my_teams'
              ? 'Join your first legendary team or create one!'
              : 'No teams available in this category.'
            }
          </Text>
          <View style={styles.emptyStateActions}>
            <LegendaryButton
              mode="contained"
              onPress={handleCreateTeam}
              style={styles.emptyStateButton}
              icon="plus"
            >
              Create Legendary Team
            </LegendaryButton>
            <LegendaryButton
              mode="outlined"
              onPress={handleJoinTeam}
              style={styles.emptyStateButton}
              icon="person-add"
            >
              Join Team
            </LegendaryButton>
          </View>
        </Animatable.View>
      )}
    </Animated.View>
  );

  return (
    <View style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={handleRefresh}
            colors={[legendaryTheme.legendary.colors.legendary]}
            tintColor={legendaryTheme.legendary.colors.legendary}
          />
        }
      >
        {/* Teams Header */}
        {renderTeamsHeader()}
        
        {/* Teams Chart */}
        {renderTeamsChart()}
        
        {/* Tabs and Filters */}
        {renderTabsAndFilters()}
        
        {/* Teams List */}
        {renderTeamsList()}
        
        {/* Bottom Spacing */}
        <View style={styles.bottomSpacing} />
      </ScrollView>

      {/* Floating Action Buttons */}
      <View style={styles.fabContainer}>
        <FAB
          icon={isFounder ? "crown" : "plus"}
          style={[
            styles.fab,
            styles.createFab,
            {
              backgroundColor: isFounder 
                ? legendaryTheme.legendary.colors.legendary
                : legendaryTheme.colors.primary,
            }
          ]}
          onPress={handleCreateTeam}
          label={isFounder ? "Legendary Team" : "Create Team"}
        />
        
        <FAB
          icon="person-add"
          style={[
            styles.fab,
            styles.joinFab,
            {
              backgroundColor: legendaryTheme.legendary.colors.codeBroEnergy,
            }
          ]}
          onPress={handleJoinTeam}
          label="Join Team"
        />
      </View>

      {/* Team Detail Modal */}
      <Portal>
        <Modal
          visible={showTeamModal}
          onDismiss={() => setShowTeamModal(false)}
          contentContainerStyle={styles.teamModal}
        >
          {selectedTeam && (
            <ScrollView style={styles.teamModalContent} showsVerticalScrollIndicator={false}>
              <View style={styles.modalHeader}>
                <View style={styles.modalTitleContainer}>
                  <Text style={styles.modalTitle} numberOfLines={2}>
                    {selectedTeam.name}
                  </Text>
                  <View style={styles.modalBadges}>
                    {selectedTeam.isLegendary && (
                      <Chip 
                        style={[styles.modalBadge, { backgroundColor: legendaryTheme.legendary.colors.legendary }]}
                        textStyle={styles.modalBadgeText}
                      >
                        Legendary
                      </Chip>
                    )}
                    <Chip 
                      style={[styles.modalBadge, { backgroundColor: getTeamStatusColor(selectedTeam.status) }]}
                      textStyle={styles.modalBadgeText}
                    >
                      {selectedTeam.status}
                    </Chip>
                  </View>
                </View>
                <TouchableOpacity
                  onPress={() => setShowTeamModal(false)}
                  style={styles.closeButton}
                >
                  <Ionicons name="close" size={24} color={legendaryTheme.colors.primary} />
                </TouchableOpacity>
              </View>

              <Text style={styles.modalDescription}>
                {selectedTeam.description}
              </Text>

              <View style={styles.modalStats}>
                <View style={styles.modalStatItem}>
                  <Text style={styles.modalStatValue}>
                    {selectedTeam.memberCount}
                  </Text>
                  <Text style={styles.modalStatLabel}>Members</Text>
                </View>
                <View style={styles.modalStatItem}>
                  <Text style={styles.modalStatValue}>
                    {selectedTeam.projectsCount}
                  </Text>
                  <Text style={styles.modalStatLabel}>Projects</Text>
                </View>
                <View style={styles.modalStatItem}>
                  <Text style={styles.modalStatValue}>
                    {selectedTeam.averagePerformance.toFixed(0)}%
                  </Text>
                  <Text style={styles.modalStatLabel}>Performance</Text>
                </View>
                <View style={styles.modalStatItem}>
                  <Text style={styles.modalStatValue}>
                    {selectedTeam.averageCodeBroEnergy.toFixed(1)}/10
                  </Text>
                  <Text style={styles.modalStatLabel}>Code Bro Energy</Text>
                </View>
              </View>

              <Text style={styles.modalSectionTitle}>👥 Team Members</Text>
              
              <View style={styles.membersList}>
                {/* Team Owner */}
                <View style={styles.memberItem}>
                  <Avatar.Image
                    size={48}
                    source={{ 
                      uri: `https://ui-avatars.com/api/?name=${selectedTeam.owner.firstName}+${selectedTeam.owner.lastName}&background=${selectedTeam.owner.isFounder ? 'FFD700' : selectedTeam.owner.isLegendary ? '1E90FF' : '6c757d'}&color=fff&size=48`
                    }}
                    style={[
                      styles.memberItemAvatar,
                      selectedTeam.owner.isFounder && styles.founderAvatar,
                      selectedTeam.owner.isLegendary && styles.legendaryAvatar
                    ]}
                  />
                  <View style={styles.memberInfo}>
                    <View style={styles.memberNameContainer}>
                      <Text style={styles.memberName}>
                        {selectedTeam.owner.isFounder ? '👑 ' : ''}{selectedTeam.owner.firstName} {selectedTeam.owner.lastName}
                      </Text>
                      <Chip 
                        style={[styles.roleChip, { backgroundColor: legendaryTheme.legendary.colors.legendary }]}
                        textStyle={styles.roleChipText}
                      >
                        Owner
                      </Chip>
                    </View>
                    <Text style={styles.memberJobTitle}>{selectedTeam.owner.jobTitle}</Text>
                    <View style={styles.memberMetrics}>
                      <Text style={styles.memberMetric}>
                        Swiss Precision: {selectedTeam.owner.swissPrecisionScore}%
                      </Text>
                      <Text style={styles.memberMetric}>
                        Code Bro Energy: {selectedTeam.owner.codeBroEnergy}/10
                      </Text>
                    </View>
                  </View>
                </View>

                {/* Team Members */}
                {selectedTeam.members.map((member) => (
                  <View key={member.id} style={styles.memberItem}>
                    <Avatar.Image
                      size={48}
                      source={{ 
                        uri: `https://ui-avatars.com/api/?name=${member.firstName}+${member.lastName}&background=${member.isLegendary ? '1E90FF' : '6c757d'}&color=fff&size=48`
                      }}
                      style={[
                        styles.memberItemAvatar,
                        member.isLegendary && styles.legendaryAvatar
                      ]}
                    />
                    <View style={styles.memberInfo}>
                      <View style={styles.memberNameContainer}>
                        <Text style={styles.memberName}>
                          {member.isLegendary ? '🎸 ' : ''}{member.firstName} {member.lastName}
                        </Text>
                        <Chip 
                          style={[styles.roleChip, { backgroundColor: legendaryTheme.colors.primary }]}
                          textStyle={styles.roleChipText}
                        >
                          {member.role}
                        </Chip>
                      </View>
                      <Text style={styles.memberJobTitle}>{member.jobTitle}</Text>
                      <View style={styles.memberMetrics}>
                        <Text style={styles.memberMetric}>
                          Swiss Precision: {member.swissPrecisionScore}%
                        </Text>
                        <Text style={styles.memberMetric}>
                          Code Bro Energy: {member.codeBroEnergy}/10
                        </Text>
                      </View>
                    </View>
                  </View>
                ))}
              </View>

              <Text style={styles.modalSectionTitle}>🏆 Team Achievements</Text>
              <View style={styles.achievementsList}>
                {selectedTeam.achievements.map((achievement, index) => (
                  <Text key={index} style={styles.achievementItem}>
                    • {achievement}
                  </Text>
                ))}
              </View>

              <Text style={styles.modalSectionTitle}>🏷️ Tags</Text>
              <View style={styles.tagsList}>
                {selectedTeam.tags.map((tag) => (
                  <Chip 
                    key={tag}
                    style={styles.tagChip}
                    textStyle={styles.tagChipText}
                  >
                    {tag}
                  </Chip>
                ))}
              </View>

              <View style={styles.modalActions}>
                <LegendaryButton
                  mode="contained"
                  onPress={() => {
                    console.log('Viewing team details:', selectedTeam.id);
                    setShowTeamModal(false);
                  }}
                  style={styles.modalActionButton}
                  icon="eye"
                >
                  View Full Team
                </LegendaryButton>
                
                {selectedTeam.owner.username !== user?.username && (
                  <LegendaryButton
                    mode="outlined"
                    onPress={() => {
                      handleJoinTeamAction(selectedTeam.id);
                      setShowTeamModal(false);
                    }}
                    style={styles.modalActionButton}
                    icon="person-add"
                  >
                    Join Team
                  </LegendaryButton>
                )}
                
                <LegendaryButton
                  mode="text"
                  onPress={() => setShowTeamModal(false)}
                  style={styles.modalActionButton}
                >
                  Close
                </LegendaryButton>
              </View>
            </ScrollView>
          )}
        </Modal>
      </Portal>

      {/* Create Team Modal */}
      <Portal>
        <Modal
          visible={showCreateModal}
          onDismiss={() => setShowCreateModal(false)}
          contentContainerStyle={styles.createModal}
        >
          <View style={styles.createModalContent}>
            <Text style={styles.createModalTitle}>👥 Create Legendary Team</Text>
            <Text style={styles.createModalDescription}>
              {isFounder 
                ? '👑 Create a legendary team with infinite Swiss precision and code bro energy!'
                : '🎸 Build your legendary team with Swiss precision collaboration!'}
            </Text>
            
            <View style={styles.createModalActions}>
              <LegendaryButton
                mode="contained"
                onPress={() => {
                  console.log('Starting team creation...');
                  setShowCreateModal(false);
                  Alert.alert(
                    '🚀 Team Creation',
                    'Team creation feature will be available in the next update!\n\nFor now, contact RICKROLL187 at letstalktech010@gmail.com for legendary team setup!'
                  );
                }}
                style={styles.createButton}
                icon="plus"
              >
                🎸 Start Creating
              </LegendaryButton>
              
              <LegendaryButton
                mode="text"
                onPress={() => setShowCreateModal(false)}
                style={styles.cancelButton}
              >
                Cancel
              </LegendaryButton>
            </View>
          </View>
        </Modal>
      </Portal>

      {/* Join Team Modal */}
      <Portal>
        <Modal
          visible={showJoinModal}
          onDismiss={() => setShowJoinModal(false)}
          contentContainerStyle={styles.joinModal}
        >
          <View style={styles.joinModalContent}>
            <Text style={styles.joinModalTitle}>🤝 Join Legendary Team</Text>
            <Text style={styles.joinModalDescription}>
              Enter team code or browse available teams to join the legendary collaboration!
            </Text>
            
            <View style={styles.joinModalActions}>
              <LegendaryButton
                mode="contained"
                onPress={() => {
                  console.log('Starting team join process...');
                  setShowJoinModal(false);
                  Alert.alert(
                    '🤝 Join Team',
                    'Team joining feature will be available in the next update!\n\nFor now, contact team leaders directly or reach out to RICKROLL187 at letstalktech010@gmail.com!'
                  );
                }}
                style={styles.joinButton}
                icon="person-add"
              >
                🎸 Browse Teams
              </LegendaryButton>
              
              <LegendaryButton
                mode="text"
                onPress={() => setShowJoinModal(false)}
                style={styles.cancelButton}
              >
                Cancel
              </LegendaryButton>
            </View>
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
    paddingBottom: 120,
  },
  headerContainer: {
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  headerGradient: {
    padding: legendaryTheme.legendary.spacing.lg,
    alignItems: 'center',
  },
  headerContent: {
    alignItems: 'center',
    width: '100%',
  },
  headerIcon: {
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  headerTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize['2xl'],
    fontFamily: legendaryTheme.legendary.typography.fontFamily.legendaryBold,
    color: '#ffffff',
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.sm,
    textShadowColor: 'rgba(0, 0, 0, 0.3)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
  },
  headerSubtitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
    color: 'rgba(255, 255, 255, 0.9)',
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  summaryStats: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
    padding: legendaryTheme.legendary.spacing.md,
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  summaryStatItem: {
    alignItems: 'center',
  },
  summaryStatValue: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xl,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: '#ffffff',
    textShadowColor: 'rgba(0, 0, 0, 0.3)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
  },
  summaryStatLabel: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.regular,
    color: 'rgba(255, 255, 255, 0.8)',
    marginTop:
      summaryStatLabel: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.regular,
    color: 'rgba(255, 255, 255, 0.8)',
    marginTop: 2,
  },
  summaryStatDivider: {
    width: 1,
    height: 30,
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    marginHorizontal: legendaryTheme.legendary.spacing.lg,
  },
  founderBadge: {
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
    paddingHorizontal: legendaryTheme.legendary.spacing.md,
    paddingVertical: legendaryTheme.legendary.spacing.xs,
  },
  founderBadgeText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.codeBroBold,
    color: '#ffffff',
    textAlign: 'center',
  },
  sectionTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xl,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.legendaryBold,
    color: legendaryTheme.colors.primary,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  chartContainer: {
    paddingHorizontal: legendaryTheme.legendary.spacing.lg,
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  chartCard: {
    padding: legendaryTheme.legendary.spacing.lg,
    alignItems: 'center',
  },
  chart: {
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
    marginVertical: legendaryTheme.legendary.spacing.md,
  },
  chartStats: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
    marginTop: legendaryTheme.legendary.spacing.md,
  },
  chartStatItem: {
    alignItems: 'center',
  },
  chartStatValue: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xl,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.primary,
  },
  chartStatLabel: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: legendaryTheme.colors.outline,
    marginTop: 2,
  },
  filtersContainer: {
    paddingHorizontal: legendaryTheme.legendary.spacing.lg,
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  searchBar: {
    marginBottom: legendaryTheme.legendary.spacing.md,
    elevation: 2,
  },
  tabsContainer: {
    flexDirection: 'row',
    backgroundColor: legendaryTheme.colors.surface,
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
    padding: 4,
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  tabButton: {
    flex: 1,
    paddingVertical: legendaryTheme.legendary.spacing.sm,
    paddingHorizontal: legendaryTheme.legendary.spacing.xs,
    borderRadius: legendaryTheme.legendary.borders.radius.md,
    alignItems: 'center',
  },
  activeTabButton: {
    backgroundColor: legendaryTheme.colors.primary,
  },
  tabButtonText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
    color: legendaryTheme.colors.onSurface,
  },
  activeTabButtonText: {
    color: legendaryTheme.colors.onPrimary,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
  },
  controlsContainer: {
    flexDirection: 'row',
    gap: legendaryTheme.legendary.spacing.md,
  },
  controlButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: legendaryTheme.legendary.spacing.xs,
    paddingVertical: legendaryTheme.legendary.spacing.sm,
    paddingHorizontal: legendaryTheme.legendary.spacing.md,
    backgroundColor: legendaryTheme.colors.surface,
    borderRadius: legendaryTheme.legendary.borders.radius.md,
    elevation: 1,
  },
  controlButtonText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.colors.primary,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
  },
  teamsListContainer: {
    paddingHorizontal: legendaryTheme.legendary.spacing.lg,
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  teamsListHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  teamsCountBadge: {
    backgroundColor: legendaryTheme.legendary.colors.legendary,
  },
  teamsList: {
    gap: legendaryTheme.legendary.spacing.lg,
  },
  teamCard: {
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  teamCardContent: {
    padding: legendaryTheme.legendary.spacing.lg,
  },
  legendaryTeamCard: {
    borderColor: legendaryTheme.legendary.colors.legendary,
    borderWidth: 2,
    backgroundColor: `${legendaryTheme.legendary.colors.legendary}05`,
  },
  founderTeamCard: {
    borderColor: legendaryTheme.legendary.colors.legendary,
    borderWidth: 3,
    backgroundColor: `${legendaryTheme.legendary.colors.legendary}10`,
    elevation: 8,
  },
  teamCardHeader: {
    flexDirection: 'row',
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  teamImageContainer: {
    marginRight: legendaryTheme.legendary.spacing.md,
  },
  teamImage: {
    width: 48,
    height: 48,
    borderRadius: 24,
  },
  teamImagePlaceholder: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
  },
  teamMainInfo: {
    flex: 1,
    marginRight: legendaryTheme.legendary.spacing.md,
  },
  teamName: {
    fontSize: legendaryTheme.legendary.typography.fontSize.lg,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.onSurface,
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  teamDescription: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.colors.outline,
    marginBottom: legendaryTheme.legendary.spacing.xs,
    lineHeight: 20,
  },
  teamMeta: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  teamMembers: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: legendaryTheme.colors.primary,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
  },
  teamType: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: legendaryTheme.colors.outline,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.regular,
  },
  teamBadges: {
    alignItems: 'flex-end',
  },
  statusChip: {
    elevation: 0,
  },
  statusChipText: {
    color: '#ffffff',
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
  },
  teamMetrics: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: legendaryTheme.legendary.spacing.md,
    backgroundColor: legendaryTheme.colors.surface,
    borderRadius: legendaryTheme.legendary.borders.radius.md,
    padding: legendaryTheme.legendary.spacing.sm,
  },
  metricItem: {
    alignItems: 'center',
  },
  metricLabel: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    color: legendaryTheme.colors.outline,
    marginBottom: 2,
  },
  metricValue: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
  },
  teamProgress: {
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  progressHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  progressLabel: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
    color: legendaryTheme.colors.onSurface,
  },
  progressValue: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.primary,
  },
  progressBar: {
    height: 6,
    borderRadius: 3,
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  progressDetails: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    color: legendaryTheme.colors.outline,
  },
  membersPreview: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  membersLabel: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.colors.onSurface,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
  },
  membersAvatars: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  memberAvatar: {
    marginLeft: -4,
    borderWidth: 2,
    borderColor: legendaryTheme.colors.background,
  },
  founderAvatar: {
    borderColor: legendaryTheme.legendary.colors.legendary,
    borderWidth: 3,
  },
  legendaryAvatar: {
    borderColor: legendaryTheme.legendary.colors.legendary,
    borderWidth: 2,
  },
  moreMembers: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: legendaryTheme.colors.outline,
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: -4,
    borderWidth: 2,
    borderColor: legendaryTheme.colors.background,
  },
  moreMembersText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    color: '#ffffff',
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
  },
  specialBadges: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: legendaryTheme.legendary.spacing.xs,
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  specialChip: {
    elevation: 0,
  },
  specialChipText: {
    color: '#ffffff',
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
  },
  teamFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: legendaryTheme.legendary.spacing.sm,
    paddingTop: legendaryTheme.legendary.spacing.sm,
    borderTopWidth: 1,
    borderTopColor: legendaryTheme.colors.outline,
  },
  lastActivity: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    color: legendaryTheme.colors.outline,
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: legendaryTheme.legendary.spacing['4xl'],
  },
  emptyStateTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xl,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.onSurface,
    marginTop: legendaryTheme.legendary.spacing.lg,
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  emptyStateDescription: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.colors.outline,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
    paddingHorizontal: legendaryTheme.legendary.spacing.lg,
  },
  emptyStateActions: {
    flexDirection: 'row',
    gap: legendaryTheme.legendary.spacing.md,
  },
  emptyStateButton: {
    backgroundColor: legendaryTheme.legendary.colors.legendary,
  },
  bottomSpacing: {
    height: legendaryTheme.legendary.spacing.xl,
  },
  fabContainer: {
    position: 'absolute',
    bottom: legendaryTheme.legendary.spacing.lg,
    right: legendaryTheme.legendary.spacing.lg,
    gap: legendaryTheme.legendary.spacing.md,
  },
  fab: {
    elevation: 8,
  },
  createFab: {
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  joinFab: {
    // Additional styling for join FAB
  },
  teamModal: {
    backgroundColor: 'white',
    margin: legendaryTheme.legendary.spacing.md,
    borderRadius: legendaryTheme.legendary.borders.radius.xl,
    maxHeight: height * 0.9,
  },
  teamModalContent: {
    padding: legendaryTheme.legendary.spacing.lg,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  modalTitleContainer: {
    flex: 1,
    marginRight: legendaryTheme.legendary.spacing.md,
  },
  modalTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xl,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.legendaryBold,
    color: legendaryTheme.colors.primary,
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  modalBadges: {
    flexDirection: 'row',
    gap: legendaryTheme.legendary.spacing.xs,
  },
  modalBadge: {
    elevation: 0,
  },
  modalBadgeText: {
    color: '#ffffff',
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
  },
  closeButton: {
    padding: legendaryTheme.legendary.spacing.xs,
  },
  modalDescription: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.colors.onSurface,
    marginBottom: legendaryTheme.legendary.spacing.lg,
    lineHeight: 22,
  },
  modalStats: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    backgroundColor: legendaryTheme.colors.surface,
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
    padding: legendaryTheme.legendary.spacing.lg,
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  modalStatItem: {
    alignItems: 'center',
  },
  modalStatValue: {
    fontSize: legendaryTheme.legendary.typography.fontSize['2xl'],
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.legendary.colors.legendary,
  },
  modalStatLabel: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: legendaryTheme.colors.outline,
    marginTop: legendaryTheme.legendary.spacing.xs,
  },
  modalSectionTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.lg,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.primary,
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  membersList: {
    gap: legendaryTheme.legendary.spacing.md,
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  memberItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: legendaryTheme.colors.surface,
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
    padding: legendaryTheme.legendary.spacing.md,
  },
  memberItemAvatar: {
    marginRight: legendaryTheme.legendary.spacing.md,
    borderWidth: 2,
    borderColor: legendaryTheme.colors.outline,
  },
  memberInfo: {
    flex: 1,
  },
  memberNameContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  memberName: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.onSurface,
    flex: 1,
  },
  roleChip: {
    elevation: 0,
    marginLeft: legendaryTheme.legendary.spacing.sm,
  },
  roleChipText: {
    color: '#ffffff',
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
  },
  memberJobTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: legendaryTheme.colors.outline,
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  memberMetrics: {
    flexDirection: 'row',
    gap: legendaryTheme.legendary.spacing.md,
  },
  memberMetric: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    color: legendaryTheme.colors.primary,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
  },
  achievementsList: {
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  achievementItem: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.colors.onSurface,
    marginBottom: legendaryTheme.legendary.spacing.sm,
    lineHeight: 22,
  },
  tagsList: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: legendaryTheme.legendary.spacing.xs,
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  tagChip: {
    backgroundColor: legendaryTheme.colors.surface,
    elevation: 0,
  },
  tagChipText: {
    color: legendaryTheme.colors.primary,
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
  },
  modalActions: {
    gap: legendaryTheme.legendary.spacing.md,
    paddingTop: legendaryTheme.legendary.spacing.lg,
    borderTopWidth: 1,
    borderTopColor: legendaryTheme.colors.outline,
  },
  modalActionButton: {
    // Additional styling for modal action buttons
  },
  createModal: {
    backgroundColor: 'white',
    margin: legendaryTheme.legendary.spacing.lg,
    borderRadius: legendaryTheme.legendary.borders.radius.xl,
    padding: legendaryTheme.legendary.spacing.lg,
  },
  createModalContent: {
    alignItems: 'center',
  },
  createModalTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xl,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.legendaryBold,
    color: legendaryTheme.colors.primary,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  createModalDescription: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.colors.onSurface,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.xl,
    lineHeight: 22,
    paddingHorizontal: legendaryTheme.legendary.spacing.md,
  },
  createModalActions: {
    width: '100%',
    gap: legendaryTheme.legendary.spacing.md,
  },
  createButton: {
    backgroundColor: legendaryTheme.legendary.colors.legendary,
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  cancelButton: {
    marginTop: 0,
  },
  joinModal: {
    backgroundColor: 'white',
    margin: legendaryTheme.legendary.spacing.lg,
    borderRadius: legendaryTheme.legendary.borders.radius.xl,
    padding: legendaryTheme.legendary.spacing.lg,
  },
  joinModalContent: {
    alignItems: 'center',
  },
  joinModalTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xl,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.legendaryBold,
    color: legendaryTheme.colors.primary,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  joinModalDescription: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.colors.onSurface,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.xl,
    lineHeight: 22,
    paddingHorizontal: legendaryTheme.legendary.spacing.md,
  },
  joinModalActions: {
    width: '100%',
    gap: legendaryTheme.legendary.spacing.md,
  },
  joinButton: {
    backgroundColor: legendaryTheme.legendary.colors.codeBroEnergy,
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
});

// =====================================
// 🎸 LEGENDARY EXPORTS 🎸
// =====================================

export default LegendaryTeamsScreen;

// =====================================
// 🎸 LEGENDARY COMPLETION MESSAGE 🎸
// =====================================

console.log('🎸🎸🎸 LEGENDARY TEAMS SCREEN COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Teams screen completed at: 2025-08-06 02:24:21 UTC`);
console.log('👥 Team collaboration: SWISS PRECISION');
console.log('👑 RICKROLL187 founder features: LEGENDARY');
console.log('📊 Interactive team analytics: MAXIMUM VISUALIZATION');
console.log('⚙️ Team management: INFINITE COLLABORATION');
console.log('🤝 Team creation & joining: COMPREHENSIVE TEAMWORK');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
