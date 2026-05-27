import { LogOut, Moon, Sun } from 'lucide-react'
import type { Role } from '../types'
import type { ThemeMode } from '../types'

type AppHeaderProps = {
  role: Role
  themeMode: ThemeMode
  onToggleTheme: () => void
  onSignOut: () => void | Promise<void>
}

export function AppHeader({ role, themeMode, onToggleTheme, onSignOut }: AppHeaderProps) {
  return (
    <header className="mb-8 flex flex-wrap items-center justify-between gap-4">
      <div className="max-w-3xl">
        <p className="text-sm uppercase tracking-[0.3em] text-amber-600 dark:text-amber-400">Farmer Helper</p>
        <h1 className="font-heading text-4xl font-semibold text-neutral-900 md:text-5xl dark:text-neutral-50">
          Precision support for farm operations
        </h1>
      </div>
      <div className="flex items-center gap-2">
        <ThemeToggle themeMode={themeMode} onToggleTheme={onToggleTheme} />
        {role !== 'guest' ? <SignOutButton onSignOut={onSignOut} /> : null}
      </div>
    </header>
  )
}

type ThemeToggleProps = {
  themeMode: ThemeMode
  onToggleTheme: () => void
}

function ThemeToggle({ themeMode, onToggleTheme }: ThemeToggleProps) {
  const isDark = themeMode === 'dark'
  const Icon = isDark ? Sun : Moon

  return (
    <button
      type="button"
      onClick={onToggleTheme}
      aria-label={isDark ? 'Switch to light theme' : 'Switch to dark theme'}
      title={isDark ? 'Switch to light theme' : 'Switch to dark theme'}
      className="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-neutral-200 bg-white text-neutral-700 transition hover:border-neutral-300 hover:bg-neutral-50 dark:border-neutral-800 dark:bg-neutral-950 dark:text-neutral-200 dark:hover:border-neutral-700 dark:hover:bg-neutral-900"
    >
      <Icon className="h-4 w-4" />
    </button>
  )
}

type SignOutButtonProps = {
  onSignOut: () => void | Promise<void>
}

function SignOutButton({ onSignOut }: SignOutButtonProps) {
  return (
    <button
      type="button"
      onClick={onSignOut}
      className="inline-flex items-center gap-2 rounded-lg border border-neutral-200 bg-white px-4 py-2 text-sm font-medium text-neutral-700 transition hover:border-neutral-300 hover:bg-neutral-50 dark:border-neutral-800 dark:bg-neutral-950 dark:text-neutral-200 dark:hover:border-neutral-700 dark:hover:bg-neutral-900"
    >
      <LogOut className="h-4 w-4" />
      Sign out
    </button>
  )
}
