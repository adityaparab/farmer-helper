import { useMemo, useState } from 'react'
import type { FormEvent } from 'react'
import { ApiError, createApiClient } from './api/client'
import type { AnswerGenerationResponse, ApiClient, AuthUserResponse } from './api/client'
import { AppHeader } from './components/AppHeader'
import { RoleView } from './components/RoleView'
import { initialChatHistory } from './data/dashboard'
import type { ChatItem, Role } from './types'

type AppProps = {
  apiClient?: ApiClient
}

type AuthSession = {
  accessToken: string
  refreshToken: string
  user: AuthUserResponse
}

function authErrorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    return error.message
  }

  return 'Unable to sign in. Please try again.'
}

function chatErrorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    return error.message
  }

  return 'Unable to generate an answer. Please try again.'
}

function answerText(response: AnswerGenerationResponse): string {
  if (response.decision === 'answer' && response.answer) {
    return response.answer
  }

  if (response.decision === 'clarify' && response.clarification_message) {
    return response.clarification_message
  }

  if (response.decision === 'refuse' && response.refusal_reason) {
    return response.refusal_reason
  }

  return 'The answer service returned no displayable response.'
}

function App({ apiClient: injectedApiClient }: AppProps) {
  const [session, setSession] = useState<AuthSession | null>(null)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [authIsSubmitting, setAuthIsSubmitting] = useState(false)
  const [authError, setAuthError] = useState<string | null>(null)
  const [question, setQuestion] = useState('')
  const [chatIsSubmitting, setChatIsSubmitting] = useState(false)
  const [chatError, setChatError] = useState<string | null>(null)
  const [chatHistory, setChatHistory] = useState<ChatItem[]>(initialChatHistory)

  const canSubmitQuestion = useMemo(
    () => question.trim().length > 0 && !chatIsSubmitting,
    [chatIsSubmitting, question],
  )
  const role: Role = session?.user.role ?? 'guest'
  const apiClient = useMemo(
    () =>
      injectedApiClient ??
      createApiClient({
        baseUrl: import.meta.env.VITE_API_BASE_URL,
        getAccessToken: () => session?.accessToken ?? null,
      }),
    [injectedApiClient, session?.accessToken],
  )

  const handleLogin = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setAuthIsSubmitting(true)
    setAuthError(null)

    try {
      const tokens = await apiClient.auth.login(username.trim(), password)
      const authenticatedClient =
        injectedApiClient ??
        createApiClient({
          baseUrl: import.meta.env.VITE_API_BASE_URL,
          getAccessToken: () => tokens.access_token,
        })
      const user = await authenticatedClient.auth.me()
      setSession({
        accessToken: tokens.access_token,
        refreshToken: tokens.refresh_token,
        user,
      })
      setPassword('')
    } catch (error) {
      setSession(null)
      setAuthError(authErrorMessage(error))
    } finally {
      setAuthIsSubmitting(false)
    }
  }

  const handleAsk = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!canSubmitQuestion) {
      return
    }

    const submittedQuestion = question.trim()
    setChatIsSubmitting(true)
    setChatError(null)

    try {
      const response = await apiClient.answers.generate({
        question: submittedQuestion,
        session_key: session ? `user-${session.user.id}` : undefined,
        response_mode: 'concise',
      })
      setChatHistory((previous) => [
        {
          id: `q-${Date.now()}`,
          question: submittedQuestion,
          answer: answerText(response),
        },
        ...previous,
      ])
      setQuestion('')
    } catch (error) {
      setChatError(chatErrorMessage(error))
    } finally {
      setChatIsSubmitting(false)
    }
  }

  const signOut = async () => {
    const refreshToken = session?.refreshToken
    if (refreshToken) {
      try {
        await apiClient.auth.logout(refreshToken)
      } catch {
        // The local session still needs to be cleared if server logout fails.
      }
    }

    setSession(null)
    setUsername('')
    setPassword('')
    setAuthError(null)
  }

  return (
    <main className="mx-auto min-h-screen w-full max-w-6xl px-4 py-6 md:px-8 md:py-10">
      <AppHeader role={role} onSignOut={signOut} />
      <RoleView
        role={role}
        username={username}
        password={password}
        authIsSubmitting={authIsSubmitting}
        authErrorMessage={authError}
        apiClient={apiClient}
        question={question}
        canSubmitQuestion={canSubmitQuestion}
        chatIsSubmitting={chatIsSubmitting}
        chatErrorMessage={chatError}
        chatHistory={chatHistory}
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
