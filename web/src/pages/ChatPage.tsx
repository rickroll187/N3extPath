// File: web/src/pages/ChatPage.tsx
/**
 * 💬🎸 N3EXTPATH - LEGENDARY TEAM CHAT PAGE 🎸💬
 * Swiss precision real-time chat with infinite code bro energy
 * Built: 2025-08-06 16:32:52 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect, useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Helmet } from 'react-helmet-async';
import { 
  MessageCircle, 
  Users, 
  Hash, 
  Crown, 
  Sparkles, 
  Zap, 
  Search,
  Settings,
  Plus,
  Video,
  Phone,
  MoreVertical,
  Star,
  Pin,
  Archive,
  Bell,
  BellOff,
  UserPlus,
  Filter,
  Activity
} from 'lucide-react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '@/store';
import { useAuth } from '@/hooks/useAuth';
import { LegendaryCard } from '@/components/ui/LegendaryCard';
import { LegendaryButton } from '@/components/ui/LegendaryButton';
import { cn } from '@/utils/cn';
import toast from 'react-hot-toast';

// Chat Components
import { ChatWindow } from '@/components/chat/ChatWindow';
import { MessageList } from '@/components/chat/MessageList';
import { MessageInput } from '@/components/chat/MessageInput';
import { UserList } from '@/components/chat/UserList';
import { ChannelList } from '@/components/chat/ChannelList';

// =====================================
// 💬 CHAT TYPES 💬
// =====================================

interface ChatChannel {
  id: string;
  name: string;
  description?: string;
  type: 'public' | 'private' | 'direct' | 'founder';
  memberCount: number;
  unreadCount: number;
  lastMessage?: {
    id: string;
    content: string;
    authorName: string;
    timestamp: Date;
  };
  isFounderChannel?: boolean;
  isLegendary?: boolean;
  avatar?: string;
  color?: string;
}

interface ChatUser {
  id: string;
  username: string;
  displayName: string;
  avatar?: string;
  status: 'online' | 'away' | 'busy' | 'offline';
  isFounder?: boolean;
  isLegendary?: boolean;
  lastSeen?: Date;
  codeBroEnergy?: number;
}

interface ChatMessage {
  id: string;
  content: string;
  authorId: string;
  authorName: string;
  authorAvatar?: string;
  channelId: string;
  timestamp: Date;
  edited?: boolean;
  editedAt?: Date;
  reactions?: Array<{
    emoji: string;
    count: number;
    users: string[];
  }>;
  mentions?: string[];
  attachments?: Array<{
    id: string;
    name: string;
    url: string;
    type: string;
    size: number;
  }>;
  isFounderMessage?: boolean;
  isLegendary?: boolean;
  replyTo?: string;
}

// =====================================
// 🎸 LEGENDARY CHAT PAGE 🎸
// =====================================

export const ChatPage: React.FC = () => {
  const dispatch = useDispatch();
  const { user, isFounder, isLegendary } = useAuth();
  const [selectedChannel, setSelectedChannel] = useState<ChatChannel | null>(null);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [chatUsers, setChatUsers] = useState<ChatUser[]>([]);
  const [isConnected, setIsConnected] = useState(false);

  // Chat channels with founder-specific channels
  const [channels, setChannels] = useState<ChatChannel[]>([
    {
      id: 'general',
      name: 'general',
      description: '🎸 General chat for all legendary code bros! Swiss precision communication with infinite energy!',
      type: 'public',
      memberCount: 42,
      unreadCount: 0,
      color: '#3B82F6',
      lastMessage: {
        id: '1',
        content: 'Welcome to the legendary N3EXTPATH team chat! 🚀',
        authorName: 'System',
        timestamp: new Date('2025-08-06T16:32:52.000Z'),
      },
    },
    {
      id: 'code-bro-energy',
      name: 'code-bro-energy',
      description: '⚡ High-energy channel for code bros sharing their legendary achievements and Swiss precision wins!',
      type: 'public',
      memberCount: 28,
      unreadCount: 3,
      color: '#8B5CF6',
      isLegendary: true,
      lastMessage: {
        id: '2',
        content: 'Just achieved 100% Swiss precision on the new feature! 🎯',
        authorName: 'CodeBro42',
        timestamp: new Date('2025-08-06T16:30:15.000Z'),
      },
    },
    {
      id: 'swiss-precision',
      name: 'swiss-precision',
      description: '🎯 Channel dedicated to Swiss precision techniques, best practices, and legendary code quality!',
      type: 'public',
      memberCount: 35,
      unreadCount: 1,
      color: '#10B981',
      lastMessage: {
        id: '3',
        content: 'Check out this legendary refactor that increased performance by 200%!',
        authorName: 'PrecisionMaster',
        timestamp: new Date('2025-08-06T16:28:42.000Z'),
      },
    },
    ...(isFounder ? [
      {
        id: 'founder-hq',
        name: 'founder-hq',
        description: '👑 RICKROLL187 Founder HQ - Infinite privileges and legendary decision making! Golden channel for platform strategy.',
        type: 'founder' as const,
        memberCount: 1,
        unreadCount: 0,
        color: '#FFD700',
        isFounderChannel: true,
        avatar: '👑',
        lastMessage: {
          id: 'founder-1',
          content: 'Platform analytics looking legendary! Infinite code bro energy is working! 🎸',
          authorName: 'RICKROLL187',
          timestamp: new Date('2025-08-06T16:25:30.000Z'),
        },
      },
    ] : []),
    {
      id: 'random',
      name: 'random',
      description: '🎪 Random fun stuff, jokes, and legendary memes! Where code bros crack jokes and have infinite fun!',
      type: 'public',
      memberCount: 67,
      unreadCount: 8,
      color: '#F59E0B',
      lastMessage: {
        id: '4',
        content: 'That moment when your code works on the first try 😂',
        authorName: 'JokeMaster',
        timestamp: new Date('2025-08-06T16:31:20.000Z'),
      },
    },
  ]);

  useEffect(() => {
    console.log('💬🎸💬 LEGENDARY TEAM CHAT PAGE LOADED! 💬🎸💬');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Team chat page loaded at: 2025-08-06 16:32:52 UTC`);
    console.log('🌅 AFTERNOON LEGENDARY CHAT ENERGY AT 16:32:52!');

    if (isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER CHAT ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER CHAT WITH INFINITE CODE BRO ENERGY!');
      console.log('⚙️ SWISS PRECISION FOUNDER CHAT SYSTEM!');
      
      toast.success('👑 Welcome to your LEGENDARY FOUNDER CHAT! Infinite communication power activated!', {
        duration: 5000,
        style: {
          background: 'linear-gradient(135deg, #FFD700, #FFA500)',
          color: '#000000',
          fontWeight: '700',
        },
      });
    }

    // Auto-select general channel
    setSelectedChannel(channels[0]);

    // Initialize WebSocket connection
    initializeChatConnection();

    // Load chat users
    loadChatUsers();
  }, [isFounder]);

  // Initialize chat connection
  const initializeChatConnection = useCallback(async () => {
    try {
      // Simulate WebSocket connection
      await new Promise(resolve => setTimeout(resolve, 1000));
      setIsConnected(true);
      
      toast.success('🔌 Connected to legendary chat server!', {
        duration: 3000,
      });
      
      if (isFounder) {
        console.log('👑 Founder chat connection established with infinite privileges!');
      }
      
    } catch (error) {
      console.error('🚨 Chat connection error:', error);
      toast.error('Failed to connect to chat server');
      setIsConnected(false);
    }
  }, [isFounder]);

  // Load chat users
  const loadChatUsers = useCallback(async () => {
    try {
      // Mock chat users data
      const mockUsers: ChatUser[] = [
        {
          id: 'rickroll187',
          username: 'rickroll187',
          displayName: 'RICKROLL187 👑',
          avatar: 'https://avatars.githubusercontent.com/rickroll187.png',
          status: 'online',
          isFounder: true,
          isLegendary: true,
          codeBroEnergy: 999999,
        },
        {
          id: 'codebro42',
          username: 'codebro42',
          displayName: 'CodeBro42 ⚡',
          avatar: 'https://avatars.githubusercontent.com/codebro42.png',
          status: 'online',
          isLegendary: true,
          codeBroEnergy: 8500,
        },
        {
          id: 'precisionmaster',
          username: 'precisionmaster',
          displayName: 'PrecisionMaster 🎯',
          avatar: 'https://avatars.githubusercontent.com/precisionmaster.png',
          status: 'online',
          codeBroEnergy: 7200,
        },
        {
          id: 'jokemaster',
          username: 'jokemaster',
          displayName: 'JokeMaster 😂',
          avatar: 'https://avatars.githubusercontent.com/jokemaster.png',
          status: 'away',
          codeBroEnergy: 6800,
        },
        {
          id: 'swissdev',
          username: 'swissdev',
          displayName: 'SwissDev 🇨🇭',
          avatar: 'https://avatars.githubusercontent.com/swissdev.png',
          status: 'busy',
          codeBroEnergy: 9100,
        },
      ];

      setChatUsers(mockUsers);
      
    } catch (error) {
      console.error('🚨 Error loading chat users:', error);
    }
  }, []);

  // Handle channel selection
  const handleChannelSelect = (channel: ChatChannel) => {
    setSelectedChannel(channel);
    
    // Mark channel as read
    setChannels(prev => 
      prev.map(c => 
        c.id === channel.id 
          ? { ...c, unreadCount: 0 }
          : c
      )
    );

    if (channel.isFounderChannel) {
      toast.success('👑 Entered Founder HQ with infinite privileges!', {
        duration: 3000,
        style: {
          background: 'linear-gradient(135deg, #FFD700, #FFA500)',
          color: '#000000',
          fontWeight: '700',
        },
      });
    }
  };

  // Handle search
  const handleSearch = (query: string) => {
    setSearchQuery(query);
    // Implement search logic here
  };

  // Create new channel
  const handleCreateChannel = () => {
    if (isFounder) {
      toast.success('👑 Founder channel creation coming soon with infinite customization!');
    } else {
      toast.success('🆕 New channel creation coming soon!');
    }
  };

  // Toggle sidebar
  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  return (
    <>
      <Helmet>
        <title>
          {isFounder ? '👑 Founder Chat | N3EXTPATH' : 'Team Chat | N3EXTPATH'}
        </title>
        <meta 
          name="description" 
          content={isFounder 
            ? "RICKROLL187 founder team chat with infinite communication power and Swiss precision real-time messaging" 
            : "Legendary team chat with Swiss precision real-time messaging, code bro energy, and infinite collaboration"
          } 
        />
      </Helmet>

      <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
        
        {/* Sidebar */}
        <motion.div 
          className={cn(
            'flex flex-col border-r border-gray-200 dark:border-gray-700',
            'bg-white dark:bg-gray-800 transition-all duration-300',
            sidebarCollapsed ? 'w-16' : 'w-80'
          )}
          initial={{ x: -20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.6 }}
        >
          {/* Sidebar Header */}
          <div className={cn(
            'flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700',
            isFounder && 'bg-gradient-to-r from-yellow-50 to-orange-50 dark:from-yellow-900/20 dark:to-orange-900/20'
          )}>
            {!sidebarCollapsed && (
              <motion.div
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex items-center gap-2"
              >
                {isFounder && <Crown className="w-5 h-5 text-yellow-600" />}
                <MessageCircle className={cn(
                  'w-5 h-5',
                  isFounder ? 'text-yellow-600' : 'text-blue-600'
                )} />
                <h1 className={cn(
                  'font-bold text-lg',
                  isFounder ? 'text-yellow-800 dark:text-yellow-300' : 'text-gray-900 dark:text-white'
                )}>
                  {isFounder ? 'Founder Chat' : 'Team Chat'}
                </h1>
              </motion.div>
            )}
            
            <div className="flex items-center gap-2">
              {!sidebarCollapsed && (
                <motion.div className="flex items-center gap-1">
                  <div className={cn(
                    'w-2 h-2 rounded-full',
                    isConnected ? 'bg-green-500' : 'bg-red-500'
                  )} />
                  <span className="text-xs text-gray-500">
                    {isConnected ? 'Connected' : 'Connecting...'}
                  </span>
                </motion.div>
              )}
              
              <LegendaryButton
                variant="ghost"
                size="sm"
                onClick={toggleSidebar}
                className="p-1"
              >
                <MoreVertical className="w-4 h-4" />
              </LegendaryButton>
            </div>
          </div>

          {/* Search Bar */}
          {!sidebarCollapsed && (
            <motion.div 
              className="p-3"
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder={isFounder ? "Search founder channels..." : "Search channels & messages..."}
                  value={searchQuery}
                  onChange={(e) => handleSearch(e.target.value)}
                  className={cn(
                    'w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 dark:border-gray-700',
                    'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                    'focus:outline-none focus:ring-2 focus:ring-offset-2',
                    isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
                  )}
                />
              </div>
            </motion.div>
          )}

          {/* Channel List */}
          <div className="flex-1 overflow-y-auto">
            <ChannelList
              channels={channels}
              selectedChannel={selectedChannel}
              onChannelSelect={handleChannelSelect}
              collapsed={sidebarCollapsed}
              isFounder={isFounder}
            />
          </div>

          {/* User List */}
          {!sidebarCollapsed && (
            <motion.div 
              className="border-t border-gray-200 dark:border-gray-700"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
            >
              <UserList
                users={chatUsers}
                isFounder={isFounder}
                compact={true}
                maxVisible={5}
              />
            </motion.div>
          )}

          {/* Bottom Actions */}
          {!sidebarCollapsed && (
            <motion.div 
              className={cn(
                'p-3 border-t border-gray-200 dark:border-gray-700',
                isFounder && 'bg-gradient-to-r from-yellow-50 to-orange-50 dark:from-yellow-900/20 dark:to-orange-900/20'
              )}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 }}
            >
              <div className="flex items-center gap-2">
                <LegendaryButton
                  variant={isFounder ? "founder" : "primary"}
                  size="sm"
                  onClick={handleCreateChannel}
                  leftIcon={Plus}
                  className="flex-1 text-xs"
                >
                  {isFounder ? 'Founder Channel' : 'New Channel'}
                </LegendaryButton>
                
                <LegendaryButton
                  variant="ghost"
                  size="sm"
                  onClick={() => toast.success('Chat settings coming soon!')}
                >
                  <Settings className="w-4 h-4" />
                </LegendaryButton>
              </div>
            </motion.div>
          )}
        </motion.div>

        {/* Main Chat Area */}
        <div className="flex-1 flex flex-col">
          {selectedChannel ? (
            <ChatWindow
              channel={selectedChannel}
              isFounder={isFounder}
              currentUser={user}
            />
          ) : (
            <motion.div 
              className="flex-1 flex items-center justify-center"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6 }}
            >
              <LegendaryCard 
                variant={isFounder ? 'founder' : 'elevated'}
                className="text-center max-w-md"
              >
                <div className="p-8">
                  {isFounder && <Crown className="w-16 h-16 text-yellow-600 mx-auto mb-4" />}
                  <MessageCircle className={cn(
                    'w-16 h-16 mx-auto mb-4',
                    isFounder ? 'text-yellow-600' : 'text-blue-600'
                  )} />
                  
                  <h3 className={cn(
                    'text-xl font-bold mb-2',
                    isFounder ? 'text-yellow-800' : 'text-gray-900'
                  )}>
                    {isFounder ? 'Welcome to Founder Chat!' : 'Welcome to Team Chat!'}
                  </h3>
                  
                  <p className={cn(
                    'text-sm mb-6',
                    isFounder ? 'text-yellow-600' : 'text-gray-600'
                  )}>
                    {isFounder 
                      ? '👑 Select a channel to start communicating with infinite founder energy!'
                      : '💬 Select a channel to start chatting with your legendary team!'
                    }
                  </p>
                  
                  <div className="flex items-center justify-center gap-2">
                    <Activity className="w-4 h-4 text-gray-400" />
                    <span className="text-xs text-gray-500">
                      🎸 Built with Swiss precision and infinite code bro energy! 🎸
                    </span>
                  </div>
                  
                  {isFounder && (
                    <motion.p 
                      className="text-xs text-yellow-700 mt-3 font-bold"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.6, delay: 1.0 }}
                    >
                      👑 RICKROLL187 FOUNDER CHAT • INFINITE COMMUNICATION AT 16:32:52 UTC! 👑
                    </motion.p>
                  )}
                </div>
              </LegendaryCard>
            </motion.div>
          )}
        </div>
      </div>
    </>
  );
};

console.log('🎸🎸🎸 LEGENDARY TEAM CHAT PAGE COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Team chat page completed at: 2025-08-06 16:32:52 UTC`);
console.log('💬 Chat system: SWISS PRECISION');
console.log('👑 RICKROLL187 founder chat: LEGENDARY');
console.log('🔌 Real-time communication: MAXIMUM CONNECTION');
console.log('🌅 AFTERNOON LEGENDARY CHAT ENERGY: INFINITE AT 16:32:52!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
