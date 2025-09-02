'use client';

import { useState } from 'react';
import Card from '@/components/Card';
import LoadingStates from '@/components/ui/LoadingStates';
import ErrorStates from '@/components/ui/ErrorStates';
import { FaGear, FaPencilAlt, FaEye, FaFlag, FaMountain, FaTrashCan, FaCircleUser, FaUserPlus, FaUsers } from 'react-icons/fa6';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorintent
// [CONTEXT]: Team collaboration page with Kenya-first design and mobile-first approach
// [GOAL]: Create comprehensive team management interface with cultural authenticity
// [TASK]: Implement team management with proper user controls and responsive design

interface TeamMember {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'editor' | 'viewer';
  avatar?: string;
  lastActive: string;
  status: 'active' | 'inactive' | 'pending';
  joinedAt: string;
}

export default function TeamPage() {
  const [members, setMembers] = useState<TeamMember[]>([
    {
      id: '1',
      name: 'Grace Wanjiku',
      email: 'grace@shujaa.studio',
      role: 'admin',
      lastActive: '2 minutes ago',
      status: 'active',
      joinedAt: '2024-01-15'
    },
    {
      id: '2',
      name: 'David Ochieng',
      email: 'david@shujaa.studio',
      role: 'editor',
      lastActive: '1 hour ago',
      status: 'active',
      joinedAt: '2024-01-20'
    },
    {
      id: '3',
      name: 'Amina Hassan',
      email: 'amina@shujaa.studio',
      role: 'viewer',
      lastActive: '1 day ago',
      status: 'inactive',
      joinedAt: '2024-02-01'
    }
  ]);

  const [showInviteModal, setShowInviteModal] = useState(false);
  const [inviteEmail, setInviteEmail] = useState('');
  const [inviteRole, setInviteRole] = useState<'admin' | 'editor' | 'viewer'>('viewer');

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'admin': return 'bg-red-100 text-red-800';
      case 'editor': return 'bg-blue-100 text-blue-800';
      case 'viewer': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'inactive': return 'bg-gray-100 text-gray-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const handleInviteMember = () => {
    if (!inviteEmail.trim()) {
      alert('Please enter an email address');
      return;
    }

    // Simulate sending invitation
    console.log('Inviting member:', { email: inviteEmail, role: inviteRole });
    alert(`Invitation sent to ${inviteEmail} as ${inviteRole}!`);
    setInviteEmail('');
    setShowInviteModal(false);
  };

  return (
    <div className="space-y-6">
      {/* Kenya-First Header */}
      <div className="bg-gradient-to-r from-green-600 via-red-600 to-black p-6 rounded-xl text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <FaUsers className="text-3xl" />
            <div>
              <h1 className="text-2xl font-bold">Team Collaboration 🇰🇪</h1>
              <p className="text-green-100">Manage your Kenya-first content creation team</p>
            </div>
          </div>
          <div className="hidden md:block">
            <FaMountain className="text-4xl text-yellow-300" />
          </div>
        </div>
      </div>

      {/* Team Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Total Members</p>
              <p className="text-2xl font-bold text-gray-800">{members.length}</p>
            </div>
            <FaUsers className="text-3xl text-blue-600" />
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Active Now</p>
              <p className="text-2xl font-bold text-gray-800">{members.filter(m => m.status === 'active').length}</p>
            </div>
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Admins</p>
              <p className="text-2xl font-bold text-gray-800">{members.filter(m => m.role === 'admin').length}</p>
            </div>
            <FaGear className="text-3xl text-red-600" />
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Pending</p>
              <p className="text-2xl font-bold text-gray-800">{members.filter(m => m.status === 'pending').length}</p>
            </div>
            <FaUserPlus className="text-3xl text-yellow-600" />
          </div>
        </Card>
      </div>

      {/* Team Management */}
      <Card className="p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-800">Team Members</h2>
          <button
            onClick={() => setShowInviteModal(true)}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors duration-200"
          >
            <FaUserPlus />
            <span>Invite Member</span>
          </button>
        </div>

        {/* Members List */}
        <div className="space-y-4">
          {members.map((member) => (
            <div key={member.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                  <FaCircleUser className="text-2xl text-green-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-800">{member.name}</h3>
                  <p className="text-sm text-gray-600">{member.email}</p>
                  <p className="text-xs text-gray-500">Last active: {member.lastActive}</p>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <span className={`px-2 py-1 text-xs rounded-full font-medium ${getRoleColor(member.role)}`}>
                  {member.role}
                </span>
                <span className={`px-2 py-1 text-xs rounded-full font-medium ${getStatusColor(member.status)}`}>
                  {member.status}
                </span>
                
                <div className="flex space-x-1">
                  <button className="p-2 text-gray-600 hover:text-blue-600 transition-colors duration-200">
                    <FaEye className="text-sm" />
                  </button>
                  <button className="p-2 text-gray-600 hover:text-green-600 transition-colors duration-200">
                    <FaPencil className="text-sm" />
                  </button>
                  <button className="p-2 text-gray-600 hover:text-red-600 transition-colors duration-200">
                    <FaTrashCan className="text-sm" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Team Permissions */}
      <Card className="p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Role Permissions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="border border-red-200 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-3">
              <div className="w-3 h-3 bg-red-500 rounded-full"></div>
              <h3 className="font-semibold text-red-800">Admin</h3>
            </div>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Full system access</li>
              <li>• Manage team members</li>
              <li>• Configure settings</li>
              <li>• Access analytics</li>
              <li>• Generate content</li>
            </ul>
          </div>

          <div className="border border-blue-200 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-3">
              <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
              <h3 className="font-semibold text-blue-800">Editor</h3>
            </div>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Generate content</li>
              <li>• Edit projects</li>
              <li>• Access gallery</li>
              <li>• Use audio studio</li>
              <li>• View analytics</li>
            </ul>
          </div>

          <div className="border border-green-200 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-3">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <h3 className="font-semibold text-green-800">Viewer</h3>
            </div>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• View content</li>
              <li>• Browse gallery</li>
              <li>• Download files</li>
              <li>• Basic analytics</li>
              <li>• Comment on projects</li>
            </ul>
          </div>
        </div>
      </Card>

      {/* Invite Modal */}
      {showInviteModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Invite Team Member</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  value={inviteEmail}
                  onChange={(e) => setInviteEmail(e.target.value)}
                  placeholder="colleague@example.com"
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Role
                </label>
                <select
                  value={inviteRole}
                  onChange={(e) => setInviteRole(e.target.value as 'admin' | 'editor' | 'viewer')}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                >
                  <option value="viewer">Viewer</option>
                  <option value="editor">Editor</option>
                  <option value="admin">Admin</option>
                </select>
              </div>
            </div>

            <div className="flex space-x-3 mt-6">
              <button
                onClick={() => setShowInviteModal(false)}
                className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded-lg transition-colors duration-200"
              >
                Cancel
              </button>
              <button
                onClick={handleInviteMember}
                className="flex-1 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors duration-200"
              >
                Send Invite
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Cultural Footer */}
      <div className="bg-gradient-to-r from-yellow-400 via-red-500 to-green-600 p-4 rounded-lg text-white text-center">
        <div className="flex items-center justify-center space-x-2">
          <FaFlag className="text-lg" />
          <span className="font-medium">Building Kenya-first content teams • Harambee spirit</span>
          <FaUsers className="text-lg" />
        </div>
      </div>
    </div>
  );
}

