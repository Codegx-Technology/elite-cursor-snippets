// frontend/components/User/UserProfile.tsx (Conceptual)

import React, { useState, useEffect } 'react';
import axios from 'axios';
import { useRouter } from 'next/router';

interface UserProfileData {
  username: string;
  email: string;
  full_name?: string;
  bio?: string;
  // Add other profile fields as needed
}

const UserProfile: React.FC = () => {
  const [profile, setProfile] = useState<UserProfileData | null>(null);
  const [fullName, setFullName] = useState('');
  const [bio, setBio] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const router = useRouter();

  const getAuthHeaders = () => {
    const token = localStorage.getItem('jwt_token');
    if (!token) {
      router.push('/login');
      return {};
    }
    return { Authorization: `Bearer ${token}` };
  };

  useEffect(() => {
    const fetchProfile = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const headers = getAuthHeaders();
        if (!headers.Authorization) return;

        const response = await axios.get('http://localhost:8000/users/me', { headers });
        setProfile(response.data);
        setFullName(response.data.full_name || '');
        setBio(response.data.bio || '');

      } catch (err: any) {
        if (err.response && err.response.data && err.response.data.detail) {
          setError(err.response.data.detail);
        } else {
          setError('Failed to load profile. Please try again.');
        }
        console.error('Profile fetch error:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setError(null);
    setSuccessMessage(null);

    try {
      const headers = getAuthHeaders();
      if (!headers.Authorization) return;

      const updateData: { full_name?: string; bio?: string } = {};
      if (fullName !== (profile?.full_name || '')) {
        updateData.full_name = fullName;
      }
      if (bio !== (profile?.bio || '')) {
        updateData.bio = bio;
      }

      if (Object.keys(updateData).length === 0) {
        setSuccessMessage('No changes to save.');
        return;
      }

      const response = await axios.put('http://localhost:8000/users/me', updateData, { headers });
      setProfile(response.data); // Update local state with new profile
      setSuccessMessage('Profile updated successfully!');

    } catch (err: any) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('An unexpected error occurred while saving. Please try again.');
      }
      console.error('Profile save error:', err);
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <div className="elite-container my-10 text-center">
        <div className="loading-spinner mx-auto mb-4"></div>
        <p className="text-soft-text">Loading profile...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="elite-container my-10 text-center text-red-500">
        <p>Error: {error}</p>
      </div>
    );
  }

  if (!profile) {
    return <div className="elite-container my-10 text-center text-soft-text">No profile data available.</div>;
  }

  return (
    <div className="elite-card p-8 max-w-md mx-auto my-10 rounded-xl shadow-lg">
      <h2 className="section-title text-center mb-6">My Profile</h2>
      <form onSubmit={handleSave}>
        {successMessage && <p className="text-green-500 text-sm mb-4">{successMessage}</p>}
        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
        
        <div className="mb-4">
          <label htmlFor="username" className="block text-soft-text text-sm font-medium mb-2">Username</label>
          <input
            type="text"
            id="username"
            className="form-input w-full p-3 rounded-lg bg-gray-100 cursor-not-allowed"
            value={profile.username}
            disabled // Username is not editable
          />
        </div>
        <div className="mb-4">
          <label htmlFor="email" className="block text-soft-text text-sm font-medium mb-2">Email</label>
          <input
            type="email"
            id="email"
            className="form-input w-full p-3 rounded-lg bg-gray-100 cursor-not-allowed"
            value={profile.email}
            disabled // Email is not editable
          />
        </div>
        <div className="mb-4">
          <label htmlFor="fullName" className="block text-soft-text text-sm font-medium mb-2">Full Name</label>
          <input
            type="text"
            id="fullName"
            className="form-input w-full p-3 rounded-lg"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
          />
        </div>
        <div className="mb-6">
          <label htmlFor="bio" className="block text-soft-text text-sm font-medium mb-2">Bio</label>
          <textarea
            id="bio"
            className="form-input w-full p-3 rounded-lg h-24"
            value={bio}
            onChange={(e) => setBio(e.target.value)}
          ></textarea>
        </div>
        <button
          type="submit"
          className="btn-primary w-full py-3 rounded-lg text-white font-semibold flex items-center justify-center"
          disabled={isSaving}
        >
          {isSaving ? (
            <div className="loading-spinner mr-2"></div>
          ) : (
            'Save Changes'
          )}
        </button>
      </form>
    </div>
  );
};

export default UserProfile;