// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Phase 4 - AI-powered content suggestions UI with Kenya-first intelligence
// [GOAL]: Intelligent content recommendations interface with cultural authenticity
// [TASK]: Create AI suggestions panel with real-time content analysis

'use client';

import React, { useState, useEffect } from 'react';
import { aiSuggestionEngine, ContentSuggestion, KENYA_CONTENT_CATEGORIES } from '@/lib/ai-suggestions';
import { useAriaUtils } from '@/hooks/useAccessibility';
import Card from '@/components/ui/Card';
import AccessibleButton from '@/components/AccessibleButton';
import LoadingStates from '@/components/ui/LoadingStates';
import { FaBrain, FaLightbulb, FaFlag, FaStar, FaClock, FaTools } from 'react-icons/fa';

interface AISuggestionsPanelProps {
  content?: string;
  category?: keyof typeof KENYA_CONTENT_CATEGORIES;
  onApplySuggestion?: (suggestion: ContentSuggestion) => void;
}

interface KenyaAnalysis {
  score: number;
  culturalElements: string[];
  improvements: string[];
}

const AISuggestionsPanel: React.FC<AISuggestionsPanelProps> = ({
  content = '',
  category,
  onApplySuggestion
}) => {
  const { createAriaLabel } = useAriaUtils();
  const [suggestions, setSuggestions] = useState<ContentSuggestion[]>([]);
  const [loading, setLoading] = useState(false);
  const [kenyaAnalysis, setKenyaAnalysis] = useState<KenyaAnalysis | null>(null);
  const [trendingTopics, setTrendingTopics] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<keyof typeof KENYA_CONTENT_CATEGORIES | undefined>(category);

  useEffect(() => {
    loadTrendingTopics();
  }, []);

  useEffect(() => {
    if (content.length > 10) {
      analyzeContent();
    }
    generateSuggestions();
  }, [content, selectedCategory]);

  const loadTrendingTopics = async () => {
    try {
      const topics = await aiSuggestionEngine.getTrendingTopics();
      setTrendingTopics(topics);
    } catch (error: unknown) {
      console.error('🇰🇪 Failed to load trending topics:', error);
    }
  };

  const analyzeContent = async () => {
    if (!content.trim()) return;
    
    try {
      const analysis = await aiSuggestionEngine.analyzeKenyaRelevance(content);
      setKenyaAnalysis(analysis);
    } catch (error: unknown) {
      console.error('🇰🇪 Content analysis failed:', error);
    }
  };

  const generateSuggestions = async () => {
    setLoading(true);
    try {
      const newSuggestions = await aiSuggestionEngine.generateSuggestions({
        content,
        category: selectedCategory,
        audience: 'mixed',
        purpose: 'educational'
      });
      setSuggestions(newSuggestions);
    } catch (error: unknown) {
      console.error('🇰🇪 Suggestion generation failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'text-green-600';
    if (confidence >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getKenyaRelevanceStars = (relevance: number) => {
    const stars = Math.round(relevance * 5);
    return '🇰🇪'.repeat(stars) + '⭐'.repeat(5 - stars);
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getSuggestionIcon = (type: ContentSuggestion['type']) => {
    switch (type) {
      case 'video_topic': return <FaLightbulb className="text-yellow-500" />;
      case 'script_enhancement': return <FaTools className="text-blue-500" />;
      case 'visual_element': return <FaFlag className="text-green-500" />;
      case 'cultural_context': return <FaBrain className="text-purple-500" />;
      case 'music_recommendation': return <FaStar className="text-orange-500" />;
      default: return <FaBrain className="text-gray-500" />;
    }
  };

  return (
    <div className="space-y-4">
      {/* AI Header */}
      <Card>
        <div className="p-4">
          <div className="flex items-center gap-3 mb-3">
            <FaBrain className="text-2xl text-purple-600" />
            <div>
              <h3 className="font-semibold text-gray-800">AI Content Assistant 🇰🇪</h3>
              <p className="text-sm text-gray-600">Kenya-first intelligent suggestions</p>
            </div>
          </div>
          
          {/* Category Selection */}
          <div className="mb-3">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Content Category
            </label>
            <select
              value={selectedCategory || ''}
              onChange={(e) => setSelectedCategory(e.target.value as keyof typeof KENYA_CONTENT_CATEGORIES || undefined)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="">Select category...</option>
              {Object.entries(KENYA_CONTENT_CATEGORIES).map(([key, cat]) => (
                <option key={key} value={key}>{cat.name}</option>
              ))}
            </select>
          </div>

          <AccessibleButton
            variant="kenya"
            size="sm"
            onClick={generateSuggestions}
            loading={loading}
            loadingText="Generating..."
            ariaLabel={createAriaLabel('Generate AI suggestions', 'content creation')}
            icon={<FaBrain />}
          >
            Generate Suggestions
          </AccessibleButton>
        </div>
      </Card>

      {/* Kenya Relevance Analysis */}
      {kenyaAnalysis && (
        <Card>
          <div className="p-4">
            <h4 className="font-medium text-gray-800 mb-3 flex items-center gap-2">
              <FaFlag className="text-green-600" />
              Kenya-First Analysis
            </h4>
            
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Relevance Score</span>
                <div className="flex items-center gap-2">
                  <div className="w-24 bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-green-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${kenyaAnalysis.score * 100}%` }}
                    />
                  </div>
                  <span className="text-sm font-medium">{Math.round(kenyaAnalysis.score * 100)}%</span>
                </div>
              </div>

              {kenyaAnalysis.culturalElements.length > 0 && (
                <div>
                  <span className="text-sm text-gray-600">Cultural Elements:</span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {kenyaAnalysis.culturalElements.map((element: string, index: number) => (
                      <span key={index} className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs">
                        {element}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {kenyaAnalysis.improvements.length > 0 && (
                <div>
                  <span className="text-sm text-gray-600">Improvements:</span>
                  <ul className="mt-1 space-y-1">
                    {kenyaAnalysis.improvements.map((improvement: string, index: number) => (
                      <li key={index} className="text-xs text-gray-700 flex items-start gap-1">
                        <span className="text-yellow-500">💡</span>
                        {improvement}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </Card>
      )}

      {/* Trending Topics */}
      {trendingTopics.length > 0 && (
        <Card>
          <div className="p-4">
            <h4 className="font-medium text-gray-800 mb-3 flex items-center gap-2">
              📈 Trending in Kenya
            </h4>
            <div className="flex flex-wrap gap-2">
              {trendingTopics.slice(0, 6).map((topic, index) => (
                <button
                  key={index}
                  onClick={() => onApplySuggestion?.({
                    id: `trending_${index}`,
                    type: 'video_topic',
                    title: topic,
                    description: `Create content about: ${topic}`,
                    confidence: 0.85,
                    kenyaRelevance: 0.90,
                    culturalTags: ['trending', 'topical'],
                    implementation: {
                      difficulty: 'medium',
                      estimatedTime: '2-3 days',
                      resources: ['research', 'interviews']
                    }
                  })}
                  className="px-3 py-1 bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-full text-xs transition-colors"
                >
                  {topic}
                </button>
              ))}
            </div>
          </div>
        </Card>
      )}

      {/* AI Suggestions */}
      <Card>
        <div className="p-4">
          <h4 className="font-medium text-gray-800 mb-3 flex items-center gap-2">
            <FaLightbulb className="text-yellow-500" />
            AI Suggestions ({suggestions.length})
          </h4>

          {loading ? (
            <div className="py-8">
              <LoadingStates.LoadingSpinner size="md" variant="kenya" />
              <p className="text-center text-gray-600 mt-2">Generating Kenya-first suggestions...</p>
            </div>
          ) : suggestions.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <FaBrain className="text-4xl mx-auto mb-2 opacity-50" />
              <p>No suggestions yet. Add content or select a category to get started! 🇰🇪</p>
            </div>
          ) : (
            <div className="space-y-4">
              {suggestions.map((suggestion) => (
                <div key={suggestion.id} className="border border-gray-200 rounded-lg p-4 hover:border-green-300 transition-colors">
                  <div className="flex items-start gap-3">
                    <div className="flex-shrink-0 mt-1">
                      {getSuggestionIcon(suggestion.type)}
                    </div>
                    
                    <div className="flex-1">
                      <div className="flex items-start justify-between mb-2">
                        <h5 className="font-medium text-gray-800">{suggestion.title}</h5>
                        <div className="flex items-center gap-2 text-xs">
                          <span className={`font-medium ${getConfidenceColor(suggestion.confidence)}`}>
                            {Math.round(suggestion.confidence * 100)}%
                          </span>
                          <span title="Kenya Relevance">
                            {getKenyaRelevanceStars(suggestion.kenyaRelevance)}
                          </span>
                        </div>
                      </div>
                      
                      <p className="text-sm text-gray-600 mb-3">{suggestion.description}</p>
                      
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3 text-xs text-gray-500">
                          <span className={`px-2 py-1 rounded-full ${getDifficultyColor(suggestion.implementation.difficulty)}`}>
                            {suggestion.implementation.difficulty}
                          </span>
                          <span className="flex items-center gap-1">
                            <FaClock />
                            {suggestion.implementation.estimatedTime}
                          </span>
                        </div>
                        
                        <AccessibleButton
                          size="sm"
                          variant="outline"
                          onClick={() => onApplySuggestion?.(suggestion)}
                          ariaLabel={createAriaLabel(`Apply suggestion: ${suggestion.title}`, 'AI assistance')}
                        >
                          Apply
                        </AccessibleButton>
                      </div>
                      
                      {suggestion.culturalTags.length > 0 && (
                        <div className="mt-2 flex flex-wrap gap-1">
                          {suggestion.culturalTags.map((tag, index) => (
                            <span key={index} className="px-2 py-1 bg-gray-100 text-gray-600 rounded-full text-xs">
                              #{tag}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </Card>

      {/* Kenya-First Footer */}
      <div className="text-center text-xs text-gray-500 py-2">
        🇰🇪 Powered by Kenya-first AI intelligence
      </div>
    </div>
  );
};

export default AISuggestionsPanel;
