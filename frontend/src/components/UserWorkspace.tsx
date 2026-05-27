import { useMemo, useState } from 'react'
import type { FormEvent } from 'react'
import { useChat } from '@ai-sdk/react'
import { createAnswerChatTransport } from '../ai/answerTransport'
import { initialChatMessages } from '../data/dashboard'
import { ChatComposer } from './ChatComposer'
import { QuestionHistory } from './QuestionHistory'

type UserWorkspaceProps = {
  answerBaseUrl?: string
  accessToken: string | null
  sessionKey?: string
}

export function UserWorkspace({
  answerBaseUrl,
  accessToken,
  sessionKey,
}: UserWorkspaceProps) {
  const [question, setQuestion] = useState('')
  const transport = useMemo(
    () =>
      createAnswerChatTransport({
        baseUrl: answerBaseUrl,
        getAccessToken: () => accessToken,
        sessionKey,
      }),
    [accessToken, answerBaseUrl, sessionKey],
  )
  const { messages, sendMessage, status, error, clearError } = useChat({
    messages: initialChatMessages,
    transport,
  })
  const isSubmitting = status === 'submitted' || status === 'streaming'
  const canSubmit = question.trim().length > 0 && !isSubmitting

  const submitQuestion = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const submittedQuestion = question.trim()
    if (!submittedQuestion || isSubmitting) {
      return
    }

    clearError()
    void sendMessage({ text: submittedQuestion })
    setQuestion('')
  }

  return (
    <section className="grid gap-6 lg:grid-cols-[1.2fr,0.8fr]" aria-label="User workspace">
      <ChatComposer
        question={question}
        canSubmit={canSubmit}
        isSubmitting={isSubmitting}
        errorMessage={error?.message ?? null}
        onQuestionChange={setQuestion}
        onSubmit={submitQuestion}
      />
      <QuestionHistory messages={messages} />
    </section>
  )
}
