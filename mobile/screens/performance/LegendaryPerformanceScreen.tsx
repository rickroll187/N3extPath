// File: mobile/src/screens/performance/LegendaryPerformanceScreen.tsx
/**
 * 📈🎸 N3EXTPATH - LEGENDARY PERFORMANCE SCREEN 🎸📈
 * Professional performance analytics with Swiss precision
 * Built: 2025-08-06 01:57:33 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useState, useEffect, useRef } from 'react';
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
  Searchbar
} from 'react-native-paper';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation, useFocusEffect } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { useDispatch, useSelector } from 'react-redux';
import * as Animatable from 'react-native-animatable';
import { LineChart, BarChart, PieChart, ProgressChart } from 'react-native-chart-kit';

// Import legendary components and services
import { RootStackParamList } from '../../navigation/LegendaryNavigation';
import { RootState } from '../../store';
import { fetchPerformanceData, fetchPerformanceReviews } from '../../store/slices/performanceSlice';
import { legendaryTheme } from '../../theme/legendaryTheme';
import { LegendaryButton } from '../../components/ui/LegendaryButton';
import { LegendaryCard } from '../../components/ui/LegendaryCard';
import { LegendaryMetricCard } from '../../components/dashboard/LegendaryMetricCard';
import { LegendaryPerformanceChart } from '../../components/performance/LegendaryPerformanceChart';
import { LegendaryReviewCard } from '../../components/performance/LegendaryReviewCard';

type PerformanceScreenNavigationProp = NativeStackNavigationProp<RootStackParamList>;

const { width, height } = Dimensions.get('window');

// =====================================
// 📊 PERFORMANCE DATA TYPES 📊
// =====================================

interface PerformanceMetrics {
  overallScore: number;
  swissPrecisionScore: number;
  codeBroRating: number;
  performanceGrade: string;
  technicalSkills: number;
  communication: number;
  leadership: number;
  collaboration: number;
  innovation: number;
  reliability: number;
  problemSolving: number;
  goalAchievement: number;
}

interface PerformanceReview {
  id: string;
  reviewDate: Date;
  reviewPeriod: string;
  reviewer: string;
  overallScore: number;
  status: 'completed' | 'in_progress' | 'pending';
  isLegendary: boolean;
  swissPrecisionScore: number;
  codeBroRating: number;
  achievements: string[];
  improvementAreas: string[];
}

interface PerformanceTrend {
  month: string;
  score: number;
  swissPrecision: number;
  codeBroEnergy: number;
}

// =====================================
// 🎸 LEGENDARY PERFORMANCE SCREEN 🎸
// =====================================

export function LegendaryPerformanceScreen(): JSX.Element {
  const navigation = useNavigation<PerformanceScreenNavigationProp>();
  const dispatch = useDispatch();
  
  // Redux state
  const { user } = useSelector((state: RootState) => state.auth);
  const { performanceData, reviews, isLoading } = useSelector((state: RootState) => state.performance);
  
  // Local state
  const [refreshing, setRefreshing] = useState(false);
  const [selectedTab, setSelectedTab] = useState('overview');
  const [searchQuery, setSearchQuery] = useState('');
  const [showReviewModal, setShowReviewModal] = useState(false);
  const [selectedReview, setSelectedReview] = useState<PerformanceReview | null>(null);
  const [showInsights, setShowInsights] = useState(false);
  
  // Animation refs
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(30)).current;
  const scaleAnim = useRef(new Animated.Value(0.9)).current;
  const pulseAnim = useRef(new Animated.Value(1)).current;

  // Check if user is RICKROLL187 founder
  const isFounder = user?.username === 'rickroll187';
  const isLegendary = user?.is_legendary || false;
  const userName = user?.first_name || user?.username || 'User';

  // Mock performance data (in real app, fetch from API)
  const [performanceMetrics, setPerformanceMetrics] = useState<PerformanceMetrics>({
    overallScore: isFounder ? 100.0 : isLegendary ? 88.5 : 75.2,
    swissPrecisionScore: isFounder ? 100.0 : isLegendary ? 91.2 : 78.8,
    codeBroRating: isFounder ? 10 : isLegendary ? 9 : 7,
    performanceGrade: isFounder ? 'A+' : isLegendary ? 'A' : 'B+',
    technicalSkills: isFounder ? 100 : isLegendary ? 92 : 80,
    communication: isFounder ? 100 : isLegendary ? 87 : 75,
    leadership: isFounder ? 100 : isLegendary ? 85 : 70,
    collaboration: isFounder ? 100 : isLegendary ? 95 : 82,
    innovation: isFounder ? 100 : isLegendary ? 90 : 77,
    reliability: isFounder ? 100 : isLegendary ? 93 : 85,
    problemSolving: isFounder ? 100 : isLegendary ? 89 : 79,
    goalAchievement: isFounder ? 100 : isLegendary ? 91 : 73,
  });

  const [performanceTrends, setPerformanceTrends] = useState<PerformanceTrend[]>([
    { month: 'Jan', score: isFounder ? 100 : 70, swissPrecision: isFounder ? 100 : 72, codeBroEnergy: isFounder ? 10 : 6 },
    { month: 'Feb', score: isFounder ? 100 : 75, swissPrecision: isFounder ? 100 : 75, codeBroEnergy: isFounder ? 10 : 6.2 },
    { month: 'Mar', score: isFounder ? 100 : 78, swissPrecision: isFounder ? 100 : 78, codeBroEnergy: isFounder ? 10 : 6.5 },
    { month: 'Apr', score: isFounder ? 100 : 82, swissPrecision: isFounder ? 100 : 82, codeBroEnergy: isFounder ? 10 : 7 },
    { month: 'May', score: isFounder ? 100 : 80, swissPrecision: isFounder ? 100 : 85, codeBroEnergy: isFounder ? 10 : 7.5 },
    { month: 'Jun', score: isFounder ? 100 : 85, swissPrecision: isFounder ? 100 : 88, codeBroEnergy: isFounder ? 10 : 8 },
  ]);

  const [performanceReviews, setPerformanceReviews] = useState<PerformanceReview[]>([
    {
      id: '1',
      reviewDate: new Date('2025-07-01'),
      reviewPeriod: 'Q2 2025',
      reviewer: isFounder ? 'Self-Assessment' : 'Manager Review',
      overallScore: performanceMetrics.overallScore,
      status: 'completed',
      isLegendary: isLegendary,
      swissPrecisionScore: performanceMetrics.swissPrecisionScore,
      codeBroRating: performanceMetrics.codeBroRating,
      achievements: isFounder 
        ? [
            '👑 Created legendary N3EXTPATH platform with infinite code bro energy',
            '🎸 Inspired entire team with Swiss precision standards',
            '⚙️ Built platform architecture with maximum reliability',
            '💪 Maintained 100% performance across all metrics'
          ]
        : isLegendary
        ? [
            '🎸 Achieved legendary status with Swiss precision',
            '⚙️ Consistently delivered high-quality code',
            '👥 Led successful team collaborations',
            '📊 Exceeded performance targets'
          ]
        : [
            '📈 Improved performance score by 15 points',
            '👥 Strong team collaboration skills',
            '⚙️ Consistent quality delivery',
            '🎯 Met quarterly goals'
          ],
      improvementAreas: isFounder 
        ? ['Continue inspiring legendary potential in others']
        : isLegendary
        ? ['Focus on mentoring junior team members']
        : ['Enhance technical leadership skills', 'Increase code bro energy level']
    },
    {
      id: '2',
      reviewDate: new Date('2025-04-01'),
      reviewPeriod: 'Q1 2025',
      reviewer: 'Annual Review',
      overallScore: isFounder ? 100 : isLegendary ? 85 : 70,
      status: 'completed',
      isLegendary: false,
      swissPrecisionScore: isFounder ? 100 : isLegendary ? 88 : 75,
      codeBroRating: isFounder ? 10 : isLegendary ? 8 : 6,
      achievements: [
        '📊 Strong quarterly performance',
        '⚙️ Improved Swiss precision score',
        '👥 Good team integration'
      ],
      improvementAreas: ['Increase innovation focus', 'Enhance problem-solving skills']
    }
  ]);

  useEffect(() => {
    console.log('📈🎸📈 LEGENDARY PERFORMANCE SCREEN LOADED! 📈🎸📈');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Performance screen loaded at: 2025-08-06 01:57:33 UTC`);
    
    if (isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER PERFORMANCE METRICS ACTIVATED! 👑🎸👑');
      console.log('🚀 100% PERFORMANCE ACROSS ALL METRICS!');
      console.log('⚙️ INFINITE SWISS PRECISION & CODE BRO ENERGY!');
    }

    // Start legendary animations
    startLegendaryAnimations();
    
    // Set up founder pulse animation
    if (isFounder) {
      startFounderAnimations();
    }

    // Load performance data
    loadPerformanceData();
  }, []);

  useFocusEffect(
    React.useCallback(() => {
      loadPerformanceData();
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

  const loadPerformanceData = async () => {
    try {
      console.log('📊 Loading legendary performance data...');
      
      // Dispatch performance data fetch
      // await dispatch(fetchPerformanceData() as any);
      // await dispatch(fetchPerformanceReviews() as any);
      
      console.log('✅ Performance data loaded with Swiss precision!');
      
    } catch (error) {
      console.error('🚨 Error loading performance data:', error);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    console.log('🔄 Refreshing legendary performance data...');
    
    try {
      await loadPerformanceData();
      
      if (isFounder) {
        console.log('👑 RICKROLL187 performance data refreshed with infinite power!');
      }
    } catch (error) {
      console.error('🚨 Error refreshing performance data:', error);
    } finally {
      setRefreshing(false);
    }
  };

  const handleReviewPress = (review: PerformanceReview) => {
    setSelectedReview(review);
    setShowReviewModal(true);
    console.log(`📋 Viewing performance review: ${review.id}`);
  };

  const handleCreateReview = () => {
    console.log('📝 Creating new performance review...');
    Alert.alert(
      '📝 Create Performance Review',
      isFounder 
        ? '👑 As legendary founder, you have access to all performance review features!\n\nWould you like to create a self-assessment or review a team member?'
        : '🎸 Ready to create a new performance review?\n\nThis will help track your legendary progress!',
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: isFounder ? '👑 Self-Assessment' : '📝 Self-Review', 
          onPress: () => console.log('Creating self-review...') 
        },
        ...(isFounder ? [{ 
          text: '👥 Team Review', 
          onPress: () => console.log('Creating team review...') 
        }] : [])
      ]
    );
  };

  const handleViewInsights = () => {
    setShowInsights(true);
    console.log('🔍 Viewing AI-powered performance insights...');
  };

  const getGradeColor = (grade: string): string => {
    switch (grade) {
      case 'A+': return legendaryTheme.legendary.colors.legendary;
      case 'A': return legendaryTheme.legendary.colors.success;
      case 'B+': return legendaryTheme.legendary.colors.info;
      case 'B': return legendaryTheme.legendary.colors.warning;
      default: return legendaryTheme.legendary.colors.outline;
    }
  };

  const renderPerformanceHeader = () => (
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
              name={isFounder ? "crown" : isLegendary ? "trophy" : "trending-up"} 
              size={50} 
              color="#ffffff" 
            />
          </Animatable.View>
          
          <Text style={styles.headerTitle}>
            {isFounder ? '👑 Legendary Founder Performance' : '📈 Performance Overview'}
          </Text>
          
          <Text style={styles.headerSubtitle}>
            {isFounder 
              ? 'Infinite Code Bro Energy • Swiss Precision Master'
              : isLegendary 
              ? 'Legendary Performance • Swiss Precision Certified'
              : 'Building legendary performance with Swiss precision'
            }
          </Text>

          {/* Overall Score Display */}
          <View style={styles.scoreDisplay}>
            <Text style={styles.scoreValue}>{performanceMetrics.overallScore.toFixed(1)}</Text>
            <Text style={styles.scoreLabel}>Overall Score</Text>
            <View style={styles.gradeContainer}>
              <Text 
                style={[
                  styles.gradeText,
                  { color: getGradeColor(performanceMetrics.performanceGrade) }
                ]}
              >
                {performanceMetrics.performanceGrade}
              </Text>
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

  const renderQuickMetrics = () => (
    <Animated.View 
      style={[
        styles.quickMetricsContainer,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      <Text style={styles.sectionTitle}>
        ⚙️ {isFounder ? 'Legendary Founder Metrics' : 'Key Performance Metrics'}
      </Text>
      
      <View style={styles.quickMetricsGrid}>
        <Animatable.View animation="bounceInLeft" delay={300}>
          <LegendaryMetricCard
            title="Swiss Precision"
            value={performanceMetrics.swissPrecisionScore}
            unit="%"
            icon="precision-manufacturing"
            color={legendaryTheme.legendary.colors.swissPrecision}
            trend={+2.3}
            onPress={() => console.log('Swiss Precision details')}
            isFounder={isFounder}
          />
        </Animatable.View>
        
        <Animatable.View animation="bounceInRight" delay={500}>
          <LegendaryMetricCard
            title="Code Bro Rating"
            value={performanceMetrics.codeBroRating}
            unit="/10"
            icon="musical-notes"
            color={legendaryTheme.legendary.colors.codeBroEnergy}
            trend={isFounder ? 0 : +0.5}
            onPress={() => console.log('Code Bro details')}
            isFounder={isFounder}
          />
        </Animatable.View>
      </View>
    </Animated.View>
  );

  const renderPerformanceChart = () => {
    const chartData = {
      labels: performanceTrends.map(trend => trend.month),
      datasets: [
        {
          data: performanceTrends.map(trend => trend.score),
          color: (opacity = 1) => isFounder 
            ? `rgba(255, 215, 0, ${opacity})`
            : `rgba(26, 26, 26, ${opacity})`,
          strokeWidth: 3,
        },
        {
          data: performanceTrends.map(trend => trend.swissPrecision),
          color: (opacity = 1) => `rgba(220, 20, 60, ${opacity})`,
          strokeWidth: 2,
        },
      ],
    };

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
            📊 {isFounder ? 'Legendary Performance Journey' : 'Performance Trends'}
          </Text>
          
          <LineChart
            data={chartData}
            width={width - 60}
            height={220}
            chartConfig={{
              backgroundColor: 'transparent',
              backgroundGradientFrom: '#ffffff',
              backgroundGradientTo: '#ffffff',
              decimalPlaces: 0,
              color: (opacity = 1) => isFounder 
                ? `rgba(255, 215, 0, ${opacity})`
                : `rgba(26, 26, 26, ${opacity})`,
              labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
              style: {
                borderRadius: legendaryTheme.legendary.borders.radius.lg,
              },
              propsForDots: {
                r: "5",
                strokeWidth: "2",
                stroke: isFounder 
                  ? legendaryTheme.legendary.colors.legendary
                  : legendaryTheme.colors.primary,
              },
            }}
            bezier
            style={styles.chart}
          />
          
          <View style={styles.chartLegend}>
            <View style={styles.legendItem}>
              <View style={[styles.legendDot, { backgroundColor: isFounder ? legendaryTheme.legendary.colors.legendary : legendaryTheme.colors.primary }]} />
              <Text style={styles.legendText}>Overall Score</Text>
            </View>
            <View style={styles.legendItem}>
              <View style={[styles.legendDot, { backgroundColor: legendaryTheme.legendary.colors.swissPrecision }]} />
              <Text style={styles.legendText}>Swiss Precision</Text>
            </View>
          </View>
          
          <Text style={styles.chartDescription}>
            {isFounder 
              ? '👑 Consistently perfect performance with infinite legendary power!'
              : isLegendary
              ? '🎸 Strong upward trajectory with legendary potential!'
              : '📈 Steady improvement toward legendary status!'
            }
          </Text>
        </LegendaryCard>
      </Animated.View>
    );
  };

  const renderSkillsBreakdown = () => {
    const skillsData = [
      { name: 'Technical', score: performanceMetrics.technicalSkills, color: legendaryTheme.legendary.colors.legendary },
      { name: 'Communication', score: performanceMetrics.communication, color: legendaryTheme.legendary.colors.codeBroEnergy },
      { name: 'Leadership', score: performanceMetrics.leadership, color: legendaryTheme.legendary.colors.swissPrecision },
      { name: 'Collaboration', score: performanceMetrics.collaboration, color: legendaryTheme.legendary.colors.success },
      { name: 'Innovation', score: performanceMetrics.innovation, color: legendaryTheme.legendary.colors.info },
      { name: 'Reliability', score: performanceMetrics.reliability, color: legendaryTheme.legendary.colors.warning },
      { name: 'Problem Solving', score: performanceMetrics.problemSolving, color: legendaryTheme.legendary.colors.legendary },
      { name: 'Goal Achievement', score: performanceMetrics.goalAchievement, color: legendaryTheme.legendary.colors.success },
    ];

    return (
      <Animated.View 
        style={[
          styles.skillsContainer,
          {
            opacity: fadeAnim,
            transform: [{ translateY: slideAnim }],
          },
        ]}
      >
        <LegendaryCard style={styles.skillsCard}>
          <Text style={styles.sectionTitle}>
            ⚙️ {isFounder ? 'Legendary Skills Mastery' : 'Skills Breakdown'}
          </Text>
          
          <View style={styles.skillsList}>
            {skillsData.map((skill, index) => (
              <Animatable.View 
                key={skill.name}
                animation="fadeInLeft"
                delay={200 + (index * 100)}
                style={styles.skillItem}
              >
                <View style={styles.skillHeader}>
                  <Text style={styles.skillName}>{skill.name}</Text>
                  <Text style={styles.skillScore}>{skill.score}%</Text>
                </View>
                <View style={styles.skillProgressContainer}>
                  <ProgressBar
                    progress={skill.score / 100}
                    color={skill.color}
                    style={styles.skillProgress}
                  />
                </View>
              </Animatable.View>
            ))}
          </View>

          <LegendaryButton
            mode="text"
            onPress={handleViewInsights}
            style={styles.insightsButton}
            icon="lightbulb"
            labelStyle={styles.insightsButtonText}
          >
            🔍 View AI Insights & Recommendations
          </LegendaryButton>
        </LegendaryCard>
      </Animated.View>
    );
  };

  const renderRecentReviews = () => (
    <Animated.View 
      style={[
        styles.reviewsContainer,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      <LegendaryCard style={styles.reviewsCard}>
        <View style={styles.reviewsHeader}>
          <Text style={styles.sectionTitle}>📋 Performance Reviews</Text>
          <Badge style={styles.reviewsBadge}>
            {performanceReviews.length}
          </Badge>
        </View>
        
        <View style={styles.reviewsList}>
          {performanceReviews.map((review, index) => (
            <Animatable.View 
              key={review.id}
              animation="fadeInUp"
              delay={300 + (index * 200)}
            >
              <TouchableOpacity
                onPress={() => handleReviewPress(review)}
                style={styles.reviewItem}
              >
                <View style={styles.reviewContent}>
                  <View style={styles.reviewMainInfo}>
                    <Text style={styles.reviewPeriod}>{review.reviewPeriod}</Text>
                    <Text style={styles.reviewDate}>
                      {review.reviewDate.toLocaleDateString()}
                    </Text>
                  </View>
                  
                  <View style={styles.reviewScores}>
                    <View style={styles.reviewScoreItem}>
                      <Text style={styles.reviewScoreValue}>
                        {review.overallScore.toFixed(1)}
                      </Text>
                      <Text style={styles.reviewScoreLabel}>Overall</Text>
                    </View>
                    <View style={styles.reviewScoreItem}>
                      <Text style={styles.reviewScoreValue}>
                        {review.codeBroRating}/10
                      </Text>
                      <Text style={styles.reviewScoreLabel}>Code Bro</Text>
                    </View>
                  </View>
                  
                  <View style={styles.reviewStatus}>
                    <Chip 
                      style={[
                        styles.statusChip,
                        { backgroundColor: review.status === 'completed' ? legendaryTheme.legendary.colors.success : legendaryTheme.legendary.colors.warning }
                      ]}
                      textStyle={styles.statusChipText}
                    >
                      {review.status}
                    </Chip>
                    {review.isLegendary && (
                      <Chip 
                        style={[styles.statusChip, { backgroundColor: legendaryTheme.legendary.colors.legendary }]}
                        textStyle={styles.statusChipText}
                      >
                        Legendary
                      </Chip>
                    )}
                  </View>
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
      </LegendaryCard>
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
        {/* Performance Header */}
        {renderPerformanceHeader()}
        
        {/* Quick Metrics */}
        {renderQuickMetrics()}
        
        {/* Performance Chart */}
        {renderPerformanceChart()}
        
        {/* Skills Breakdown */}
        {renderSkillsBreakdown()}
        
        {/* Recent Reviews */}
        {renderRecentReviews()}
        
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
        onPress={handleCreateReview}
        label={isFounder ? "Legendary Review" : "New Review"}
      />

      {/* Review Detail Modal */}
      <Portal>
        <Modal
          visible={showReviewModal}
          onDismiss={() => setShowReviewModal(false)}
          contentContainerStyle={styles.reviewModal}
        >
          {selectedReview && (
            <View style={styles.reviewModalContent}>
              <Text style={styles.reviewModalTitle}>
                📋 {selectedReview.reviewPeriod} Review
              </Text>
              
              <View style={styles.reviewModalScores}>
                <View style={styles.modalScoreItem}>
                  <Text style={styles.modalScoreValue}>
                    {selectedReview.overallScore.toFixed(1)}
                  </Text>
                  <Text style={styles.modalScoreLabel}>Overall Score</Text>
                </View>
                <View style={styles.modalScoreItem}>
                  <Text style={styles.modalScoreValue}>
                    {selectedReview.swissPrecisionScore.toFixed(1)}%
                  </Text>
                  <Text style={styles.modalScoreLabel}>Swiss Precision</Text>
                </View>
                <View style={styles.modalScoreItem}>
                  <Text style={styles.modalScoreValue}>
                    {selectedReview.codeBroRating}/10
                  </Text>
                  <Text style={styles.modalScoreLabel}>Code Bro Rating</Text>
                </View>
              </View>

              <Text style={styles.reviewModalSectionTitle}>🏆 Achievements</Text>
              <View style={styles.reviewModalAchievements}>
                {selectedReview.achievements.map((achievement, index) => (
                  <Text key={index} style={styles.reviewModalAchievement}>
                    • {achievement}
                  </Text>
                ))}
              </View>

              <Text style={styles.reviewModalSectionTitle}>📈 Areas for Growth</Text>
              <View style={styles.reviewModalImprovements}>
                {selectedReview.improvementAreas.map((area, index) => (
                  <Text key={index} style={styles.reviewModalImprovement}>
                    • {area}
                  </Text>
                ))}
              </View>

              <LegendaryButton
                mode="text"
                onPress={() => setShowReviewModal(false)}
                style={styles.closeModalButton}
              >
                Close
              </LegendaryButton>
            </View>
          )}
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
  scoreDisplay: {
    alignItems: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: legendaryTheme.legendary.borders.radius.xl,
    padding: legendaryTheme.legendary.spacing.lg,
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  scoreValue: {
    fontSize: legendaryTheme.legendary.typography.fontSize.founder,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.legendaryBold,
    color: '#ffffff',
    textShadowColor: 'rgba(0, 0, 0, 0.3)',
    textShadowOffset: { width: 2, height: 2 },
    textShadowRadius: 4,
  },
  scoreLabel: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.regular,
    color: 'rgba(255, 255, 255, 0.9)',
    marginTop: legendaryTheme.legendary.spacing.xs,
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  gradeContainer: {
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    borderRadius: legendaryTheme.legendary.borders.radius.md,
    paddingHorizontal: legendaryTheme.legendary.spacing.md,
    paddingVertical: legendaryTheme.legendary.spacing.xs,
  },
  gradeText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xl,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    textShadowColor: 'rgba(0, 0, 0, 0.2)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
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
  quickMetricsContainer: {
    paddingHorizontal: legendaryTheme.legendary.spacing.lg,
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  quickMetricsGrid: {
    flexDirection: 'row',
    gap: legendaryTheme.legendary.spacing.md,
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
  chartLegend: {
    flexDirection: 'row',
    gap: legendaryTheme.legendary.spacing.lg,
    marginTop: legendaryTheme.legendary.spacing.md,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: legendaryTheme.legendary.spacing.xs,
  },
  legendDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
  },
  legendText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: legendaryTheme.colors.onSurface,
  },
  chartDescription: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
    color: legendaryTheme.colors.onSurface,
    textAlign: 'center',
    fontStyle: 'italic',
    marginTop: legendaryTheme.legendary.spacing.md,
  },
  skillsContainer: {
    paddingHorizontal: legendaryTheme.legendary.spacing.lg,
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  skillsCard: {
    padding: legendaryTheme.legendary.spacing.lg,
  },
  skillsList: {
    gap: legendaryTheme.legendary.spacing.md,
  },
  skillItem: {
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  skillHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  skillName: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
    color: legendaryTheme.colors.onSurface,
  },
  skillScore: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.primary,
  },
  skillProgressContainer: {
    height: 8,
    backgroundColor: legendaryTheme.colors.outline,
    borderRadius: 4,
    overflow: 'hidden',
  },
  skillProgress: {
    height: 8,
    borderRadius: 4,
  },
  insightsButton: {
    marginTop: legendaryTheme.legendary.spacing.lg,
  },
  insightsButtonText: {
    color: legendaryTheme.colors.primary,
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
  },
  reviewsContainer: {
    paddingHorizontal: legendaryTheme.legendary.spacing.lg,
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  reviewsCard: {
    padding: legendaryTheme.legendary.spacing.lg,
  },
  reviewsHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  reviewsBadge: {
    backgroundColor: legendaryTheme.legendary.colors.legendary,
  },
  reviewsList: {
    gap: legendaryTheme.legendary.spacing.md,
  },
  reviewItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: legendaryTheme.legendary.spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: legendaryTheme.colors.outline,
  },
  reviewContent: {
    flex: 1,
  },
  reviewMainInfo: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  reviewPeriod: {
    fontSize: legendaryTheme.legendary.typography.fontSize.lg,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.onSurface,
  },
  reviewDate: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: legendaryTheme.colors.outline,
  },
  reviewScores: {
    flexDirection: 'row',
    gap: legendaryTheme.legendary.spacing.lg,
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  reviewScoreItem: {
    alignItems: 'center',
  },
  reviewScoreValue: {
    fontSize: legendaryTheme.legendary.typography.fontSize.lg,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.primary,
  },
  reviewScoreLabel: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    color: legendaryTheme.colors.outline,
  },
  reviewStatus: {
    flexDirection: 'row',
    gap: legendaryTheme.legendary.spacing.sm,
  },
  statusChip: {
    elevation: 0,
  },
  statusChipText: {
    color: '#ffffff',
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
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
  reviewModal: {
    backgroundColor: 'white',
    margin: legendaryTheme.legendary.spacing.lg,
    borderRadius: legendaryTheme.legendary.borders.radius.xl,
    maxHeight: height * 0.8,
  },
  reviewModalContent: {
    padding: legendaryTheme.legendary.spacing.lg,
  },
  reviewModalTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xl,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.legendaryBold,
    color: legendaryTheme.colors.primary,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  reviewModalScores: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  modalScoreItem: {
    alignItems: 'center',
  },
  modalScoreValue: {
    fontSize: legendaryTheme.legendary.typography.fontSize['2xl'],
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.legendary.colors.legendary,
  },
  modalScoreLabel: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: legendaryTheme.colors.outline,
    marginTop: legendaryTheme.legendary.spacing.xs,
  },
  reviewModalSectionTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.lg,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.primary,
    marginBottom: legendaryTheme.legendary.spacing.md,
    marginTop: legendaryTheme.legendary.spacing.lg,
  },
  reviewModalAchievements: {
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  reviewModalAchievement: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.colors.onSurface,
    marginBottom: legendaryTheme.legendary.spacing.sm,
    lineHeight: 22,
  },
  reviewModalImprovements: {
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  reviewModalImprovement: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.colors.onSurface,
    marginBottom: legendaryTheme.legendary.spacing.sm,
    lineHeight: 22,
  },
  closeModalButton: {
    marginTop: legendaryTheme.legendary.spacing.lg,
  },
});

// =====================================
// 🎸 LEGENDARY EXPORTS 🎸
// =====================================

export default LegendaryPerformanceScreen;

// =====================================
// 🎸 LEGENDARY COMPLETION MESSAGE 🎸
// =====================================

console.log('🎸🎸🎸 LEGENDARY PERFORMANCE SCREEN LOADED! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Performance screen loaded at: 2025-08-06 01:57:33 UTC`);
console.log('📊 Performance analytics: SWISS PRECISION');
console.log('👑 RICKROLL187 founder metrics: LEGENDARY');
console.log('📈 Interactive charts: MAXIMUM VISUALIZATION');
console.log('⚙️ Skills breakdown: INFINITE INSIGHTS');
console.log('📋 Performance reviews: COMPREHENSIVE TRACKING');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
