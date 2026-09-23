'use client';

import { useEffect, useState } from 'react';

import { AuthCard } from '@/components/auth/auth-card';

type SessionUser = {
  id: string;
  email: string;
  full_name?: string | null;
  organization_id?: string | null;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';
const ACCESS_TOKEN_KEY = 'retainai_access_token';

export function AppShell() {
  const [sessionUser, setSessionUser] = useState<SessionUser | null>(null);

  useEffect(() => {
    const loadSession = async () => {
      const token = localStorage.getItem(ACCESS_TOKEN_KEY);
      if (!token) {
        setSessionUser(null);
        return;
      }

      try {
        const response = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          localStorage.removeItem(ACCESS_TOKEN_KEY);
          setSessionUser(null);
          return;
        }

        const payload = await response.json();
        setSessionUser(payload.user ?? null);
      } catch {
        localStorage.removeItem(ACCESS_TOKEN_KEY);
        setSessionUser(null);
      }
    };

    loadSession();
  }, []);

  const handleSignOut = () => {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    setSessionUser(null);
  };

  return (
    <main style={{ maxWidth: 1200, margin: '0 auto', padding: '32px 20px 80px' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24, gap: 16, flexWrap: 'wrap' }}>
        <div>
          <div style={{ fontSize: 12, letterSpacing: 1.2, textTransform: 'uppercase', color: '#5a6781', fontWeight: 700 }}>
            RetainAI
          </div>
          <h1 style={{ margin: '8px 0 0', fontSize: 32 }}>{sessionUser ? 'Workspace overview' : 'Retention intelligence foundation'}</h1>
        </div>
        <div style={{ display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
          {sessionUser ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '8px 12px', border: '1px solid #dfe7f1', borderRadius: 999, background: '#f6f9ff' }}>
              <span style={{ fontWeight: 700, color: '#14213d' }}>{sessionUser.full_name ?? sessionUser.email}</span>
              <button
                type="button"
                onClick={handleSignOut}
                style={{ border: 'none', background: '#eef2ff', color: '#2148c0', borderRadius: 999, padding: '6px 10px', cursor: 'pointer', fontWeight: 700 }}
              >
                Sign out
              </button>
            </div>
          ) : (
            <div style={{ fontSize: 14, color: '#5a6781', fontWeight: 600 }}>Signed out</div>
          )}
          {['Overview', 'Customers', 'Actions', 'Analytics', 'Settings'].map((item) => (
            <button
              key={item}
              style={{
                border: '1px solid #dfe7f1',
                background: '#ffffff',
                borderRadius: 10,
                padding: '10px 14px',
                color: '#14213d',
                cursor: 'pointer',
              }}
            >
              {item}
            </button>
          ))}
        </div>
      </header>

      {sessionUser ? (
        <AuthenticatedWorkspace user={sessionUser} />
      ) : (
        <section style={{ marginTop: 28 }}>
          <AuthCard onAuthSuccess={(user) => setSessionUser(user)} />
        </section>
      )}
    </main>
  );
}

function AuthenticatedWorkspace({ user }: { user: SessionUser }) {
  const displayName = user.full_name ?? user.email.split('@')[0] ?? 'Operator';

  return (
    <>
      <section style={{ marginBottom: 24, background: '#ffffff', border: '1px solid #dfe7f1', borderRadius: 18, padding: 22, boxShadow: '0 12px 30px rgba(20, 33, 61, 0.04)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', gap: 16, alignItems: 'center', flexWrap: 'wrap' }}>
          <div>
            <div style={{ fontSize: 12, letterSpacing: 1.2, textTransform: 'uppercase', color: '#5a6781', fontWeight: 700 }}>
              Active workspace
            </div>
            <h2 style={{ margin: '8px 0 0', fontSize: 30, color: '#14213d' }}>Welcome back, {displayName}</h2>
          </div>
          <div style={{ padding: '10px 14px', background: '#eef4ff', borderRadius: 12, color: '#2148c0', fontWeight: 700 }}>
            {user.organization_id ? 'Tenant connected' : 'No tenant linked'}
          </div>
        </div>
      </section>

      <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 16 }}>
        {[
          { label: 'Total customers', value: '1,248' },
          { label: 'At risk', value: '143' },
          { label: 'Critical', value: '27' },
          { label: 'Revenue at risk', value: '$184.6K' },
        ].map((tile) => (
          <div key={tile.label} style={{ background: '#ffffff', border: '1px solid #dfe7f1', borderRadius: 16, padding: 18, boxShadow: '0 10px 30px rgba(20, 33, 61, 0.05)' }}>
            <div style={{ fontSize: 12, textTransform: 'uppercase', color: '#5a6781', letterSpacing: 0.8 }}>{tile.label}</div>
            <div style={{ fontSize: 28, fontWeight: 700, marginTop: 8 }}>{tile.value}</div>
          </div>
        ))}
      </section>

      <section style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 16, marginTop: 24 }}>
        <div style={{ background: '#ffffff', border: '1px solid #dfe7f1', borderRadius: 16, padding: 20 }}>
          <h2 style={{ marginBottom: 12 }}>Operational overview</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: 8, alignItems: 'end', minHeight: 180 }}>
            {[30, 50, 65, 48, 72, 90].map((height, index) => (
              <div key={index} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8 }}>
                <div style={{ width: '100%', height: height, background: index % 2 === 0 ? '#2148c0' : '#dfe7f1', borderRadius: 8 }} />
                <span style={{ fontSize: 12, color: '#5a6781' }}>Q{index + 1}</span>
              </div>
            ))}
          </div>
        </div>

        <div style={{ background: '#ffffff', border: '1px solid #dfe7f1', borderRadius: 16, padding: 20 }}>
          <h2 style={{ marginBottom: 14 }}>Priority actions</h2>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'grid', gap: 10 }}>
            {[
              'Review 27 critical customers',
              'Schedule 6 intervention follow-ups',
              'Audit recent data imports',
            ].map((item) => (
              <li key={item} style={{ padding: '12px 14px', background: '#eef3f8', borderRadius: 10, color: '#14213d' }}>{item}</li>
            ))}
          </ul>
        </div>
      </section>
    </>
  );
}
