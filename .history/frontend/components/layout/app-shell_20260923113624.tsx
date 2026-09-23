export function AppShell() {
  return (
    <main style={{ maxWidth: 1200, margin: '0 auto', padding: '32px 20px 80px' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <div style={{ fontSize: 12, letterSpacing: 1.2, textTransform: 'uppercase', color: '#5a6781', fontWeight: 700 }}>
            RetainAI
          </div>
          <h1 style={{ margin: '8px 0 0', fontSize: 32 }}>Retention intelligence foundation</h1>
        </div>
        <nav style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
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
        </nav>
      </header>

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
    </main>
  );
}
