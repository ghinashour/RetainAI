'use client';

import { useEffect, useState } from 'react';

import { AuthCard } from '@/components/auth/auth-card';

type SessionUser = {
  id: string;
  email: string;
  full_name?: string | null;
  organization_id?: string | null;
};

type DashboardSnapshot = {
  total_customers: number;
  at_risk_customers: number;
  critical_customers: number;
  revenue_at_risk: number;
  currency: string;
};

type DashboardResponse = {
  organization: {
    id: string;
    name: string;
  };
  snapshot: DashboardSnapshot;
  priority_actions: string[];
};

type Customer = {
  id: string;
  name: string;
  email: string;
  status: string;
  health_score: number;
  risk_level: string;
  monthly_revenue: number;
  last_interaction: string;
  segment: string;
};

type CustomerResponse = {
  organization_name: string;
  customers: Customer[];
};

type Action = {
  id: string;
  title: string;
  priority: string;
  reason: string;
  next_step: string;
};

type ActionResponse = {
  organization_name: string;
  available: boolean;
  status: string;
  message: string | null;
  actions: Action[];
};

type AnalyticsSummary = {
  total_customers: number;
  healthy_customers: number;
  at_risk_customers: number;
  critical_customers: number;
  revenue_at_risk: number;
  currency: string;
  positive_outcomes: number;
  scheduled_interventions: number;
};

type BriefingResponse = {
  organization_name: string;
  available: boolean;
  status: string;
  message: string | null;
  headline: string | null;
  risk_summary: string | null;
  next_steps: string[];
  top_risk_customers: string[];
  retention_assessment: {
    score: number | null;
    confidence: string;
    rationale: string;
  } | null;
  summary: AnalyticsSummary;
};

type View = 'Overview' | 'Customers' | 'Actions' | 'Insights';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';
const ACCESS_TOKEN_KEY = 'retainai_access_token';

