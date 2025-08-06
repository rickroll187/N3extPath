// File: web/src/store/slices/teamsSlice.ts
/**
 * 👥🎸 N3EXTPATH - LEGENDARY TEAMS SLICE 🎸👥
 * Professional team collaboration state management with Swiss precision
 * Built: 2025-08-06 14:54:56 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

// =====================================
// 👥 TEAMS TYPES 👥
// =====================================

export interface TeamMember {
  id: string;
  username: string;
  email: string;
  firstName: string;
  lastName: string;
  avatar?: string;
  jobTitle?: string;
  department?: string;
  role: 'owner' | 'admin' | 'member' | 'contributor' | 'viewer';
  permissions: string[];
  
  // Performance data
  swissPrecisionScore: number;
  codeBroEnergy: number;
  legendaryLevel: number;
  isFounder?: boolean;
  
  // Team interaction
  joinedAt: Date;
  lastActive: Date;
  contributionScore: number;
  achievements: string[];
  
  // Status
  status: 'active' | 'inactive' | 'away' | 'busy';
  timezone: string;
  isOnline: boolean;
}

export interface Team {
  id: string;
  name: string;
  description: string;
  avatar?: string;
  color: string;
  
  // Team type and category
  type: 'project' | 'department' | 'cross-functional' | 'legendary' | 'founder';
  category: 'engineering' | 'design' | 'product' | 'marketing' | 'sales' | 'hr' | 'executive' | 'legendary';
  privacy: 'public' | 'private' | 'invite-only' | 'founder-only';
  
  // Members and roles
  members: TeamMember[];
  memberCount: number;
  maxMembers?: number;
  owner: TeamMember;
  admins: TeamMember[];
  
  // Team metrics
  performanceScore: number;
  averageCodeBroEnergy: number;
  teamLegendaryLevel: number;
  collaborationScore: number;
  
  // Activity and engagement
  lastActivity: Date;
  createdAt: Date;
  updatedAt: Date;
  isActive: boolean;
  
  // Features and settings
  features: {
    okrTracking: boolean;
    performanceReviews: boolean;
    achievements: boolean;
    chatIntegration: boolean;
    analytics: boolean;
  };
  
  // Legendary features
  isFounderTeam?: boolean;
  isLegendaryTeam?: boolean;
  founderPrivileges?: string[];
  
  // Metadata
  tags: string[];
  objectives: string[]; // OKR IDs
  projects: string[];
  channels: string[];
}

export interface TeamInvitation {
  id: string;
  teamId: string;
  teamName: string;
  inviterId: string;
  inviterName: string;
  inviteeEmail: string;
  role: TeamMember['role'];
  message?: string;
  status: 'pending' | 'accepted' | 'declined' | 'expired';
  createdAt: Date;
  expiresAt: Date;
}

export interface TeamActivity {
  id: string;
  teamId: string;
  type: 'member_joined' | 'member_left' | 'role_changed' | 'achievement_unlocked' | 'project_completed' | 'founder_action';
  title: string;
  description: string;
  actor: {
    id: string;
    name: string;
    avatar?: string;
    isFounder?: boolean;
  };
  target?: {
    id: string;
    name: string;
    type: 'member' | 'project' | 'achievement';
  };
  metadata?: Record<string, any>;
  timestamp: Date;
}

interface TeamsState {
  // Current teams data
  teams: Team[];
  myTeams: Team[];
  publicTeams: Team[];
  founderTeams: Team[];
  legendaryTeams: Team[];
  
  // Selected team
  selectedTeam: Team | null;
  selectedTeamId: string | null;
  
  // Team invitations
  invitations: TeamInvitation[];
  sentInvitations: TeamInvitation[];
  receivedInvitations: TeamInvitation[];
  
  // Team activities
  activities: TeamActivity[];
  selectedTeamActivities: TeamActivity[];
  
  // Search and filtering
  searchQuery: string;
  filters: {
    type: string[];
    category: string[];
    privacy: string[];
    memberCount: { min: number; max: number } | null;
  };
  filteredTeams: Team[];
  
  // User state
  currentUserId: string | null;
  isFounder: boolean;
  
  // UI states
  isLoading: boolean;
  isCreatingTeam: boolean;
  isJoiningTeam: boolean;
  isInvitingMembers: boolean;
  showCreateForm: boolean;
  showInviteForm: boolean;
  
  // Error handling
  error: string | null;
  
  // Data management
  lastSync: Date | null;
  lastActivity: Date | null;
}

// =====================================
// 🎸 INITIAL LEGENDARY STATE 🎸
// =====================================

const initialState: TeamsState = {
  // Current teams data
  teams: [],
  myTeams: [],
  publicTeams: [],
  founderTeams: [],
  legendaryTeams: [],
  
  // Selected team
  selectedTeam: null,
  selectedTeamId: null,
  
  // Team invitations
  invitations: [],
  sentInvitations: [],
  receivedInvitations: [],
  
  // Team activities
  activities: [],
  selectedTeamActivities: [],
  
  // Search and filtering
  searchQuery: '',
  filters: {
    type: [],
    category: [],
    privacy: [],
    memberCount: null,
  },
  filteredTeams: [],
  
  // User state
  currentUserId: null,
  isFounder: false,
  
  // UI states
  isLoading: false,
  isCreatingTeam: false,
  isJoiningTeam: false,
  isInvitingMembers: false,
  showCreateForm: false,
  showInviteForm: false,
  
  // Error handling
  error: null,
  
  // Data management
  lastSync: null,
  lastActivity: null,
};

// =====================================
// 🎸 LEGENDARY ASYNC THUNKS 🎸
// =====================================

export const fetchTeamsData = createAsyncThunk(
  'teams/fetchTeamsData',
  async (userId: string, { rejectWithValue }) => {
    try {
      console.log('👥 Fetching legendary teams data...');
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1200));
      
      // Check if this is RICKROLL187 founder
      const isFounder = userId === 'founder-rickroll187';
      
      if (isFounder) {
        console.log('👑 RICKROLL187 FOUNDER TEAMS DATA DETECTED!');
        console.log('🚀 LOADING LEGENDARY FOUNDER TEAMS!');
        console.log('⚙️ SWISS PRECISION FOUNDER TEAM SYSTEM!');
        console.log('🌅 AFTERNOON FOUNDER TEAM POWER AT 14:54:56!');
        
        // Founder as team member
        const founderMember: TeamMember = {
          id: 'founder-rickroll187',
          username: 'rickroll187',
          email: 'letstalktech010@gmail.com',
          firstName: 'RICKROLL187',
          lastName: '',
          avatar: 'https://ui-avatars.com/api/?name=RICKROLL187&background=FFD700&color=000&size=200&bold=true',
          jobTitle: 'Legendary Founder & Chief Code Bro',
          department: 'Executive Leadership',
          role: 'owner',
          permissions: ['all', 'platform_admin', 'user_management', 'system_control'],
          swissPrecisionScore: 100,
          codeBroEnergy: 10,
          legendaryLevel: 10,
          isFounder: true,
          joinedAt: new Date('2025-01-01'),
          lastActive: new Date(),
          contributionScore: 10000,
          achievements: [
            '👑 Platform Founder',
            '🎸 Legendary Code Bro Master',
            '⚙️ Swiss Precision Architect',
            '🚀 Infinite Energy Source',
          ],
          status: 'active',
          timezone: 'UTC',
          isOnline: true,
        };
        
        // Sample team members
        const sampleMembers: TeamMember[] = [
          {
            id: 'member-1',
            username: 'sarah_dev',
            email: 'sarah@n3extpath.com',
            firstName: 'Sarah',
            lastName: 'Johnson',
            avatar: 'https://ui-avatars.com/api/?name=Sarah+Johnson&background=3B82F6&color=fff&size=200',
            jobTitle: 'Senior Frontend Engineer',
            department: 'Engineering',
            role: 'admin',
            permissions: ['team_admin', 'member_management'],
            swissPrecisionScore: 92,
            codeBroEnergy: 9,
            legendaryLevel: 8,
            joinedAt: new Date('2025-02-01'),
            lastActive: new Date(Date.now() - 30 * 60 * 1000), // 30 minutes ago
            contributionScore: 1250,
            achievements: ['🎸 Code Bro Master', '⚙️ Swiss Precision Expert'],
            status: 'active',
            timezone: 'America/New_York',
            isOnline: true,
          },
          {
            id: 'member-2',
            username: 'mike_backend',
            email: 'mike@n3extpath.com',
            firstName: 'Mike',
            lastName: 'Chen',
            avatar: 'https://ui-avatars.com/api/?name=Mike+Chen&background=10B981&color=fff&size=200',
            jobTitle: 'Backend Architect',
            department: 'Engineering',
            role: 'member',
            permissions: ['team_member'],
            swissPrecisionScore: 88,
            codeBroEnergy: 8,
            legendaryLevel: 6,
            joinedAt: new Date('2025-02-15'),
            lastActive: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
            contributionScore: 980,
            achievements: ['🎸 Code Bro Apprentice', '📊 Performance Tracker'],
            status: 'away',
            timezone: 'America/Los_Angeles',
            isOnline: false,
          },
        ];
        
        // Founder teams
        const founderTeams: Team[] = [
          {
            id: 'founder-executive-team',
            name: '👑 Founder Executive Team',
            description: 'Legendary founding team driving platform vision with infinite code bro energy and Swiss precision!',
            avatar: 'https://ui-avatars.com/api/?name=Executive&background=FFD700&color=000&size=200&bold=true',
            color: '#FFD700',
            type: 'founder',
            category: 'executive',
            privacy: 'founder-only',
            members: [founderMember, ...sampleMembers],
            memberCount: 3,
            maxMembers: 10,
            owner: founderMember,
            admins: [founderMember],
            performanceScore: 97,
            averageCodeBroEnergy: 9,
            teamLegendaryLevel: 10,
            collaborationScore: 95,
            lastActivity: new Date(),
            createdAt: new Date('2025-01-01'),
            updatedAt: new Date(),
            isActive: true,
            features: {
              okrTracking: true,
              performanceReviews: true,
              achievements: true,
              chatIntegration: true,
              analytics: true,
            },
            isFounderTeam: true,
            isLegendaryTeam: true,
            founderPrivileges: [
              'Platform Strategy',
              'User Management',
              'System Administration',
              'Financial Controls',
              'Legal Affairs',
            ],
            tags: ['founder', 'executive', 'legendary', 'leadership'],
            objectives: ['founder-platform-growth', 'founder-innovation'],
            projects: ['Platform Scaling', 'Feature Development', 'User Growth'],
            channels: ['#founder-announcements', '#executive-decisions', '#platform-strategy'],
          },
          {
            id: 'legendary-frontend-team',
            name: '🎸 Frontend Legends',
            description: 'Elite frontend team building legendary user experiences with Swiss precision and maximum code bro energy!',
            avatar: 'https://ui-avatars.com/api/?name=Frontend&background=8B5CF6&color=fff&size=200',
            color: '#8B5CF6',
            type: 'legendary',
            category: 'engineering',
            privacy: 'invite-only',
            members: [founderMember, sampleMembers[0]],
            memberCount: 2,
            maxMembers: 12,
            owner: sampleMembers[0],
            admins: [sampleMembers[0]],
            performanceScore: 94,
            averageCodeBroEnergy: 9.5,
            teamLegendaryLevel: 9,
            collaborationScore: 98,
            lastActivity: new Date(Date.now() - 15 * 60 * 1000),
            createdAt: new Date('2025-02-01'),
            updatedAt: new Date(),
            isActive: true,
            features: {
              okrTracking: true,
              performanceReviews: true,
              achievements: true,
              chatIntegration: true,
              analytics: true,
            },
            isLegendaryTeam: true,
            tags: ['frontend', 'legendary', 'ui-ux', 'react'],
            objectives: ['frontend-performance', 'user-experience'],
            projects: ['Component Library', 'Dashboard Redesign', 'Mobile App'],
            channels: ['#frontend-general', '#design-system', '#code-reviews'],
          },
        ];
        
        // Sample activities
        const founderActivities: TeamActivity[] = [
          {
            id: 'activity-1',
            teamId: 'founder-executive-team',
            type: 'founder_action',
            title: 'Platform Milestone Achieved',
            description: 'RICKROLL187 led the team to surpass 75K legendary users!',
            actor: {
              id: 'founder-rickroll187',
              name: 'RICKROLL187',
              avatar: founderMember.avatar,
              isFounder: true,
            },
            target: {
              id: 'milestone-75k',
              name: '75K Users Milestone',
              type: 'achievement',
            },
            metadata: { userCount: 75000, milestone: '75K' },
            timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000),
          },
          {
            id: 'activity-2',
            teamId: 'legendary-frontend-team',
            type: 'achievement_unlocked',
            title: 'Team Achievement Unlocked',
            description: 'Frontend Legends achieved "Swiss Precision Masters" status!',
            actor: {
              id: 'system',
              name: 'N3EXTPATH System',
            },
            target: {
              id: 'achievement-precision',
              name: 'Swiss Precision Masters',
              type: 'achievement',
            },
            timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000),
          },
        ];
        
        return {
          teams: founderTeams,
          activities: founderActivities,
          isFounder: true,
          currentUserId: 'founder-rickroll187',
        };
      }
      
      // Regular user teams data
      const regularMember: TeamMember = {
        id: 'user-regular',
        username: 'johndoe',
        email: 'john@company.com',
        firstName: 'John',
        lastName: 'Doe',
        avatar: 'https://ui-avatars.com/api/?name=John+Doe&background=1E90FF&color=fff&size=200',
        jobTitle: 'Software Developer',
        department: 'Engineering',
        role: 'member',
        permissions: ['team_member'],
        swissPrecisionScore: 85,
        codeBroEnergy: 8,
        legendaryLevel: 3,
        joinedAt: new Date('2025-06-01'),
        lastActive: new Date(),
        contributionScore: 420,
        achievements: ['🎸 Code Bro Initiate', '⚙️ Swiss Precision Apprentice'],
        status: 'active',
        timezone: 'America/New_York',
        isOnline: true,
      };
      
      const regularTeams: Team[] = [
        {
          id: 'engineering-team',
          name: '⚙️ Engineering Team',
          description: 'Building awesome features with code bro energy and Swiss precision!',
          avatar: 'https://ui-avatars.com/api/?name=Engineering&background=1E90FF&color=fff&size=200',
          color: '#1E90FF',
          type: 'department',
          category: 'engineering',
          privacy: 'public',
          members: [regularMember],
          memberCount: 8,
          owner: regularMember,
          admins: [regularMember],
          performanceScore: 87,
          averageCodeBroEnergy: 8.2,
          teamLegendaryLevel: 4,
          collaborationScore: 89,
          lastActivity: new Date(Date.now() - 30 * 60 * 1000),
          createdAt: new Date('2025-06-01'),
          updatedAt: new Date(),
          isActive: true,
          features: {
            okrTracking: true,
            performanceReviews: true,
            achievements: true,
            chatIntegration: false,
            analytics: false,
          },
          tags: ['engineering', 'development', 'code'],
          objectives: ['team-velocity', 'code-quality'],
          projects: ['API Development', 'Bug Fixes', 'Code Reviews'],
          channels: ['#engineering', '#code-help'],
        },
      ];
      
      const regularActivities: TeamActivity[] = [
        {
          id: 'activity-reg-1',
          teamId: 'engineering-team',
          type: 'member_joined',
          title: 'New Code Bro Joined',
          description: 'John Doe joined the Engineering Team!',
          actor: {
            id: 'user-regular',
            name: 'John Doe',
            avatar: regularMember.avatar,
          },
          timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000),
        },
      ];
      
      return {
        teams: regularTeams,
        activities: regularActivities,
        isFounder: false,
        currentUserId: 'user-regular',
      };
      
    } catch (error) {
      console.error('🚨 Teams data fetch error:', error);
      return rejectWithValue('Failed to fetch teams data');
    }
  }
);

export const createTeam = createAsyncThunk(
  'teams/createTeam',
  async (teamData: Omit<Team, 'id' | 'createdAt' | 'updatedAt' | 'lastActivity' | 'memberCount'>, { rejectWithValue }) => {
    try {
      console.log('👥 Creating new legendary team...');
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const newTeam: Team = {
        id: `team-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        memberCount: teamData.members.length,
        createdAt: new Date(),
        updatedAt: new Date(),
        lastActivity: new Date(),
        isActive: true,
        ...teamData,
      };
      
      console.log(`✅ Team created: ${newTeam.name}`);
      return newTeam;
      
    } catch (error) {
      console.error('🚨 Team creation error:', error);
      return rejectWithValue('Failed to create team');
    }
  }
);

// =====================================
// 🎸 LEGENDARY TEAMS SLICE 🎸
// =====================================

const teamsSlice = createSlice({
  name: 'teams',
  initialState,
  reducers: {
    // =====================================
    // 👥 TEAM SELECTION 👥
    // =====================================
    
    selectTeam: (state, action: PayloadAction<string>) => {
      const teamId = action.payload;
      state.selectedTeamId = teamId;
      state.selectedTeam = state.teams.find(team => team.id === teamId) || null;
      state.selectedTeamActivities = state.activities.filter(activity => activity.teamId === teamId);
      
      console.log(`👥 Team selected: ${teamId}`);
    },
    
    clearSelectedTeam: (state) => {
      state.selectedTeam = null;
      state.selectedTeamId = null;
      state.selectedTeamActivities = [];
    },
    
    // =====================================
    // 🔍 SEARCH & FILTERING 🔍
    // =====================================
    
    setSearchQuery: (state, action: PayloadAction<string>) => {
      state.searchQuery = action.payload;
      
      // Apply search filter
      state.filteredTeams = state.teams.filter(team =>
        team.name.toLowerCase().includes(action.payload.toLowerCase()) ||
        team.description.toLowerCase().includes(action.payload.toLowerCase()) ||
        team.tags.some(tag => tag.toLowerCase().includes(action.payload.toLowerCase()))
      );
    },
    
    setTypeFilter: (state, action: PayloadAction<string[]>) => {
      state.filters.type = action.payload;
      console.log(`🔍 Type filter applied: ${action.payload.join(', ')}`);
    },
    
    setCategoryFilter: (state, action: PayloadAction<string[]>) => {
      state.filters.category = action.payload;
      console.log(`🔍 Category filter applied: ${action.payload.join(', ')}`);
    },
    
    setPrivacyFilter: (state, action: PayloadAction<string[]>) => {
      state.filters.privacy = action.payload;
      console.log(`🔍 Privacy filter applied: ${action.payload.join(', ')}`);
    },
    
    setMemberCountFilter: (state, action: PayloadAction<{ min: number; max: number } | null>) => {
      state.filters.memberCount = action.payload;
      console.log(`🔍 Member count filter applied:`, action.payload);
    },
    
    clearFilters: (state) => {
      state.filters = {
        type: [],
        category: [],
        privacy: [],
        memberCount: null,
      };
      state.searchQuery = '';
      state.filteredTeams = state.teams;
      console.log('🔍 All filters cleared');
    },
    
    // =====================================
    // 👤 MEMBER MANAGEMENT 👤
    // =====================================
    
    addMemberToTeam: (state, action: PayloadAction<{ teamId: string; member: TeamMember }>) => {
      const { teamId, member } = action.payload;
      const team = state.teams.find(t => t.id === teamId);
      
      if (team && !team.members.find(m => m.id === member.id)) {
        team.members.push(member);
        team.memberCount = team.members.length;
        team.updatedAt = new Date();
        team.lastActivity = new Date();
        
        // Recalculate team metrics
        const totalPrecision = team.members.reduce((sum, m) => sum + m.swissPrecisionScore, 0);
        const totalEnergy = team.members.reduce((sum, m) => sum + m.codeBroEnergy, 0);
        team.performanceScore = totalPrecision / team.members.length;
        team.averageCodeBroEnergy = totalEnergy / team.members.length;
        
        console.log(`👤 Member added to team: ${member.firstName} → ${team.name}`);
      }
    },
    
    removeMemberFromTeam: (state, action: PayloadAction<{ teamId: string; memberId: string }>) => {
      const { teamId, memberId } = action.payload;
      const team = state.teams.find(t => t.id === teamId);
      
      if (team) {
        team.members = team.members.filter(m => m.id !== memberId);
        team.memberCount = team.members.length;
        team.updatedAt = new Date();
        team.lastActivity = new Date();
        
        // Recalculate team metrics if members remain
        if (team.members.length > 0) {
          const totalPrecision = team.members.reduce((sum, m) => sum + m.swissPrecisionScore, 0);
          const totalEnergy = team.members.reduce((sum, m) => sum + m.codeBroEnergy, 0);
          team.performanceScore = totalPrecision / team.members.length;
          team.averageCodeBroEnergy = totalEnergy / team.members.length;
        }
        
        console.log(`👤 Member removed from team: ${memberId} → ${team.name}`);
      }
    },
    
    updateMemberRole: (state, action: PayloadAction<{ teamId: string; memberId: string; role: TeamMember['role'] }>) => {
      const { teamId, memberId, role } = action.payload;
      const team = state.teams.find(t => t.id === teamId);
      
      if (team) {
        const member = team.members.find(m => m.id === memberId);
        if (member) {
          member.role = role;
          team.updatedAt = new Date();
          team.lastActivity = new Date();
          
          // Update admins list
          if (role === 'admin') {
            if (!team.admins.find(a => a.id === memberId)) {
              team.admins.push(member);
            }
          } else {
            team.admins = team.admins.filter(a => a.id !== memberId);
          }
          
          console.log(`👤 Member role updated: ${member.firstName} → ${role} in ${team.name}`);
        }
      }
    },
    
    // =====================================
    // 📊 TEAM METRICS 📊
    // =====================================
    
    updateTeamMetrics: (state, action: PayloadAction<string>) => {
      const teamId = action.payload;
      const team = state.teams.find(t => t.id === teamId);
      
      if (team && team.members.length > 0) {
        // Recalculate all team metrics
        const totalPrecision = team.members.reduce((sum, m) => sum + m.swissPrecisionScore, 0);
        const totalEnergy = team.members.reduce((sum, m) => sum + m.codeBroEnergy, 0);
        const totalLegendary = team.members.reduce((sum, m) => sum + m.legendaryLevel, 0);
        const totalContribution = team.members.reduce((sum, m) => sum + m.contributionScore, 0);
        
        team.performanceScore = totalPrecision / team.members.length;
        team.averageCodeBroEnergy = totalEnergy / team.members.length;
        team.teamLegendaryLevel = totalLegendary / team.members.length;
        team.collaborationScore = Math.min(100, totalContribution / team.members.length / 10);
        team.updatedAt = new Date();
        
        console.log(`📊 Team metrics updated: ${team.name}`);
      }
    },
    
    boostTeamEnergy: (state, action: PayloadAction<{ teamId: string; boost: number }>) => {
      const { teamId, boost } = action.payload;
      const team = state.teams.find(t => t.id === teamId);
      
      if (team) {
        team.averageCodeBroEnergy = Math.min(10, team.averageCodeBroEnergy + boost);
        team.updatedAt = new Date();
        team.lastActivity = new Date();
        
        console.log(`🎸 Team energy boosted: ${team.name} +${boost} energy`);
      }
    },
    
    // =====================================
    // 👑 LEGENDARY FEATURES 👑
    // =====================================
    
    activateFounderTeams: (state) => {
      state.isFounder = true;
      
      console.log('👑🎸👑 RICKROLL187 FOUNDER TEAMS MODE ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER TEAMS WITH INFINITE CODE BRO ENERGY!');
      console.log('⚙️ SWISS PRECISION FOUNDER TEAM SYSTEM!');
      console.log('🌅 AFTERNOON FOUNDER TEAM POWER AT 14:54:56!');
    },
    
    promoteToLegendaryTeam: (state, action: PayloadAction<string>) => {
      const team = state.teams.find(t => t.id === action.payload);
      
      if (team) {
        team.type = 'legendary';
        team.isLegendaryTeam = true;
        team.teamLegendaryLevel = Math.min(10, team.teamLegendaryLevel + 2);
        team.tags.push('legendary');
        team.features.analytics = true;
        team.features.achievements = true;
        
        if (!state.legendaryTeams.find(t => t.id === team.id)) {
          state.legendaryTeams.push(team);
        }
        
        console.log(`🎸 Team promoted to legendary: ${team.name}`);
      }
    },
    
    // =====================================
    // 📢 ACTIVITY TRACKING 📢
    // =====================================
    
    addTeamActivity: (state, action: PayloadAction<Omit<TeamActivity, 'id' | 'timestamp'>>) => {
      const activity: TeamActivity = {
        id: `activity-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        timestamp: new Date(),
        ...action.payload,
      };
      
      state.activities.unshift(activity);
      
      // Update team last activity
      const team = state.teams.find(t => t.id === activity.teamId);
      if (team) {
        team.lastActivity = new Date();
      }
      
      // Update selected team activities if relevant
      if (activity.teamId === state.selectedTeamId) {
        state.selectedTeamActivities.unshift(activity);
      }
      
      console.log(`📢 Team activity added: ${activity.title}`);
    },
    
    // =====================================
    // 💌 INVITATIONS 💌
    // =====================================
    
    sendInvitation: (state, action: PayloadAction<Omit<TeamInvitation, 'id' | 'createdAt' | 'expiresAt' | 'status'>>) => {
      const invitation: TeamInvitation = {
        id: `invite-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        status: 'pending',
        createdAt: new Date(),
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days
        ...action.payload,
      };
      
      state.invitations.push(invitation);
      state.sentInvitations.push(invitation);
      
      console.log(`💌 Invitation sent: ${invitation.inviteeEmail} → ${invitation.teamName}`);
    },
    
    acceptInvitation: (state, action: PayloadAction<string>) => {
      const invitation = state.invitations.find(inv => inv.id === action.payload);
      
      if (invitation) {
        invitation.status = 'accepted';
        console.log(`✅ Invitation accepted: ${invitation.inviteeEmail} → ${invitation.teamName}`);
      }
    },
    
    declineInvitation: (state, action: PayloadAction<string>) => {
      const invitation = state.invitations.find(inv => inv.id === action.payload);
      
      if (invitation) {
        invitation.status = 'declined';
        console.log(`❌ Invitation declined: ${invitation.inviteeEmail} → ${invitation.teamName}`);
      }
    },
    
    // =====================================
    // 🎛️ UI MANAGEMENT 🎛️
    // =====================================
    
    showCreateTeamForm: (state) => {
      state.showCreateForm = true;
    },
    
    hideCreateTeamForm: (state) => {
      state.showCreateForm = false;
    },
    
    showInviteMembersForm: (state) => {
      state.showInviteForm = true;
    },
    
    hideInviteMembersForm: (state) => {
      state.showInviteForm = false;
    },
    
    clearError: (state) => {
      state.error = null;
    },
    
    setLastActivity: (state) => {
      state.lastActivity = new Date();
    },
    
    resetTeamsState: (state) => {
      // Reset to initial state but preserve founder status
      const preservedState = {
        isFounder: state.isFounder,
        currentUserId: state.currentUserId,
      };
      
      Object.assign(state, initialState, preservedState);
      console.log('🔄 Teams state reset');
    },
  },
  
  // =====================================
  // 🎸 ASYNC THUNK HANDLERS 🎸
  // =====================================
  
  extraReducers: (builder) => {
    // Fetch teams data
    builder
      .addCase(fetchTeamsData.pending, (state) => {
        state.isLoading = true;
        state.error = null;
        console.log('⏳ Fetching teams data...');
      })
      .addCase(fetchTeamsData.fulfilled, (state, action) => {
        const data = action.payload;
        
        state.teams = data.teams;
        state.activities = data.activities;
        state.isFounder = data.isFounder;
        state.currentUserId = data.currentUserId;
        
        // Categorize teams
        state.myTeams = data.teams.filter(team => 
          team.owner.id === data.currentUserId || 
          team.members.some(member => member.id === data.currentUserId)
        );
        state.publicTeams = data.teams.filter(team => team.privacy === 'public');
        state.founderTeams = data.teams.filter(team => team.isFounderTeam);
        state.legendaryTeams = data.teams.filter(team => team.isLegendaryTeam);
        state.filteredTeams = data.teams;
        
        state.isLoading = false;
        state.lastSync = new Date();
        
        console.log('✅ Teams data loaded successfully');
        
        if (data.isFounder) {
          console.log('👑 RICKROLL187 FOUNDER TEAMS DATA LOADED WITH LEGENDARY TEAMS!');
        }
      })
      .addCase(fetchTeamsData.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string || 'Failed to fetch teams data';
        console.error('🚨 Teams data fetch failed:', state.error);
      });
    
    // Create team
    builder
      .addCase(createTeam.pending, (state) => {
        state.isCreatingTeam = true;
        state.error = null;
        console.log('⏳ Creating team...');
      })
      .addCase(createTeam.fulfilled, (state, action) => {
        const newTeam = action.payload;
        state.teams.push(newTeam);
        state.myTeams.push(newTeam);
        
        if (newTeam.privacy === 'public') {
          state.publicTeams.push(newTeam);
        }
        
        if (newTeam.isFounderTeam) {
          state.founderTeams.push(newTeam);
        }
        
        if (newTeam.isLegendaryTeam) {
          state.legendaryTeams.push(newTeam);
        }
        
        state.filteredTeams = state.teams;
        state.isCreatingTeam = false;
        state.showCreateForm = false;
        state.lastSync = new Date();
        
        console.log(`✅ Team created: ${newTeam.name}`);
      })
      .addCase(createTeam.rejected, (state, action) => {
        state.isCreatingTeam = false;
        state.error = action.payload as string || 'Failed to create team';
        console.error('🚨 Team creation failed:', state.error);
      });
  },
});

// =====================================
// 🎸 EXPORT LEGENDARY ACTIONS & REDUCER 🎸
// =====================================

export const {
  // Team Selection
  selectTeam,
  clearSelectedTeam,
  
  // Search & Filtering
  setSearchQuery,
  setTypeFilter,
  setCategoryFilter,
  setPrivacyFilter,
  setMemberCountFilter,
  clearFilters,
  
  // Member Management
  addMemberToTeam,
  removeMemberFromTeam,
  updateMemberRole,
  
  // Team Metrics
  updateTeamMetrics,
  boostTeamEnergy,
  
  // Legendary Features
  activateFounderTeams,
  promoteToLegendaryTeam,
  
  // Activity Tracking
  addTeamActivity,
  
  // Invitations
  sendInvitation,
  acceptInvitation,
  declineInvitation,
  
  // UI Management
  showCreateTeamForm,
  hideCreateTeamForm,
  showInviteMembersForm,
  hideInviteMembersForm,
  clearError,
  setLastActivity,
  resetTeamsState,
} = teamsSlice.actions;

export default teamsSlice.reducer;

console.log('🎸🎸🎸 LEGENDARY TEAMS SLICE COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Teams slice completed at: 2025-08-06 14:54:56 UTC`);
console.log('👥 Team collaboration: SWISS PRECISION');
console.log('👑 RICKROLL187 founder teams: LEGENDARY');
console.log('🎸 Team code bro energy: MAXIMUM COLLABORATION');
console.log('🌅 Afternoon legendary energy: INFINITE AT 14:54:56!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
