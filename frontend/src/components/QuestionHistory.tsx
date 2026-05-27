import type { UIMessage } from 'ai'

type QuestionHistoryProps = {
  messages: UIMessage[]
}

export function QuestionHistory({ messages }: QuestionHistoryProps) {
  return (
    <aside className="rounded-lg border border-neutral-200 bg-white p-6 shadow-sm dark:border-neutral-800 dark:bg-neutral-950" aria-label="Question history">
      <h3 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-50">Question history</h3>
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
