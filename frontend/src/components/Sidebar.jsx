import ThemeToggle from './ThemeToggle'
import './Sidebar.css'

const AGENT_INFO = {
  weather: { icon: '🌤️', label: 'Weather', color: 'var(--agent-weather)' },
  calculator: { icon: '🔢', label: 'Calculator', color: 'var(--agent-calculator)' },
  crypto: { icon: '📈', label: 'Crypto', color: 'var(--agent-crypto)' },
  general: { icon: '💬', label: 'General', color: 'var(--agent-general)' },
}

function Sidebar({
  isOpen,
  onClose,
  theme,
  onToggleTheme,
  lastAgent,
  sessions,
  activeSessionId,
  onSelectSession,
  onNewChat,
  onDeleteSession,
}) {
  return (
    <aside className={`sidebar ${isOpen ? 'sidebar-open' : ''}`}>
      <div className="sidebar-header">
        <div className="sidebar-brand">
          <div className="brand-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 2L2 7l10 5 10-5-10-5z" />
              <path d="M2 17l10 5 10-5" />
              <path d="M2 12l10 5 10-5" />
            </svg>
          </div>
          <div>
            <span className="brand-name">MAS</span>
            <span className="brand-version">v1.0</span>
          </div>
        </div>
        <button className="sidebar-close" onClick={onClose} aria-label="Close sidebar">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>

      <button className="new-chat-btn" onClick={onNewChat}>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
          <line x1="12" y1="5" x2="12" y2="19" />
          <line x1="5" y1="12" x2="19" y2="12" />
        </svg>
        New Chat
      </button>

      {/* Agent status panel */}
      <div className="sidebar-section">
        <h3 className="section-title">Agents</h3>
        <div className="agent-list">
          {Object.entries(AGENT_INFO).map(([key, info]) => (
            <div
              key={key}
              className={`agent-item ${lastAgent === key ? 'agent-active' : ''}`}
            >
              <span className="agent-item-icon">{info.icon}</span>
              <span className="agent-item-label">{info.label}</span>
              {lastAgent === key && (
                <span className="agent-status-dot" style={{ background: info.color }} />
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Sessions */}
      <div className="sidebar-section sidebar-sessions">
        <h3 className="section-title">History</h3>
        <div className="session-list">
          {sessions.length === 0 && (
            <p className="no-sessions">No conversations yet</p>
          )}
          {sessions.map((s) => (
            <div
              key={s.id}
              className={`session-item ${s.id === activeSessionId ? 'session-active' : ''}`}
              onClick={() => onSelectSession(s.id)}
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
              </svg>
              <span className="session-title">{s.title}</span>
              <button
                className="session-delete"
                onClick={(e) => { e.stopPropagation(); onDeleteSession(s.id) }}
                aria-label="Delete session"
              >
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className="sidebar-footer">
        <ThemeToggle theme={theme} onToggle={onToggleTheme} />
      </div>
    </aside>
  )
}

export default Sidebar
