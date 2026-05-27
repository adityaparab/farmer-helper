import { useCallback, useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import { ApiError } from '../api/client'
import type { AdminDashboardMetricsResponse, AdminPdfUploadResponse, ApiClient } from '../api/client'
import { MetricGrid } from './MetricGrid'
import { PdfUploadPanel } from './PdfUploadPanel'

type AdminDashboardProps = {
  apiClient: ApiClient
  answerBaseUrl?: string
  accessToken: string | null
  sessionKey?: string
}

type MetricsState =
  | { status: 'loading' }
  | { status: 'ready'; metrics: AdminDashboardMetricsResponse }
  | { status: 'error'; message: string }

function errorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    return error.message
  }

  if (error instanceof Error) {
    return error.message
  }

  return 'Unable to load admin data.'
}

function normalizeBaseUrl(value: string | undefined): string {
  return (value ?? '').replace(/\/$/, '')
}

type StreamEventRecord = {
  id: number
  text: string
}

export function AdminDashboard({
  apiClient,
  answerBaseUrl,
  accessToken,
  sessionKey,
}: AdminDashboardProps) {
  const [metricsState, setMetricsState] = useState<MetricsState>({ status: 'loading' })
  const [streamQuestion, setStreamQuestion] = useState('')
  const [streamText, setStreamText] = useState('')
  const [streamEvents, setStreamEvents] = useState<StreamEventRecord[]>([])
  const [streamError, setStreamError] = useState<string | null>(null)
  const [isStreaming, setIsStreaming] = useState(false)

  const fetchMetrics = useCallback(
    () => apiClient.admin.getDashboardMetrics(),
    [apiClient],
  )

  const refreshMetrics = useCallback(async () => {
    setMetricsState({ status: 'loading' })
    try {
      const metrics = await fetchMetrics()
      setMetricsState({ status: 'ready', metrics })
    } catch (error) {
      setMetricsState({ status: 'error', message: errorMessage(error) })
    }
  }, [fetchMetrics])

  useEffect(() => {
    let isCurrent = true

    fetchMetrics()
      .then((metrics) => {
        if (isCurrent) {
          setMetricsState({ status: 'ready', metrics })
        }
      })
      .catch((error: unknown) => {
        if (isCurrent) {
          setMetricsState({ status: 'error', message: errorMessage(error) })
        }
      })

    return () => {
      isCurrent = false
    }
  }, [fetchMetrics])

  const uploadPdf = async (file: File, contentVersion: string): Promise<AdminPdfUploadResponse> => {
    const response = await apiClient.admin.uploadPdf(file, contentVersion)
    await refreshMetrics()
    return response
  }

  const runRagStream = async () => {
    const submittedQuestion = streamQuestion.trim()
    if (!submittedQuestion || isStreaming) {
      return
    }

    setIsStreaming(true)
    setStreamError(null)
    setStreamText('')
    setStreamEvents([])

    try {
      const headers = new Headers({ 'Content-Type': 'application/json' })
      if (accessToken) {
        headers.set('Authorization', `Bearer ${accessToken}`)
      }

      const response = await fetch(`${normalizeBaseUrl(answerBaseUrl)}/answers/generate-stream`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          question: submittedQuestion,
          session_key: sessionKey,
          response_mode: 'concise',
        }),
      })
      if (!response.ok || !response.body) {
        throw new Error('Unable to stream RAG output.')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) {
          break
        }

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() ?? ''

        for (const line of lines) {
          const trimmedLine = line.trim()
          if (!trimmedLine) {
            continue
          }

          const event = JSON.parse(trimmedLine) as Record<string, unknown>
          const eventType = typeof event.event === 'string' ? event.event : 'unknown'
          if (eventType === 'chunk') {
            const chunkText = typeof event.text === 'string' ? event.text : ''
            if (chunkText) {
              setStreamText((current) => `${current}${current ? ' ' : ''}${chunkText}`)
            }
          }

          setStreamEvents((current) => {
            const nextId = current.length === 0 ? 1 : current[current.length - 1].id + 1
            return [...current, { id: nextId, text: `${eventType}: ${trimmedLine}` }]
          })

          if (eventType === 'final') {
            const responsePayload = event.response
            if (
              typeof responsePayload === 'object' &&
              responsePayload !== null &&
              typeof (responsePayload as { answer?: unknown }).answer === 'string'
            ) {
              setStreamText((responsePayload as { answer: string }).answer)
            }
          }
        }
      }
    } catch (error) {
      setStreamError(errorMessage(error))
    } finally {
      setIsStreaming(false)
    }
  }

  const submitRagStream = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    void runRagStream()
  }

  return (
    <section className="space-y-6" aria-label="Admin dashboard">
      <AdminMetricsView state={metricsState} />
      <AdminRagStreamingPanel
        question={streamQuestion}
        streamText={streamText}
        streamEvents={streamEvents}
        errorMessage={streamError}
        isStreaming={isStreaming}
        onQuestionChange={setStreamQuestion}
        onSubmit={submitRagStream}
      />
      <PdfUploadPanel onUpload={uploadPdf} />
    </section>
  )
}

