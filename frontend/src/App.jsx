import { useState, useEffect } from 'react'
import Sidebar from './components/Sidebar'
import ChatWindow from './components/ChatWindow'
import './App.css'

function App() {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('mas-theme') || 'dark'
  })
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [lastAgent, setLastAgent] = useState(null)
  const [sessions, setSessions] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('mas-sessions') || '[]')
    } catch {
      return []
    }
  })
  const [activeSessionId, setActiveSessionId] = useState(() => {
    return sessions.length > 0 ? sessions[0].id : null
  })

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('mas-theme', theme)
  }, [theme])

  useEffect(() => {
    localStorage.setItem('mas-sessions', JSON.stringify(sessions))
  }, [sessions])

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark')
  }

  const createSession = () => {
    const newSession = {
      id: Date.now().toString(),
      title: 'New Chat',
      messages: [],
      createdAt: new Date().toISOString(),
    }
    setSessions(prev => [newSession, ...prev])
    setActiveSessionId(newSession.id)
    setSidebarOpen(false)
    return newSession
  }

  const updateSessionMessages = (sessionId, messages) => {
    setSessions(prev => prev.map(s => {
      if (s.id !== sessionId) return s
      const title = messages.find(m => m.role === 'user')?.content?.slice(0, 40) || 'New Chat'
      return { ...s, messages, title }
    }))
  }

  const deleteSession = (sessionId) => {
    setSessions(prev => prev.filter(s => s.id !== sessionId))
    if (activeSessionId === sessionId) {
      const remaining = sessions.filter(s => s.id !== sessionId)
      setActiveSessionId(remaining.length > 0 ? remaining[0].id : null)
    }
  }

  const activeSession = sessions.find(s => s.id === activeSessionId)

  return (
    <div className="app-layout">
      <Sidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        theme={theme}
        onToggleTheme={toggleTheme}
        lastAgent={lastAgent}
        sessions={sessions}
        activeSessionId={activeSessionId}
        onSelectSession={(id) => { setActiveSessionId(id); setSidebarOpen(false) }}
        onNewChat={createSession}
        onDeleteSession={deleteSession}
      />

      <main className="main-content">
        <header className="main-header">
          <button
            className="menu-toggle"
            onClick={() => setSidebarOpen(true)}
            aria-label="Open menu"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <line x1="3" y1="6" x2="21" y2="6" />
              <line x1="3" y1="12" x2="21" y2="12" />
              <line x1="3" y1="18" x2="21" y2="18" />
            </svg>
          </button>
          <div className="header-title">
            <h1>Multi-Agent System</h1>
            <span className="header-badge">LangGraph</span>
          </div>
        </header>

        <ChatWindow
          session={activeSession}
          onCreateSession={createSession}
          onUpdateMessages={(msgs) => {
            const sid = activeSessionId || createSession().id
            updateSessionMessages(sid, msgs)
          }}
          onAgentUsed={setLastAgent}
        />
      </main>

      {sidebarOpen && (
        <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)} />
      )}
    </div>
  )
}

export default App
