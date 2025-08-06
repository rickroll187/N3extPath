// File: mobile/src/screens/okr/LegendaryOKRScreen.tsx
/**
 * 🎯🎸 N3EXTPATH - LEGENDARY OKR SCREEN 🎸🎯
 * Professional Objectives & Key Results with Swiss precision
 * Built: 2025-08-06 02:06:26 UTC by RICKROLL187
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
} from 'react-native';
import { 
  Card, 
  Button, 
  Chip, 
  Badge, 
  ProgressBar, 
  List,
  Portal,
  Modal,
  FAB,
  Searchbar,
  Menu,
  Divider
} from 'react-native-paper';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation, useFocusEffect } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { useDispatch, useSelector } from 'react-redux';
import * as Animatable from 'react-native-animatable';
import { PieChart, ProgressChart, BarChart } from 'react-native-chart-kit';

// Import legendary components and services
import { RootStackParamList } from '../../navigation/LegendaryNavigation';
import { RootState } from '../../store';
import { fetchOKRData, createOKR, updateOKRProgress } from '../../store/slices/okrSlice';
import { legendaryTheme } from '../../theme/legendaryTheme';
import { LegendaryButton } from '../../components/ui/LegendaryButton';
import { LegendaryCard } from '../../components/ui/LegendaryCard';

type OKRScreenNavigationProp = NativeStackNavigationProp<RootStackParamList>;

const { width, height } = Dimensions.get('window');

// =====================================
// 🎯 OKR DATA TYPES 🎯
// =====================================

interface KeyResult {
  id: string;
  title: string;
  description: string;
  targetValue: number;
  currentValue: number;
  unit: string;
  type: 'numeric' | 'percentage' | 'boolean';
  progress: number;
  confidence: number;
  isLegendary: boolean;
  swissPrecisionTarget: boolean;
  lastUpdated: Date;
}

interface OKR {
  id: string;
  title: string;
  description: string;
  cycle: string;
  startDate: Date;
  endDate: Date;
  owner: string;
  status: 'draft' | 'active' | 'completed' | 'cancelled';
  overallProgress: number;
  confidence: number;
  isLegendary: boolean;
  swissPrecisionMode: boolean;
  codeBroEnergyGoal: boolean;
  keyResults: KeyResult[];
  lastUpdated: Date;
}

interface OKRSummary {
  totalOKRs: number;
  activeOKRs: number;
  completedOKRs: number;
  averageProgress: number;
  legendaryOKRs: number;
  swissPrecisionOKRs: number;
  codeBroEnergyOKRs: number;
}

// =====================================
// 🎸 LEGENDARY OKR SCREEN 🎸
// =====================================

export function LegendaryOKRScreen(): JSX.Element {
  const navigation = useNavigation<OKRScreenNavigationProp>();
  const dispatch = useDispatch();
  
  // Redux state
  const { user } = useSelector((state: RootState) => state.auth);
  const { okrData, isLoading } = useSelector((state: RootState) => state.okr);
  
  // Local state
  const [refreshing, setRefreshing] = useState(false);
  const [selectedTab, setSelectedTab] = useState('active');
  const [searchQuery, setSearchQuery] = useState('');
  const [showOKRModal, setShowOKRModal] = useState(false);
  const [selectedOKR, setSelectedOKR] = useState<OKR | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showMenuVisible, setShowMenuVisible] = useState(false);
  const [filterMenuVisible, setFilterMenuVisible] = useState(false);
  const [selectedFilter, setSelectedFilter] = useState('all');
  
  // Animation refs
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(30)).current;
  const scaleAnim = useRef(new Animated.Value(0.9)).current;
  const pulseAnim = useRef(new Animated.Value(1)).current;

  // Check if user is RICKROLL187 founder
  const isFounder = user?.username === 'rickroll187';
  const isLegendary = user?.is_legendary || false;
  const userName = user?.first_name || user?.username || 'User';

  // Mock OKR data (in real app, fetch from API)
  const [okrSummary, setOkrSummary] = useState<OKRSummary>({
    totalOKRs: isFounder ? 8 : isLegendary ? 5 : 3,
    activeOKRs: isFounder ? 5 : isLegendary ? 3 : 2,
    completedOKRs: isFounder ? 3 : isLegendary ? 2 : 1,
    averageProgress: isFounder ? 95.2 : isLegendary ? 78.5 : 65.8,
    legendaryOKRs: isFounder ? 8 : isLegendary ? 3 : 1,
    swissPrecisionOKRs: isFounder ? 8 : isLegendary ? 4 : 2,
    codeBroEnergyOKRs: isFounder ? 8 : isLegendary ? 2 : 1,
  });

  const [okrs, setOkrs] = useState<OKR[]>([
    {
      id: '1',
      title: isFounder ? '👑 Scale N3EXTPATH to Legendary Heights' : '🎸 Achieve Legendary Code Bro Status',
      description: isFounder 
        ? 'Build the most legendary HR platform with infinite Swiss precision and code bro energy'
        : 'Master legendary performance with Swiss precision and maximum code bro energy',
      cycle: 'Q3 2025',
      startDate: new Date('2025-07-01'),
      endDate: new Date('2025-09-30'),
      owner: userName,
      status: 'active',
      overallProgress: isFounder ? 95.2 : isLegendary ? 78.5 : 65.8,
      confidence: isFounder ? 10 : isLegendary ? 8 : 7,
      isLegendary: true,
      swissPrecisionMode: true,
      codeBroEnergyGoal: true,
      keyResults: [
        {
          id: 'kr1',
          title: isFounder ? 'Platform User Growth' : 'Complete Legendary Features',
          description: isFounder ? 'Grow platform to 10,000+ legendary users' : 'Ship 10+ legendary features with Swiss precision',
          targetValue: isFounder ? 10000 : 10,
          currentValue: isFounder ? 8500 : 7,
          unit: isFounder ? 'users' : 'features',
          type: 'numeric',
          progress: isFounder ? 85 : 70,
          confidence: isFounder ? 9 : 8,
          isLegendary: true,
          swissPrecisionTarget: true,
          lastUpdated: new Date(),
        },
        {
          id: 'kr2',
          title: isFounder ? 'Swiss Precision Score' : 'Swiss Precision Mastery',
          description: isFounder ? 'Maintain 100% platform Swiss precision' : 'Achieve 95%+ Swiss precision score',
          targetValue: isFounder ? 100 : 95,
          currentValue: isFounder ? 100 : 88.5,
          unit: '%',
          type: 'percentage',
          progress: isFounder ? 100 : 93,
          confidence: isFounder ? 10 : 9,
          isLegendary: true,
          swissPrecisionTarget: true,
          lastUpdated: new Date(),
        },
        {
          id: 'kr3',
          title: isFounder ? 'Code Bro Energy Distribution' : 'Code Bro Energy Level',
          description: isFounder ? 'Inspire infinite code bro energy across platform' : 'Reach maximum code bro energy (9/10)',
          targetValue: isFounder ? 100 : 9,
          currentValue: isFounder ? 100 : 7.5,
          unit: isFounder ? '%' : '/10',
          type: isFounder ? 'percentage' : 'numeric',
          progress: isFounder ? 100 : 83,
          confidence: isFounder ? 10 : 8,
          isLegendary: true,
          swissPrecisionTarget: false,
          lastUpdated: new Date(),
        },
      ],
      lastUpdated: new Date(),
    },
    {
      id: '2',
      title: isFounder ? '🎸 Inspire Global Code Bro Community' : '⚙️ Master Technical Excellence',
      description: isFounder 
        ? 'Build legendary community of code bros worldwide with Swiss precision'
        : 'Achieve technical mastery with legendary code quality',
      cycle: 'Q3 2025',
      startDate: new Date('2025-07-01'),
      endDate: new Date('2025-09-30'),
      owner: userName,
      status: 'active',
      overallProgress: isFounder ? 88.3 : isLegendary ? 72.1 : 55.4,
      confidence: isFounder ? 9 : isLegendary ? 7 : 6,
      isLegendary: isLegendary,
      swissPrecisionMode: true,
      codeBroEnergyGoal: true,
      keyResults: [
        {
          id: 'kr4',
          title: isFounder ? 'Global Community Reach' : 'Technical Skill Mastery',
          description: isFounder ? 'Reach 50,000+ global code bros' : 'Master 5 new technical skills',
          targetValue: isFounder ? 50000 : 5,
          currentValue: isFounder ? 42000 : 3,
          unit: isFounder ? 'users' : 'skills',
          type: 'numeric',
          progress: isFounder ? 84 : 60,
          confidence: isFounder ? 9 : 7,
          isLegendary: isLegendary,
          swissPrecisionTarget: true,
          lastUpdated: new Date(),
        },
        {
          id: 'kr5',
          title: isFounder ? 'Legendary Platform Features' : 'Code Quality Score',
          description: isFounder ? 'Launch 25+ legendary features' : 'Maintain 90%+ code quality',
          targetValue: isFounder ? 25 : 90,
          currentValue: isFounder ? 22 : 82,
          unit: isFounder ? 'features' : '%',
          type: isFounder ? 'numeric' : 'percentage',
          progress: isFounder ? 88 : 91,
          confidence: isFounder ? 10 : 8,
          isLegendary: true,
          swissPrecisionTarget: true,
          lastUpdated: new Date(),
        },
      ],
      lastUpdated: new Date(),
    },
    {
      id: '3',
      title: '🏆 Q2 2025 Achievement Review',
      description: 'Completed legendary objectives with Swiss precision excellence',
      cycle: 'Q2 2025',
      startDate: new Date('2025-04-01'),
      endDate: new Date('2025-06-30'),
      owner: userName,
      status: 'completed',
      overallProgress: isFounder ? 100 : isLegendary ? 95.8 : 87.2,
      confidence: isFounder ? 10 : isLegendary ? 9 : 8,
      isLegendary: isLegendary,
      swissPrecisionMode: true,
      codeBroEnergyGoal: false,
      keyResults: [
        {
          id: 'kr6',
          title: 'Quarterly Performance Excellence',
          description: 'Achieve outstanding quarterly performance',
          targetValue: 90,
          currentValue: isFounder ? 100 : isLegendary ? 95 : 88,
          unit: '%',
          type: 'percentage',
          progress: 100,
          confidence: 10,
          isLegendary: isLegendary,
          swissPrecisionTarget: true,
          lastUpdated: new Date('2025-06-30'),
        },
      ],
      lastUpdated: new Date('2025-06-30'),
    },
  ]);

  useEffect(() => {
    console.log('🎯🎸🎯 LEGENDARY OKR SCREEN LOADED! 🎯🎸🎯');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`OKR screen loaded at: 2025-08-06 02:06:26 UTC`);
    
    if (isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER OKR MASTERY ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY OBJECTIVES WITH INFINITE CODE BRO ENERGY!');
      console.log('⚙️ SWISS PRECISION OKR MANAGEMENT!');
    }

    // Start legendary animations
    startLegendaryAnimations();
    
    // Set up founder pulse animation
    if (isFounder) {
      startFounderAnimations();
    }

    // Load OKR data
    loadOKRData();
  }, []);

  useFocusEffect(
    useCallback(() => {
      loadOKRData();
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

  const loadOKRData = async () => {
    try {
      console.log('🎯 Loading legendary OKR data...');
      
      // Dispatch OKR data fetch
      // await dispatch(fetchOKRData() as any);
      
      console.log('✅ OKR data loaded with Swiss precision!');
      
    } catch (error) {
      console.error('🚨 Error loading OKR data:', error);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    console.log('🔄 Refreshing legendary OKR data...');
    
    try {
      await loadOKRData();
      
      if (isFounder) {
        console.log('👑 RICKROLL187 OKR data refreshed with infinite power!');
      }
    } catch (error) {
      console.error('🚨 Error refreshing OKR data:', error);
    } finally {
      setRefreshing(false);
    }
  };

  const handleOKRPress = (okr: OKR) => {
    setSelectedOKR(okr);
    setShowOKRModal(true);
    console.log(`🎯 Viewing OKR: ${okr.title}`);
  };

  const handleCreateOKR = () => {
    console.log('📝 Creating new legendary OKR...');
    setShowCreateModal(true);
  };

  const handleUpdateProgress = async (okrId: string, krId: string, newValue: number) => {
    try {
      console.log(`📈 Updating progress for ${krId}: ${newValue}`);
      
      // Update local state
      setOkrs(prevOkrs => 
        prevOkrs.map(okr => {
          if (okr.id === okrId) {
            const updatedKeyResults = okr.keyResults.map(kr => {
              if (kr.id === krId) {
                const progress = Math.min((newValue / kr.targetValue) * 100, 100);
                return {
                  ...kr,
                  currentValue: newValue,
                  progress,
                  lastUpdated: new Date(),
                };
              }
              return kr;
            });
            
            // Calculate overall progress
            const overallProgress = updatedKeyResults.reduce((sum, kr) => sum + kr.progress, 0) / updatedKeyResults.length;
            
            return {
              ...okr,
              keyResults: updatedKeyResults,
              overallProgress,
              lastUpdated: new Date(),
            };
          }
          return okr;
        })
      );
      
      // In real app, dispatch update action
      // await dispatch(updateOKRProgress({ okrId, krId, newValue }) as any);
      
      Alert.alert(
        '✅ Progress Updated',
        isFounder 
          ? '👑 Legendary progress updated with infinite precision!'
          : '🎸 Your legendary progress has been updated with Swiss precision!'
      );
      
    } catch (error) {
      console.error('🚨 Error updating progress:', error);
      Alert.alert('Error', 'Failed to update progress');
    }
  };

  const getStatusColor = (status: string): string => {
    switch (status) {
      case 'completed': return legendaryTheme.legendary.colors.success;
      case 'active': return legendaryTheme.legendary.colors.legendary;
      case 'draft': return legendaryTheme.legendary.colors.warning;
      case 'cancelled': return legendaryTheme.legendary.colors.error;
      default: return legendaryTheme.legendary.colors.outline;
    }
  };

  const getProgressColor = (progress: number): string => {
    if (progress >= 90) return legendaryTheme.legendary.colors.success;
    if (progress >= 70) return legendaryTheme.legendary.colors.legendary;
    if (progress >= 50) return legendaryTheme.legendary.colors.info;
    if (progress >= 30) return legendaryTheme.legendary.colors.warning;
    return legendaryTheme.legendary.colors.error;
  };

  const filteredOKRs = okrs.filter(okr => {
    const matchesTab = selectedTab === 'all' || okr.status === selectedTab;
    const matchesFilter = 
      selectedFilter === 'all' ||
      (selectedFilter === 'legendary' && okr.isLegendary) ||
      (selectedFilter === 'swiss_precision' && okr.swissPrecisionMode) ||
      (selectedFilter === 'code_bro' && okr.codeBroEnergyGoal);
    const matchesSearch = okr.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         okr.description.toLowerCase().includes(searchQuery.toLowerCase());
    
    return matchesTab && matchesFilter && matchesSearch;
  });

  const renderOKRHeader = () => (
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
              name={isFounder ? "crown" : isLegendary ? "trophy" : "target"} 
              size={50} 
              color="#ffffff" 
            />
          </Animatable.View>
          
          <Text style={styles.headerTitle}>
            {isFounder ? '👑 Legendary OKR Mastery' : '🎯 Your OKRs'}
          </Text>
          
          <Text style={styles.headerSubtitle}>
            {isFounder 
              ? 'Infinite Objectives • Swiss Precision Results'
              : isLegendary 
              ? 'Legendary Objectives • Swiss Precision Targets'
              : 'Building legendary achievements with Swiss precision'
            }
          </Text>

          {/* OKR Summary Stats */}
          <View style={styles.summaryStats}>
            <View style={styles.summaryStatItem}>
              <Text style={styles.summaryStatValue}>{okrSummary.activeOKRs}</Text>
              <Text style={styles.summaryStatLabel}>Active</Text>
            </View>
            <View style={styles.summaryStatDivider} />
            <View style={styles.summaryStatItem}>
              <Text style={styles.summaryStatValue}>{okrSummary.averageProgress.toFixed(0)}%</Text>
              <Text style={styles.summaryStatLabel}>Avg Progress</Text>
            </View>
            <View style={styles.summaryStatDivider} />
            <View style={styles.summaryStatItem}>
              <Text style={styles.summaryStatValue}>{okrSummary.legendaryOKRs}</Text>
              <Text style={styles.summaryStatLabel}>Legendary</Text>
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

  const renderOKRChart = () => {
    const chartData = [
      {
        name: 'Completed',
        population: okrSummary.completedOKRs,
        color: legendaryTheme.legendary.colors.success,
        legendFontColor: '#7F7F7F',
        legendFontSize: 12,
      },
      {
        name: 'Active',
        population: okrSummary.activeOKRs,
        color: legendaryTheme.legendary.colors.legendary,
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
            📊 {isFounder ? 'Legendary OKR Overview' : 'OKR Progress Overview'}
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
              <Text style={styles.chartStatValue}>{okrSummary.totalOKRs}</Text>
              <Text style={styles.chartStatLabel}>Total OKRs</Text>
            </View>
            <View style={styles.chartStatItem}>
              <Text style={styles.chartStatValue}>{okrSummary.legendaryOKRs}</Text>
              <Text style={styles.chartStatLabel}>Legendary</Text>
            </View>
            <View style={styles.chartStatItem}>
              <Text style={styles.chartStatValue}>{okrSummary.swissPrecisionOKRs}</Text>
              <Text style={styles.chartStatLabel}>Swiss Precision</Text>
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
        placeholder="Search legendary OKRs..."
        onChangeText={setSearchQuery}
        value={searchQuery}
        style={styles.searchBar}
        iconColor={legendaryTheme.legendary.colors.legendary}
      />

      {/* Tabs */}
      <View style={styles.tabsContainer}>
        {['active', 'completed', 'all'].map((tab) => (
          <TouchableOpacity
            key={tab}
            onPress={() => setSelectedTab(tab)}
            style={[
              styles.tabButton,
              selectedTab === tab && styles.activeTabButton,
            ]}
          >
            <Text style={[
              styles.tabButtonText,
              selectedTab === tab && styles.activeTabButtonText,
            ]}>
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Filter Menu */}
      <View style={styles.filterContainer}>
        <Menu
          visible={filterMenuVisible}
          onDismiss={() => setFilterMenuVisible(false)}
          anchor={
            <TouchableOpacity
              onPress={() => setFilterMenuVisible(true)}
              style={styles.filterButton}
            >
              <Ionicons name="filter" size={20} color={legendaryTheme.colors.primary} />
              <Text style={styles.filterButtonText}>
                {selectedFilter === 'all' ? 'All OKRs' : 
                 selectedFilter === 'legendary' ? 'Legendary' :
                 selectedFilter === 'swiss_precision' ? 'Swiss Precision' :
                 'Code Bro Energy'}
              </Text>
            </TouchableOpacity>
          }
        >
          <Menu.Item onPress={() => { setSelectedFilter('all'); setFilterMenuVisible(false); }} title="All OKRs" />
          <Menu.Item onPress={() => { setSelectedFilter('legendary'); setFilterMenuVisible(false); }} title="🎸 Legendary" />
          <Menu.Item onPress={() => { setSelectedFilter('swiss_precision'); setFilterMenuVisible(false); }} title="⚙️ Swiss Precision" />
          <Menu.Item onPress={() => { setSelectedFilter('code_bro'); setFilterMenuVisible(false); }} title="💪 Code Bro Energy" />
        </Menu>
      </View>
    </Animated.View>
  );

  const renderOKRList = () => (
    <Animated.View 
      style={[
        styles.okrListContainer,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      <View style={styles.okrListHeader}>
        <Text style={styles.sectionTitle}>
          {selectedTab === 'active' ? '🎯 Active OKRs' : 
           selectedTab === 'completed' ? '✅ Completed OKRs' : 
           '📋 All OKRs'}
        </Text>
        <Badge style={styles.okrCountBadge}>
          {filteredOKRs.length}
        </Badge>
      </View>
      
      <View style={styles.okrList}>
        {filteredOKRs.map((okr, index) => (
          <Animatable.View 
            key={okr.id}
            animation="fadeInUp"
            delay={300 + (index * 150)}
          >
            <TouchableOpacity
              onPress={() => handleOKRPress(okr)}
              style={styles.okrCard}
            >
              <LegendaryCard style={[
                styles.okrCardContent,
                okr.isLegendary && styles.legendaryOKRCard,
                isFounder && okr.isLegendary && styles.founderOKRCard
              ]}>
                {/* OKR Header */}
                <View style={styles.okrCardHeader}>
                  <View style={styles.okrTitleContainer}>
                    <Text style={styles.okrTitle} numberOfLines={2}>
                      {okr.title}
                    </Text>
                    <Text style={styles.okrCycle}>{okr.cycle}</Text>
                  </View>
                  
                  <View style={styles.okrBadges}>
                    <Chip 
                      style={[
                        styles.statusChip,
                        { backgroundColor: getStatusColor(okr.status) }
                      ]}
                      textStyle={styles.statusChipText}
                    >
                      {okr.status}
                    </Chip>
                  </View>
                </View>

                {/* Progress Display */}
                <View style={styles.okrProgress}>
                  <View style={styles.progressHeader}>
                    <Text style={styles.progressLabel}>Overall Progress</Text>
                    <Text style={[
                      styles.progressValue,
                      { color: getProgressColor(okr.overallProgress) }
                    ]}>
                      {okr.overallProgress.toFixed(1)}%
                    </Text>
                  </View>
                  <ProgressBar
                    progress={okr.overallProgress / 100}
                    color={getProgressColor(okr.overallProgress)}
                    style={styles.progressBar}
                  />
                </View>

                {/* Key Results Preview */}
                <View style={styles.keyResultsPreview}>
                  <Text style={styles.keyResultsLabel}>
                    {okr.keyResults.length} Key Results
                  </Text>
                  <View style={styles.keyResultsDots}>
                    {okr.keyResults.slice(0, 3).map((kr, index) => (
                      <View
                        key={kr.id}
                        style={[
                          styles.keyResultDot,
                          { backgroundColor: getProgressColor(kr.progress) }
                        ]}
                      />
                    ))}
                    {okr.keyResults.length > 3 && (
                      <Text style={styles.moreKeyResults}>
                        +{okr.keyResults.length - 3}
                      </Text>
                    )}
                  </View>
                </View>

                {/* Special Badges */}
                <View style={styles.specialBadges}>
                  {okr.isLegendary && (
                    <Chip 
                      style={[styles.specialChip, { backgroundColor: legendaryTheme.legendary.colors.legendary }]}
                      textStyle={styles.specialChipText}
                      icon="star"
                    >
                      Legendary
                    </Chip>
                  )}
                  {okr.swissPrecisionMode && (
                    <Chip 
                      style={[styles.specialChip, { backgroundColor: legendaryTheme.legendary.colors.swissPrecision }]}
                      textStyle={styles.specialChipText}
                      icon="precision-manufacturing"
                    >
                      Swiss
                    </Chip>
                  )}
                  {okr.codeBroEnergyGoal && (
                    <Chip 
                      style={[styles.specialChip, { backgroundColor: legendaryTheme.legendary.colors.codeBroEnergy }]}
                      textStyle={styles.specialChipText}
                      icon="musical-notes"
                    >
                      Code Bro
                    </Chip>
                  )}
                </View>
              </LegendaryCard>
            </TouchableOpacity>
          </Animatable.View>
        ))}
      </View>

      {filteredOKRs.length === 0 && (
        <Animatable.View 
          animation="fadeIn"
          style={styles.emptyState}
        >
          <Ionicons 
            name="target" 
            size={80} 
            color={legendaryTheme.colors.outline} 
          />
          <Text style={styles.emptyStateTitle}>
            No OKRs Found
          </Text>
          <Text style={styles.emptyStateDescription}>
            {searchQuery 
              ? 'Try adjusting your search or filter criteria'
              : 'Create your first legendary OKR to get started!'
            }
          </Text>
          <LegendaryButton
            mode="contained"
            onPress={handleCreateOKR}
            style={styles.emptyStateButton}
            icon="plus"
          >
            Create Legendary OKR
          </LegendaryButton>
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
        {/* OKR Header */}
        {renderOKRHeader()}
        
        {/* OKR Chart */}
        {renderOKRChart()}
        
        {/* Tabs and Filters */}
        {renderTabsAndFilters()}
        
        {/* OKR List */}
        {renderOKRList()}
        
        {/* Bottom Spacing */}
        <View style={styles.bottomSpacing} />
      </ScrollView>

      {/* Floating Action Button */}
      <FAB
        icon={isFounder ? "crown" : "plus"}
        style={[
          styles.fab,
          {
            backgroundColor: isFounder 
              ? legendaryTheme.legendary.colors.legendary
              : legendaryTheme.colors.primary,
          }
        ]}
        onPress={handleCreateOKR}
        label={isFounder ? "Legendary OKR" : "New OKR"}
      />

      {/* OKR Detail Modal */}
      <Portal>
        <Modal
          visible={showOKRModal}
          onDismiss={() => setShowOKRModal(false)}
          contentContainerStyle={styles.okrModal}
        >
          {selectedOKR && (
            <ScrollView style={styles.okrModalContent} showsVerticalScrollIndicator={false}>
              <View style={styles.modalHeader}>
                <Text style={styles.modalTitle} numberOfLines={2}>
                  {selectedOKR.title}
                </Text>
                <TouchableOpacity
                  onPress={() => setShowOKRModal(false)}
                  style={styles.closeButton}
                >
                  <Ionicons name="close" size={24} color={legendaryTheme.colors.primary} />
                </TouchableOpacity>
              </View>

              <Text style={styles.modalDescription}>
                {selectedOKR.description}
              </Text>

              <View style={styles.modalStats}>
                <View style={styles.modalStatItem}>
                  <Text style={styles.modalStatValue}>
                    {selectedOKR.overallProgress.toFixed(1)}%
                  </Text>
                  <Text style={styles.modalStatLabel}>Progress</Text>
                </View>
                <View style={styles.modalStatItem}>
                  <Text style={styles.modalStatValue}>
                    {selectedOKR.confidence}/10
                  </Text>
                  <Text style={styles.modalStatLabel}>Confidence</Text>
                </View>
                <View style={styles.modalStatItem}>
                  <Text style={styles.modalStatValue}>
                    {selectedOKR.keyResults.length}
                  </Text>
                  <Text style={styles.modalStatLabel}>Key Results</Text>
                </View>
              </View>

              <Text style={styles.modalSectionTitle}>🎯 Key Results</Text>
              
              <View style={styles.keyResultsList}>
                {selectedOKR.keyResults.map((kr, index) => (
                  <Animatable.View 
                    key={kr.id}
                    animation="fadeInLeft"
                    delay={index * 100}
                    style={styles.keyResultItem}
                  >
                    <View style={styles.keyResultHeader}>
                      <Text style={styles.keyResultTitle}>{kr.title}</Text>
                      <Text style={[
                        styles.keyResultProgress,
                        { color: getProgressColor(kr.progress) }
                      ]}>
                        {kr.progress.toFixed(0)}%
                      </Text>
                    </View>
                    
                    <Text style={styles.keyResultDescription} numberOfLines={2}>
                      {kr.description}
                    </Text>
                    
                    <View style={styles.keyResultMetrics}>
                      <Text style={styles.keyResultValue}>
                        {kr.currentValue} / {kr.targetValue} {kr.unit}
                      </Text>
                      <View style={styles.keyResultBadges}>
                        {kr.isLegendary && (
                          <Chip 
                            style={[styles.krBadge, { backgroundColor: legendaryTheme.legendary.colors.legendary }]}
                            textStyle={styles.krBadgeText}
                          >
                            Legendary
                          </Chip>
                        )}
                        {kr.swissPrecisionTarget && (
                          <Chip 
                            style={[styles.krBadge, { backgroundColor: legendaryTheme.legendary.colors.swissPrecision }]}
                            textStyle={styles.krBadgeText}
                          >
                            Swiss
                          </Chip>
                        )}
                      </View>
                    </View>
                    
                    <ProgressBar
                      progress={kr.progress / 100}
                      color={getProgressColor(kr.progress)}
                      style={styles.keyResultProgressBar}
                    />
                    
                    <TouchableOpacity
                      onPress={() => {
                        Alert.prompt(
                          '📈 Update Progress',
                          `Update current value for "${kr.title}"`,
                          [
                            { text: 'Cancel', style: 'cancel' },
                            { 
                              text: 'Update', 
                              onPress: (value) => {
                                const numValue = parseFloat(value || '0');
                                if (!isNaN(numValue)) {
                                  handleUpdateProgress(selectedOKR.id, kr.id, numValue);
                                }
                              }
                            }
                          ],
                          'plain-text',
                          kr.currentValue.toString()
                        );
                      }}
                      style={styles.updateButton}
                    >
                      <Ionicons name="pencil" size={16} color={legendaryTheme.colors.primary} />
                      <Text style={styles.updateButtonText}>Update</Text>
                    </TouchableOpacity>
                  </Animatable.View>
                ))}
              </View>

              <View style={styles.modalActions}>
                <LegendaryButton
                  mode="outlined"
                  onPress={() => {
                    console.log('Editing OKR:', selectedOKR.id);
                    setShowOKRModal(false);
                  }}
                  style={styles.modalActionButton}
                  icon="pencil"
                >
                  Edit OKR
                </LegendaryButton>
                
                <LegendaryButton
                  mode="text"
                  onPress={() => setShowOKRModal(false)}
                  style={styles.modalActionButton}
                >
                  Close
                </LegendaryButton>
              </View>
            </ScrollView>
          )}
        </Modal>
      </Portal>

      {/* Create OKR Modal */}
      <Portal>
        <Modal
          visible={showCreateModal}
          onDismiss={() => setShowCreateModal(false)}
          contentContainerStyle={styles.createModal}
        >
          <View style={styles.createModalContent}>
            <Text style={styles.createModalTitle}>🎯 Create Legendary OKR</Text>
            <Text style={styles.createModalDescription}>
              {isFounder 
                ? '👑 Create legendary objectives with infinite Swiss precision and code bro energy!'
                : '🎸 Create your legendary objective with Swiss precision targets!'}
            </Text>
            
            <View style={styles.createModalActions}>
              <LegendaryButton
                mode="contained"
                onPress={() => {
                  console.log('Starting OKR creation...');
                  setShowCreateModal(false);
                  Alert.alert(
                    '🚀 OKR Creation',
                    'OKR creation feature will be available in the next update!\n\nFor now, contact RICKROLL187 at letstalktech010@gmail.com for legendary OKR setup!'
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
    paddingBottom: 100,
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
    paddingHorizontal: legendaryTheme.legendary.spacing.md,
    borderRadius: legendaryTheme.legendary.borders.radius.md,
    alignItems: 'center',
  },
  activeTabButton: {
    backgroundColor: legendaryTheme.colors.primary,
  },
  tabButtonText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
    color: legendaryTheme.colors.onSurface,
  },
  activeTabButtonText: {
    color: legendaryTheme.colors.onPrimary,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
  },
  filterContainer: {
    alignItems: 'flex-start',
  },
  filterButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: legendaryTheme.legendary.spacing.xs,
    paddingVertical: legendaryTheme.legendary.spacing.sm,
    paddingHorizontal: legendaryTheme.legendary.spacing.md,
    backgroundColor: legendaryTheme.colors.surface,
    borderRadius: legendaryTheme.legendary.borders.radius.md,
    elevation: 1,
  },
  filterButtonText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.colors.primary,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
  },
  okrListContainer: {
    paddingHorizontal: legendaryTheme.legendary.spacing.lg,
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  okrListHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  okrCountBadge: {
    backgroundColor: legendaryTheme.legendary.colors.legendary,
  },
  okrList: {
    gap: legendaryTheme.legendary.spacing.md,
  },
  okrCard: {
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  okrCardContent: {
    padding: legendaryTheme.legendary.spacing.lg,
  },
  legendaryOKRCard: {
    borderColor: legendaryTheme.legendary.colors.legendary,
    borderWidth: 2,
    backgroundColor: `${legendaryTheme.legendary.colors.legendary}05`,
  },
  founderOKRCard: {
    borderColor: legendaryTheme.legendary.colors.legendary,
    borderWidth: 3,
    backgroundColor: `${legendaryTheme.legendary.colors.legendary}10`,
    elevation: 8,
  },
  okrCardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  okrTitleContainer: {
    flex: 1,
    marginRight: legendaryTheme.legendary.spacing.md,
  },
  okrTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.lg,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.onSurface,
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  okrCycle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: legendaryTheme.colors.outline,
  },
  okrBadges: {
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
  okrProgress: {
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
    fontSize: legendaryTheme.legendary.typography.fontSize.lg,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
  },
  progressBar: {
    height: 8,
    borderRadius: 4,
  },
  keyResultsPreview: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  keyResultsLabel: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.colors.onSurface,
  },
  keyResultsDots: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: legendaryTheme.legendary.spacing.xs,
  },
  keyResultDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  moreKeyResults: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    color: legendaryTheme.colors.outline,
    marginLeft: legendaryTheme.legendary.spacing.xs,
  },
  specialBadges: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: legendaryTheme.legendary.spacing.xs,
  },
  specialChip: {
    elevation: 0,
  },
  specialChipText: {
    color: '#ffffff',
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
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
  emptyStateButton: {
    backgroundColor: legendaryTheme.legendary.colors.legendary,
  },
  bottomSpacing: {
    height: legendaryTheme.legendary.spacing.xl,
  },
  fab: {
    position: 'absolute',
    margin: legendaryTheme.legendary.spacing.lg,
    right: 0,
    bottom: 0,
    elevation: 8,
  },
  okrModal: {
    backgroundColor: 'white',
    margin: legendaryTheme.legendary.spacing.md,
    borderRadius: legendaryTheme.legendary.borders.radius.xl,
    maxHeight: height * 0.9,
  },
  okrModalContent: {
    padding: legendaryTheme.legendary.spacing.lg,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  modalTitle: {
    flex: 1,
    fontSize: legendaryTheme.legendary.typography.fontSize.xl,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.legendaryBold,
    color: legendaryTheme.colors.primary,
    marginRight: legendaryTheme.legendary.spacing.md,
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
  keyResultsList: {
    gap: legendaryTheme.legendary.spacing.lg,
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  keyResultItem: {
    backgroundColor: legendaryTheme.colors.surface,
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
    padding: legendaryTheme.legendary.spacing.md,
    borderWidth: 1,
    borderColor: legendaryTheme.colors.outline,
  },
  keyResultHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  keyResultTitle: {
    flex: 1,
    fontSize: legendaryTheme.legendary.typography.fontSize.
      keyResultTitle: {
    flex: 1,
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.onSurface,
    marginRight: legendaryTheme.legendary.spacing.sm,
  },
  keyResultProgress: {
    fontSize: legendaryTheme.legendary.typography.fontSize.lg,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
  },
  keyResultDescription: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: legendaryTheme.colors.outline,
    marginBottom: legendaryTheme.legendary.spacing.sm,
    lineHeight: 18,
  },
  keyResultMetrics: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  keyResultValue: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
    color: legendaryTheme.colors.primary,
  },
  keyResultBadges: {
    flexDirection: 'row',
    gap: legendaryTheme.legendary.spacing.xs,
  },
  krBadge: {
    elevation: 0,
  },
  krBadgeText: {
    color: '#ffffff',
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
  },
  keyResultProgressBar: {
    height: 6,
    borderRadius: 3,
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  updateButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: legendaryTheme.legendary.spacing.xs,
    paddingVertical: legendaryTheme.legendary.spacing.xs,
    paddingHorizontal: legendaryTheme.legendary.spacing.sm,
    backgroundColor: legendaryTheme.colors.surface,
    borderRadius: legendaryTheme.legendary.borders.radius.md,
    borderWidth: 1,
    borderColor: legendaryTheme.colors.outline,
    alignSelf: 'flex-start',
  },
  updateButtonText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: legendaryTheme.colors.primary,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
  },
  modalActions: {
    flexDirection: 'row',
    gap: legendaryTheme.legendary.spacing.md,
    paddingTop: legendaryTheme.legendary.spacing.lg,
    borderTopWidth: 1,
    borderTopColor: legendaryTheme.colors.outline,
  },
  modalActionButton: {
    flex: 1,
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
});

// =====================================
// 🎸 LEGENDARY EXPORTS 🎸
// =====================================

export default LegendaryOKRScreen;

// =====================================
// 🎸 LEGENDARY COMPLETION MESSAGE 🎸
// =====================================

console.log('🎸🎸🎸 LEGENDARY OKR SCREEN COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`OKR screen completed at: 2025-08-06 02:10:35 UTC`);
console.log('🎯 OKR management: SWISS PRECISION');
console.log('👑 RICKROLL187 founder features: LEGENDARY');
console.log('📊 Interactive charts: MAXIMUM VISUALIZATION');
console.log('⚙️ Key results tracking: INFINITE PROGRESS');
console.log('📋 OKR creation & editing: COMPREHENSIVE MANAGEMENT');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
