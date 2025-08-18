'use client';

import React from 'react';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix
// [CONTEXT]: Profile page main component with Kenya-first design tokens
// [GOAL]: Provide a basic, styled user profile block to verify routing and CSS

export default function UserProfile() {
  return (
    <section className="max-w-3xl mx-auto p-6">
      <div className="elite-card p-8">
        <header className="mb-6">
          <h1 className="section-title">Your Profile</h1>
          <p className="section-subtitle">Manage your account details</p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm text-soft-text mb-1">Full Name</label>
            <input className="form-input" placeholder="John Doe" />
          </div>
          <div>
            <label className="block text-sm text-soft-text mb-1">Email</label>
            <input className="form-input" placeholder="john@example.com" />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm text-soft-text mb-1">Bio</label>
            <textarea className="form-input min-h-[100px]" placeholder="Tell us about yourself" />
          </div>
        </div>

        <div className="mt-8 flex gap-3">
          <button className="btn-primary">Save Changes</button>
          <button className="btn-secondary">Cancel</button>
        </div>
      </div>
    </section>
  );
}
