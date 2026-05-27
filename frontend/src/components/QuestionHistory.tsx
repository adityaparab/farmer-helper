import type { UIMessage } from 'ai'

type QuestionHistoryProps = {
  messages: UIMessage[]
  storedQuestions: string[]
  onRecallQuestion: (value: string) => void
}

export function QuestionHistory({ messages, storedQuestions, onRecallQuestion }: QuestionHistoryProps) {
  return (
    <aside className="rounded-lg border border-neutral-200 bg-white p-6 shadow-sm dark:border-neutral-800 dark:bg-neutral-950" aria-label="Question history">
      <h3 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-50">Question history</h3>
      <h4 className="mt-4 text-sm font-semibold uppercase tracking-wide text-neutral-500 dark:text-neutral-400">
        Past queries
      </h4>
      <ul className="mt-3 space-y-2">
        {storedQuestions.length === 0 ? (
          <li className="rounded-lg border border-dashed border-neutral-300 p-3 text-sm text-neutral-500 dark:border-neutral-700 dark:text-neutral-400">
            No past queries yet.
          </li>
        ) : (
          storedQuestions.map((item) => (
            <li key={item}>
              <button
                type="button"
                onClick={() => onRecallQuestion(item)}
                className="w-full rounded-lg border border-neutral-200 px-3 py-2 text-left text-sm text-neutral-700 transition hover:border-neutral-300 hover:bg-neutral-50 dark:border-neutral-800 dark:text-neutral-200 dark:hover:border-neutral-700 dark:hover:bg-neutral-900"
              >
                {item}
              </button>
            </li>
          ))
        )}
      </ul>
      <h4 className="mt-6 text-sm font-semibold uppercase tracking-wide text-neutral-500 dark:text-neutral-400">
        Current conversation
      </h4>
      <ul className="mt-4 space-y-3">
        {messages.map((message) => (
          <li key={message.id} className="rounded-lg border border-neutral-200 p-3 dark:border-neutral-800">
            <p className="text-sm font-semibold text-neutral-900 dark:text-neutral-50">
              {message.role === 'user' ? 'Q:' : 'A:'} {messageText(message)}
            </p>
          </li>
        ))}
      </ul>
    </aside>
  )
}

function messageText(message: UIMessage): string {
  return message.parts
    .filter((part) => part.type === 'text')
    .map((part) => part.text)
    .join('')
}
