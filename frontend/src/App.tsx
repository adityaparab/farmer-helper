import { useEffect, useMemo, useState } from 'react'
import type { FormEvent } from 'react'
import { ApiError, createApiClient } from './api/client'
import type { ApiClient, AuthUserResponse } from './api/client'
import { AppHeader } from './components/AppHeader'
import { RoleView } from './components/RoleView'
import type { Role, ThemeMode } from './types'

const AUTH_SESSION_STORAGE_KEY = 'farmer-helper.auth-session'
const THEME_STORAGE_KEY = 'farmer-helper.theme-mode'

type AppProps = {
  apiClient?: ApiClient
}

type AuthSession = {
  accessToken: string
  refreshToken: string
  user: AuthUserResponse
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function readStoredThemeMode(): ThemeMode {
  if (typeof window === 'undefined') {
    return 'dark'
  }

  const storedValue = window.localStorage.getItem(THEME_STORAGE_KEY)
  return storedValue === 'light' || storedValue === 'dark' ? storedValue : 'dark'
}

function readStoredSession(): AuthSession | null {
  if (typeof window === 'undefined') {
    return null
  }

  const serialized = window.localStorage.getItem(AUTH_SESSION_STORAGE_KEY)
  if (!serialized) {
    return null
  }

  try {
    const parsed = JSON.parse(serialized) as unknown
    if (!isRecord(parsed)) {
      return null
    }

    const accessToken = parsed.accessToken
    const refreshToken = parsed.refreshToken
    const user = parsed.user
    if (typeof accessToken !== 'string' || typeof refreshToken !== 'string' || !isRecord(user)) {
      return null
    }

    const userId = user.id
    const username = user.username
    const role = user.role
    if (
      typeof userId !== 'number' ||
      typeof username !== 'string' ||
      (role !== 'admin' && role !== 'user')
    ) {
      return null
    }

    return {
      accessToken,
      refreshToken,
      user: {
        id: userId,
        username,
        role,
      },
    }
  } catch {
    return null
  }
}

function authErrorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    return error.message
  }

  return 'Unable to sign in. Please try again.'
}

function App({ apiClient: injectedApiClient }: AppProps) {
  const [initialStoredSession] = useState<AuthSession | null>(() => readStoredSession())
  const [session, setSession] = useState<AuthSession | null>(initialStoredSession)
  const [themeMode, setThemeMode] = useState<ThemeMode>(() => readStoredThemeMode())
  const [isRestoringSession, setIsRestoringSession] = useState(initialStoredSession !== null)
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
    window.localStorage.setItem(THEME_STORAGE_KEY, themeMode)
  }, [themeMode])

  useEffect(() => {
    if (session) {
      window.localStorage.setItem(AUTH_SESSION_STORAGE_KEY, JSON.stringify(session))
    } else {
      window.localStorage.removeItem(AUTH_SESSION_STORAGE_KEY)
    }
  }, [session])

  useEffect(() => {
    if (!initialStoredSession) {
      return
    }

    let isCurrent = true

    const hydrateSession = async () => {
      try {
        const unauthenticatedClient = injectedApiClient ??
          createApiClient({
            baseUrl: import.meta.env.VITE_API_BASE_URL,
          })
        const refreshed = await unauthenticatedClient.auth.refresh(initialStoredSession.refreshToken)
        const authenticatedClient =
          injectedApiClient ??
          createApiClient({
            baseUrl: import.meta.env.VITE_API_BASE_URL,
            getAccessToken: () => refreshed.access_token,
          })
        const user = await authenticatedClient.auth.me()
        if (isCurrent) {
          setSession({
            accessToken: refreshed.access_token,
            refreshToken: refreshed.refresh_token,
            user,
          })
        }
      } catch {
        if (isCurrent) {
          setSession(null)
        }
      } finally {
        if (isCurrent) {
          setIsRestoringSession(false)
        }
      }
    }

    void hydrateSession()

    return () => {
      isCurrent = false
    }
  }, [initialStoredSession, injectedApiClient])

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
      {isRestoringSession ? (
        <section
          className="rounded-lg border border-neutral-200 bg-white p-6 text-sm text-neutral-600 shadow-sm dark:border-neutral-800 dark:bg-neutral-950 dark:text-neutral-300"
          aria-label="Restoring session"
        >
          Restoring your session...
        </section>
      ) : null}
      {!isRestoringSession ? (
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
      ) : null}
    </main>
  )
}

export default App
