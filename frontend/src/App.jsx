import { useState, useEffect, useRef } from 'react'
import './styles/App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  // Load messages from localStorage on mount
  useEffect(() => {
    const savedMessages = localStorage.getItem('chatHistory')
    if (savedMessages) {
      try {
        setMessages(JSON.parse(savedMessages))
      } catch (e) {
        console.error('Failed to parse saved messages:', e)
      }
    }
  }, [])

  // Save messages to localStorage whenever they change
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem('chatHistory', JSON.stringify(messages))
    }
  }, [messages])

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!inputValue.trim() || isLoading) return

    const userMessage = {
      role: 'user',
      content: inputValue.trim(),
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      // Get API URL - use environment variable or default to Vercel function
      const apiUrl = import.meta.env.VITE_API_URL || '/api/ask'

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: userMessage.content })
      })

      const data = await response.json()

      if (response.ok) {
        const agentMessage = {
          role: 'agent',
          content: data.response,
          timestamp: new Date().toISOString()
        }
        setMessages(prev => [...prev, agentMessage])
      } else {
        throw new Error(data.error || 'Failed to get response')
      }
    } catch (error) {
      console.error('Error:', error)
      const errorMessage = {
        role: 'agent',
        content: `❌ Error: ${error.message}. Please try again.`,
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const clearHistory = () => {
    if (window.confirm('¿Estás seguro de que quieres borrar todo el historial?')) {
      setMessages([])
      localStorage.removeItem('chatHistory')
    }
  }

  return (
    <div className="app-container">
      <div className="chat-container">
        {/* Header */}
        <div className="chat-header">
          <h1>
            <span>🤖</span>
            Google AI Agent
          </h1>
          {messages.length > 0 && (
            <button onClick={clearHistory} className="clear-button">
              🗑️ Limpiar
            </button>
          )}
        </div>

        {/* Messages */}
        <div className="messages-container">
          {messages.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">💬</div>
              <h2>¡Hola! Soy tu asistente AI</h2>
              <p>Pregúntame lo que quieras y te ayudaré</p>
            </div>
          ) : (
            <>
              {messages.map((message, index) => (
                <div key={index} className={`message ${message.role}`}>
                  <div className={`message-avatar ${message.role}-avatar`}>
                    {message.role === 'user' ? '👤' : '🤖'}
                  </div>
                  <div className="message-content">
                    <div className="message-role">
                      {message.role === 'user' ? 'Tú' : 'Agente AI'}
                    </div>
                    <div className="message-text">{message.content}</div>
                  </div>
                </div>
              ))}

              {isLoading && (
                <div className="message agent">
                  <div className="message-avatar agent-avatar">🤖</div>
                  <div className="message-content">
                    <div className="message-role">Agente AI</div>
                    <div className="typing-indicator">
                      <div className="typing-dot"></div>
                      <div className="typing-dot"></div>
                      <div className="typing-dot"></div>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* Input */}
        <div className="input-container">
          <form onSubmit={handleSubmit} className="input-form">
            <div className="input-wrapper">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Escribe tu pregunta aquí..."
                className="input-field"
                disabled={isLoading}
              />
            </div>
            <button
              type="submit"
              className="send-button"
              disabled={isLoading || !inputValue.trim()}
            >
              {isLoading ? 'Enviando...' : 'Enviar'}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default App