type AdminMetricsViewProps = {
  state: MetricsState
}

function AdminMetricsView({ state }: AdminMetricsViewProps) {
  if (state.status === 'loading') {
    return <MetricsLoading />
  }

  if (state.status === 'error') {
    return <MetricsError message={state.message} />
  }

  return <MetricGrid metrics={state.metrics.cards} />
}

function MetricsLoading() {
  return (
    <div className="rounded-lg border border-neutral-200 bg-white p-4 text-sm text-neutral-600 dark:border-neutral-800 dark:bg-neutral-950 dark:text-neutral-300" role="status">
      Loading admin metrics...
    </div>
  )
}

type MetricsErrorProps = {
  message: string
}

function MetricsError({ message }: MetricsErrorProps) {
  return (
    <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-900 dark:bg-red-950 dark:text-red-200" role="alert">
      {message}
    </div>
  )
}

type AdminRagStreamingPanelProps = {
  question: string
  streamText: string
  streamEvents: StreamEventRecord[]
  errorMessage: string | null
  isStreaming: boolean
  onQuestionChange: (value: string) => void
  onSubmit: (event: FormEvent<HTMLFormElement>) => void
}

function AdminRagStreamingPanel({
  question,
  streamText,
  streamEvents,
  errorMessage,
  isStreaming,
  onQuestionChange,
  onSubmit,
}: AdminRagStreamingPanelProps) {
  const canSubmit = question.trim().length > 0 && !isStreaming

  return (
    <article className="rounded-lg border border-neutral-200 bg-white p-6 shadow-sm dark:border-neutral-800 dark:bg-neutral-950">
      <h3 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-50">
        RAG pipeline stream
      </h3>
      <form onSubmit={onSubmit} className="mt-4 space-y-3" aria-label="Run admin RAG stream">
        <textarea
          value={question}
          onChange={(event) => onQuestionChange(event.target.value)}
          placeholder="Run a live RAG answer stream for admin validation..."
          disabled={isStreaming}
          className="min-h-24 w-full rounded-lg border border-neutral-300 bg-white px-3 py-2 text-neutral-900 outline-none transition focus:border-amber-500 dark:border-neutral-700 dark:bg-neutral-900 dark:text-neutral-50 dark:placeholder:text-neutral-500"
        />
        <button
          type="submit"
          disabled={!canSubmit}
          className="rounded-lg bg-neutral-900 px-4 py-2 text-sm font-medium text-white transition enabled:hover:bg-neutral-800 disabled:cursor-not-allowed disabled:bg-neutral-300 dark:bg-amber-500 dark:text-neutral-950 dark:enabled:hover:bg-amber-400 dark:disabled:bg-neutral-700 dark:disabled:text-neutral-400"
        >
          {isStreaming ? 'Streaming...' : 'Start RAG stream'}
        </button>
      </form>
      {errorMessage ? (
        <p className="mt-3 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700 dark:border-red-900 dark:bg-red-950 dark:text-red-200" role="alert">
          {errorMessage}
        </p>
      ) : null}
      <div className="mt-4 rounded-lg border border-neutral-200 bg-neutral-50 p-4 dark:border-neutral-800 dark:bg-neutral-900">
        <p className="text-xs font-semibold uppercase tracking-wide text-neutral-500 dark:text-neutral-400">Streamed answer</p>
        <p className="mt-2 text-sm text-neutral-800 dark:text-neutral-100">{streamText || 'No stream output yet.'}</p>
      </div>
      <div className="mt-4 rounded-lg border border-neutral-200 bg-white p-4 dark:border-neutral-800 dark:bg-neutral-950">
        <p className="text-xs font-semibold uppercase tracking-wide text-neutral-500 dark:text-neutral-400">Event log</p>
        <ul className="mt-2 max-h-56 space-y-2 overflow-auto">
          {streamEvents.length === 0 ? (
            <li className="text-sm text-neutral-500 dark:text-neutral-400">No events yet.</li>
          ) : (
            streamEvents.map((event) => (
              <li key={event.id} className="rounded-md border border-neutral-200 px-2 py-1 font-mono text-xs text-neutral-700 dark:border-neutral-800 dark:text-neutral-300">
                {event.text}
              </li>
            ))
          )}
        </ul>
      </div>
    </article>
  )
}
