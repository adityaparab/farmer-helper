import type { Role } from '../types'

type AppHeaderProps = {
  role: Role
  onSignOut: () => void
}

export function AppHeader({ role, onSignOut }: AppHeaderProps) {
  return (
    <header className="mb-8 flex flex-wrap items-center justify-between gap-4">
      <div className="max-w-3xl">
        <p className="text-sm uppercase tracking-[0.3em] text-amber-600">Farmer Helper</p>
        <h1 className="font-heading text-4xl font-semibold text-neutral-900 md:text-5xl">
          Precision support for farm operations
        </h1>
      </div>
      {role !== 'guest' ? <SignOutButton onSignOut={onSignOut} /> : null}
    </header>
  )
}

type SignOutButtonProps = {
  onSignOut: () => void
}

function SignOutButton({ onSignOut }: SignOutButtonProps) {
  return (
    <button
      type="button"
      onClick={onSignOut}
      className="rounded-xl border border-neutral-200 bg-white px-4 py-2 text-sm font-medium text-neutral-700 transition hover:border-neutral-300 hover:bg-neutral-50"
    >
      Sign out
    </button>
  )
}
