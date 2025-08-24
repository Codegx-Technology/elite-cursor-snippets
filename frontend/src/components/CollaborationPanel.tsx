// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Phase 4 - Real-time collaboration UI with Kenya-first design
// [GOAL]: Multi-user collaboration interface with cultural authenticity
// [TASK]: Create collaboration panel with presence indicators and real-time features

'use client';

import React, { useState, useEffect } from 'react';
import { useCollaboration, UserPresence } from '@/lib/collaboration';
import { useAriaUtils } from '@/hooks/useAccessibility';
import Card from '@/components/ui/Card';
import AccessibleButton from '@/components/AccessibleButton';
import { FaUsers, FaComments, FaCursor, FaVideo, FaEdit } from 'react-icons/fa';

interface CollaborationPanelProps {
  roomId: string;
  userId: string;
  userName: string;
  kenyaProfile?: {
    region: string;
    preferredLanguage: 'en' | 'sw';
    timezone: string;
  };
}

interface Comment {
  userName: string;
  timestamp: string;
  kenyaContext?: {
    region: string;
  };
  data: {
    content: string;
  };
}

const CollaborationPanel: React.FC<CollaborationPanelProps> = ({
  roomId,
  userId,
  userName,
  kenyaProfile
}) => {
  const { createAriaLabel } = useAriaUtils();
  const [showComments, setShowComments] = useState(false);
  const [newComment, setNewComment] = useState('');
  const [comments, setComments] = useState<Comment[]>([]);

  const {
    collaborators,
    isConnected,
    connectionError,
    manager,
    sendComment,
    sendPresence
  } = useCollaboration({
    roomId,
    userId,
    userName,
    kenyaProfile
  });

  useEffect(() => {
    if (manager) {
      manager.on('event', (event: Comment) => {
        if (event.type === 'comment') {
          setComments(prev => [...prev, event]);
        }
      });
    }
  }, [manager]);

  const handleSendComment = () => {
    if (newComment.trim()) {
      sendComment('general', newComment);
      setNewComment('');
    }
  };

  const getStatusColor = (status: UserPresence['status']) => {
    switch (status) {
      case 'active': return 'bg-green-500';
      case 'idle': return 'bg-yellow-500';
      case 'away': return 'bg-gray-500';
      default: return 'bg-gray-500';
    }
  };

  const getRegionFlag = (region?: string) => {
    const regionFlags: { [key: string]: string } = {
      'Nairobi': '🏙️',
      'Mombasa': '🏖️',
      'Kisumu': '🏞️',
      'Nakuru': '🦩',
      'Eldoret': '🏃‍♂️'
    };
    return regionFlags[region || 'Nairobi'] || '🇰🇪';
  };

  if (connectionError) {
    return (
      <Card>
        <div className="p-4 text-center">
          <div className="text-red-500 mb-2">🇰🇪 Collaboration Unavailable</div>
          <p className="text-sm text-gray-600">{connectionError}</p>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {/* Connection Status */}
      <Card>
        <div className="p-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-semibold text-gray-800 flex items-center gap-2">
              <FaUsers className="text-green-600" />
              Collaboration 🇰🇪
            </h3>
            <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
          </div>
          
          <div className="text-sm text-gray-600">
            {isConnected ? (
              <span className="text-green-600">✅ Connected - Harambee!</span>
            ) : (
              <span className="text-red-600">❌ Disconnected</span>
            )}
          </div>
        </div>
      </Card>

      {/* Active Collaborators */}
      <Card>
        <div className="p-4">
          <h4 className="font-medium text-gray-800 mb-3 flex items-center gap-2">
            <FaUsers className="text-blue-600" />
            Active Users ({collaborators.length + 1})
          </h4>
          
          <div className="space-y-2">
            {/* Current User */}
            <div className="flex items-center gap-3 p-2 bg-green-50 rounded-lg">
              <div className="relative">
                <div className="w-8 h-8 bg-green-600 rounded-full flex items-center justify-center text-white text-sm font-bold">
                  {userName.charAt(0).toUpperCase()}
                </div>
                <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-white" />
              </div>
              <div className="flex-1">
                <div className="font-medium text-sm">{userName} (You)</div>
                <div className="text-xs text-gray-500 flex items-center gap-1">
                  {getRegionFlag(kenyaProfile?.region)} {kenyaProfile?.region || 'Nairobi'}
                </div>
              </div>
            </div>

            {/* Other Collaborators */}
            {collaborators.map((user) => (
              <div key={user.userId} className="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg">
                <div className="relative">
                  <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-bold">
                    {user.userName.charAt(0).toUpperCase()}
                  </div>
                  <div className={`absolute -bottom-1 -right-1 w-3 h-3 rounded-full border-2 border-white ${getStatusColor(user.status)}`} />
                </div>
                <div className="flex-1">
                  <div className="font-medium text-sm">{user.userName}</div>
                  <div className="text-xs text-gray-500 flex items-center gap-1">
                    {getRegionFlag(user.kenyaProfile?.region)} {user.kenyaProfile?.region || 'Kenya'}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </Card>

      {/* Comments Section */}
      <Card>
        <div className="p-4">
          <div className="flex items-center justify-between mb-3">
            <h4 className="font-medium text-gray-800 flex items-center gap-2">
              <FaComments className="text-purple-600" />
              Comments ({comments.length})
            </h4>
            <AccessibleButton
              size="sm"
              variant="ghost"
              onClick={() => setShowComments(!showComments)}
              ariaLabel={createAriaLabel('Toggle comments', 'collaboration')}
            >
              {showComments ? 'Hide' : 'Show'}
            </AccessibleButton>
          </div>

          {showComments && (
            <div className="space-y-3">
              {/* Comments List */}
              <div className="max-h-40 overflow-y-auto space-y-2">
                {comments.length === 0 ? (
                  <div className="text-center text-gray-500 text-sm py-4">
                    🇰🇪 No comments yet - Start the conversation!
                  </div>
                ) : (
                  comments.map((comment, index) => (
                    <div key={index} className="bg-gray-50 rounded-lg p-3">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-medium text-sm">{comment.userName}</span>
                        <span className="text-xs text-gray-500">
                          {new Date(comment.timestamp).toLocaleTimeString()}
                        </span>
                        {comment.kenyaContext?.region && (
                          <span className="text-xs">
                            {getRegionFlag(comment.kenyaContext.region)}
                          </span>
                        )}
                      </div>
                      <p className="text-sm text-gray-700">{comment.data.content}</p>
                    </div>
                  ))
                )}
              </div>

              {/* New Comment Input */}
              <div className="flex gap-2">
                <input
                  type="text"
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  placeholder="Add a comment... 🇰🇪"
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                  onKeyPress={(e) => e.key === 'Enter' && handleSendComment()}
                />
                <AccessibleButton
                  size="sm"
                  variant="kenya"
                  onClick={handleSendComment}
                  disabled={!newComment.trim()}
                  ariaLabel={createAriaLabel('Send comment', 'collaboration')}
                >
                  Send
                </AccessibleButton>
              </div>
            </div>
          )}
        </div>
      </Card>

      {/* Collaboration Tools */}
      <Card>
        <div className="p-4">
          <h4 className="font-medium text-gray-800 mb-3">Collaboration Tools</h4>
          
          <div className="grid grid-cols-2 gap-2">
            <AccessibleButton
              size="sm"
              variant="outline"
              icon={<FaCursor />}
              ariaLabel={createAriaLabel('Show cursors', 'collaboration')}
              culturalContext="Real-time cursor tracking"
            >
              Cursors
            </AccessibleButton>
            
            <AccessibleButton
              size="sm"
              variant="outline"
              icon={<FaEdit />}
              ariaLabel={createAriaLabel('Text editing', 'collaboration')}
              culturalContext="Collaborative text editing"
            >
              Text Edit
            </AccessibleButton>
            
            <AccessibleButton
              size="sm"
              variant="outline"
              icon={<FaVideo />}
              ariaLabel={createAriaLabel('Video collaboration', 'collaboration')}
              culturalContext="Collaborative video editing"
            >
              Video
            </AccessibleButton>
            
            <AccessibleButton
              size="sm"
              variant="outline"
              onClick={() => sendPresence('active')}
              ariaLabel={createAriaLabel('Update presence', 'collaboration')}
              culturalContext="Update your presence status"
            >
              Present
            </AccessibleButton>
          </div>
        </div>
      </Card>

      {/* Kenya-First Footer */}
      <div className="text-center text-xs text-gray-500 py-2">
        🇰🇪 Harambee - Working together builds Kenya
      </div>
    </div>
  );
};

export default CollaborationPanel;
