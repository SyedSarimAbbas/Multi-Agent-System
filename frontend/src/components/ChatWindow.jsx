import { useState, useRef, useEffect } from 'react'
import MessageBubble from './MessageBubble'
import ChatInput from './ChatInput'
import { sendQuery, streamQuery } from '../services/api'
import './ChatWindow.css'

const AGENT_LABELS = {
  weather: 'Fetching weather data',
  calculator: 'Crunching numbers',
  crypto: 'Checking crypto markets',
  general: 'Thinking',
}

function ChatWindow({ session, onCreateSession, onUpdateMessages, onAgentUsed }) {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [loadingText, setLoadingText] = useState('Routing query...')
  const bottomRef = useRef(null)
  const loadingInterval = useRef(null)

  useEffect(() => {
    setMessages(session?.messages || [])
  }, [session?.id])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  useEffect(() => {
    return () => {
      if (loadingInterval.current) clearInterval(loadingInterval.current)
    }
  }, [])

  const cycleLoadingText = () => {
    const steps = ['Routing query...', 'Processing with agent...', 'Generating response...']
    let i = 0
    loadingInterval.current = setInterval(() => {
      i = (i + 1) % steps.length
      setLoadingText(steps[i])
    }, 1800)
  }

  const handleSend = async (text, maxTokens = 100) => {
    if (!text.trim() || loading) return

    if (!session) {
      onCreateSession()
    }

    const userMsg = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      timestamp: new Date().toISOString(),
    }

    const updated = [...messages, userMsg]
    setMessages(updated)
    onUpdateMessages(updated)
    setLoading(true)
    setLoadingText('Routing query...')

    const agentMsgId = (Date.now() + 1).toString()
    let currentAgentMsg = {
      id: agentMsgId,
      role: 'agent',
      content: '',
      agent: 'thinking',
      trace: [],
      timestamp: new Date().toISOString(),
    }

    try {
      await streamQuery(text, maxTokens, ({ event, data }) => {
        if (event === 'token') {
          const { text: token, node } = data
          
          if (node === 'responder' || node === 'general') {
            // Main response tokens
            currentAgentMsg = {
              ...currentAgentMsg,
              content: currentAgentMsg.content + token,
              agent: node
            }
          } else {
            // Thinking/Routing tokens - show in the trace or a dedicated thinking field
            // For now, let's append them to a temporary "thinking" status in the trace or as a separate indicator
            // Or just append to content if it's the current node
             currentAgentMsg = {
              ...currentAgentMsg,
              agent: node
            }
          }
          setMessages([...updated, currentAgentMsg])
        } else if (event === 'node') {
          const { node, output } = data
          
          // Update execution trace
          currentAgentMsg = {
            ...currentAgentMsg,
            trace: [...currentAgentMsg.trace, `[Node: ${node}] completed`],
          }
          
          if (output && output.answer && !currentAgentMsg.content) {
             currentAgentMsg.content = output.answer
          }

          setMessages([...updated, currentAgentMsg])
        } else if (event === 'error') {
          throw new Error(data.detail || 'Streaming failed')
        }
      })

      // Final commit to session storage
      onUpdateMessages([...updated, currentAgentMsg])
      if (currentAgentMsg.agent) onAgentUsed(currentAgentMsg.agent)

    } catch (err) {
      const errorMsg = {
        id: (Date.now() + 1).toString(),
        role: 'agent',
        content: `Something went wrong. ${err.message || 'Please check if the backend server is running.'}`,
        agent: 'error',
        trace: [],
        timestamp: new Date().toISOString(),
        isError: true,
      }

      const final = [...updated, errorMsg]
      setMessages(final)
      onUpdateMessages(final)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat-window">
      <div className="chat-messages">
        {messages.length === 0 && !loading && (
          <div className="chat-empty">
            <div className="empty-banner">
              <img src="/banner.png" alt="Multi-Agent System" className="brand-image-large" />
            </div>
            <h2>What can I help you with?</h2>
            <p>Ask about weather, do calculations, check crypto prices, or just chat.</p>
            <div className="empty-suggestions">
              <button onClick={() => handleSend("What's the weather in Tokyo?")}>
                <span className="suggestion-icon">🌤</span>
                Weather in Tokyo
              </button>
              <button onClick={() => handleSend("Calculate 847 * 23 + 156")}>
                <span className="suggestion-icon">🔢</span>
                847 × 23 + 156
              </button>
              <button onClick={() => handleSend("What's the price of Bitcoin?")}>
                <span className="suggestion-icon">📈</span>
                Bitcoin price
              </button>
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}

        {loading && (
          <div className="loading-indicator">
            <div className="loading-avatar">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 2L2 7l10 5 10-5-10-5z" />
                <path d="M2 17l10 5 10-5" />
                <path d="M2 12l10 5 10-5" />
              </svg>
            </div>
            <div className="loading-content">
              <div className="loading-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <span className="loading-label">{loadingText}</span>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <ChatInput onSend={handleSend} disabled={loading} />
    </div>
  )
}

export default ChatWindow
