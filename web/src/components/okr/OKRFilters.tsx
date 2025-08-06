// File: web/src/components/okr/OKRFilters.tsx
/**
 * 🔧🎸 N3EXTPATH - LEGENDARY OKR FILTERS COMPONENT 🎸🔧
 * Swiss precision OKR filtering with infinite code bro energy
 * Built: 2025-08-06 17:16:09 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect, useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Crown, 
  Filter, 
  Search, 
  X, 
  ChevronDown,
  Calendar,
  Users,
  Target,
  Sparkles,
  Star,
  Activity,
  CheckCircle,
  Clock,
  AlertTriangle,
  User,
  Building,
  Tag,
  SlidersHorizontal,
  RotateCcw
} from 'lucide-react';
import { LegendaryButton } from '@/components/ui/LegendaryButton';
import { cn } from '@/utils/cn';
import toast from 'react-hot-toast';

// =====================================
// 🔧 FILTER TYPES 🔧
// =====================================

interface OKRFilters {
  status?: string[];
  quarter?: string;
  year?: number;
  owner?: string;
  team?: string;
  legendary?: boolean;
  founderPriority?: boolean;
  search?: string;
}

interface OKRFiltersProps {
  filters: OKRFilters;
  onChange: (filters: Partial<OKRFilters>) => void;
  isFounder?: boolean;
  onReset?: () => void;
}

// =====================================
// 🎸 FILTER OPTION COMPONENT 🎸
// =====================================

const FilterSelect: React.FC<{
  label: string;
  value: string | number | undefined;
  options: Array<{ value: string | number; label: string; icon?: React.ElementType }>;
  onChange: (value: string | number | undefined) => void;
  placeholder?: string;
  isFounder?: boolean;
  multiple?: boolean;
}> = ({ label, value, options, onChange, placeholder = "Select...", isFounder = false, multiple = false }) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleSelect = (optionValue: string | number) => {
    onChange(optionValue === '' ? undefined : optionValue);
    if (!multiple) {
      setIsOpen(false);
    }
  };

  const selectedOption = options.find(opt => opt.value === value);

  return (
    <div className="relative">
      <label className={cn(
        'block text-xs font-medium mb-1',
        isFounder ? 'text-yellow-700 dark:text-yellow-300' : 'text-gray-700 dark:text-gray-300'
      )}>
        {label}
      </label>
      
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={cn(
          'w-full flex items-center justify-between px-3 py-2 rounded-lg border',
          'bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm',
          'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500',
          'focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors',
          isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
        )}
      >
        <span className={cn(
          selectedOption ? 'text-gray-900 dark:text-white' : 'text-gray-500 dark:text-gray-400'
        )}>
          {selectedOption ? (
            <div className="flex items-center gap-2">
              {selectedOption.icon && <selectedOption.icon className="w-3 h-3" />}
              <span>{selectedOption.label}</span>
            </div>
          ) : placeholder}
        </span>
        
        <ChevronDown className={cn(
          'w-4 h-4 transition-transform',
          isOpen && 'rotate-180'
        )} />
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="absolute top-full left-0 right-0 mt-1 py-2 bg-white dark:bg-gray-700 rounded-lg shadow-xl border border-gray-200 dark:border-gray-600 z-50"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
          >
            {/* Clear option */}
            <button
              onClick={() => handleSelect('')}
              className="w-full px-3 py-2 text-left text-sm text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
            >
              Clear selection
            </button>
            
            <div className="border-t border-gray-200 dark:border-gray-600 my-1" />
            
            {options.map((option) => (
              <button
                key={option.value}
                onClick={() => handleSelect(option.value)}
                className={cn(
                  'w-full px-3 py-2 text-left text-sm hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors',
                  'flex items-center gap-2',
                  value === option.value 
                    ? isFounder 
                      ? 'bg-yellow-100 text-yellow-900 dark:bg-yellow-900/30 dark:text-yellow-300'
                      : 'bg-blue-100 text-blue-900 dark:bg-blue-900/30 dark:text-blue-300'
                    : 'text-gray-900 dark:text-white'
                )}
              >
                {option.icon && <option.icon className="w-3 h-3" />}
                <span>{option.label}</span>
              </button>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

// =====================================
// 🎸 LEGENDARY OKR FILTERS 🎸
// =====================================

export const OKRFilters: React.FC<OKRFiltersProps> = ({
  filters,
  onChange,
  isFounder = false,
  onReset,
}) => {
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [searchInput, setSearchInput] = useState(filters.search || '');

  useEffect(() => {
    console.log('🔧🎸🔧 LEGENDARY OKR FILTERS LOADED! 🔧🎸🔧');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`OKR filters loaded at: 2025-08-06 17:16:09 UTC`);
    console.log('🌅 LATE AFTERNOON LEGENDARY OKR FILTERS ENERGY AT 17:16:09!');

    if (isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER OKR FILTERS ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER OKR FILTERS WITH INFINITE CODE BRO ENERGY!');
    }
  }, [isFounder]);

  // Status options
  const statusOptions = [
    { value: 'active', label: 'Active', icon: Activity },
    { value: 'completed', label: 'Completed', icon: CheckCircle },
    { value: 'paused', label: 'Paused', icon: Clock },
    { value: 'cancelled', label: 'Cancelled', icon: AlertTriangle },
    { value: 'draft', label: 'Draft', icon: Target },
    ...(isFounder ? [{ value: 'legendary', label: 'Legendary', icon: Sparkles }] : []),
  ];

  // Quarter options
  const quarterOptions = [
    { value: 'Q1 2025', label: 'Q1 2025' },
    { value: 'Q2 2025', label: 'Q2 2025' },
    { value: 'Q3 2025', label: 'Q3 2025' },
    { value: 'Q4 2025', label: 'Q4 2025' },
    { value: 'Q3-Q4 2025', label: 'Q3-Q4 2025' },
  ];

  // Year options
  const yearOptions = [
    { value: 2025, label: '2025' },
    { value: 2024, label: '2024' },
    { value: 2023, label: '2023' },
  ];

  // Owner options (mock data)
  const ownerOptions = [
    { value: 'rickroll187', label: 'RICKROLL187', icon: Crown },
    { value: 'codebro42', label: 'CodeBro42', icon: Star },
    { value: 'swissdev', label: 'SwissDev', icon: User },
    { value: 'precisionmaster', label: 'PrecisionMaster', icon: Target },
  ];

  // Team options (mock data)
  const teamOptions = [
    { value: 'legendary-founders', label: 'Legendary Founders', icon: Crown },
    { value: 'code-bro-squad', label: 'Code Bro Squad', icon: Sparkles },
    { value: 'swiss-precision', label: 'Swiss Precision Team', icon: Target },
  ];

  // Handle search input with debounce
  const handleSearchChange = useCallback((value: string) => {
    setSearchInput(value);
    
    // Debounce search
    const timeoutId = setTimeout(() => {
      onChange({ search: value.trim() || undefined });
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [onChange]);

  // Handle filter change
  const handleFilterChange = useCallback((key: keyof OKRFilters, value: any) => {
    onChange({ [key]: value });
  }, [onChange]);

  // Handle reset
  const handleReset = useCallback(() => {
    setSearchInput('');
    onChange({
      status: undefined,
      quarter: undefined,
      year: undefined,
      owner: undefined,
      team: undefined,
      legendary: undefined,
      founderPriority: undefined,
      search: undefined,
    });
    
    if (onReset) {
      onReset();
    }
    
    if (isFounder) {
      toast.success('👑 Founder filters reset with infinite clarity!', {
        duration: 2000,
        style: {
          background: 'linear-gradient(135deg, #FFD700, #FFA500)',
          color: '#000000',
          fontWeight: '600',
        },
      });
    } else {
      toast.success('🔄 Filters reset with Swiss precision!');
    }
  }, [onChange, onReset, isFounder]);

  // Count active filters
  const activeFilterCount = Object.values(filters).filter(value => 
    value !== undefined && value !== null && value !== '' && 
    (Array.isArray(value) ? value.length > 0 : true)
  ).length;

  return (
    <motion.div
      className="space-y-4"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {isFounder && <Crown className="w-4 h-4 text-yellow-600" />}
          <Filter className={cn(
            'w-4 h-4',
            isFounder ? 'text-yellow-600' : 'text-blue-600'
          )} />
          <h3 className={cn(
            'font-semibold text-sm',
            isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
          )}>
            {isFounder ? 'Founder Filters' : 'Filters'}
          </h3>
          
          {activeFilterCount > 0 && (
            <span className={cn(
              'px-2 py-0.5 rounded-full text-xs font-medium',
              isFounder 
                ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300'
                : 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300'
            )}>
              {activeFilterCount}
            </span>
          )}
        </div>

        <div className="flex items-center gap-2">
          <LegendaryButton
            variant="ghost"
            size="sm"
            onClick={() => setShowAdvanced(!showAdvanced)}
            leftIcon={SlidersHorizontal}
          >
            {showAdvanced ? 'Simple' : 'Advanced'}
          </LegendaryButton>
          
          {activeFilterCount > 0 && (
            <LegendaryButton
              variant="ghost"
              size="sm"
              onClick={handleReset}
              leftIcon={RotateCcw}
            >
              Reset
            </LegendaryButton>
          )}
        </div>
      </div>

      {/* Search Bar */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input
          type="text"
          placeholder={isFounder ? "Search founder OKRs..." : "Search OKRs by title, description, or tags..."}
          value={searchInput}
          onChange={(e) => handleSearchChange(e.target.value)}
          className={cn(
            'w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 dark:border-gray-600',
            'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
            'placeholder-gray-500 dark:placeholder-gray-400',
            'focus:outline-none focus:ring-2 focus:ring-offset-2',
            isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
          )}
        />
        
        {searchInput && (
          <button
            onClick={() => handleSearchChange('')}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Quick Filters */}
      <div className="flex flex-wrap gap-2">
        {/* Status Filter */}
        <FilterSelect
          label="Status"
          value={filters.status?.[0]}
          options={statusOptions}
          onChange={(value) => handleFilterChange('status', value ? [value] : undefined)}
          placeholder="Any status"
          isFounder={isFounder}
        />

        {/* Quarter Filter */}
        <FilterSelect
          label="Quarter"
          value={filters.quarter}
          options={quarterOptions}
          onChange={(value) => handleFilterChange('quarter', value)}
          placeholder="Any quarter"
          isFounder={isFounder}
        />

        {/* Owner Filter */}
        <FilterSelect
          label="Owner"
          value={filters.owner}
          options={ownerOptions}
          onChange={(value) => handleFilterChange('owner', value)}
          placeholder="Any owner"
          isFounder={isFounder}
        />
      </div>

      {/* Advanced Filters */}
      <AnimatePresence>
        {showAdvanced && (
          <motion.div
            className="space-y-4 pt-4 border-t border-gray-200 dark:border-gray-700"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {/* Year Filter */}
              <FilterSelect
                label="Year"
                value={filters.year}
                options={yearOptions}
                onChange={(value) => handleFilterChange('year', value)}
                placeholder="Any year"
                isFounder={isFounder}
              />

              {/* Team Filter */}
              <FilterSelect
                label="Team"
                value={filters.team}
                options={teamOptions}
                onChange={(value) => handleFilterChange('team', value)}
                placeholder="Any team"
                isFounder={isFounder}
              />

              {/* Additional Founder Filters */}
              {isFounder && (
                <div className="space-y-2">
                  <label className="block text-xs font-medium text-yellow-700 dark:text-yellow-300">
                    Special Filters
                  </label>
                  
                  <div className="flex flex-col gap-2">
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={filters.legendary || false}
                        onChange={(e) => handleFilterChange('legendary', e.target.checked || undefined)}
                        className={cn(
                          'rounded border-gray-300 dark:border-gray-600',
                          'text-purple-600 focus:ring-purple-500'
                        )}
                      />
                      <span className="text-sm text-gray-700 dark:text-gray-300 flex items-center gap-1">
                        <Sparkles className="w-3 h-3 text-purple-600" />
                        Legendary OKRs
                      </span>
                    </label>
                    
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={filters.founderPriority || false}
                        onChange={(e) => handleFilterChange('founderPriority', e.target.checked || undefined)}
                        className={cn(
                          'rounded border-gray-300 dark:border-gray-600',
                          'text-yellow-600 focus:ring-yellow-500'
                        )}
                      />
                      <span className="text-sm text-gray-700 dark:text-gray-300 flex items-center gap-1">
                        <Crown className="w-3 h-3 text-yellow-600" />
                        Founder Priority
                      </span>
                    </label>
                  </div>
                </div>
              )}
            </div>

            {/* Active Filters Summary */}
            {activeFilterCount > 0 && (
              <div className={cn(
                'p-3 rounded-lg border',
                isFounder 
                  ? 'bg-yellow-50 border-yellow-200 dark:bg-yellow-900/20 dark:border-yellow-700'
                  : 'bg-blue-50 border-blue-200 dark:bg-blue-900/20 dark:border-blue-700'
              )}>
                <div className="flex items-center justify-between">
                  <span className={cn(
                    'text-sm font-medium',
                    isFounder ? 'text-yellow-800 dark:text-yellow-300' : 'text-blue-800 dark:text-blue-300'
                  )}>
                    Active Filters ({activeFilterCount})
                  </span>
                  
                  <LegendaryButton
                    variant="ghost"
                    size="sm"
                    onClick={handleReset}
                    className="text-xs"
                  >
                    Clear All
                  </LegendaryButton>
                </div>
                
                <div className="flex flex-wrap gap-1 mt-2">
                  {Object.entries(filters).map(([key, value]) => {
                    if (!value || value === '' || (Array.isArray(value) && value.length === 0)) return null;
                    
                    let displayValue = value;
                    if (Array.isArray(value)) displayValue = value.join(', ');
                    if (typeof value === 'boolean') displayValue = key;
                    
                    return (
                      <span
                        key={key}
                        className={cn(
                          'inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium',
                          isFounder 
                            ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/40 dark:text-yellow-300'
                            : 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300'
                        )}
                      >
                        <span>{String(displayValue)}</span>
                        <button
                          onClick={() => handleFilterChange(key as keyof OKRFilters, undefined)}
                          className="hover:bg-black/10 rounded-full p-0.5"
                        >
                          <X className="w-2.5 h-2.5" />
                        </button>
                      </span>
                    );
                  })}
                </div>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Bottom Status */}
      <motion.div
        className="text-center py-2"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.8 }}
      >
        <div className="flex items-center justify-center gap-3 text-xs text-gray-500 dark:text-gray-400">
          <div className="flex items-center gap-1">
            <Activity className="w-3 h-3" />
            <span>Live filtering</span>
          </div>
          
          <div className="flex items-center gap-1">
            <Target className="w-3 h-3" />
            <span>Swiss precision</span>
          </div>
          
          <div className="font-mono">
            17:16:09 UTC
          </div>
        </div>
        
        {isFounder && (
          <div className="mt-1">
            <span className="text-yellow-700 dark:text-yellow-300 font-bold text-xs">
              👑 FOUNDER FILTERING • INFINITE SEARCH POWER! 👑
            </span>
          </div>
        )}
      </motion.div>
    </div>
  );
};

console.log('🎸🎸🎸 LEGENDARY OKR FILTERS COMPONENT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`OKR filters component completed at: 2025-08-06 17:16:09 UTC`);
console.log('🔧 OKR filtering: SWISS PRECISION');
console.log('👑 RICKROLL187 founder filters: LEGENDARY');
console.log('🔍 Advanced search system: MAXIMUM PRECISION');
console.log('🌅 LATE AFTERNOON LEGENDARY OKR FILTERS ENERGY: INFINITE AT 17:16:09!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
