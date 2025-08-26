// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Phase 4 - Real-time collaboration infrastructure for enterprise SaaS
// [GOAL]: Multi-user collaboration with Kenya-first cultural considerations
// [TASK]: Implement WebSocket-based real-time collaboration system

'use client';

import { useEffect, useCallback, useState, useRef } from 'react';

// Collaboration event types
export interface CollaborationEvent {
  id: string;
  type: 'cursor_move' | 'text_edit' | 'video_edit' | 'comment' | 'presence';
  userId: string;
  userName: string;
  timestamp: number;
  data: unknown;
  kenyaContext?: {
    region?: string;
    language?: 'en' | 'sw';
    culturalNote?: string;
  };
}

// User presence information
export interface UserPresence {
  userId: string;
  userName: string;
  avatar?: string;
  cursor?: { x: number; y: number };
  activeElement?: string;
  status: 'active' | 'idle' | 'away';
  kenyaProfile?: {
    region: string;
    preferredLanguage: 'en' | 'sw';
    timezone: string;
  };
}

// Real-time collaboration manager
export class CollaborationManager {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private heartbeatInterval: NodeJS.Timeout | null = null;
  private eventListeners: Map<string, ((data: unknown) => void)[]> = new Map();
  private currentUser: UserPresence | null = null;
  private collaborators: Map<string, UserPresence> = new Map();

  constructor(private config: {
    wsUrl: string;
    roomId: string;
    userId: string;
    userName: string;
    kenyaProfile?: UserPresence['kenyaProfile'];
  }) {}

  // Initialize collaboration connection
  async connect(): Promise<void> {
    try {
      const wsUrl = `${this.config.wsUrl}?room=${this.config.roomId}&user=${this.config.userId}`;
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        console.log('🇰🇪 Collaboration connected - Harambee!');
        this.reconnectAttempts = 0;
        this.startHeartbeat();
        this.sendPresence('active');
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.handleMessage(data);
        } catch (error) {
          console.error('🇰🇪 Failed to parse collaboration message:', error);
        }
      };

      this.ws.onclose = () => {
        console.log('🇰🇪 Collaboration disconnected');
        this.stopHeartbeat();
        this.attemptReconnect();
      };

