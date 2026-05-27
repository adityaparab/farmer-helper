import { useMemo, useState } from 'react'
import type { FormEvent } from 'react'
import { AppHeader } from './components/AppHeader'
import { RoleView } from './components/RoleView'
import { dashboardMetrics, draftAnswer, initialChatHistory } from './data/dashboard'
import type { ChatItem, Role } from './types'

function App() {
  const [role, setRole] = useState<Role>('guest')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [question, setQuestion] = useState('')
  const [chatHistory, setChatHistory] = useState<ChatItem[]>(initialChatHistory)

  const canSubmitQuestion = useMemo(() => question.trim().length > 0, [question])

  const handleLogin = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const normalizedUser = username.trim().toLowerCase()
    setRole(normalizedUser === 'admin' ? 'admin' : 'user')
  }

  const handleAsk = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!canSubmitQuestion) {
      return
    }

    setChatHistory((previous) => [
      {
        id: `q-${Date.now()}`,
        question: question.trim(),
        answer: draftAnswer,
      },
      ...previous,
    ])
    setQuestion('')
  }

  const signOut = () => {
    setRole('guest')
    setUsername('')
    setPassword('')
  }

  return (
    <main className="mx-auto min-h-screen w-full max-w-6xl px-4 py-6 md:px-8 md:py-10">
      <AppHeader role={role} onSignOut={signOut} />
      <RoleView
        role={role}
        username={username}
        password={password}
        question={question}
        canSubmitQuestion={canSubmitQuestion}
        chatHistory={chatHistory}
        dashboardMetrics={dashboardMetrics}
        onUsernameChange={setUsername}
        onPasswordChange={setPassword}
        onQuestionChange={setQuestion}
        onLogin={handleLogin}
        onAsk={handleAsk}
      />
    </main>
  )
}

export default App