export function AppShell() {
  const [sessionUser, setSessionUser] = useState<SessionUser | null>(null);
  const [dashboard, setDashboard] = useState<DashboardResponse | null>(null);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [actions, setActions] = useState<Action[]>([]);
  const [actionAnalysis, setActionAnalysis] = useState<{ available: boolean; status: string; message: string | null }>({
    available: false,
    status: 'loading',
    message: null,
  });
  const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null);
  const [briefing, setBriefing] = useState<BriefingResponse | null>(null);
  const [selectedView, setSelectedView] = useState<View>('Overview');
  const [customerQuery, setCustomerQuery] = useState('');
  const [customerStatus, setCustomerStatus] = useState('All');
  const [customerImportCsv, setCustomerImportCsv] = useState('name,email,company,status,health_score,monthly_revenue,segment');

  useEffect(() => {
    const loadSession = async () => {
      const token = localStorage.getItem(ACCESS_TOKEN_KEY);
      if (!token) {
        setSessionUser(null);
        setDashboard(null);
        setCustomers([]);
        setActions([]);
        setAnalytics(null);
        setBriefing(null);
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
          setDashboard(null);
          setCustomers([]);
          setActions([]);
          setAnalytics(null);
          setBriefing(null);
          return;
        }

        const payload = await response.json();
        const user = payload.user ?? null;
        setSessionUser(user);

      } catch {
        localStorage.removeItem(ACCESS_TOKEN_KEY);
        setSessionUser(null);
        setDashboard(null);
        setCustomers([]);
        setActions([]);
        setAnalytics(null);
        setBriefing(null);
      }
    };

    loadSession();
  }, []);

  useEffect(() => {
    if (!sessionUser) {
      return;
    }

    const token = localStorage.getItem(ACCESS_TOKEN_KEY);
    if (!token) {
      return;
    }

    const headers = { Authorization: `Bearer ${token}` };
    const loadWorkspaceData = async () => {
      const [overviewResponse, customersResponse, actionsResponse, analyticsResponse, briefingResponse] = await Promise.all([
        fetch(`${API_BASE_URL}/api/v1/dashboard/overview`, { headers }),
        fetch(`${API_BASE_URL}/api/v1/customers`, { headers }),
        fetch(`${API_BASE_URL}/api/v1/actions`, { headers }),
        fetch(`${API_BASE_URL}/api/v1/analytics/summary`, { headers }),
        fetch(`${API_BASE_URL}/api/v1/assistant/briefing`, { headers }),
      ]);

      if (overviewResponse.ok) setDashboard(await overviewResponse.json());
      if (customersResponse.ok) {
        const payload: CustomerResponse = await customersResponse.json();
        setCustomers(payload.customers ?? []);
      }
      if (actionsResponse.ok) {
        const payload: ActionResponse = await actionsResponse.json();
        setActions(payload.actions ?? []);
        setActionAnalysis({ available: payload.available, status: payload.status, message: payload.message });
      }
      if (analyticsResponse.ok) {
        const payload = await analyticsResponse.json();
        setAnalytics(payload.summary ?? null);
      }
      if (briefingResponse.ok) setBriefing(await briefingResponse.json());
    };

    loadWorkspaceData().catch(() => {
      setDashboard(null);
      setCustomers([]);
      setActions([]);
      setActionAnalysis({ available: false, status: 'error', message: 'Workspace data could not be loaded.' });
      setAnalytics(null);
      setBriefing(null);
    });
  }, [sessionUser]);

  useEffect(() => {
    if (!sessionUser) {
      return;
    }

    const token = localStorage.getItem(ACCESS_TOKEN_KEY);
    if (!token || selectedView !== 'Customers') {
      return;
    }

    const loadCustomers = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/v1/customers`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const payload: CustomerResponse = await response.json();
          setCustomers(payload.customers ?? []);
        }
      } catch {
        setCustomers([]);
      }
    };

    loadCustomers();
  }, [selectedView, sessionUser]);

  const handleSignOut = () => {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    setSessionUser(null);
    setDashboard(null);
    setCustomers([]);
    setActions([]);
    setActionAnalysis({ available: false, status: 'loading', message: null });
    setAnalytics(null);
    setBriefing(null);
    setSelectedView('Overview');
    setCustomerQuery('');
    setCustomerStatus('All');
  };

  const handleImportCustomers = async () => {
    const token = localStorage.getItem(ACCESS_TOKEN_KEY);
    if (!token || !customerImportCsv.trim()) {
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/customers/import`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ csv: customerImportCsv }),
      });

      if (!response.ok) {
        return;
      }

      const payload: CustomerResponse = await response.json();
      setCustomers(payload.customers ?? []);
    } catch {
      // Ignore import failures in the UI and let the user retry.
    }
  };

  const navItems: View[] = ['Overview', 'Customers', 'Actions', 'Insights'];

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
          {sessionUser && navItems.map((item) => (
            <button
              key={item}
              type="button"
              onClick={() => setSelectedView(item)}
              style={{
                border: '1px solid #dfe7f1',
                background: selectedView === item ? '#2148c0' : '#ffffff',
                borderRadius: 10,
                padding: '10px 14px',
                color: selectedView === item ? '#ffffff' : '#14213d',
                cursor: 'pointer',
                fontWeight: 700,
              }}
            >
              {item}
            </button>
          ))}
        </div>
      </header>

      {sessionUser ? (
        <AuthenticatedWorkspace
          user={sessionUser}
          dashboard={dashboard}
          customers={customers}
          actions={actions}
          actionAnalysis={actionAnalysis}
          analytics={analytics}
          briefing={briefing}
          selectedView={selectedView}
          customerQuery={customerQuery}
          customerStatus={customerStatus}
          customerImportCsv={customerImportCsv}
          onCustomerQueryChange={setCustomerQuery}
          onCustomerStatusChange={setCustomerStatus}
          onCustomerImportCsvChange={setCustomerImportCsv}
          onImportCustomers={handleImportCustomers}
        />
      ) : (
        <section style={{ marginTop: 28 }}>
          <AuthCard onAuthSuccess={(user) => setSessionUser(user)} />
        </section>
      )}
    </main>
  );
}