      this.ws.onerror = (error) => {
        console.error('🇰🇪 Collaboration error:', error);
      };

    } catch (error) {
      console.error('🇰🇪 Failed to connect to collaboration service:', error);
      throw error;
    }
  }

  // Send collaboration event
  sendEvent(event: Omit<CollaborationEvent, 'id' | 'userId' | 'userName' | 'timestamp'>): void {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      console.warn('🇰🇪 Collaboration not connected');
      return;
    }

    const fullEvent: CollaborationEvent = {
      ...event,
      id: this.generateEventId(),
      userId: this.config.userId,
      userName: this.config.userName,
      timestamp: Date.now(),
      kenyaContext: {
        region: this.config.kenyaProfile?.region || 'Nairobi',
        language: this.config.kenyaProfile?.preferredLanguage || 'en',
        culturalNote: 'Kenya-first collaboration'
      }
    };

    this.ws.send(JSON.stringify(fullEvent));
  }

  // Handle incoming messages
  private handleMessage(data: { type: string; event?: unknown; user?: UserPresence; userId?: string }): void {
    switch (data.type) {
      case 'collaboration_event':
        this.emit('event', data.event);
        break;
      case 'user_joined':
        this.handleUserJoined(data.user);
        break;
      case 'user_left':
        this.handleUserLeft(data.userId);
        break;
      case 'presence_update':
        this.handlePresenceUpdate(data.user);
        break;
      case 'heartbeat_response':
        // Keep connection alive
        break;
      default:
        console.warn('🇰🇪 Unknown collaboration message type:', data.type);
    }
  }

  // User presence management
  private handleUserJoined(user: UserPresence): void {
    this.collaborators.set(user.userId, user);
    this.emit('user_joined', user);
    
    // Kenya-first welcome message
    if (user.kenyaProfile?.region) {
      console.log(`🇰🇪 ${user.userName} joined from ${user.kenyaProfile.region} - Karibu!`);
    }
  }

  private handleUserLeft(userId: string): void {
    const user = this.collaborators.get(userId);
    this.collaborators.delete(userId);
    this.emit('user_left', { userId, user });
    
    if (user) {
      console.log(`🇰🇪 ${user.userName} left - Kwaheri!`);
    }
  }

  private handlePresenceUpdate(user: UserPresence): void {
    this.collaborators.set(user.userId, user);
    this.emit('presence_update', user);
  }

  // Send presence update
  sendPresence(status: UserPresence['status'], additionalData?: Partial<UserPresence>): void {
    const presence: UserPresence = {
      userId: this.config.userId,
      userName: this.config.userName,
      status,
      kenyaProfile: this.config.kenyaProfile,
      ...additionalData
    };

    this.currentUser = presence;
    this.sendEvent({
      type: 'presence',
      data: presence
    });
  }

  // Cursor tracking
  sendCursorMove(x: number, y: number, element?: string): void {
    this.sendEvent({
      type: 'cursor_move',
      data: { x, y, element }
    });
  }

  // Text editing collaboration
  sendTextEdit(elementId: string, operation: unknown): void {
    this.sendEvent({
      type: 'text_edit',
      data: { elementId, operation }
    });
  }

  // Video editing collaboration
  sendVideoEdit(videoId: string, operation: unknown): void {
    this.sendEvent({
      type: 'video_edit',
      data: { videoId, operation }
    });
  }

  // Comments system
  sendComment(targetId: string, content: string, position?: { x: number; y: number }): void {
    this.sendEvent({
      type: 'comment',
      data: { targetId, content, position }
    });
  }

  // Event system
  on(event: string, callback: (data: unknown) => void): void {
    if (!this.eventListeners.has(event)) {
      this.eventListeners.set(event, []);
    }
    this.eventListeners.get(event)!.push(callback);
  }

  off(event: string, callback: (data: unknown) => void): void {
    const listeners = this.eventListeners.get(event);
    if (listeners) {
      const index = listeners.indexOf(callback);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    }
  }

  private emit(event: string, data: unknown): void {
    const listeners = this.eventListeners.get(event);
    if (listeners) {
      listeners.forEach(callback => callback(data));
    }
  }

  // Connection management
  private startHeartbeat(): void {
    this.heartbeatInterval = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: 'heartbeat' }));
      }
    }, 30000); // 30 seconds
  }

  private stopHeartbeat(): void {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }

  private attemptReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('🇰🇪 Max reconnection attempts reached');
      this.emit('connection_failed', {});
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
    
    console.log(`🇰🇪 Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);
    
    setTimeout(() => {
      this.connect().catch(error => {
        console.error('🇰🇪 Reconnection failed:', error);
      });
    }, delay);
  }

  private generateEventId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  // Cleanup
  disconnect(): void {
    this.stopHeartbeat();
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.collaborators.clear();
    this.eventListeners.clear();
  }

  // Getters
  getCollaborators(): UserPresence[] {
    return Array.from(this.collaborators.values());
  }

  getCurrentUser(): UserPresence | null {
    return this.currentUser;
  }

  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }
}

// React hook for collaboration
export const useCollaboration = (config: {
  roomId: string;
  userId: string;
  userName: string;
  kenyaProfile?: UserPresence['kenyaProfile'];
}) => {
  const [manager] = useState(() => new CollaborationManager({
    ...config,
    wsUrl: process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8001/ws'
  }));
  
  const [collaborators, setCollaborators] = useState<UserPresence[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [connectionError, setConnectionError] = useState<string | null>(null);

  useEffect(() => {
    const handleUserJoined = (user: UserPresence) => {
      setCollaborators(prev => [...prev.filter(u => u.userId !== user.userId), user]);
    };

    const handleUserLeft = ({ userId }: { userId: string }) => {
      setCollaborators(prev => prev.filter(u => u.userId !== userId));
    };

    const handlePresenceUpdate = (user: UserPresence) => {
      setCollaborators(prev => prev.map(u => u.userId === user.userId ? user : u));
    };

    const handleConnectionFailed = () => {
      setConnectionError('Failed to connect to collaboration service');
      setIsConnected(false);
    };

    manager.on('user_joined', handleUserJoined);
    manager.on('user_left', handleUserLeft);
    manager.on('presence_update', handlePresenceUpdate);
    manager.on('connection_failed', handleConnectionFailed);

    // Connect
    manager.connect().then(() => {
      setIsConnected(true);
      setConnectionError(null);
    }).catch(error => {
      setConnectionError(error.message);
      setIsConnected(false);
    });

    return () => {
      manager.disconnect();
    };
  }, [manager]);

  return {
    manager,
    collaborators,
    isConnected,
    connectionError,
    sendEvent: manager.sendEvent.bind(manager),
    sendCursorMove: manager.sendCursorMove.bind(manager),
    sendTextEdit: manager.sendTextEdit.bind(manager),
    sendVideoEdit: manager.sendVideoEdit.bind(manager),
    sendComment: manager.sendComment.bind(manager),
    sendPresence: manager.sendPresence.bind(manager)
  };
};
