
import { useState, useEffect } from 'react';
import { useUserProfile, UserProfileData } from '@/hooks/useUserProfile';
import { FaSpinner } from 'react-icons/fa';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Reusable user profile component
// [GOAL]: Provide a clean and reusable component for displaying and updating user profiles

export default function UserProfile() {
  const { profile, isLoading, isSaving, error, successMessage, updateProfile } = useUserProfile();
  const [fullName, setFullName] = useState('');
  const [bio, setBio] = useState('');

  useEffect(() => {
    if (profile) {
      setFullName(profile.full_name || '');
      setBio(profile.bio || '');
    }
  }, [profile]);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    const data: Partial<UserProfileData> = {};
    if (fullName !== (profile?.full_name || '')) {
      data.full_name = fullName;
    }
    if (bio !== (profile?.bio || '')) {
      data.bio = bio;
    }
    if (Object.keys(data).length > 0) {
      await updateProfile(data);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <FaSpinner className="w-8 h-8 text-green-600 animate-spin mx-auto mb-4" />
          <span className="text-gray-600 font-medium">Loading profile...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-500 text-center">
        <p>Error: {error}</p>
      </div>
    );
  }

  if (!profile) {
    return <div className="text-center text-soft-text">No profile data available.</div>;
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
            disabled
          />
        </div>
        <div className="mb-4">
          <label htmlFor="email" className="block text-soft-text text-sm font-medium mb-2">Email</label>
          <input
            type="email"
            id="email"
            className="form-input w-full p-3 rounded-lg bg-gray-100 cursor-not-allowed"
            value={profile.email}
            disabled
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
            <FaSpinner className="animate-spin mr-2" />
          ) : (
            'Save Changes'
          )}
        </button>
      </form>
    </div>
  );
}

