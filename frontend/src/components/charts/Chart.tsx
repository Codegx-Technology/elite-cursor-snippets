// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Enterprise-grade Chart components with Kenya-first design system integration
// [GOAL]: Create reusable chart components with cultural authenticity and mobile-first design
// [TASK]: Phase 2.1b - Advanced Data Visualization Components

'use client';

import React from 'react';
import { colors, spacing, typography } from '@/config/designTokens';
import { cn } from '@/lib/utils';

// Base Chart Props
export interface ChartProps {
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  className?: string;
  title?: string;
  subtitle?: string;
  height?: number;
  width?: number;
}

// Simple Bar Chart Component
export interface BarChartProps extends ChartProps {
  data: Array<{
    label: string;
    value: number;
    color?: string;
  }>;
  showValues?: boolean;
  maxValue?: number;
}

export const BarChart: React.FC<BarChartProps> = ({
  data,
  variant = 'default',
  className,
  title,
  subtitle,
  height = 300,
  showValues = true,
  maxValue
}) => {
  const max = maxValue || Math.max(...data.map(d => d.value));
  
  const variantColors = {
    default: '#3B82F6',
    kenya: colors.kenya.green,
    cultural: colors.cultural.gold,
    elite: '#8B5CF6'
  };

  const baseColor = variantColors[variant];

  return (
    <div className={cn('bg-white rounded-lg border p-6 shadow-sm', className)}>
      {title && (
        <div className="mb-4">
          <h3 className={cn(
            'font-semibold text-gray-900',
            `text-[${typography.fontSizes.lg}]`
          )}>
            {title}
          </h3>
          {subtitle && (
            <p className={cn(
              'text-gray-600 mt-1',
              `text-[${typography.fontSizes.sm}]`
            )}>
              {subtitle}
            </p>
          )}
        </div>
      )}
      
      <div className="space-y-3" style={{ height }}>
        {data.map((item, index) => {
          const percentage = (item.value / max) * 100;
          const itemColor = item.color || baseColor;
          
          return (
            <div key={index} className="flex items-center space-x-3">
              <div className={cn(
                'min-w-0 flex-1',
                `text-[${typography.fontSizes.sm}]`
              )}>
                <div className="flex justify-between items-center mb-1">
                  <span className="text-gray-700 truncate">{item.label}</span>
                  {showValues && (
                    <span className="text-gray-900 font-medium ml-2">
                      {item.value.toLocaleString()}
                    </span>
                  )}
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="h-2 rounded-full transition-all duration-500 ease-out"
                    style={{
                      width: `${percentage}%`,
                      backgroundColor: itemColor
                    }}
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

// Simple Line Chart Component (SVG-based)
export interface LineChartProps extends ChartProps {
  data: Array<{
    label: string;
    value: number;
  }>;
  showDots?: boolean;
  smooth?: boolean;
}

export const LineChart: React.FC<LineChartProps> = ({
  data,
  variant = 'default',
  className,
  title,
  subtitle,
  height = 300,
  width = 400,
  showDots = true,
  smooth = false
}) => {
  const variantColors = {
    default: '#3B82F6',
    kenya: colors.kenya.green,
    cultural: colors.cultural.gold,
    elite: '#8B5CF6'
  };

  const strokeColor = variantColors[variant];
  const maxValue = Math.max(...data.map(d => d.value));
  const minValue = Math.min(...data.map(d => d.value));
  const range = maxValue - minValue;

  const padding = 40;
  const chartWidth = width - (padding * 2);
  const chartHeight = height - (padding * 2);

  const points = data.map((item, index) => {
    const x = padding + (index / (data.length - 1)) * chartWidth;
    const y = padding + ((maxValue - item.value) / range) * chartHeight;
    return { x, y, ...item };
  });

  const pathData = points.reduce((path, point, index) => {
    const command = index === 0 ? 'M' : smooth ? 'L' : 'L';
    return `${path} ${command} ${point.x} ${point.y}`;
  }, '');

  return (
    <div className={cn('bg-white rounded-lg border p-6 shadow-sm', className)}>
      {title && (
        <div className="mb-4">
          <h3 className={cn(
            'font-semibold text-gray-900',
            `text-[${typography.fontSizes.lg}]`
          )}>
            {title}
          </h3>
          {subtitle && (
            <p className={cn(
              'text-gray-600 mt-1',
              `text-[${typography.fontSizes.sm}]`
            )}>
              {subtitle}
            </p>
          )}
        </div>
      )}

      <div className="relative">
        <svg width={width} height={height} className="overflow-visible">
          {/* Grid lines */}
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#f3f4f6" strokeWidth="1"/>
            </pattern>
          </defs>
          <rect width={width} height={height} fill="url(#grid)" />
          
          {/* Chart line */}
          <path
            d={pathData}
            fill="none"
            stroke={strokeColor}
            strokeWidth="3"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="drop-shadow-sm"
          />
          
          {/* Data points */}
          {showDots && points.map((point, index) => (
            <g key={index}>
              <circle
                cx={point.x}
                cy={point.y}
                r="4"
                fill="white"
                stroke={strokeColor}
                strokeWidth="3"
                className="drop-shadow-sm"
              />
              <title>{`${point.label}: ${point.value}`}</title>
            </g>
          ))}
          
          {/* Axis labels */}
          {points.map((point, index) => (
            <text
              key={index}
              x={point.x}
              y={height - 10}
              textAnchor="middle"
              className={cn('fill-gray-600', `text-[${typography.fontSizes.xs}]`)}
            >
              {point.label}
            </text>
          ))}
        </svg>
      </div>
    </div>
  );
};

// Donut Chart Component
export interface DonutChartProps extends ChartProps {
  data: Array<{
    label: string;
    value: number;
    color?: string;
  }>;
  centerText?: string;
  showLegend?: boolean;
}

export const DonutChart: React.FC<DonutChartProps> = ({
  data,
  variant = 'default',
  className,
  title,
  subtitle,
  height = 300,
  centerText,
  showLegend = true
}) => {
  const variantColors = {
    default: ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'],
    kenya: [colors.kenya.green, colors.cultural.gold, colors.cultural.sunset, colors.cultural.earth, colors.cultural.sky],
    cultural: [colors.cultural.gold, colors.cultural.sunset, colors.cultural.earth, colors.cultural.sky, colors.cultural.savanna],
    elite: ['#8B5CF6', '#EC4899', '#06B6D4', '#10B981', '#F59E0B']
  };

  const colorPalette = variantColors[variant];
  const total = data.reduce((sum, item) => sum + item.value, 0);
  const size = 200;
  const strokeWidth = 30;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;

  let currentAngle = 0;
  const segments = data.map((item, index) => {
    const percentage = item.value / total;
    const angle = percentage * 360;
    const strokeDasharray = `${percentage * circumference} ${circumference}`;
    const strokeDashoffset = -currentAngle * (circumference / 360);
    const color = item.color || colorPalette[index % colorPalette.length];
    
    currentAngle += angle;
    
    return {
      ...item,
      percentage: Math.round(percentage * 100),
      strokeDasharray,
      strokeDashoffset,
      color
    };
  });

  return (
    <div className={cn('bg-white rounded-lg border p-6 shadow-sm', className)}>
      {title && (
        <div className="mb-4">
          <h3 className={cn(
            'font-semibold text-gray-900',
            `text-[${typography.fontSizes.lg}]`
          )}>
            {title}
          </h3>
          {subtitle && (
            <p className={cn(
              'text-gray-600 mt-1',
              `text-[${typography.fontSizes.sm}]`
            )}>
              {subtitle}
            </p>
          )}
        </div>
      )}

      <div className="flex flex-col lg:flex-row items-center space-y-4 lg:space-y-0 lg:space-x-6">
        <div className="relative">
          <svg width={size} height={size} className="transform -rotate-90">
            <circle
              cx={size / 2}
              cy={size / 2}
              r={radius}
              fill="none"
              stroke="#f3f4f6"
              strokeWidth={strokeWidth}
            />
            {segments.map((segment, index) => (
              <circle
                key={index}
                cx={size / 2}
                cy={size / 2}
                r={radius}
                fill="none"
                stroke={segment.color}
                strokeWidth={strokeWidth}
                strokeDasharray={segment.strokeDasharray}
                strokeDashoffset={segment.strokeDashoffset}
                strokeLinecap="round"
                className="transition-all duration-500"
              />
            ))}
          </svg>
          {centerText && (
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center">
                <div className={cn(
                  'font-bold text-gray-900',
                  `text-[${typography.fontSizes['2xl']}]`
                )}>
                  {centerText}
                </div>
              </div>
            </div>
          )}
        </div>

        {showLegend && (
          <div className="space-y-2">
            {segments.map((segment, index) => (
              <div key={index} className="flex items-center space-x-3">
                <div
                  className="w-4 h-4 rounded-full"
                  style={{ backgroundColor: segment.color }}
                />
                <div className="flex-1">
                  <div className={cn(
                    'text-gray-700',
                    `text-[${typography.fontSizes.sm}]`
                  )}>
                    {segment.label}
                  </div>
                  <div className={cn(
                    'text-gray-500',
                    `text-[${typography.fontSizes.xs}]`
                  )}>
                    {segment.value.toLocaleString()} ({segment.percentage}%)
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

// Export all chart components
export { BarChart as Chart };
