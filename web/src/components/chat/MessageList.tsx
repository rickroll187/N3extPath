// File: web/src/components/chat/MessageList.tsx
/**
 * 📝🎸 N3EXTPATH - LEGENDARY MESSAGE LIST COMPONENT 🎸📝
 * Swiss precision message rendering with infinite code bro energy
 * Built: 2025-08-06 16:46:01 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect, useState, useMemo, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Crown, 
  Heart, 
  ThumbsUp, 
  Laugh, 
  Zap, 
  Star, 
  Fire,
  Reply,
  MoreHorizontal,
  Edit,
  Trash2,
  Pin,
  Copy,
  Flag,
  Sparkles,
  Activity,
  Clock
} from 'lucide-react';
import { LegendaryButton } from '@/components/ui/LegendaryButton';
import { cn } from '@/utils/cn';
import toast from 'react-hot-toast';

// =====================================
// 📝 MESSAGE TYPES 📝
// =====================================

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

interface MessageListProps {
  messages: ChatMessage[];
  isLoading?: boolean;
  currentUserId?: string;
  isFounderChannel?: boolean;
  onReaction?: (messageId: string, emoji: string) => void;
  onReply?: (messageId: string) => void;
  onEdit?: (messageId: string) => void;
  onDelete?: (messageId: string) => void;
}

// =====================================
// 🎸 MESSAGE ITEM COMPONENT 🎸
// =====================================

const MessageItem: React.FC<{
  message: ChatMessage;
  isOwn: boolean;
  isFounderChannel: boolean;
  onReaction: (emoji: string) => void;
  onReply: () => void;
  onEdit: () => void;
  onDelete: () => void;
}> = ({ message, isOwn, isFounderChannel, onReaction, onReply, onEdit, onDelete }) => {
  const [showActions, setShowActions] = useState(false);
  const [showReactions, setShowReactions] = useState(false);

  // Quick reaction emojis
  const quickReactions = message.isFounderMessage || isFounderChannel
    ? ['👑', '🚀', '⚡', '🎸', '✨', '💎']
    : ['👍', '❤️', '😄', '⚡', '🎯', '🚀'];

  // Format timestamp
  const formatTime = (date: Date) => {
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return 'now';
  };

  // Parse mentions and format content
  const formatMessageContent = (content: string) => {
    // Simple mention highlighting - would be more sophisticated in production
    return content.replace(/@(\w+)/g, '<span class="text-blue-600 font-semibold bg-blue-100 px-1 rounded">@$1</span>');
  };

  return (
    <motion.div
      className={cn(
        'group px-4 py-2 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors',
        message.isFounderMessage && 'bg-gradient-to-r from-yellow-50/50 via-orange-50/30 to-yellow-50/50 dark:from-yellow-900/10 dark:via-orange-900/10 dark:to-yellow-900/10'
      )}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
    >
      <div className="flex items-start gap-3">
        {/* Avatar */}
        <div className="flex-shrink-0">
          <div className={cn(
            'w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold',
            message.isFounderMessage 
              ? 'bg-gradient-to-r from-yellow-400 to-orange-500 text-white'
              : message.isLegendary
              ? 'bg-gradient-to-r from-purple-500 to-blue-600 text-white'
              : 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
          )}>
            {message.authorAvatar ? (
              <img 
                src={message.authorAvatar} 
                alt={message.authorName}
                className="w-full h-full rounded-full object-cover"
              />
            ) : (
              <span>{message.authorName.charAt(0).toUpperCase()}</span>
            )}
          </div>
        </div>

        {/* Message Content */}
        <div className="flex-1 min-w-0">
          {/* Author and Timestamp */}
          <div className="flex items-center gap-2 mb-1">
            <span className={cn(
              'font-semibold text-sm',
              message.isFounderMessage 
                ? 'text-yellow-800 dark:text-yellow-300'
                : message.isLegendary
                ? 'text-purple-800 dark:text-purple-300'
                : 'text-gray-900 dark:text-white'
            )}>
              {message.authorName}
              {message.isFounderMessage && (
                <Crown className="inline w-3 h-3 ml-1 text-yellow-600" />
              )}
              {message.isLegendary && !message.isFounderMessage && (
                <Sparkles className="inline w-3 h-3 ml-1 text-purple-600" />
              )}
            </span>
            
            <span className="text-xs text-gray-500 dark:text-gray-400">
              {formatTime(message.timestamp)}
              {message.edited && (
                <span className="ml-1 text-xs text-gray-400">(edited)</span>
              )}
            </span>
          </div>

          {/* Message Text */}
          <div className={cn(
            'text-sm leading-relaxed',
            message.isFounderMessage 
              ? 'text-yellow-900 dark:text-yellow-100'
              : 'text-gray-900 dark:text-gray-100'
          )}>
            <div 
              dangerouslySetInnerHTML={{ 
                __html: formatMessageContent(message.content) 
              }}
            />
          </div>

          {/* Attachments */}
          {message.attachments && message.attachments.length > 0 && (
            <div className="mt-2 space-y-2">
              {message.attachments.map((attachment) => (
                <div
                  key={attachment.id}
                  className="flex items-center gap-2 p-2 bg-gray-100 dark:bg-gray-700 rounded-lg"
                >
                  <div className="text-xs text-gray-600 dark:text-gray-400">
                    📎 {attachment.name}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Reactions */}
          {message.reactions && message.reactions.length > 0 && (
            <div className="flex flex-wrap gap-1 mt-2">
              {message.reactions.map((reaction, index) => (
                <motion.button
                  key={index}
                  onClick={() => onReaction(reaction.emoji)}
                  className={cn(
                    'inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs',
                    'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600',
                    'transition-colors cursor-pointer'
                  )}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <span>{reaction.emoji}</span>
                  <span className="text-gray-600 dark:text-gray-300">
                    {reaction.count}
                  </span>
                </motion.button>
              ))}
            </div>
          )}
        </div>

        {/* Message Actions */}
        <AnimatePresence>
          {showActions && (
            <motion.div
              className="flex items-center gap-1"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ duration: 0.2 }}
            >
              {/* Quick Reactions */}
              <div className="relative">
                <LegendaryButton
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowReactions(!showReactions)}
                  className="text-xs p-1"
                >
                  ⚡
                </LegendaryButton>
                
                <AnimatePresence>
                  {showReactions && (
                    <motion.div
                      className="absolute bottom-full right-0 mb-2 p-2 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700"
                      initial={{ opacity: 0, scale: 0.9, y: 10 }}
                      animate={{ opacity: 1, scale: 1, y: 0 }}
                      exit={{ opacity: 0, scale: 0.9, y: 10 }}
                      transition={{ duration: 0.2 }}
                    >
                      <div className="flex gap-1">
                        {quickReactions.map((emoji) => (
                          <button
                            key={emoji}
                            onClick={() => {
                              onReaction(emoji);
                              setShowReactions(false);
                            }}
                            className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded text-lg"
                          >
                            {emoji}
                          </button>
                        ))}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              <LegendaryButton
                variant="ghost"
                size="sm"
                onClick={onReply}
                className="text-xs p-1"
              >
                <Reply className="w-3 h-3" />
              </LegendaryButton>

              {isOwn && (
                <>
                  <LegendaryButton
                    variant="ghost"
                    size="sm"
                    onClick={onEdit}
                    className="text-xs p-1"
                  >
                    <Edit className="w-3 h-3" />
                  </LegendaryButton>
                  
                  <LegendaryButton
                    variant="ghost"
                    size="sm"
                    onClick={onDelete}
                    className="text-xs p-1 text-red-500 hover:text-red-700"
                  >
                    <Trash2 className="w-3 h-3" />
                  </LegendaryButton>
                </>
              )}

              <LegendaryButton
                variant="ghost"
                size="sm"
                onClick={() => {
                  navigator.clipboard.writeText(message.content);
                  toast.success('Message copied!');
                }}
                className="text-xs p-1"
              >
                <Copy className="w-3 h-3" />
              </LegendaryButton>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
};

// =====================================
// 🎸 LEGENDARY MESSAGE LIST 🎸
// =====================================

export const MessageList: React.FC<MessageListProps> = ({
  messages,
  isLoading = false,
  currentUserId,
  isFounderChannel = false,
  onReaction,
  onReply,
  onEdit,
  onDelete,
}) => {
  const [visibleMessages, setVisibleMessages] = useState<ChatMessage[]>([]);

  useEffect(() => {
    console.log('📝🎸📝 LEGENDARY MESSAGE LIST LOADED! 📝🎸📝');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Message list loaded at: 2025-08-06 16:46:01 UTC`);
    console.log('🌅 AFTERNOON LEGENDARY MESSAGE LIST ENERGY AT 16:46:01!');

    if (isFounderChannel) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER MESSAGE LIST ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER MESSAGE LIST WITH INFINITE CODE BRO ENERGY!');
    }
  }, [isFounderChannel]);

  // Group messages by date
  const groupedMessages = useMemo(() => {
    const groups: Array<{
      date: string;
      messages: ChatMessage[];
    }> = [];

    let currentDate = '';
    let currentMessages: ChatMessage[] = [];

    messages.forEach((message) => {
      const messageDate = message.timestamp.toDateString();
      
      if (messageDate !== currentDate) {
        if (currentMessages.length > 0) {
          groups.push({
            date: currentDate,
            messages: [...currentMessages],
          });
        }
        currentDate = messageDate;
        currentMessages = [message];
      } else {
        currentMessages.push(message);
      }
    });

    if (currentMessages.length > 0) {
      groups.push({
        date: currentDate,
        messages: currentMessages,
      });
    }

    return groups;
  }, [messages]);

  // Handle reactions
  const handleReaction = useCallback((messageId: string, emoji: string) => {
    if (onReaction) {
      onReaction(messageId, emoji);
    }
    
    // Show different toasts for different message types
    if (messages.find(m => m.id === messageId)?.isFounderMessage) {
      toast.success(`👑 ${emoji} reaction added to founder message!`, {
        duration: 2000,
        style: {
          background: 'linear-gradient(135deg, #FFD700, #FFA500)',
          color: '#000000',
          fontWeight: '600',
        },
      });
    } else {
      toast.success(`${emoji} Great energy, code bro!`, { duration: 1500 });
    }
  }, [messages, onReaction]);

  // Loading state
  if (isLoading) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <motion.div
          className="flex flex-col items-center gap-4"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6 }}
        >
          <div className="flex gap-2">
            {[0, 1, 2].map((i) => (
              <motion.div
                key={i}
                className={cn(
                  'w-3 h-3 rounded-full',
                  isFounderChannel ? 'bg-yellow-500' : 'bg-blue-500'
                )}
                animate={{
                  scale: [1, 1.2, 1],
                  opacity: [0.7, 1, 0.7],
                }}
                transition={{
                  duration: 1.5,
                  repeat: Infinity,
                  delay: i * 0.2,
                }}
              />
            ))}
          </div>
          <p className={cn(
            'text-sm font-medium',
            isFounderChannel ? 'text-yellow-700' : 'text-gray-700'
          )}>
            {isFounderChannel 
              ? 'Loading founder messages with infinite energy...'
              : 'Loading legendary messages...'
            }
          </p>
        </motion.div>
      </div>
    );
  }

  // Empty state
  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center p-8">
        <motion.div
          className="text-center max-w-md"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className={cn(
            'w-16 h-16 rounded-full mx-auto mb-4 flex items-center justify-center',
            isFounderChannel 
              ? 'bg-gradient-to-r from-yellow-100 to-orange-100'
              : 'bg-gradient-to-r from-blue-100 to-purple-100'
          )}>
            {isFounderChannel ? (
              <Crown className="w-8 h-8 text-yellow-600" />
            ) : (
              <Activity className="w-8 h-8 text-blue-600" />
            )}
          </div>
          
          <h3 className={cn(
            'text-lg font-semibold mb-2',
            isFounderChannel ? 'text-yellow-800' : 'text-gray-900'
          )}>
            {isFounderChannel ? 'Founder HQ Ready!' : 'Start the Conversation!'}
          </h3>
          
          <p className={cn(
            'text-sm',
            isFounderChannel ? 'text-yellow-600' : 'text-gray-600'
          )}>
            {isFounderChannel 
              ? '👑 Be the first to send a legendary founder message with infinite energy!'
              : '🎸 Send the first message and spark some legendary code bro energy!'
            }
          </p>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto">
      <div className="py-4">
        {groupedMessages.map((group, groupIndex) => (
          <div key={group.date}>
            {/* Date Separator */}
            {group.date && (
              <div className="flex items-center justify-center my-4">
                <div className={cn(
                  'px-3 py-1 rounded-full text-xs font-medium',
                  isFounderChannel
                    ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300'
                    : 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
                )}>
                  {group.date === new Date().toDateString() ? 'Today' : group.date}
                </div>
              </div>
            )}

            {/* Messages */}
            {group.messages.map((message, messageIndex) => (
              <MessageItem
                key={message.id}
                message={message}
                isOwn={message.authorId === currentUserId}
                isFounderChannel={isFounderChannel}
                onReaction={(emoji) => handleReaction(message.id, emoji)}
                onReply={() => onReply?.(message.id)}
                onEdit={() => onEdit?.(message.id)}
                onDelete={() => onDelete?.(message.id)}
              />
            ))}
          </div>
        ))}

        {/* Bottom Spacer */}
        <div className="h-4" />
      </div>
    </div>
  );
};

console.log('🎸🎸🎸 LEGENDARY MESSAGE LIST COMPONENT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Message list component completed at: 2025-08-06 16:46:01 UTC`);
console.log('📝 Message rendering: SWISS PRECISION');
console.log('👑 RICKROLL187 founder messages: LEGENDARY');
console.log('⚡ Reactions & interactions: MAXIMUM ENERGY');
console.log('🌅 AFTERNOON LEGENDARY MESSAGE LIST ENERGY: INFINITE AT 16:46:01!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
