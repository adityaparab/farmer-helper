import type { FormEvent } from 'react'
import type { ApiClient } from '../api/client'
import type { ChatItem, Role } from '../types'
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
  question: string
  canSubmitQuestion: boolean
  chatIsSubmitting: boolean
  chatErrorMessage: string | null
  chatHistory: ChatItem[]
  onUsernameChange: (value: string) => void
  onPasswordChange: (value: string) => void
  onQuestionChange: (value: string) => void
  onLogin: (event: FormEvent<HTMLFormElement>) => void
  onAsk: (event: FormEvent<HTMLFormElement>) => void
}

export function RoleView({
  role,
  username,
  password,
  authIsSubmitting,
  authErrorMessage,
  apiClient,
  question,
  canSubmitQuestion,
  chatIsSubmitting,
  chatErrorMessage,
  chatHistory,
  onUsernameChange,
  onPasswordChange,
  onQuestionChange,
  onLogin,
  onAsk,
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
    return <AdminDashboard apiClient={apiClient} />
  }

  return (
    <UserWorkspace
      question={question}
      canSubmit={canSubmitQuestion}
      isSubmitting={chatIsSubmitting}
      errorMessage={chatErrorMessage}
      history={chatHistory}
      onQuestionChange={onQuestionChange}
      onSubmit={onAsk}
    />
  )
}
