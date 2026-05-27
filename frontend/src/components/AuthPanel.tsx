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
    <article className="rounded-3xl border border-neutral-200 bg-white p-6 shadow-sm">
      <form onSubmit={onSubmit} className="space-y-4" aria-label="Login or register">
        {errorMessage ? <AuthErrorMessage message={errorMessage} /> : null}
        <label className="block text-sm font-medium text-neutral-700">
          Username
          <input
            className="mt-1 w-full rounded-xl border border-neutral-300 px-3 py-2 outline-none transition focus:border-amber-500"
            value={username}
            onChange={(event) => onUsernameChange(event.target.value)}
            placeholder={usernamePlaceholder}
            disabled={isSubmitting}
          />
        </label>
        <label className="block text-sm font-medium text-neutral-700">
          Password
          <input
            className="mt-1 w-full rounded-xl border border-neutral-300 px-3 py-2 outline-none transition focus:border-amber-500"
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
          className="w-full rounded-xl bg-neutral-900 px-4 py-2 font-medium text-white transition hover:bg-neutral-800 disabled:cursor-not-allowed disabled:bg-neutral-500"
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
    <p className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700" role="alert">
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
