import { useEffect, useMemo, useState } from 'react'
import type { FormEvent } from 'react'
import { ApiError, createApiClient } from './api/client'
import type { ApiClient, AuthUserResponse } from './api/client'
import { AppHeader } from './components/AppHeader'
import { RoleView } from './components/RoleView'
import type { Role, ThemeMode } from './types'

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

function App({ apiClient: injectedApiClient }: AppProps) {
  const [session, setSession] = useState<AuthSession | null>(null)
  const [themeMode, setThemeMode] = useState<ThemeMode>('light')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [authIsSubmitting, setAuthIsSubmitting] = useState(false)
  const [authError, setAuthError] = useState<string | null>(null)

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

  useEffect(() => {
    document.documentElement.classList.toggle('dark', themeMode === 'dark')
  }, [themeMode])

  const toggleTheme = () => {
    setThemeMode((current) => (current === 'light' ? 'dark' : 'light'))
  }

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
      <AppHeader role={role} themeMode={themeMode} onToggleTheme={toggleTheme} onSignOut={signOut} />
      <RoleView
        role={role}
        username={username}
        password={password}
        authIsSubmitting={authIsSubmitting}
        authErrorMessage={authError}
        apiClient={apiClient}
        answerBaseUrl={import.meta.env.VITE_API_BASE_URL}
        accessToken={session?.accessToken ?? null}
        sessionKey={session ? `user-${session.user.id}` : undefined}
        onUsernameChange={setUsername}
        onPasswordChange={setPassword}
        onLogin={handleLogin}
      />
    </main>
  )
}

export default App
