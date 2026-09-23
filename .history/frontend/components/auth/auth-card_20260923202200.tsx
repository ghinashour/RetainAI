'use client';

import { type CSSProperties, type FormEvent, useState } from 'react';

type AuthMode = 'login' | 'register';

type SessionUser = {
  id: string;
  email: string;
  full_name?: string | null;
  organization_id?: string | null;
};

type Notice = {
  kind: 'success' | 'error';
  text: string;
};

type AuthCardProps = {
  onAuthSuccess?: (user: SessionUser) => void;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';
const ACCESS_TOKEN_KEY = 'retainai_access_token';

export function AuthCard({ onAuthSuccess }: AuthCardProps) {
  const [mode, setMode] = useState<AuthMode>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [organizationName, setOrganizationName] = useState('');
  const [fullName, setFullName] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [notice, setNotice] = useState<Notice | null>(null);

  const submitForm = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsSubmitting(true);
    setNotice(null);

    try {
      const endpoint = mode === 'login' ? '/api/v1/auth/login' : '/api/v1/auth/register';
      const payload =
        mode === 'login'
          ? { email, password }
          : {
              email,
              password,
              organization_name: organizationName,
              full_name: fullName || undefined,
            };

      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();
      if (!response.ok) {
        const detail = Array.isArray(data?.detail) ? data.detail[0]?.msg : data?.detail ?? 'Authentication failed';
        throw new Error(typeof detail === 'string' ? detail : 'Authentication failed');
      }

      const token = data?.tokens?.access_token;
      if (token) {
        localStorage.setItem(ACCESS_TOKEN_KEY, token);
      }

      const user = data?.user as SessionUser | undefined;
      if (user && onAuthSuccess) {
        onAuthSuccess(user);
      }

      setNotice({
        kind: 'success',
        text:
          mode === 'login'
            ? 'Signed in successfully. Your workspace is ready.'
            : 'Account created successfully. Your tenant has been initialized.',
      });

      setPassword('');
      setOrganizationName('');
      setFullName('');
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Something went wrong';
      setNotice({ kind: 'error', text: message });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: 520,
        margin: '0 auto',
        background: '#ffffff',
        border: '1px solid #dfe7f1',
        borderRadius: 20,
        padding: 24,
        boxShadow: '0 16px 40px rgba(20, 33, 61, 0.06)',
      }}
    >
      <div style={{ display: 'flex', gap: 8, marginBottom: 18 }}>
        {(['login', 'register'] as const).map((tab) => (
          <button
            key={tab}
            type="button"
            onClick={() => setMode(tab)}
            style={{
              flex: 1,
              border: 'none',
              borderRadius: 10,
              padding: '10px 12px',
              background: mode === tab ? '#2148c0' : '#edf2fb',
              color: mode === tab ? '#ffffff' : '#14213d',
              fontWeight: 700,
              cursor: 'pointer',
            }}
          >
            {tab === 'login' ? 'Log in' : 'Register'}
          </button>
        ))}
      </div>

      <h2 style={{ margin: '0 0 18px', fontSize: 28, color: '#14213d' }}>
        {mode === 'login' ? 'Welcome back' : 'Create your workspace'}
      </h2>

      <form onSubmit={submitForm} style={{ display: 'grid', gap: 14 }}>
        {mode === 'register' && (
          <label style={{ display: 'grid', gap: 8, color: '#344056', fontWeight: 600 }}>
            Full name
            <input
              value={fullName}
              onChange={(event) => setFullName(event.target.value)}
              placeholder="Alex Morgan"
              style={inputStyle}
            />
          </label>
        )}

        {mode === 'register' && (
          <label style={{ display: 'grid', gap: 8, color: '#344056', fontWeight: 600 }}>
            Organization name
            <input
              value={organizationName}
              onChange={(event) => setOrganizationName(event.target.value)}
              placeholder="Northwind Labs"
              style={inputStyle}
            />
          </label>
        )}

        <label style={{ display: 'grid', gap: 8, color: '#344056', fontWeight: 600 }}>
          Email
          <input
            type="email"
            autoComplete="email"
            required
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="you@company.com"
            style={inputStyle}
          />
        </label>

        <label style={{ display: 'grid', gap: 8, color: '#344056', fontWeight: 600 }}>
          Password
          <input
            type="password"
            autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
            required
            minLength={8}
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="At least 8 characters"
            style={inputStyle}
          />
        </label>

        {notice && (
          <div
            style={{
              borderRadius: 12,
              padding: '10px 12px',
              background: notice.kind === 'success' ? '#ebf9f1' : '#fff0f0',
              border: `1px solid ${notice.kind === 'success' ? '#bfe7cf' : '#f1c4c4'}`,
              color: notice.kind === 'success' ? '#166534' : '#9a1c1c',
              fontSize: 14,
            }}
          >
            {notice.text}
          </div>
        )}

        <button
          type="submit"
          disabled={isSubmitting}
          style={{
            border: 'none',
            background: isSubmitting ? '#6a82d9' : '#2148c0',
            color: '#ffffff',
            borderRadius: 12,
            padding: '12px 16px',
            fontWeight: 700,
            cursor: isSubmitting ? 'wait' : 'pointer',
          }}
        >
          {isSubmitting ? 'Please wait...' : mode === 'login' ? 'Access dashboard' : 'Create account'}
        </button>
      </form>
    </div>
  );
}

const inputStyle: CSSProperties = {
  width: '100%',
  border: '1px solid #dfe7f1',
  borderRadius: 12,
  padding: '12px 14px',
  fontSize: 15,
  background: '#f8fafc',
  color: '#14213d',
  boxSizing: 'border-box',
};
