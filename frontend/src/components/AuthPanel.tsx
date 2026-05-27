import type { FormEvent } from 'react'

const usernamePlaceholder = 'admin'
const passwordPlaceholder = 'P@ssw0rd'

type AuthPanelProps = {
  username: string
  password: string
  onUsernameChange: (value: string) => void
  onPasswordChange: (value: string) => void
  onSubmit: (event: FormEvent<HTMLFormElement>) => void
}

export function AuthPanel({
  username,
  password,
  onUsernameChange,
  onPasswordChange,
  onSubmit,
}: AuthPanelProps) {
  return (
    <article className="rounded-3xl border border-neutral-200 bg-white p-6 shadow-sm">
      <form onSubmit={onSubmit} className="space-y-4" aria-label="Login or register">
        <label className="block text-sm font-medium text-neutral-700">
          Username
          <input
            className="mt-1 w-full rounded-xl border border-neutral-300 px-3 py-2 outline-none transition focus:border-amber-500"
            value={username}
            onChange={(event) => onUsernameChange(event.target.value)}
            placeholder={usernamePlaceholder}
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
          />
        </label>
        <button
          type="submit"
          className="w-full rounded-xl bg-neutral-900 px-4 py-2 font-medium text-white transition hover:bg-neutral-800"
        >
          Continue
        </button>
      </form>
    </article>
  )
}
