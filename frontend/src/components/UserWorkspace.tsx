import type { FormEvent } from 'react'
import type { ChatItem } from '../types'
import { ChatComposer } from './ChatComposer'
import { QuestionHistory } from './QuestionHistory'

type UserWorkspaceProps = {
  question: string
  canSubmit: boolean
  isSubmitting: boolean
  errorMessage: string | null
  history: ChatItem[]
  onQuestionChange: (value: string) => void
  onSubmit: (event: FormEvent<HTMLFormElement>) => void
}

export function UserWorkspace({
  question,
  canSubmit,
  isSubmitting,
  errorMessage,
  history,
  onQuestionChange,
  onSubmit,
}: UserWorkspaceProps) {
  return (
    <section className="grid gap-6 lg:grid-cols-[1.2fr,0.8fr]" aria-label="User workspace">
      <ChatComposer
        question={question}
        canSubmit={canSubmit}
        isSubmitting={isSubmitting}
        errorMessage={errorMessage}
        onQuestionChange={onQuestionChange}
        onSubmit={onSubmit}
      />
      <QuestionHistory history={history} />
    </section>
  )
}
