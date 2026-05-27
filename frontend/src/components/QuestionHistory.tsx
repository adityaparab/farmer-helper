import type { ChatItem } from '../types'

type QuestionHistoryProps = {
  history: ChatItem[]
}

export function QuestionHistory({ history }: QuestionHistoryProps) {
  return (
    <aside className="rounded-3xl border border-neutral-200 bg-white p-6 shadow-sm" aria-label="Question history">
      <h3 className="font-heading text-xl font-semibold text-neutral-900">Question history</h3>
      <ul className="mt-4 space-y-3">
        {history.map((item) => (
          <li key={item.id} className="rounded-xl border border-neutral-200 p-3">
            <p className="text-sm font-semibold text-neutral-900">Q: {item.question}</p>
            <p className="mt-1 text-sm text-neutral-600">A: {item.answer}</p>
          </li>
        ))}
      </ul>
    </aside>
  )
}
