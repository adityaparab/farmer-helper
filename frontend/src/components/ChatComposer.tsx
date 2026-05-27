import type { FormEvent } from 'react'

type ChatComposerProps = {
  question: string
  canSubmit: boolean
  isSubmitting: boolean
  errorMessage: string | null
  onQuestionChange: (value: string) => void
  onSubmit: (event: FormEvent<HTMLFormElement>) => void
}

export function ChatComposer({
  question,
  canSubmit,
  isSubmitting,
  errorMessage,
  onQuestionChange,
  onSubmit,
}: ChatComposerProps) {
  return (
    <article className="rounded-3xl border border-neutral-200 bg-white p-6 shadow-sm">
      <h2 className="font-heading text-2xl font-semibold text-neutral-900">TanStack AI Chat</h2>
      <p className="mt-1 text-sm text-neutral-600">
        Ask grounded questions and continue from previous context in one workspace.
      </p>
      <form onSubmit={onSubmit} className="mt-4 space-y-3" aria-label="Ask a farming question">
        <ChatStatusMessage isSubmitting={isSubmitting} errorMessage={errorMessage} />
        <textarea
          className="min-h-28 w-full rounded-xl border border-neutral-300 px-3 py-2 outline-none transition focus:border-amber-500"
          placeholder="Ask about crop planning, irrigation, or disease response..."
          value={question}
          disabled={isSubmitting}
          onChange={(event) => onQuestionChange(event.target.value)}
        />
        <button
          type="submit"
          disabled={!canSubmit || isSubmitting}
          className="rounded-xl bg-neutral-900 px-4 py-2 text-sm font-medium text-white transition enabled:hover:bg-neutral-800 disabled:cursor-not-allowed disabled:bg-neutral-300"
        >
          {isSubmitting ? <SubmittingQuestionLabel /> : <AskQuestionLabel />}
        </button>
      </form>
    </article>
  )
}

type ChatStatusMessageProps = {
  isSubmitting: boolean
  errorMessage: string | null
}

function ChatStatusMessage({ isSubmitting, errorMessage }: ChatStatusMessageProps) {
  if (isSubmitting) {
    return <p className="text-sm text-neutral-600" role="status">Generating grounded answer...</p>
  }

  if (errorMessage) {
    return <p className="text-sm text-red-700" role="alert">{errorMessage}</p>
  }

  return null
}

function AskQuestionLabel() {
  return <>Ask question</>
}

function SubmittingQuestionLabel() {
  return <>Generating...</>
}
