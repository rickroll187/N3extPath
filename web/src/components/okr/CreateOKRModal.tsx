// File: web/src/components/okr/CreateOKRModal.tsx
/**
 * 📋🎸 N3EXTPATH - LEGENDARY CREATE OKR MODAL COMPONENT 🎸📋
 * Swiss precision OKR creation with infinite code bro energy
 * Built: 2025-08-06 17:20:47 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect, useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Crown, 
  Target, 
  X, 
  Plus,
  Minus,
  Calendar,
  Users,
  User,
  Building,
  Tag,
  Star,
  Sparkles,
  Zap,
  Trophy,
  CheckCircle,
  AlertCircle,
  Info,
  Save,
  ArrowRight,
  ArrowLeft,
  Upload,
  Link,
  Hash,
  Percent,
  ToggleLeft,
  ToggleRight,
  Clock,
  Globe,
  Lock
} from 'lucide-react';
import { LegendaryButton } from '@/components/ui/LegendaryButton';
import { LegendaryCard } from '@/components/ui/LegendaryCard';
import { Modal } from '@/components/ui/Modal';
import { ProgressBar } from '@/components/ui/ProgressBar';
import { cn } from '@/utils/cn';
import toast from 'react-hot-toast';

// =====================================
// 📋 CREATE OKR TYPES 📋
// =====================================

interface KeyResultForm {
  id: string;
  title: string;
  description: string;
  type: 'numeric' | 'percentage' | 'boolean' | 'milestone';
  startValue: number;
  targetValue: number;
  unit: string;
  dueDate: string;
}

interface OKRForm {
  title: string;
  description: string;
  teamId: string;
  startDate: string;
  endDate: string;
  quarter: string;
  year: number;
  isLegendary: boolean;
  founderPriority: boolean;
  isPublic: boolean;
  tags: string[];
  keyResults: KeyResultForm[];
}

interface CreateOKRModalProps {
  isOpen: boolean;
  onClose: () => void;
  isFounder?: boolean;
  onCreated: (okr: any) => void;
}

// =====================================
// 🎸 KEY RESULT FORM COMPONENT 🎸
// =====================================

const KeyResultForm: React.FC<{
  keyResult: KeyResultForm;
  onChange: (keyResult: KeyResultForm) => void;
  onRemove: () => void;
  isFounder: boolean;
}> = ({ keyResult, onChange, onRemove, isFounder }) => {
  const [expanded, setExpanded] = useState(false);

  const handleChange = (field: keyof KeyResultForm, value: any) => {
    onChange({ ...keyResult, [field]: value });
  };

  const typeOptions = [
    { value: 'numeric', label: 'Numeric', icon: Hash, description: 'Count or amount (e.g., 5 features)' },
    { value: 'percentage', label: 'Percentage', icon: Percent, description: 'Percentage target (e.g., 95% uptime)' },
    { value: 'boolean', label: 'Boolean', icon: CheckCircle, description: 'Yes/No completion (e.g., Launch product)' },
    { value: 'milestone', label: 'Milestone', icon: Target, description: 'Project milestone completion' },
  ];

  const selectedType = typeOptions.find(t => t.value === keyResult.type) || typeOptions[0];
  const TypeIcon = selectedType.icon;

  return (
    <motion.div
      className={cn(
        'border rounded-lg p-4 space-y-4',
        isFounder 
          ? 'border-yellow-200 bg-yellow-50/30 dark:border-yellow-700 dark:bg-yellow-900/10'
          : 'border-gray-200 bg-gray-50/30 dark:border-gray-700 dark:bg-gray-800/30'
      )}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <TypeIcon className={cn(
            'w-4 h-4',
            isFounder ? 'text-yellow-600' : 'text-blue-600'
          )} />
          <span className={cn(
            'font-medium text-sm',
            isFounder ? 'text-yellow-800 dark:text-yellow-300' : 'text-gray-800 dark:text-gray-300'
          )}>
            Key Result
          </span>
        </div>

        <div className="flex items-center gap-2">
          <LegendaryButton
            variant="ghost"
            size="sm"
            onClick={() => setExpanded(!expanded)}
            className="text-xs"
          >
            {expanded ? 'Collapse' : 'Expand'}
          </LegendaryButton>
          
          <LegendaryButton
            variant="ghost"
            size="sm"
            onClick={onRemove}
            className="text-xs text-red-600 hover:text-red-700"
          >
            <X className="w-3 h-3" />
          </LegendaryButton>
        </div>
      </div>

      {/* Title */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Title *
        </label>
        <input
          type="text"
          value={keyResult.title}
          onChange={(e) => handleChange('title', e.target.value)}
          placeholder={isFounder ? "Legendary key result title..." : "Key result title..."}
          className={cn(
            'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg',
            'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
            'focus:outline-none focus:ring-2 focus:ring-offset-2',
            isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
          )}
          required
        />
      </div>

      {/* Expanded Fields */}
      <AnimatePresence>
        {expanded && (
          <motion.div
            className="space-y-4"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            {/* Description */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Description
              </label>
              <textarea
                value={keyResult.description}
                onChange={(e) => handleChange('description', e.target.value)}
                placeholder={isFounder ? "Describe this legendary key result..." : "Describe this key result..."}
                rows={2}
                className={cn(
                  'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg resize-none',
                  'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                  'focus:outline-none focus:ring-2 focus:ring-offset-2',
                  isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
                )}
              />
            </div>

            {/* Type Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Type *
              </label>
              <div className="grid grid-cols-2 gap-2">
                {typeOptions.map((type) => {
                  const IconComponent = type.icon;
                  return (
                    <button
                      key={type.value}
                      type="button"
                      onClick={() => handleChange('type', type.value)}
                      className={cn(
                        'p-3 rounded-lg border text-left transition-colors',
                        keyResult.type === type.value
                          ? isFounder
                            ? 'border-yellow-500 bg-yellow-50 text-yellow-900 dark:border-yellow-400 dark:bg-yellow-900/30 dark:text-yellow-100'
                            : 'border-blue-500 bg-blue-50 text-blue-900 dark:border-blue-400 dark:bg-blue-900/30 dark:text-blue-100'
                          : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
                      )}
                    >
                      <div className="flex items-center gap-2 mb-1">
                        <IconComponent className="w-4 h-4" />
                        <span className="font-medium text-sm">{type.label}</span>
                      </div>
                      <p className="text-xs text-gray-600 dark:text-gray-400">
                        {type.description}
                      </p>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Values */}
            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Start Value
                </label>
                <input
                  type="number"
                  value={keyResult.startValue}
                  onChange={(e) => handleChange('startValue', parseFloat(e.target.value) || 0)}
                  className={cn(
                    'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg',
                    'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                    'focus:outline-none focus:ring-2 focus:ring-offset-2',
                    isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
                  )}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Target Value *
                </label>
                <input
                  type="number"
                  value={keyResult.targetValue}
                  onChange={(e) => handleChange('targetValue', parseFloat(e.target.value) || 0)}
                  className={cn(
                    'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg',
                    'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                    'focus:outline-none focus:ring-2 focus:ring-offset-2',
                    isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
                  )}
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Unit
                </label>
                <input
                  type="text"
                  value={keyResult.unit}
                  onChange={(e) => handleChange('unit', e.target.value)}
                  placeholder="e.g., %, users, features"
                  className={cn(
                    'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg',
                    'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                    'focus:outline-none focus:ring-2 focus:ring-offset-2',
                    isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
                  )}
                />
              </div>
            </div>

            {/* Due Date */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Due Date
              </label>
              <input
                type="date"
                value={keyResult.dueDate}
                onChange={(e) => handleChange('dueDate', e.target.value)}
                className={cn(
                  'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg',
                  'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                  'focus:outline-none focus:ring-2 focus:ring-offset-2',
                  isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
                )}
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

// =====================================
// 🎸 LEGENDARY CREATE OKR MODAL 🎸
// =====================================

export const CreateOKRModal: React.FC<CreateOKRModalProps> = ({
  isOpen,
  onClose,
  isFounder = false,
  onCreated,
}) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [tagInput, setTagInput] = useState('');

  // Form state
  const [formData, setFormData] = useState<OKRForm>({
    title: '',
    description: '',
    teamId: '',
    startDate: new Date().toISOString().split('T')[0],
    endDate: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000).toISOString().split('T')[0], // 90 days from now
    quarter: 'Q3 2025',
    year: 2025,
    isLegendary: isFounder,
    founderPriority: isFounder,
    isPublic: true,
    tags: [],
    keyResults: [],
  });

  useEffect(() => {
    console.log('📋🎸📋 LEGENDARY CREATE OKR MODAL LOADED! 📋🎸📋');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Create OKR modal loaded at: 2025-08-06 17:20:47 UTC`);
    console.log('🌅 LATE AFTERNOON LEGENDARY CREATE OKR ENERGY AT 17:20:47!');

    if (isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER CREATE OKR MODAL ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER OKR CREATION WITH INFINITE CODE BRO ENERGY!');
    }

    // Reset form when modal opens
    if (isOpen) {
      setCurrentStep(0);
      setFormData(prev => ({
        ...prev,
        title: '',
        description: '',
        teamId: '',
        tags: [],
        keyResults: [],
        isLegendary: isFounder,
        founderPriority: isFounder,
      }));
    }
  }, [isOpen, isFounder]);

  const steps = [
    { 
      title: isFounder ? 'Founder OKR Details' : 'OKR Details', 
      icon: Target,
      description: isFounder ? 'Define your legendary founder objective' : 'Define your objective and basic details'
    },
    { 
      title: 'Key Results', 
      icon: CheckCircle,
      description: 'Add measurable key results to track progress'
    },
    { 
      title: 'Settings & Review', 
      icon: Star,
      description: 'Configure settings and review your OKR'
    },
  ];

  // Team options (mock data)
  const teamOptions = [
    { value: 'legendary-founders', label: 'Legendary Founders', icon: Crown },
    { value: 'code-bro-squad', label: 'Code Bro Squad', icon: Sparkles },
    { value: 'swiss-precision', label: 'Swiss Precision Team', icon: Target },
    { value: 'individual', label: 'Individual OKR', icon: User },
  ];

  // Handle form change
  const handleFormChange = (field: keyof OKRForm, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  // Handle tag addition
  const handleAddTag = useCallback(() => {
    if (tagInput.trim() && !formData.tags.includes(tagInput.trim().toLowerCase())) {
      handleFormChange('tags', [...formData.tags, tagInput.trim().toLowerCase()]);
      setTagInput('');
    }
  }, [tagInput, formData.tags]);

  // Handle tag removal
  const handleRemoveTag = (tagToRemove: string) => {
    handleFormChange('tags', formData.tags.filter(tag => tag !== tagToRemove));
  };

  // Add key result
  const handleAddKeyResult = () => {
    const newKeyResult: KeyResultForm = {
      id: `kr-${Date.now()}`,
      title: '',
      description: '',
      type: 'percentage',
      startValue: 0,
      targetValue: 100,
      unit: '%',
      dueDate: formData.endDate,
    };
    
    handleFormChange('keyResults', [...formData.keyResults, newKeyResult]);
  };

  // Update key result
  const handleUpdateKeyResult = (index: number, keyResult: KeyResultForm) => {
    const updatedKeyResults = [...formData.keyResults];
    updatedKeyResults[index] = keyResult;
    handleFormChange('keyResults', updatedKeyResults);
  };

  // Remove key result
  const handleRemoveKeyResult = (index: number) => {
    handleFormChange('keyResults', formData.keyResults.filter((_, i) => i !== index));
  };

  // Validation
  const validateStep = (step: number): boolean => {
    switch (step) {
      case 0:
        return formData.title.trim() !== '' && formData.description.trim() !== '';
      case 1:
        return formData.keyResults.length > 0 && formData.keyResults.every(kr => kr.title.trim() !== '');
      case 2:
        return true; // Settings step is always valid
      default:
        return false;
    }
  };

  // Handle next step
  const handleNextStep = () => {
    if (validateStep(currentStep)) {
      setCurrentStep(prev => Math.min(prev + 1, steps.length - 1));
    } else {
      toast.error('Please fill in all required fields');
    }
  };

  // Handle previous step
  const handlePrevStep = () => {
    setCurrentStep(prev => Math.max(prev - 1, 0));
  };

  // Handle submit
  const handleSubmit = async () => {
    if (!validateStep(0) || !validateStep(1)) {
      toast.error('Please complete all required fields');
      return;
    }

    setIsLoading(true);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));

      // Create mock OKR
      const newOKR = {
        id: `okr-${Date.now()}`,
        ...formData,
        ownerId: 'rickroll187',
        ownerName: isFounder ? 'RICKROLL187' : 'Current User',
        ownerAvatar: 'https://avatars.githubusercontent.com/rickroll187.png',
        progress: 0,
        status: 'active' as const,
        confidence: 80,
        legendaryLevel: isFounder ? 10 : 5,
        keyResults: formData.keyResults.map(kr => ({
          ...kr,
          okrId: `okr-${Date.now()}`,
          currentValue: kr.startValue,
          progress: 0,
          status: 'not_started' as const,
          confidence: 70,
        })),
        createdAt: new Date(),
        updatedAt: new Date(),
      };

      onCreated(newOKR);
      onClose();
      
      if (isFounder) {
        toast.success('👑 LEGENDARY FOUNDER OKR created with infinite power!', {
          duration: 4000,
          style: {
            background: 'linear-gradient(135deg, #FFD700, #FFA500)',
            color: '#000000',
            fontWeight: '700',
          },
        });
      } else {
        toast.success('🚀 OKR created with Swiss precision and legendary energy!', { duration: 3000 });
      }
      
    } catch (error) {
      console.error('🚨 Error creating OKR:', error);
      toast.error('Failed to create OKR');
    } finally {
      setIsLoading(false);
    }
  };

  // Render step content
  const renderStepContent = () => {
    switch (currentStep) {
      case 0:
        return (
          <div className="space-y-6">
            {/* Title */}
            <div>
              <label className={cn(
                'block text-sm font-medium mb-2',
                isFounder ? 'text-yellow-700 dark:text-yellow-300' : 'text-gray-700 dark:text-gray-300'
              )}>
                {isFounder ? 'Founder Objective Title' : 'Objective Title'} *
              </label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => handleFormChange('title', e.target.value)}
                placeholder={isFounder 
                  ? "Build legendary platform features with infinite code bro energy..." 
                  : "Create amazing features with Swiss precision..."
                }
                className={cn(
                  'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg text-lg',
                  'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                  'focus:outline-none focus:ring-2 focus:ring-offset-2',
                  isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
                )}
                required
              />
            </div>

            {/* Description */}
            <div>
              <label className={cn(
                'block text-sm font-medium mb-2',
                isFounder ? 'text-yellow-700 dark:text-yellow-300' : 'text-gray-700 dark:text-gray-300'
              )}>
                Description *
              </label>
              <textarea
                value={formData.description}
                onChange={(e) => handleFormChange('description', e.target.value)}
                placeholder={isFounder 
                  ? "Describe your legendary founder objective in detail. How will this create infinite value and inspire legendary performance across the platform?" 
                  : "Describe your objective and why it matters. What impact will it have?"
                }
                rows={4}
                className={cn(
                  'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg resize-none',
                  'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                  'focus:outline-none focus:ring-2 focus:ring-offset-2',
                  isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
                )}
                required
              />
            </div>

            {/* Team Selection */}
            <div>
              <label className={cn(
                'block text-sm font-medium mb-2',
                isFounder ? 'text-yellow-700 dark:text-yellow-300' : 'text-gray-700 dark:text-gray-300'
              )}>
                Team
              </label>
              <div className="grid grid-cols-2 gap-3">
                {teamOptions.map((team) => {
                  const IconComponent = team.icon;
                  return (
                    <button
                      key={team.value}
                      type="button"
                      onClick={() => handleFormChange('teamId', team.value)}
                      className={cn(
                        'p-3 rounded-lg border text-left transition-colors',
                        formData.teamId === team.value
                          ? isFounder
                            ? 'border-yellow-500 bg-yellow-50 text-yellow-900 dark:border-yellow-400 dark:bg-yellow-900/30 dark:text-yellow-100'
                            : 'border-blue-500 bg-blue-50 text-blue-900 dark:border-blue-400 dark:bg-blue-900/30 dark:text-blue-100'
                          : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
                      )}
                    >
                      <div className="flex items-center gap-2">
                        <IconComponent className="w-4 h-4" />
                        <span className="font-medium text-sm">{team.label}</span>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Date Range */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className={cn(
                  'block text-sm font-medium mb-2',
                  isFounder ? 'text-yellow-700 dark:text-yellow-300' : 'text-gray-700 dark:text-gray-300'
                )}>
                  Start Date
                </label>
                <input
                  type="date"
                  value={formData.startDate}
                  onChange={(e) => handleFormChange('startDate', e.target.value)}
                  className={cn(
                    'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg',
                    'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                    'focus:outline-none focus:ring-2 focus:ring-offset-2',
                    isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
                  )}
                />
              </div>

              <div>
                <label className={cn(
                  'block text-sm font-medium mb-2',
                  isFounder ? 'text-yellow-700 dark:text-yellow-300' : 'text-gray-700 dark:text-gray-300'
                )}>
                  End Date
                </label>
                <input
                  type="date"
                  value={formData.endDate}
                  onChange={(e) => handleFormChange('endDate', e.target.value)}
                  className={cn(
                    'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg',
                    'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                    'focus:outline-none focus:ring-2 focus:ring-offset-2',
                    isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
                  )}
                />
              </div>
            </div>
          </div>
        );

      case 1:
        return (
          <div className="space-y-6">
            {/* Key Results Header */}
            <div className="flex items-center justify-between">
              <div>
                <h3 className={cn(
                  'text-lg font-semibold',
                  isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
                )}>
                  Key Results
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  Add 2-5 measurable outcomes that will indicate success
                </p>
              </div>

              <LegendaryButton
                variant={isFounder ? "founder" : "primary"}
                onClick={handleAddKeyResult}
                leftIcon={Plus}
              >
                Add Key Result
              </LegendaryButton>
            </div>

            {/* Key Results List */}
            <div className="space-y-4">
              {formData.keyResults.map((keyResult, index) => (
                <KeyResultForm
                  key={keyResult.id}
                  keyResult={keyResult}
                  onChange={(kr) => handleUpdateKeyResult(index, kr)}
                  onRemove={() => handleRemoveKeyResult(index)}
                  isFounder={isFounder}
                />
              ))}
              
              {formData.keyResults.length === 0 && (
                <div className="text-center py-12">
                  <Target className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    {isFounder 
                      ? "Ready to add legendary key results? Click 'Add Key Result' to start tracking your founder objectives!"
                      : "No key results yet. Add your first measurable outcome to track progress!"
                    }
                  </p>
                  <LegendaryButton
                    variant={isFounder ? "founder" : "primary"}
                    onClick={handleAddKeyResult}
                    leftIcon={Plus}
                  >
                    Add Your First Key Result
                  </LegendaryButton>
                </div>
              )}
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            {/* Settings */}
            <div>
              <h3 className={cn(
                'text-lg font-semibold mb-4',
                isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
              )}>
                OKR Settings
              </h3>

              <div className="space-y-4">
                {/* Visibility */}
                <div className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                  <div className="flex items-center gap-3">
                    {formData.isPublic ? <Globe className="w-4 h-4" /> : <Lock className="w-4 h-4" />}
                    <div>
                      <p className="font-medium text-gray-900 dark:text-white">
                        {formData.isPublic ? 'Public OKR' : 'Private OKR'}
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {formData.isPublic 
                          ? 'Visible to all team members'
                          : 'Only visible to you and assigned team members'
                        }
                      </p>
                    </div>
                  </div>
                  
                  <button
                    onClick={() => handleFormChange('isPublic', !formData.isPublic)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    {formData.isPublic ? (
                      <ToggleRight className="w-6 h-6 text-green-500" />
                    ) : (
                      <ToggleLeft className="w-6 h-6" />
                    )}
                  </button>
                </div>

                {/* Legendary Status */}
                <div className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Sparkles className="w-4 h-4 text-purple-600" />
                    <div>
                      <p className="font-medium text-gray-900 dark:text-white">Legendary OKR</p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        Mark as legendary for extra recognition and tracking
                      </p>
                    </div>
                  </div>
                  
                  <button
                    onClick={() => handleFormChange('isLegendary', !formData.isLegendary)}
                    className="text-gray-400 hover:text-gray-600"
                    disabled={isFounder} // Auto-enabled for founder
                  >
                    {formData.isLegendary ? (
                      <ToggleRight className="w-6 h-6 text-purple-500" />
                    ) : (
                      <ToggleLeft className="w-6 h-6" />
                    )}
                  </button>
                </div>

                {/* Founder Priority */}
                {isFounder && (
                  <div className="flex items-center justify-between p-4 border border-yellow-200 dark:border-yellow-700 rounded-lg bg-yellow-50/30 dark:bg-yellow-900/10">
                    <div className="flex items-center gap-3">
                      <Crown className="w-4 h-4 text-yellow-600" />
                      <div>
                        <p className="font-medium text-yellow-900 dark:text-yellow-100">Founder Priority</p>
                        <p className="text-sm text-yellow-700 dark:text-yellow-300">
                          High-priority founder objective with infinite tracking power
                        </p>
                      </div>
                    </div>
                    
                    <ToggleRight className="w-6 h-6 text-yellow-500" />
                  </div>
                )}
              </div>
            </div>

            {/* Tags */}
            <div>
              <label className={cn(
                'block text-sm font-medium mb-2',
                isFounder ? 'text-yellow-700 dark:text-yellow-300' : 'text-gray-700 dark:text-gray-300'
              )}>
                Tags
              </label>
              
              <div className="flex flex-wrap gap-2 mb-3">
                {formData.tags.map((tag) => (
                  <span
                    key={tag}
                    className={cn(
                      'inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium',
                      isFounder 
                        ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300'
                        : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'
                    )}
                  >
                    #{tag}
                    <button
                      onClick={() => handleRemoveTag(tag)}
                      className="hover:bg-black/10 rounded-full p-0.5"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                ))}
              </div>

              <div className="flex gap-2">
                <input
                  type="text"
                  value={tagInput}
                  onChange={(e) => setTagInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddTag())}
                  placeholder="Add a tag..."
                  className={cn(
                    'flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg',
                    'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                    'focus:outline-none focus:ring-2 focus:ring-offset-2',
                    isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
                  )}
                />
                <LegendaryButton
                  variant="secondary"
                  onClick={handleAddTag}
                  disabled={!tagInput.trim()}
                >
                  Add
                </LegendaryButton>
              </div>
            </div>

            {/* Summary */}
            <div className={cn(
              'p-4 rounded-lg border',
              isFounder 
                ? 'border-yellow-200 bg-yellow-50/50 dark:border-yellow-700 dark:bg-yellow-900/20'
                : 'border-blue-200 bg-blue-50/50 dark:border-blue-700 dark:bg-blue-900/20'
            )}>
              <h4 className={cn(
                'font-medium mb-2',
                isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-blue-900 dark:text-blue-100'
              )}>
                Review Summary
              </h4>
              <div className="text-sm space-y-1">
                <p><strong>Title:</strong> {formData.title || 'Untitled OKR'}</p>
                <p><strong>Key Results:</strong> {formData.keyResults.length}</p>
                <p><strong>Duration:</strong> {formData.startDate} to {formData.endDate}</p>
                <p><strong>Team:</strong> {teamOptions.find(t => t.value === formData.teamId)?.label || 'None'}</p>
                <p><strong>Status:</strong> {formData.isLegendary ? '✨ Legendary' : '📋 Standard'} {formData.founderPriority && '👑 Founder Priority'}</p>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="xl">
      <div className={cn(
        'bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-h-[90vh] overflow-hidden',
        isFounder && 'border-2 border-yellow-200 dark:border-yellow-700'
      )}>
        {/* Header */}
        <div className={cn(
          'px-6 py-4 border-b border-gray-200 dark:border-gray-700',
          isFounder && 'bg-gradient-to-r from-yellow-50 via-orange-50 to-yellow-50 dark:from-yellow-900/20 dark:via-orange-900/20 dark:to-yellow-900/20'
        )}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              {isFounder && <Crown className="w-6 h-6 text-yellow-600" />}
              <Target className={cn(
                'w-6 h-6',
                isFounder ? 'text-yellow-600' : 'text-blue-600'
              )} />
              <h2 className={cn(
                'text-xl font-bold',
                isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
              )}>
                {isFounder ? 'Create Legendary Founder OKR' : 'Create New OKR'}
              </h2>
            </div>

            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
              disabled={isLoading}
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Progress Steps */}
          <div className="flex items-center gap-4 mt-4">
            {steps.map((step, index) => {
              const StepIcon = step.icon;
              return (
                <div
                  key={index}
                  className={cn(
                    'flex items-center gap-2',
                    index < steps.length - 1 && 'flex-1'
                  )}
                >
                  <div className={cn(
                    'flex items-center gap-2 px-3 py-2 rounded-lg transition-colors',
                    currentStep === index 
                      ? isFounder
                        ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300'
                        : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'
                      : currentStep > index
                        ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'
                        : 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400'
                  )}>
                    <StepIcon className="w-4 h-4" />
                    <span className="text-sm font-medium">{step.title}</span>
                  </div>
                  
                  {index < steps.length - 1 && (
                    <div className={cn(
                      'flex-1 h-0.5',
                      currentStep > index ? 'bg-green-300' : 'bg-gray-300'
                    )} />
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Content */}
        <div className="px-6 py-6 max-h-[60vh] overflow-y-auto">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentStep}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              {renderStepContent()}
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Footer */}
        <div className={cn(
          'px-6 py-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50',
          isFounder && 'bg-gradient-to-r from-yellow-50/50 to-orange-50/50 dark:from-yellow-900/10 dark:to-orange-900/10'
        )}>
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-500 dark:text-gray-400">
              Step {currentStep + 1} of {steps.length}: {steps[currentStep].description}
              {isFounder && (
                <div className="mt-1 font-bold text-yellow-700 dark:text-yellow-300 text-xs">
                  👑 LEGENDARY FOUNDER OKR CREATION AT 17:20:47 UTC! 👑
                </div>
              )}
            </div>

            <div className="flex items-center gap-3">
              {currentStep > 0 && (
                <LegendaryButton
                  variant="secondary"
                  onClick={handlePrevStep}
                  leftIcon={ArrowLeft}
                  disabled={isLoading}
                >
                  Previous
                </LegendaryButton>
              )}

              {currentStep < steps.length - 1 ? (
                <LegendaryButton
                  variant={isFounder ? "founder" : "primary"}
                  onClick={handleNextStep}
                  rightIcon={ArrowRight}
                  disabled={!validateStep(currentStep)}
                >
                  Next
                </LegendaryButton>
              ) : (
                <LegendaryButton
                  variant={isFounder ? "founder" : "primary"}
                  onClick={handleSubmit}
                  leftIcon={isLoading ? undefined : Save}
                  disabled={isLoading || !validateStep(0) || !validateStep(1)}
                >
                  {isLoading ? (
                    <div className="flex items-center gap-2">
                      <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                      <span>Creating...</span>
                    </div>
                  ) : (
                    isFounder ? 'Create Legendary OKR' : 'Create OKR'
                  )}
                </LegendaryButton>
              )}
            </div>
          </div>
        </div>
      </div>
    </Modal>
  );
};

console.log('🎸🎸🎸 LEGENDARY CREATE OKR MODAL COMPONENT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Create OKR modal component completed at: 2025-08-06 17:20:47 UTC`);
console.log('📋 OKR creation: SWISS PRECISION');
console.log('👑 RICKROLL187 founder OKR creation: LEGENDARY');
console.log('🎯 Multi-step creation flow: MAXIMUM USABILITY');
console.log('🌅 LATE AFTERNOON LEGENDARY OKR CREATION ENERGY: INFINITE AT 17:20:47!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
