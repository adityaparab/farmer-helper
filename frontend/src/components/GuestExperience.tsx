import type { FormEvent } from 'react'
import { AuthPanel } from './AuthPanel'
import { LandingHero } from './LandingHero'

type GuestExperienceProps = {
  username: string
  password: string
  onUsernameChange: (value: string) => void
  onPasswordChange: (value: string) => void
  onSubmit: (event: FormEvent<HTMLFormElement>) => void
}

export function GuestExperience({
  username,
  password,
  onUsernameChange,
  onPasswordChange,
  onSubmit,
}: GuestExperienceProps) {
  return (
    <section className="grid gap-6 lg:grid-cols-[1.5fr,1fr]">
      <LandingHero />
      <AuthPanel
        username={username}
        password={password}
        onUsernameChange={onUsernameChange}
        onPasswordChange={onPasswordChange}
        onSubmit={onSubmit}
      />
    </section>
  )
}
