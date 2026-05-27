export type BackendRole = 'admin' | 'user'

export type AuthUserResponse = {
  id: number
  username: string
  role: BackendRole
}

export type AuthTokenResponse = {
  access_token: string
  refresh_token: string
  token_type: 'bearer'
  expires_in_seconds: number
  user: AuthUserResponse
}

export type AuthMessageResponse = {
  status: string
}

export type AdminJobStatus = 'pending' | 'processing' | 'succeeded' | 'failed'

export type AdminDashboardMetricCard = {
  label: string
  value: number
}

export type AdminDashboardMetricsResponse = {
  cards: AdminDashboardMetricCard[]
  ingestion_jobs_by_status: Record<string, number>
  chat_sessions_by_status: Record<string, number>
  gold_answers_by_status: Record<string, number>
  qa_review_items_by_status: Record<string, number>
  embedding_jobs_by_status: Record<string, number>
}

export type AdminPdfUploadResponse = {
  job_id: number
  document_id: number
  status: AdminJobStatus
  source_path: string
  content_hash: string
  size_bytes: number
  document_created: boolean
}

export type Citation = {
  document_id: number
  chunk_index: number
  content_hash: string
}

export type RetrievedChunk = {
  citation: Citation
  text: string
  score: number
}

export type AnswerGenerationRequest = {
  question: string
  retrieved_chunks?: RetrievedChunk[]
  idempotency_key?: string
  session_key?: string
  context_max_messages?: number
  context_max_turns?: number
  model?: string
  response_mode?: 'concise' | 'detailed'
  language?: string
  max_chunks?: number
  max_answer_tokens?: number
  temperature?: number
}

export type AnswerGenerationResponse = {
  response_mode: 'concise' | 'detailed'
  language: string
  decision: 'answer' | 'clarify' | 'refuse'
  answer: string | null
  citations: Citation[]
  clarification_message: string | null
  clarification_code: string | null
  refusal_reason: string | null
  refusal_code: string | null
  model: string | null
  finish_reason: 'stop' | 'length' | 'content_filter' | null
  input_tokens: number
  output_tokens: number
  reliability_status: 'normal' | 'degraded'
  reliability_retryable: boolean | null
  reliability_code: string | null
  degraded: boolean
  degradation_code: string | null
}

type FetchLike = (input: RequestInfo | URL, init?: RequestInit) => Promise<Response>

type ApiClientConfig = {
  baseUrl?: string
  apiKey?: string
  getAccessToken?: () => string | null
  fetchImpl?: FetchLike
}

type RequestOptions = {
  method?: string
  body?: unknown
  formData?: FormData
  authenticated?: boolean
}

export class ApiError extends Error {
  status: number
  code: string | null
  details: unknown

  constructor(message: string, status: number, code: string | null = null, details: unknown = null) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.code = code
    this.details = details
  }
}

function normalizeBaseUrl(value: string | undefined): string {
  return (value ?? '').replace(/\/$/, '')
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
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

function detailCode(detail: unknown): string | null {
  if (isRecord(detail) && typeof detail.code === 'string') {
    return detail.code
  }

  return null
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

export function createApiClient(config: ApiClientConfig = {}) {
  const baseUrl = normalizeBaseUrl(config.baseUrl)
  const fetchImpl = config.fetchImpl ?? fetch.bind(globalThis)

  const buildUrl = (path: string) => `${baseUrl}${path}`

  const request = async <TResponse>(path: string, options: RequestOptions = {}): Promise<TResponse> => {
    const headers = new Headers()
    if (config.apiKey) {
      headers.set('x-api-key', config.apiKey)
    }

    const accessToken = config.getAccessToken?.()
    if (options.authenticated && accessToken) {
      headers.set('Authorization', `Bearer ${accessToken}`)
    }

    let body: BodyInit | undefined
    if (options.formData) {
      body = options.formData
    } else if (options.body !== undefined) {
      headers.set('Content-Type', 'application/json')
      body = JSON.stringify(options.body)
    }

    const response = await fetchImpl(buildUrl(path), {
      method: options.method ?? 'GET',
      headers,
      body,
    })
    const payload = await parseJson(response)

    if (!response.ok) {
      const detail = isRecord(payload) ? payload.detail : payload
      const message = detailMessage(detail) ?? response.statusText ?? 'Request failed'
      throw new ApiError(message, response.status, detailCode(detail), payload)
    }

    return payload as TResponse
  }

  return {
    auth: {
      login: (username: string, password: string) =>
        request<AuthTokenResponse>('/auth/login', {
          method: 'POST',
          body: { username, password },
        }),
      register: (username: string, password: string) =>
        request<AuthTokenResponse>('/auth/register', {
          method: 'POST',
          body: { username, password },
        }),
      me: () =>
        request<AuthUserResponse>('/auth/me', {
          authenticated: true,
        }),
      refresh: (refreshToken: string) =>
        request<AuthTokenResponse>('/auth/refresh', {
          method: 'POST',
          body: { refresh_token: refreshToken },
        }),
      logout: (refreshToken: string) =>
        request<AuthMessageResponse>('/auth/logout', {
          method: 'POST',
          body: { refresh_token: refreshToken },
        }),
    },
    admin: {
      getDashboardMetrics: () =>
        request<AdminDashboardMetricsResponse>('/admin/dashboard/metrics', {
          authenticated: true,
        }),
      uploadPdf: (file: File, contentVersion = 'v1') => {
        const formData = new FormData()
        formData.set('file', file)
        formData.set('content_version', contentVersion)
        return request<AdminPdfUploadResponse>('/admin/documents/upload', {
          method: 'POST',
          formData,
          authenticated: true,
        })
      },
    },
    answers: {
      generate: (payload: AnswerGenerationRequest) =>
        request<AnswerGenerationResponse>('/answers/generate', {
          method: 'POST',
          body: payload,
          authenticated: true,
        }),
    },
  }
}