// File: web/src/components/chat/MessageInput.tsx
/**
 * ✍️🎸 N3EXTPATH - LEGENDARY MESSAGE INPUT COMPONENT 🎸✍️
 * Swiss precision message composition with infinite code bro energy
 * Built: 2025-08-06 16:57:32 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect, useState, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Send, 
  Crown, 
  Paperclip, 
  Smile, 
  Image, 
  File, 
  Mic, 
  Video,
  Plus,
  X,
  Sparkles,
  Zap,
  Hash,
  AtSign,
  Bold,
  Italic,
  Code,
  Link
} from 'lucide-react';
import { LegendaryButton } from '@/components/ui/LegendaryButton';
import { cn } from '@/utils/cn';
import toast from 'react-hot-toast';

// =====================================
// ✍️ MESSAGE INPUT TYPES ✍️
// =====================================

interface MessageInputProps {
  channelId: string;
  onSendMessage: (content: string, attachments?: any[]) => void;
  isFounderChannel?: boolean;
  placeholder?: string;
  disabled?: boolean;
  maxLength?: number;
}

interface Attachment {
  id: string;
  name: string;
  size: number;
  type: string;
  url: string;
  preview?: string;
}

// =====================================
// 🎸 LEGENDARY MESSAGE INPUT 🎸
// =====================================

export const MessageInput: React.FC<MessageInputProps> = ({
  channelId,
  onSendMessage,
  isFounderChannel = false,
  placeholder = "💬 Type your legendary message...",
  disabled = false,
  maxLength = 2000,
}) => {
  const [message, setMessage] = useState('');
  const [attachments, setAttachments] = useState<Attachment[]>([]);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [showFormatting, setShowFormatting] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [mentionSuggestions, setMentionSuggestions] = useState<string[]>([]);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    console.log('✍️🎸✍️ LEGENDARY MESSAGE INPUT LOADED! ✍️🎸✍️');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Message input loaded at: 2025-08-06 16:57:32 UTC`);
    console.log('🌅 AFTERNOON LEGENDARY MESSAGE INPUT ENERGY AT 16:57:32!');

    if (isFounderChannel) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER MESSAGE INPUT ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER MESSAGE INPUT WITH INFINITE CODE BRO ENERGY!');
    }

    // Focus on textarea
    if (textareaRef.current) {
      textareaRef.current.focus();
    }
  }, [isFounderChannel]);

  // Handle message change
  const handleMessageChange = useCallback((value: string) => {
    if (value.length > maxLength) return;
    
    setMessage(value);
    
    // Handle typing indicator
    if (!isTyping && value.trim()) {
      setIsTyping(true);
      // Simulate typing indicator
      setTimeout(() => setIsTyping(false), 3000);
    }

    // Handle mentions
    const mentionMatch = value.match(/@(\w*)$/);
    if (mentionMatch) {
      // Mock mention suggestions - in real app would fetch from API
      const suggestions = ['rickroll187', 'codebro42', 'swissdev', 'precisionmaster', 'jokemaster']
        .filter(user => user.toLowerCase().includes(mentionMatch[1].toLowerCase()));
      setMentionSuggestions(suggestions);
    } else {
      setMentionSuggestions([]);
    }
  }, [maxLength, isTyping]);

  // Handle key press
  const handleKeyPress = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  }, []);

  // Handle send message
  const handleSendMessage = useCallback(async () => {
    if (!message.trim() && attachments.length === 0) return;
    if (isSending || disabled) return;

    setIsSending(true);
    
    try {
      await onSendMessage(message.trim(), attachments);
      
      // Clear input
      setMessage('');
      setAttachments([]);
      setIsTyping(false);
      
      // Focus back to textarea
      if (textareaRef.current) {
        textareaRef.current.focus();
      }

      if (isFounderChannel) {
        // Don't show toast for founder messages as it's handled in parent
      } else {
        toast.success('🚀 Message sent with legendary energy!', { duration: 1500 });
      }
      
    } catch (error) {
      console.error('🚨 Error sending message:', error);
      toast.error('Failed to send message');
    } finally {
      setIsSending(false);
    }
  }, [message, attachments, isSending, disabled, onSendMessage, isFounderChannel]);

  // Handle file upload
  const handleFileUpload = useCallback((files: FileList) => {
    const maxFileSize = isFounderChannel ? 100 * 1024 * 1024 : 10 * 1024 * 1024; // 100MB for founder, 10MB for others
    const maxFiles = isFounderChannel ? 20 : 5;

    if (attachments.length + files.length > maxFiles) {
      toast.error(`Maximum ${maxFiles} files allowed`);
      return;
    }

    Array.from(files).forEach((file) => {
      if (file.size > maxFileSize) {
        toast.error(`File "${file.name}" is too large. Max size: ${isFounderChannel ? '100MB' : '10MB'}`);
        return;
      }

      const attachment: Attachment = {
        id: `attach-${Date.now()}-${Math.random()}`,
        name: file.name,
        size: file.size,
        type: file.type,
        url: URL.createObjectURL(file),
        preview: file.type.startsWith('image/') ? URL.createObjectURL(file) : undefined,
      };

      setAttachments(prev => [...prev, attachment]);
    });

    if (isFounderChannel) {
      toast.success('👑 Files added with founder privileges!', { duration: 2000 });
    }
  }, [attachments.length, isFounderChannel]);

  // Remove attachment
  const removeAttachment = useCallback((id: string) => {
    setAttachments(prev => prev.filter(a => a.id !== id));
  }, []);

  // Insert emoji
  const insertEmoji = useCallback((emoji: string) => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const newMessage = message.slice(0, start) + emoji + message.slice(end);
    
    setMessage(newMessage);
    setShowEmojiPicker(false);
    
    // Reset cursor position
    setTimeout(() => {
      textarea.focus();
      textarea.setSelectionRange(start + emoji.length, start + emoji.length);
    }, 0);
  }, [message]);

  // Format text
  const formatText = useCallback((format: 'bold' | 'italic' | 'code' | 'link') => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selectedText = message.slice(start, end);
    
    let formattedText = selectedText;
    let cursorOffset = 0;

    switch (format) {
      case 'bold':
        formattedText = `**${selectedText}**`;
        cursorOffset = selectedText ? 0 : 2;
        break;
      case 'italic':
        formattedText = `*${selectedText}*`;
        cursorOffset = selectedText ? 0 : 1;
        break;
      case 'code':
        formattedText = `\`${selectedText}\``;
        cursorOffset = selectedText ? 0 : 1;
        break;
      case 'link':
        formattedText = `[${selectedText || 'link text'}](url)`;
        cursorOffset = selectedText ? formattedText.length - 5 : 1;
        break;
    }

    const newMessage = message.slice(0, start) + formattedText + message.slice(end);
    setMessage(newMessage);
    
    // Reset cursor position
    setTimeout(() => {
      textarea.focus();
      const newPosition = selectedText ? end + formattedText.length - selectedText.length : start + formattedText.length - cursorOffset;
      textarea.setSelectionRange(newPosition, newPosition);
    }, 0);
  }, [message]);

  // Quick emoji sets
  const quickEmojis = isFounderChannel 
    ? ['👑', '🚀', '⚡', '🎸', '✨', '💎', '🔥', '💯', '🌟', '🎯']
    : ['😄', '👍', '❤️', '🚀', '⚡', '🎯', '💯', '🔥', '✨', '🎸'];

  return (
    <div className={cn(
      'border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800',
      isFounderChannel && 'bg-gradient-to-r from-yellow-50/30 via-orange-50/20 to-yellow-50/30 dark:from-yellow-900/10 dark:via-orange-900/10 dark:to-yellow-900/10'
    )}>
      {/* Attachments Preview */}
      <AnimatePresence>
        {attachments.length > 0 && (
          <motion.div
            className="px-4 py-2 border-b border-gray-200 dark:border-gray-700"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <div className="flex flex-wrap gap-2">
              {attachments.map((attachment) => (
                <motion.div
                  key={attachment.id}
                  className={cn(
                    'flex items-center gap-2 px-3 py-2 rounded-lg border',
                    'bg-gray-50 dark:bg-gray-700 border-gray-200 dark:border-gray-600',
                    isFounderChannel && 'bg-yellow-50 border-yellow-200 dark:bg-yellow-900/20 dark:border-yellow-700'
                  )}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  transition={{ duration: 0.2 }}
                >
                  {attachment.preview ? (
                    <img 
                      src={attachment.preview} 
                      alt={attachment.name}
                      className="w-8 h-8 rounded object-cover"
                    />
                  ) : (
                    <File className="w-4 h-4 text-gray-500" />
                  )}
                  
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">{attachment.name}</p>
                    <p className="text-xs text-gray-500">
                      {(attachment.size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                  
                  <button
                    onClick={() => removeAttachment(attachment.id)}
                    className="p-1 hover:bg-gray-200 dark:hover:bg-gray-600 rounded"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Input Area */}
      <div className="p-4">
        {/* Toolbar */}
        <div className="flex items-center gap-2 mb-3">
          {/* File Upload */}
          <div className="relative">
            <input
              ref={fileInputRef}
              type="file"
              multiple
              className="hidden"
              onChange={(e) => e.target.files && handleFileUpload(e.target.files)}
              accept={isFounderChannel ? "*/*" : "image/*,.pdf,.doc,.docx,.txt"}
            />
            
            <LegendaryButton
              variant="ghost"
              size="sm"
              onClick={() => fileInputRef.current?.click()}
              className="p-2"
              disabled={disabled}
            >
              <Paperclip className="w-4 h-4" />
            </LegendaryButton>
          </div>

          {/* Emoji Picker */}
          <div className="relative">
            <LegendaryButton
              variant="ghost"
              size="sm"
              onClick={() => setShowEmojiPicker(!showEmojiPicker)}
              className="p-2"
              disabled={disabled}
            >
              <Smile className="w-4 h-4" />
            </LegendaryButton>

            <AnimatePresence>
              {showEmojiPicker && (
                <motion.div
                  className="absolute bottom-full left-0 mb-2 p-3 bg-white dark:bg-gray-800 rounded-xl shadow-xl border border-gray-200 dark:border-gray-700 z-50"
                  initial={{ opacity: 0, scale: 0.9, y: 10 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.9, y: 10 }}
                  transition={{ duration: 0.2 }}
                >
                  <div className="grid grid-cols-5 gap-2 w-48">
                    {quickEmojis.map((emoji) => (
                      <button
                        key={emoji}
                        onClick={() => insertEmoji(emoji)}
                        className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded text-lg"
                      >
                        {emoji}
                      </button>
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Formatting */}
          <div className="relative">
            <LegendaryButton
              variant="ghost"
              size="sm"
              onClick={() => setShowFormatting(!showFormatting)}
              className="p-2"
              disabled={disabled}
            >
              <Bold className="w-4 h-4" />
            </LegendaryButton>

            <AnimatePresence>
              {showFormatting && (
                <motion.div
                  className="absolute bottom-full left-0 mb-2 p-2 bg-white dark:bg-gray-800 rounded-xl shadow-xl border border-gray-200 dark:border-gray-700 z-50"
                  initial={{ opacity: 0, scale: 0.9, y: 10 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.9, y: 10 }}
                  transition={{ duration: 0.2 }}
                >
                  <div className="flex gap-1">
                    <LegendaryButton
                      variant="ghost"
                      size="sm"
                      onClick={() => formatText('bold')}
                      className="p-2"
                    >
                      <Bold className="w-3 h-3" />
                    </LegendaryButton>
                    
                    <LegendaryButton
                      variant="ghost"
                      size="sm"
                      onClick={() => formatText('italic')}
                      className="p-2"
                    >
                      <Italic className="w-3 h-3" />
                    </LegendaryButton>
                    
                    <LegendaryButton
                      variant="ghost"
                      size="sm"
                      onClick={() => formatText('code')}
                      className="p-2"
                    >
                      <Code className="w-3 h-3" />
                    </LegendaryButton>
                    
                    <LegendaryButton
                      variant="ghost"
                      size="sm"
                      onClick={() => formatText('link')}
                      className="p-2"
                    >
                      <Link className="w-3 h-3" />
                    </LegendaryButton>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Spacer */}
          <div className="flex-1" />

          {/* Character Count */}
          <div className={cn(
            'text-xs',
            message.length > maxLength * 0.8 
              ? 'text-red-500' 
              : isFounderChannel 
                ? 'text-yellow-600' 
                : 'text-gray-500'
          )}>
            {message.length}/{maxLength}
          </div>
        </div>

        {/* Text Input */}
        <div className="flex items-end gap-3">
          <div className="flex-1 relative">
            <textarea
              ref={textareaRef}
              value={message}
              onChange={(e) => handleMessageChange(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={placeholder}
              disabled={disabled || isSending}
              className={cn(
                'w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-600',
                'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                'placeholder-gray-500 dark:placeholder-gray-400',
                'focus:outline-none focus:ring-2 focus:ring-offset-2',
                'resize-none min-h-[44px] max-h-32',
                isFounderChannel 
                  ? 'focus:ring-yellow-500 border-yellow-200 dark:border-yellow-700' 
                  : 'focus:ring-blue-500',
                disabled && 'opacity-50 cursor-not-allowed'
              )}
              rows={1}
              style={{ height: 'auto' }}
              onInput={(e) => {
                const target = e.target as HTMLTextAreaElement;
                target.style.height = 'auto';
                target.style.height = `${Math.min(target.scrollHeight, 128)}px`;
              }}
            />

            {/* Mention Suggestions */}
            <AnimatePresence>
              {mentionSuggestions.length > 0 && (
                <motion.div
                  className="absolute bottom-full left-0 mb-2 py-2 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 z-50"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                  transition={{ duration: 0.2 }}
                >
                  {mentionSuggestions.map((user) => (
                    <button
                      key={user}
                      onClick={() => {
                        const newMessage = message.replace(/@\w*$/, `@${user} `);
                        setMessage(newMessage);
                        setMentionSuggestions([]);
                        textareaRef.current?.focus();
                      }}
                      className="flex items-center gap-2 px-3 py-2 w-full hover:bg-gray-100 dark:hover:bg-gray-700 text-left"
                    >
                      <AtSign className="w-3 h-3 text-gray-500" />
                      <span className="font-medium">{user}</span>
                      {user === 'rickroll187' && (
                        <Crown className="w-3 h-3 text-yellow-600" />
                      )}
                    </button>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Send Button */}
          <LegendaryButton
            variant={isFounderChannel ? "founder" : "primary"}
            onClick={handleSendMessage}
            disabled={(!message.trim() && attachments.length === 0) || isSending || disabled}
            className={cn(
              'px-4 py-3 rounded-xl',
              isSending && 'animate-pulse'
            )}
          >
            {isSending ? (
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                <span className="text-sm">Sending...</span>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                {isFounderChannel && <Crown className="w-4 h-4" />}
                <Send className="w-4 h-4" />
                <span className="hidden sm:inline text-sm">
                  {isFounderChannel ? 'Send with Power' : 'Send'}
                </span>
              </div>
            )}
          </LegendaryButton>
        </div>

        {/* Helper Text */}
        <div className="flex items-center justify-between mt-2 text-xs text-gray-500 dark:text-gray-400">
          <div className="flex items-center gap-4">
            <span>**bold** *italic* `code` @mention</span>
            {isFounderChannel && (
              <div className="flex items-center gap-1 text-yellow-600 dark:text-yellow-400">
                <Crown className="w-3 h-3" />
                <span className="font-medium">Founder privileges active</span>
              </div>
            )}
          </div>
          
          <div className="flex items-center gap-1">
            <Zap className="w-3 h-3" />
            <span>Press Enter to send</span>
          </div>
        </div>
      </div>
    </div>
  );
};

console.log('🎸🎸🎸 LEGENDARY MESSAGE INPUT COMPONENT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Message input component completed at: 2025-08-06 16:57:32 UTC`);
console.log('✍️ Message composition: SWISS PRECISION');
console.log('👑 RICKROLL187 founder input: LEGENDARY');
console.log('⚡ Rich formatting & attachments: MAXIMUM FEATURES');
console.log('🌅 AFTERNOON LEGENDARY MESSAGE INPUT ENERGY: INFINITE AT 16:57:32!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