function AuthenticatedWorkspace({
  user,
  dashboard,
  customers,
  actions,
  actionAnalysis,
  analytics,
  briefing,
  selectedView,
  customerQuery,
  customerStatus,
  customerImportCsv,
  onCustomerQueryChange,
  onCustomerStatusChange,
  onCustomerImportCsvChange,
  onImportCustomers,
}: {
  user: SessionUser;
  dashboard: DashboardResponse | null;
  customers: Customer[];
  actions: Action[];
  actionAnalysis: { available: boolean; status: string; message: string | null };
  analytics: AnalyticsSummary | null;
  briefing: BriefingResponse | null;
  selectedView: View;
  customerQuery: string;
  customerStatus: string;
  customerImportCsv: string;
  onCustomerQueryChange: (value: string) => void;
  onCustomerStatusChange: (value: string) => void;
  onCustomerImportCsvChange: (value: string) => void;
  onImportCustomers: () => void;
}) {
  const displayName = user.full_name ?? user.email.split('@')[0] ?? 'Operator';
  const snapshot = dashboard?.snapshot ?? {
    total_customers: 0,
    at_risk_customers: 0,
    critical_customers: 0,
    revenue_at_risk: 0,
    currency: 'USD',
  };
  const visibleCustomers = customers.filter((customer) => {
    const query = customerQuery.trim().toLowerCase();
    const matchesQuery = !query || `${customer.name} ${customer.email} ${customer.segment}`.toLowerCase().includes(query);
    const matchesStatus = customerStatus === 'All' || customer.status === customerStatus;
    return matchesQuery && matchesStatus;
  });
  const visibleActions = actions;

  if (selectedView === 'Customers') {
    return (
      <section style={{ background: '#ffffff', border: '1px solid #dfe7f1', borderRadius: 18, padding: 22, boxShadow: '0 12px 30px rgba(20, 33, 61, 0.04)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 18, gap: 12, flexWrap: 'wrap' }}>
          <div>
            <div style={{ fontSize: 12, letterSpacing: 1.2, textTransform: 'uppercase', color: '#5a6781', fontWeight: 700 }}>Customer watchlist</div>
            <h2 style={{ margin: '8px 0 0', fontSize: 30, color: '#14213d' }}>Accounts in focus</h2>
          </div>
          <div style={{ padding: '8px 12px', borderRadius: 999, background: '#eef4ff', color: '#2148c0', fontWeight: 700 }}>
            {visibleCustomers.length} of {customers.length} tracked accounts
          </div>
        </div>

        <div style={{ display: 'flex', gap: 10, marginBottom: 18, flexWrap: 'wrap' }}>
          <input
            value={customerQuery}
            onChange={(event) => onCustomerQueryChange(event.target.value)}
            placeholder="Search name, email, or segment"
            aria-label="Search customers"
            style={{ flex: '1 1 260px', minWidth: 220, border: '1px solid #dfe7f1', borderRadius: 10, padding: '11px 12px', color: '#14213d' }}
          />
          <select
            value={customerStatus}
            onChange={(event) => onCustomerStatusChange(event.target.value)}
            aria-label="Filter customers by status"
            style={{ flex: '0 1 160px', border: '1px solid #dfe7f1', borderRadius: 10, padding: '11px 12px', background: '#ffffff', color: '#14213d' }}
          >
            <option>All</option>
            <option>Critical</option>
            <option>At risk</option>
            <option>Healthy</option>
          </select>
        </div>

        <div style={{ display: 'grid', gap: 12, marginBottom: 18, padding: 14, borderRadius: 14, background: '#f8fbff', border: '1px solid #dfe7f1' }}>
          <div style={{ fontWeight: 700, color: '#14213d' }}>CSV customer import</div>
          <textarea
            value={customerImportCsv}
            onChange={(event) => onCustomerImportCsvChange(event.target.value)}
            rows={5}
            style={{ width: '100%', border: '1px solid #dfe7f1', borderRadius: 10, padding: 12, resize: 'vertical', color: '#14213d' }}
          />
          <div>
            <button
              type="button"
              onClick={onImportCustomers}
              style={{ border: 'none', background: '#2148c0', color: '#ffffff', borderRadius: 10, padding: '10px 16px', cursor: 'pointer', fontWeight: 700 }}
            >
              Import customers
            </button>
          </div>
        </div>

        <div style={{ display: 'grid', gap: 14 }}>
          {visibleCustomers.length > 0 ? (
            visibleCustomers.map((customer) => (
              <div key={customer.id} style={{ border: '1px solid #dfe7f1', borderRadius: 16, padding: 18, display: 'grid', gridTemplateColumns: 'minmax(180px, 2fr) minmax(120px, 1fr) minmax(120px, 1fr) minmax(120px, 1fr) minmax(140px, 1fr)', gap: 16, alignItems: 'center' }}>
                <div>
                  <div style={{ fontWeight: 700, fontSize: 18, color: '#14213d' }}>{customer.name}</div>
                  <div style={{ color: '#5a6781', marginTop: 4 }}>{customer.email}</div>
                </div>
                <div>
                  <div style={{ fontSize: 12, textTransform: 'uppercase', color: '#5a6781', letterSpacing: 0.8 }}>Segment</div>
                  <div style={{ fontWeight: 600, marginTop: 4 }}>{customer.segment}</div>
                </div>
                <div>
                  <div style={{ fontSize: 12, textTransform: 'uppercase', color: '#5a6781', letterSpacing: 0.8 }}>Health</div>
                  <div style={{ fontWeight: 600, marginTop: 4 }}>{customer.health_score}/100</div>
                </div>
                <div>
                  <div style={{ fontSize: 12, textTransform: 'uppercase', color: '#5a6781', letterSpacing: 0.8 }}>Status</div>
                  <div style={{ fontWeight: 700, color: customer.status === 'Critical' ? '#b42318' : customer.status === 'At risk' ? '#c77700' : '#067647', marginTop: 4 }}>{customer.status}</div>
                </div>
                <div>
                  <div style={{ fontSize: 12, textTransform: 'uppercase', color: '#5a6781', letterSpacing: 0.8 }}>Revenue</div>
                  <div style={{ fontWeight: 700, marginTop: 4 }}>${(customer.monthly_revenue / 1000).toFixed(1)}K / mo</div>
                </div>
              </div>
            ))
          ) : (
            <div style={{ padding: 20, color: '#5a6781' }}>No customers match the current filters.</div>
          )}
        </div>
      </section>
    );
  }

  if (selectedView === 'Actions') {
    return (
      <section style={{ background: '#ffffff', border: '1px solid #dfe7f1', borderRadius: 18, padding: 22, boxShadow: '0 12px 30px rgba(20, 33, 61, 0.04)' }}>
        <div style={{ marginBottom: 18 }}>
          <div style={{ fontSize: 12, letterSpacing: 1.2, textTransform: 'uppercase', color: '#5a6781', fontWeight: 700 }}>Next best actions</div>
          <h2 style={{ margin: '8px 0 0', fontSize: 30, color: '#14213d' }}>Operational playbook</h2>
        </div>

        <div style={{ display: 'grid', gap: 12 }}>
          {actionAnalysis.status === 'not_configured' && (
            <p style={{ marginTop: 0, color: '#7a4b00' }}>{actionAnalysis.message}</p>
          )}
          {visibleActions.length > 0 ? visibleActions.map((action) => (
            <div key={action.id} style={{ padding: '16px 18px', border: '1px solid #dfe7f1', borderRadius: 14, background: '#f8fbff', display: 'flex', justifyContent: 'space-between', gap: 16, alignItems: 'center', flexWrap: 'wrap' }}>
              <div>
                <div style={{ fontWeight: 700, color: '#14213d' }}>{action.title}</div>
                <div style={{ color: '#5a6781', marginTop: 5 }}>{action.reason}</div>
                <div style={{ color: '#5a6781', marginTop: 5 }}>Next step: {action.next_step}</div>
              </div>
              <span style={{ color: action.priority === 'High' ? '#b42318' : action.priority === 'Info' ? '#5a6781' : '#c77700', fontWeight: 700 }}>{action.priority}</span>
            </div>
          )) : actionAnalysis.status !== 'not_configured' && (
            <p style={{ color: '#5a6781' }}>{actionAnalysis.message ?? 'No AI-generated actions are available.'}</p>
          )}
        </div>
      </section>
    );
  }

  if (selectedView === 'Insights') {
    if (customers.length === 0) {
      const emptyStateActions = actions.length > 0
        ? actions
        : (dashboard?.priority_actions ?? []).map((title, index) => ({
            id: `priority-${index}`,
            title,
            priority: index === 0 ? 'High' : 'Medium',
            due_in: index === 0 ? 'Today' : 'This week',
            owner: 'CS Ops',
          }));

      return (
        <section style={{ background: '#ffffff', border: '1px solid #dfe7f1', borderRadius: 18, padding: 22 }}>
          <div style={{ fontSize: 12, textTransform: 'uppercase', color: '#5a6781', fontWeight: 700 }}>Retention intelligence</div>
          <h2 style={{ margin: '8px 0 12px', fontSize: 30, color: '#14213d' }}>No portfolio data yet</h2>
          <p style={{ color: '#5a6781' }}>Import customer records to see account insights. In the meantime, here are the available actions.</p>
          <div style={{ display: 'grid', gap: 10, marginTop: 18 }}>
            {emptyStateActions.map((action) => (
              <div key={action.id} style={{ padding: '12px 14px', background: '#f8fbff', border: '1px solid #dfe7f1', borderRadius: 10, color: '#14213d' }}>
                {action.title}
              </div>
            ))}
          </div>
        </section>
      );
    }

    const summary = analytics ?? {
      total_customers: 0,
      healthy_customers: 0,
      at_risk_customers: 0,
      critical_customers: 0,
      revenue_at_risk: 0,
      currency: 'USD',
      positive_outcomes: 0,
      scheduled_interventions: 0,
    };

    return (
      <section style={{ background: '#ffffff', border: '1px solid #dfe7f1', borderRadius: 18, padding: 22, boxShadow: '0 12px 30px rgba(20, 33, 61, 0.04)' }}>
        <div style={{ marginBottom: 18 }}>
          <div style={{ fontSize: 12, letterSpacing: 1.2, textTransform: 'uppercase', color: '#5a6781', fontWeight: 700 }}>Retention intelligence</div>
          <h2 style={{ margin: '8px 0 0', fontSize: 30, color: '#14213d' }}>{briefing?.headline ?? 'Portfolio retention summary'}</h2>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 14, marginBottom: 18 }}>
          {[
            {
              label: 'AI retention assessment',
              value: briefing?.available && briefing.retention_assessment?.score !== null
                ? `${briefing.retention_assessment?.score}/100`
                : 'Unavailable',
            },
            { label: 'Positive outcomes', value: summary.positive_outcomes.toString() },
            { label: 'Scheduled interventions', value: summary.scheduled_interventions.toString() },
            { label: 'At-risk accounts', value: summary.at_risk_customers.toString() },
          ].map((item) => (
            <div key={item.label} style={{ background: '#f8fbff', border: '1px solid #dfe7f1', borderRadius: 14, padding: 16 }}>
              <div style={{ fontSize: 12, textTransform: 'uppercase', letterSpacing: 0.8, color: '#5a6781' }}>{item.label}</div>
              <div style={{ fontSize: 26, fontWeight: 700, marginTop: 8 }}>{item.value}</div>
            </div>
          ))}
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1.3fr 1fr', gap: 18 }}>
          <div style={{ padding: 18, background: '#f8fbff', border: '1px solid #dfe7f1', borderRadius: 14 }}>
            <div style={{ fontSize: 12, letterSpacing: 1.2, textTransform: 'uppercase', color: '#5a6781', fontWeight: 700 }}>Portfolio briefing</div>
            <p style={{ margin: '12px 0 0', color: '#14213d', lineHeight: 1.6, fontSize: 16 }}>
              {briefing?.available ? briefing.risk_summary : briefing?.message ?? 'AI analysis is unavailable.'}
            </p>
            <div style={{ marginTop: 18, display: 'grid', gap: 8 }}>
              {briefing?.available && briefing.next_steps.length ? (
                briefing.next_steps.map((step, index) => (
                  <div key={`${step}-${index}`} style={{ padding: '10px 12px', borderRadius: 10, background: '#ffffff', border: '1px solid #dfe7f1' }}>{step}</div>
                ))
              ) : briefing?.available && <div style={{ color: '#5a6781' }}>The provider did not return next steps.</div>}
            </div>
          </div>

          <div style={{ padding: 18, background: '#f8fbff', border: '1px solid #dfe7f1', borderRadius: 14 }}>
            <div style={{ fontSize: 12, letterSpacing: 1.2, textTransform: 'uppercase', color: '#5a6781', fontWeight: 700 }}>Top risk customers</div>
            <div style={{ display: 'grid', gap: 8, marginTop: 12 }}>
              {briefing?.available && briefing.top_risk_customers.length ? (
                briefing.top_risk_customers.map((customer) => (
                  <div key={customer} style={{ padding: '10px 12px', borderRadius: 10, background: '#ffffff', border: '1px solid #dfe7f1', color: '#14213d', fontWeight: 600 }}>
                    {customer}
                  </div>
                ))
              ) : briefing?.available ? (
                <div style={{ padding: '10px 12px', borderRadius: 10, background: '#ffffff', border: '1px solid #dfe7f1', color: '#5a6781' }}>The provider returned no top-risk accounts.</div>
              ) : (
                <div style={{ padding: '10px 12px', borderRadius: 10, background: '#ffffff', border: '1px solid #dfe7f1', color: '#5a6781' }}>{briefing?.message ?? 'AI analysis is unavailable.'}</div>
              )}
            </div>
          </div>
        </div>
      </section>
    );
  }

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
            {dashboard?.organization?.name ?? 'Tenant connected'}
          </div>
        </div>
      </section>

      <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 16 }}>
        {[
          { label: 'Total customers', value: snapshot.total_customers.toLocaleString() },
          { label: 'At risk', value: snapshot.at_risk_customers.toLocaleString() },
          { label: 'Critical', value: snapshot.critical_customers.toLocaleString() },
          { label: 'Revenue at risk', value: `$${(snapshot.revenue_at_risk / 1000).toFixed(1)}K` },
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
          {customers.length > 0 ? (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12, minHeight: 120 }}>
              {(['Healthy', 'At risk', 'Critical'] as const).map((status) => {
                const count = customers.filter((customer) => customer.status === status).length;
                return (
                    <div key={status} style={{ alignSelf: 'end', textAlign: 'center' }}>
                    <div style={{ height: `${count === 0 ? 0 : Math.max(12, (count / customers.length) * 100)}px`, background: status === 'Critical' ? '#b42318' : status === 'At risk' ? '#c77700' : '#067647', borderRadius: 8 }} />
                    <span style={{ display: 'block', marginTop: 8, fontSize: 12, color: '#5a6781' }}>{status} ({count})</span>
                  </div>
                );
              })}
            </div>
          ) : (
            <p style={{ color: '#5a6781' }}>No customer data yet. Import accounts to see live portfolio signals.</p>
          )}
        </div>

        <div style={{ background: '#ffffff', border: '1px solid #dfe7f1', borderRadius: 16, padding: 20 }}>
          <h2 style={{ marginBottom: 14 }}>Priority actions</h2>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'grid', gap: 10 }}>
            {visibleActions.length > 0 ? visibleActions.map((action) => (
              <li key={action.id} style={{ padding: '12px 14px', background: '#eef3f8', borderRadius: 10, color: '#14213d' }}>{action.title}</li>
            )) : dashboard?.priority_actions.map((title) => (
              <li key={title} style={{ padding: '12px 14px', background: '#eef3f8', borderRadius: 10, color: '#14213d' }}>{title}</li>
            ))}
          </ul>
        </div>
      </section>
    </>
  );
}
