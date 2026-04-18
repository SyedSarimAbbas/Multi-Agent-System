import './AgentTrace.css'

function AgentTrace({ steps, agent }) {
  if (!steps || steps.length === 0) return null

  return (
    <div className="agent-trace">
      <div className="trace-header">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="12" cy="12" r="10" />
          <polyline points="12 6 12 12 16 14" />
        </svg>
        <span>Execution Trace</span>
      </div>
      <div className="trace-steps">
        {steps.map((step, i) => (
          <div key={i} className="trace-step">
            <div className="step-dot" />
            {i < steps.length - 1 && <div className="step-line" />}
            <code className="step-text">{step}</code>
          </div>
        ))}
      </div>
    </div>
  )
}

export default AgentTrace
