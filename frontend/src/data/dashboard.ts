import type { UIMessage } from 'ai'
import type { ChatItem, Metric } from '../types'

export const dashboardMetrics: Metric[] = [
  { label: 'Documents', value: '124' },
  { label: 'Ingestion jobs', value: '17' },
  { label: 'Embedding chunks', value: '52,910' },
  { label: 'Pending QA items', value: '6' },
]

export const initialChatHistory: ChatItem[] = [
  {
    id: 'q-1',
    question: 'How often should I irrigate tomatoes in sandy soil?',
    answer: 'Use frequent light cycles and monitor moisture daily during fruit set.',
  },
  {
    id: 'q-2',
    question: 'What is a quick response for aphid infestation?',
    answer: 'Start with targeted neem treatment in evening and isolate affected patches.',
  },
]

export const initialChatMessages: UIMessage[] = initialChatHistory.flatMap((item) => [
  {
    id: `${item.id}-user`,
    role: 'user' as const,
    parts: [{ type: 'text' as const, text: item.question }],
  },
  {
    id: `${item.id}-assistant`,
    role: 'assistant' as const,
    parts: [{ type: 'text' as const, text: item.answer }],
  },
])
