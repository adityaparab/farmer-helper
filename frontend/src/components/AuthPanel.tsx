import type { FormEvent } from 'react'

const usernamePlaceholder = 'admin'
const passwordPlaceholder = 'P@ssw0rd'

type AuthPanelProps = {
  username: string
  password: string
  isSubmitting: boolean
  errorMessage: string | null
  onUsernameChange: (value: string) => void
  onPasswordChange: (value: string) => void
  onSubmit: (event: FormEvent<HTMLFormElement>) => void
}

export function AuthPanel({
  username,
  password,
  isSubmitting,
  errorMessage,
  onUsernameChange,
  onPasswordChange,
  onSubmit,
}: AuthPanelProps) {
  return (
    <article className="rounded-lg border border-neutral-200 bg-white p-6 shadow-sm dark:border-neutral-800 dark:bg-neutral-950">
      <form onSubmit={onSubmit} className="space-y-4" aria-label="Login or register">
        {errorMessage ? <AuthErrorMessage message={errorMessage} /> : null}
        <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-200">
          Username
          <input
            className="mt-1 w-full rounded-lg border border-neutral-300 bg-white px-3 py-2 text-neutral-900 outline-none transition focus:border-amber-500 dark:border-neutral-700 dark:bg-neutral-900 dark:text-neutral-50"
            value={username}
            onChange={(event) => onUsernameChange(event.target.value)}
            placeholder={usernamePlaceholder}
            disabled={isSubmitting}
          />
        </label>
        <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-200">
          Password
          <input
            className="mt-1 w-full rounded-lg border border-neutral-300 bg-white px-3 py-2 text-neutral-900 outline-none transition focus:border-amber-500 dark:border-neutral-700 dark:bg-neutral-900 dark:text-neutral-50"
            type="password"
            value={password}
            onChange={(event) => onPasswordChange(event.target.value)}
            placeholder={passwordPlaceholder}
            disabled={isSubmitting}
          />
        </label>
        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full rounded-lg bg-neutral-900 px-4 py-2 font-medium text-white transition hover:bg-neutral-800 disabled:cursor-not-allowed disabled:bg-neutral-500 dark:bg-amber-500 dark:text-neutral-950 dark:hover:bg-amber-400 dark:disabled:bg-neutral-700 dark:disabled:text-neutral-400"
        >
          {isSubmitting ? <SubmittingLabel /> : <ContinueLabel />}
        </button>
      </form>
    </article>
  )
}

type AuthErrorMessageProps = {
  message: string
}

function AuthErrorMessage({ message }: AuthErrorMessageProps) {
  return (
    <p className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700 dark:border-red-900 dark:bg-red-950 dark:text-red-200" role="alert">
      {message}
    </p>
  )
}

function ContinueLabel() {
  return <>Continue</>
}

function SubmittingLabel() {
  return <>Signing in...</>
}
