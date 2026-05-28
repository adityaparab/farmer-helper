import type { FormEvent } from 'react'
import type { ApiClient } from '../api/client'
import type { Role } from '../types'
import { AdminDashboard } from './AdminDashboard'
import { GuestExperience } from './GuestExperience'
import { UserWorkspace } from './UserWorkspace'

type RoleViewProps = {
  role: Role
  username: string
  password: string
  authIsSubmitting: boolean
  authErrorMessage: string | null
  apiClient: ApiClient
  answerBaseUrl?: string
  accessToken: string | null
  sessionKey?: string
  onUsernameChange: (value: string) => void
  onPasswordChange: (value: string) => void
  onLogin: (event: FormEvent<HTMLFormElement>) => void
}

export function RoleView({
  role,
  username,
  password,
  authIsSubmitting,
  authErrorMessage,
  apiClient,
  answerBaseUrl,
  accessToken,
  sessionKey,
  onUsernameChange,
  onPasswordChange,
  onLogin,
}: RoleViewProps) {
  if (role === 'guest') {
    return (
      <GuestExperience
        username={username}
        password={password}
        isSubmitting={authIsSubmitting}
        errorMessage={authErrorMessage}
        onUsernameChange={onUsernameChange}
        onPasswordChange={onPasswordChange}
        onSubmit={onLogin}
      />
    )
  }

  if (role === 'admin') {
    return (
      <AdminDashboard
        apiClient={apiClient}
        answerBaseUrl={answerBaseUrl}
        accessToken={accessToken}
        sessionKey={sessionKey}
      />
    )
  }

  return (
    <UserWorkspace
      key={sessionKey ?? 'guest'}
      answerBaseUrl={answerBaseUrl}
      accessToken={accessToken}
      sessionKey={sessionKey}
    />
  )
}
