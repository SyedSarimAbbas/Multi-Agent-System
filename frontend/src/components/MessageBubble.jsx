import { useState } from 'react'
import AgentTrace from './AgentTrace'
import './MessageBubble.css'

const AGENT_COLORS = {
  weather: 'var(--agent-weather)',
  calculator: 'var(--agent-calculator)',
  crypto: 'var(--agent-crypto)',
  general: 'var(--agent-general)',
  error: '#ef4444',
}

const AGENT_ICONS = {
  weather: '🌤️',
  calculator: '🔢',
  crypto: '📈',
  general: '💬',
  error: '⚠️',
}

const AGENT_LABELS = {
  weather: 'Weather Agent',
  calculator: 'Calculator Agent',
  crypto: 'Crypto Agent',
  general: 'General Agent',
  error: 'Error',
}

function MessageBubble({ message }) {
  const isUser = message.role === 'user'
  const [showTrace, setShowTrace] = useState(false)

  const formatTime = (ts) => {
    try {
      return new Date(ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    } catch {
      return ''
    }
  }

  if (isUser) {
    return (
      <div className="message message-user">
        <div className="message-row user-row">
          <div className="bubble user-bubble">
            <p>{message.content}</p>
          </div>
        </div>
        <span className="message-time user-time">{formatTime(message.timestamp)}</span>
      </div>
    )
  }

  const agent = message.agent || 'general'
  const agentColor = AGENT_COLORS[agent] || AGENT_COLORS.general

  return (
    <div className={`message message-agent ${message.isError ? 'message-error' : ''}`}>
      <div className="message-row agent-row">
        <div className="agent-avatar" style={{ background: agentColor + '18', color: agentColor }}>
          <span>{AGENT_ICONS[agent] || '💬'}</span>
        </div>
        <div className="bubble agent-bubble">
          <div className="agent-header">
            <span className="agent-badge" style={{ background: agentColor + '18', color: agentColor }}>
              {AGENT_LABELS[agent] || agent}
            </span>
            <span className="message-time">{formatTime(message.timestamp)}</span>
          </div>
          <div className="agent-content">
            {message.content.split('\n').map((line, i) => (
              <p key={i}>{line || '\u00A0'}</p>
            ))}
          </div>
          {message.trace && message.trace.length > 0 && (
            <button
              className="trace-toggle"
              onClick={() => setShowTrace(!showTrace)}
            >
              <svg
                width="14"
                height="14"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                style={{ transform: showTrace ? 'rotate(90deg)' : 'none', transition: 'transform 0.2s' }}
              >
                <polyline points="9 18 15 12 9 6" />
              </svg>
              {showTrace ? 'Hide' : 'Show'} trace ({message.trace.length} steps)
            </button>
          )}
          {showTrace && <AgentTrace steps={message.trace} agent={agent} />}
        </div>
      </div>
    </div>
  )
}

export default MessageBubble
