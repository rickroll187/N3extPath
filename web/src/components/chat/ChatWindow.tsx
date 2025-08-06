// File: web/src/components/chat/ChatWindow.tsx
/**
 * 💬🎸 N3EXTPATH - LEGENDARY CHAT WINDOW COMPONENT 🎸💬
 * Swiss precision chat interface with infinite code bro energy
 * Built: 2025-08-06 16:42:34 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect, useState, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Hash, 
  Crown, 
  Users, 
  Pin, 
  Star, 
  Settings, 
  Phone, 
  Video, 
  MoreVertical,
  Search,
  Info,
  Bell,
  BellOff,
  UserPlus,
  Archive,
  Trash2,
  Lock,
  Globe,
  Sparkles,
  Zap,
  Activity
} from 'lucide-react';
import { LegendaryCard } from '@/components/ui/LegendaryCard';
import { LegendaryButton } from '@/components/ui/LegendaryButton';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { UserList } from './UserList';
import { cn } from '@/utils/cn';
import toast from 'react-hot-toast';

// =====================================
// 💬 CHAT WINDOW TYPES 💬
// =====================================

interface ChatChannel {
  id: string;
  name: string;
  description?: string;
  type: 'public' | 'private' | 'direct' | 'founder';
  memberCount: number;
  unreadCount: number;
  lastMessage?: any;
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
  attachments?: any[];
  isFounderMessage?: boolean;
  isLegendary?: boolean;
  replyTo?: string;
}

interface ChatWindowProps {
  channel: ChatChannel;
  isFounder?: boolean;
  currentUser?: any;
}

// =====================================
// 🎸 LEGENDARY CHAT WINDOW 🎸
// =====================================

export const ChatWindow: React.FC<ChatWindowProps> = ({
  channel,
  isFounder = false,
  currentUser,
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showUserList, setShowUserList] = useState(false);
  const [isTyping, setIsTyping] = useState<string[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    console.log('💬🎸💬 LEGENDARY CHAT WINDOW LOADED! 💬🎸💬');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Chat window loaded at: 2025-08-06 16:42:34 UTC`);
    console.log('🌅 AFTERNOON LEGENDARY CHAT WINDOW ENERGY AT 16:42:34!');

    if (channel.isFounderChannel) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER CHAT WINDOW ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER CHAT WINDOW WITH INFINITE CODE BRO ENERGY!');
    }

    // Load messages for the channel
    loadChannelMessages();
  }, [channel.id, channel.isFounderChannel]);

  // Load messages
  const loadChannelMessages = useCallback(async () => {
    setIsLoading(true);
    
    try {
      // Generate mock messages based on channel type
      const mockMessages: ChatMessage[] = generateMockMessages();
      
      // Simulate loading delay
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setMessages(mockMessages);
      
      // Scroll to bottom
      setTimeout(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
      
    } catch (error) {
      console.error('🚨 Error loading messages:', error);
      toast.error('Failed to load messages');
    } finally {
      setIsLoading(false);
    }
  }, [channel]);

  // Generate mock messages
  const generateMockMessages = (): ChatMessage[] => {
    const baseMessages: ChatMessage[] = [
      {
        id: `${channel.id}-welcome`,
        content: channel.isFounderChannel 
          ? '👑 Welcome to the Founder HQ! This is where legendary decisions are made with infinite code bro energy! 🚀'
          : `🎸 Welcome to #${channel.name}! ${channel.description || 'Let\'s build something legendary together with Swiss precision!'}`,
        authorId: 'system',
        authorName: 'System',
        channelId: channel.id,
        timestamp: new Date('2025-08-06T16:30:00.000Z'),
        isFounderMessage: channel.isFounderChannel,
      },
    ];

    if (channel.id === 'general') {
      baseMessages.push(
        {
          id: 'general-1',
          content: 'Hey everyone! Just deployed the new feature with 100% Swiss precision! 🎯',
          authorId: 'codebro42',
          authorName: 'CodeBro42',
          authorAvatar: 'https://avatars.githubusercontent.com/codebro42.png',
          channelId: channel.id,
          timestamp: new Date('2025-08-06T16:35:15.000Z'),
          reactions: [
            { emoji: '🎯', count: 5, users: ['user1', 'user2', 'user3', 'user4', 'user5'] },
            { emoji: '🚀', count: 3, users: ['user6', 'user7', 'user8'] },
          ],
        },
        {
          id: 'general-2',
          content: 'That\'s some legendary work! The performance improvements are insane! ⚡',
          authorId: 'swissdev',
          authorName: 'SwissDev',
          authorAvatar: 'https://avatars.githubusercontent.com/swissdev.png',
          channelId: channel.id,
          timestamp: new Date('2025-08-06T16:37:22.000Z'),
        },
        {
          id: 'general-3',
          content: 'WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 😄🎸',
          authorId: 'jokemaster',
          authorName: 'JokeMaster',
          authorAvatar: 'https://avatars.githubusercontent.com/jokemaster.png',
          channelId: channel.id,
          timestamp: new Date('2025-08-06T16:40:45.000Z'),
          reactions: [
            { emoji: '😄', count: 8, users: ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7', 'user8'] },
            { emoji: '🎸', count: 6, users: ['user1', 'user3', 'user5', 'user7', 'user9', 'user10'] },
          ],
        }
      );
    }

    if (channel.id === 'code-bro-energy') {
      baseMessages.push(
        {
          id: 'energy-1',
          content: 'Just hit 9000+ code bro energy level! ⚡ Time to build something LEGENDARY!',
          authorId: 'energymaster',
          authorName: 'EnergyMaster',
          authorAvatar: 'https://avatars.githubusercontent.com/energymaster.png',
          channelId: channel.id,
          timestamp: new Date('2025-08-06T16:38:12.000Z'),
          isLegendary: true,
          reactions: [
            { emoji: '⚡', count: 12, users: Array.from({length: 12}, (_, i) => `user${i+1}`) },
            { emoji: '🚀', count: 8, users: Array.from({length: 8}, (_, i) => `user${i+1}`) },
          ],
        },
        {
          id: 'energy-2',
          content: 'That energy is INFINITE! Let\'s channel it into the new Swiss precision dashboard! 🎯',
          authorId: 'precisionmaster',
          authorName: 'PrecisionMaster',
          authorAvatar: 'https://avatars.githubusercontent.com/precisionmaster.png',
          channelId: channel.id,
          timestamp: new Date('2025-08-06T16:41:30.000Z'),
        }
      );
    }

    if (channel.isFounderChannel) {
      baseMessages.push(
        {
          id: 'founder-1',
          content: '👑 Platform analytics are looking LEGENDARY! User satisfaction at 98%, performance at 99.9%, and code bro energy is INFINITE! 🚀',
          authorId: 'rickroll187',
          authorName: 'RICKROLL187',
          authorAvatar: 'https://avatars.githubusercontent.com/rickroll187.png',
          channelId: channel.id,
          timestamp: new Date('2025-08-06T16:39:45.000Z'),
          isFounderMessage: true,
          reactions: [
            { emoji: '👑', count: 1, users: ['rickroll187'] },
            { emoji: '🚀', count: 1, users: ['rickroll187'] },
            { emoji: '⚡', count: 1, users: ['rickroll187'] },
          ],
        },
        {
          id: 'founder-2',
          content: 'Time to implement the next legendary features! Swiss precision meets infinite code bro energy! WE ARE CODE BROS THE CREATE THE BEST! 🎸',
          authorId: 'rickroll187',
          authorName: 'RICKROLL187',
          authorAvatar: 'https://avatars.githubusercontent.com/rickroll187.png',
          channelId: channel.id,
          timestamp: new Date('2025-08-06T16:42:15.000Z'),
          isFounderMessage: true,
        }
      );
    }

    return baseMessages.sort((a, b) => a.timestamp.getTime() - b.timestamp.getTime());
  };

  // Handle message send
  const handleSendMessage = useCallback(async (content: string, attachments?: any[]) => {
    if (!content.trim()) return;

    const newMessage: ChatMessage = {
      id: `msg-${Date.now()}`,
      content: content.trim(),
      authorId: currentUser?.id || 'current-user',
      authorName: currentUser?.displayName || currentUser?.username || 'You',
      authorAvatar: currentUser?.avatar,
      channelId: channel.id,
      timestamp: new Date(),
      attachments: attachments || [],
      isFounderMessage: isFounder,
      isLegendary: currentUser?.isLegendary || false,
    };

    // Add message to list
    setMessages(prev => [...prev, newMessage]);

    // Scroll to bottom
    setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, 100);

    // Simulate API call
    try {
      // Mock API delay
      await new Promise(resolve => setTimeout(resolve, 200));
      
      if (isFounder && channel.isFounderChannel) {
        toast.success('👑 Founder message sent with infinite power!', {
          duration: 2000,
          style: {
            background: 'linear-gradient(135deg, #FFD700, #FFA500)',
            color: '#000000',
            fontWeight: '700',
          },
        });
      }
      
    } catch (error) {
      console.error('🚨 Error sending message:', error);
      toast.error('Failed to send message');
      
      // Remove failed message
      setMessages(prev => prev.filter(msg => msg.id !== newMessage.id));
    }
  }, [channel.id, currentUser, isFounder, channel.isFounderChannel]);

  // Get channel icon
  const getChannelIcon = () => {
    if (channel.isFounderChannel) return Crown;
    if (channel.type === 'private') return Lock;
    if (channel.type === 'direct') return Users;
    return Hash;
  };

  const ChannelIcon = getChannelIcon();

  return (
    <div className="flex flex-col h-full bg-white dark:bg-gray-900">
      {/* Chat Header */}
      <motion.div
        className={cn(
          'flex items-center justify-between px-4 py-3 border-b border-gray-200 dark:border-gray-700',
          'bg-white dark:bg-gray-800',
          channel.isFounderChannel && 'bg-gradient-to-r from-yellow-50 via-orange-50 to-yellow-50 dark:from-yellow-900/20 dark:via-orange-900/20 dark:to-yellow-900/20'
        )}
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        {/* Left Section */}
        <div className="flex items-center gap-3">
          <div className={cn(
            'flex items-center gap-2 px-2 py-1 rounded-lg',
            channel.isFounderChannel 
              ? 'bg-yellow-100 dark:bg-yellow-900/30' 
              : 'bg-gray-100 dark:bg-gray-700'
          )}>
            <ChannelIcon className={cn(
              'w-4 h-4',
              channel.isFounderChannel ? 'text-yellow-600' : 'text-gray-600 dark:text-gray-300'
            )} />
            {channel.avatar && (
              <span className="text-sm">{channel.avatar}</span>
            )}
          </div>
          
          <div>
            <h2 className={cn(
              'font-semibold text-lg',
              channel.isFounderChannel 
                ? 'text-yellow-800 dark:text-yellow-300' 
                : 'text-gray-900 dark:text-white'
            )}>
              {channel.name}
              {channel.isFounderChannel && (
                <span className="ml-2 text-sm">👑</span>
              )}
              {channel.isLegendary && !channel.isFounderChannel && (
                <span className="ml-2 text-sm">🎸</span>
              )}
            </h2>
            
            {channel.description && (
              <p className={cn(
                'text-xs truncate max-w-md',
                channel.isFounderChannel 
                  ? 'text-yellow-600 dark:text-yellow-400' 
                  : 'text-gray-500 dark:text-gray-400'
              )}>
                {channel.description}
              </p>
            )}
          </div>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400">
            <Users className="w-3 h-3" />
            <span>{channel.memberCount}</span>
          </div>
          
          <div className="flex items-center gap-1">
            <LegendaryButton variant="ghost" size="sm">
              <Phone className="w-4 h-4" />
            </LegendaryButton>
            
            <LegendaryButton variant="ghost" size="sm">
              <Video className="w-4 h-4" />
            </LegendaryButton>
            
            <LegendaryButton 
              variant="ghost" 
              size="sm"
              onClick={() => setShowUserList(!showUserList)}
            >
              <Users className="w-4 h-4" />
            </LegendaryButton>
            
            <LegendaryButton variant="ghost" size="sm">
              <Search className="w-4 h-4" />
            </LegendaryButton>
            
            <LegendaryButton variant="ghost" size="sm">
              <MoreVertical className="w-4 h-4" />
            </LegendaryButton>
          </div>
        </div>
      </motion.div>

      {/* Chat Content Area */}
      <div className="flex flex-1 overflow-hidden">
        {/* Messages Area */}
        <div className="flex-1 flex flex-col">
          {/* Messages List */}
          <div className="flex-1 overflow-y-auto">
            <MessageList
              messages={messages}
              isLoading={isLoading}
              currentUserId={currentUser?.id}
              isFounderChannel={channel.isFounderChannel}
              onReaction={(messageId, emoji) => {
                // Handle reaction
                console.log('Reaction:', messageId, emoji);
                toast.success(`${emoji} reaction added!`);
              }}
              onReply={(messageId) => {
                // Handle reply
                console.log('Reply to:', messageId);
              }}
            />
            <div ref={messagesEndRef} />
          </div>

          {/* Typing Indicators */}
          <AnimatePresence>
            {isTyping.length > 0 && (
              <motion.div
                className="px-4 py-2 text-xs text-gray-500 dark:text-gray-400"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
              >
                <div className="flex items-center gap-2">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                  <span>
                    {isTyping.length === 1 
                      ? `${isTyping[0]} is typing...`
                      : `${isTyping.slice(0, -1).join(', ')} and ${isTyping[isTyping.length - 1]} are typing...`
                    }
                  </span>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Message Input */}
          <MessageInput
            channelId={channel.id}
            onSendMessage={handleSendMessage}
            isFounderChannel={channel.isFounderChannel}
            placeholder={
              channel.isFounderChannel 
                ? `👑 Send a founder message to #${channel.name}...`
                : `💬 Message #${channel.name}...`
            }
          />
        </div>

        {/* User List Sidebar */}
        <AnimatePresence>
          {showUserList && (
            <motion.div
              className="w-64 border-l border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.3 }}
            >
              <UserList
                users={[]} // Would be loaded based on channel
                isFounder={isFounder}
                title={`Members — ${channel.memberCount}`}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Bottom Status Bar */}
      <motion.div
        className={cn(
          'px-4 py-2 border-t border-gray-200 dark:border-gray-700 text-xs',
          'bg-gray-50 dark:bg-gray-800',
          channel.isFounderChannel && 'bg-yellow-50 dark:bg-yellow-900/20'
        )}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1 text-gray-500 dark:text-gray-400">
              <Activity className="w-3 h-3" />
              <span>Live chat active</span>
            </div>
            
            <div className={cn(
              'flex items-center gap-1',
              channel.isFounderChannel ? 'text-yellow-600' : 'text-gray-500'
            )}>
              <Zap className="w-3 h-3" />
              <span>
                {channel.isFounderChannel ? 'Infinite founder energy' : 'Code bro energy'}
              </span>
            </div>
          </div>
          
          <div className="text-gray-400 font-mono">
            2025-08-06 16:42:34 UTC
          </div>
        </div>
        
        {channel.isFounderChannel && (
          <div className="mt-1 text-center">
            <span className="text-yellow-700 dark:text-yellow-300 font-bold text-xs">
              👑 RICKROLL187 FOUNDER CHAT • INFINITE COMMUNICATION POWER! 👑
            </span>
          </div>
        )}
      </motion.div>
    </div>
  );
};

console.log('🎸🎸🎸 LEGENDARY CHAT WINDOW COMPONENT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Chat window component completed at: 2025-08-06 16:42:34 UTC`);
console.log('💬 Chat interface: SWISS PRECISION');
console.log('👑 RICKROLL187 founder chat: LEGENDARY');
console.log('🔌 Real-time messaging: MAXIMUM COMMUNICATION');
console.log('🌅 AFTERNOON LEGENDARY CHAT WINDOW ENERGY: INFINITE AT 16:42:34!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
