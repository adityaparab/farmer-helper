import { TextStreamChatTransport } from 'ai'
import type { UIMessage } from 'ai'
import type { AnswerGenerationResponse } from '../api/client'

type AnswerChatTransportConfig = {
  baseUrl?: string
  getAccessToken: () => string | null
  sessionKey?: string
  fetchImpl?: typeof fetch
}

function normalizeBaseUrl(value: string | undefined): string {
  return (value ?? '').replace(/\/$/, '')
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

async function parseJson(response: Response): Promise<unknown> {
  const text = await response.text()
  if (!text) {
    return null
  }

  try {
    return JSON.parse(text) as unknown
  } catch {
    return text
  }
}

function detailMessage(detail: unknown): string | null {
  if (typeof detail === 'string') {
    return detail
  }

  if (isRecord(detail) && typeof detail.message === 'string') {
    return detail.message
  }

  return null
}

export function answerText(response: AnswerGenerationResponse): string {
  if (response.decision === 'answer' && response.answer) {
    return response.answer
  }

  if (response.decision === 'clarify' && response.clarification_message) {
    return response.clarification_message
  }

  if (response.decision === 'refuse' && response.refusal_reason) {
    return response.refusal_reason
  }

  return 'The answer service returned no displayable response.'
}

function messageText(message: UIMessage): string {
  return message.parts
    .filter((part) => part.type === 'text')
    .map((part) => part.text)
    .join('')
    .trim()
}

function getLatestUserQuestion(messages: UIMessage[]): string {
  const latestUserMessage = [...messages].reverse().find((message) => message.role === 'user')
  return latestUserMessage ? messageText(latestUserMessage) : ''
}

export function createAnswerChatTransport({
  baseUrl,
  getAccessToken,
  sessionKey,
  fetchImpl = fetch.bind(globalThis),
}: AnswerChatTransportConfig) {
  const api = `${normalizeBaseUrl(baseUrl)}/answers/generate`

  return new TextStreamChatTransport({
    api,
    prepareSendMessagesRequest: ({ api: requestApi, headers, messages }) => {
      const accessToken = getAccessToken()
      return {
        api: requestApi,
        headers: {
          ...headers,
          ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
        },
        body: {
          question: getLatestUserQuestion(messages),
          session_key: sessionKey,
          response_mode: 'concise',
        },
      }
    },
    fetch: async (input, init) => {
      const response = await fetchImpl(input, init)
      const payload = await parseJson(response)

      if (!response.ok) {
        const detail = isRecord(payload) ? payload.detail : payload
        throw new Error(detailMessage(detail) ?? response.statusText ?? 'Request failed')
      }

      return new Response(answerText(payload as AnswerGenerationResponse), {
        headers: { 'Content-Type': 'text/plain; charset=utf-8' },
      })
    },
  })
}
