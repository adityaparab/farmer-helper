export type Role = 'guest' | 'user' | 'admin'

export type ChatItem = {
  id: string
  question: string
  answer: string
}

export type Metric = {
  label: string
  value: string
}
