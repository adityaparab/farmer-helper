import { useEffect, useMemo, useState } from 'react'
import type { FormEvent } from 'react'
import { useChat } from '@ai-sdk/react'
import { createAnswerChatTransport } from '../ai/answerTransport'
import { ChatComposer } from './ChatComposer'
import { QuestionHistory } from './QuestionHistory'

const QUERY_HISTORY_STORAGE_PREFIX = 'farmer-helper.query-history'

function queryHistoryStorageKey(sessionKey?: string): string {
  return `${QUERY_HISTORY_STORAGE_PREFIX}:${sessionKey ?? 'guest'}`
}

function loadStoredQuestions(sessionKey?: string): string[] {
  if (typeof window === 'undefined') {
    return []
  }

  const serialized = window.localStorage.getItem(queryHistoryStorageKey(sessionKey))
  if (!serialized) {
    return []
  }

  try {
    const parsed = JSON.parse(serialized) as unknown
    if (!Array.isArray(parsed)) {
      return []
    }
    return parsed.filter((item): item is string => typeof item === 'string').slice(0, 50)
  } catch {
    return []
  }
}

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
  const [storedQuestions, setStoredQuestions] = useState<string[]>(() => loadStoredQuestions(sessionKey))
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
    messages: [],
    transport,
  })

  useEffect(() => {
    setStoredQuestions(loadStoredQuestions(sessionKey))
  }, [sessionKey])

  useEffect(() => {
    if (typeof window === 'undefined') {
      return
    }

    window.localStorage.setItem(queryHistoryStorageKey(sessionKey), JSON.stringify(storedQuestions))
  }, [sessionKey, storedQuestions])
  const isSubmitting = status === 'submitted' || status === 'streaming'
  const canSubmit = question.trim().length > 0 && !isSubmitting

  const submitQuestion = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const submittedQuestion = question.trim()
    if (!submittedQuestion || isSubmitting) {
      return
    }

    clearError()
    setStoredQuestions((current) => {
      const next = [submittedQuestion, ...current.filter((item) => item !== submittedQuestion)]
      return next.slice(0, 50)
    })
    void sendMessage({ text: submittedQuestion })
    setQuestion('')
  }

  const recallQuestion = (value: string) => {
    setQuestion(value)
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
      <QuestionHistory
        messages={messages}
        storedQuestions={storedQuestions}
        onRecallQuestion={recallQuestion}
      />
    </section>
  )
}
