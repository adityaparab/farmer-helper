import { describe, expect, it } from 'vitest'
import { ApiError, createApiClient } from './client'

type CapturedRequest = {
  input: RequestInfo | URL
  init: RequestInit | undefined
}

function jsonResponse(payload: unknown, init: ResponseInit = {}) {
  return new Response(JSON.stringify(payload), {
    status: init.status ?? 200,
    statusText: init.statusText,
    headers: { 'Content-Type': 'application/json' },
  })
}

function createFetchStub(response: Response) {
  const requests: CapturedRequest[] = []
  const fetchImpl = async (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
    requests.push({ input, init })
    return response
  }

  return { fetchImpl, requests }
}

describe('createApiClient', () => {
  it('posts login credentials as JSON and returns typed auth tokens', async () => {
    const { fetchImpl, requests } = createFetchStub(
      jsonResponse({
        access_token: 'access-token',
        refresh_token: 'refresh-token',
        token_type: 'bearer',
        expires_in_seconds: 1800,
        user: { id: 1, username: 'admin', role: 'admin' },
      }),
    )
    const client = createApiClient({ baseUrl: '/api', fetchImpl })

    const result = await client.auth.login('admin', 'P@ssw0rd')

    expect(result.user.role).toBe('admin')
    expect(requests[0].input).toBe('/api/auth/login')
    expect(requests[0].init?.method).toBe('POST')
    expect(new Headers(requests[0].init?.headers).get('Content-Type')).toBe('application/json')
    expect(requests[0].init?.body).toBe(JSON.stringify({ username: 'admin', password: 'P@ssw0rd' }))
  })

  it('adds bearer and API-key headers for authenticated admin requests', async () => {
    const { fetchImpl, requests } = createFetchStub(
      jsonResponse({
        cards: [{ label: 'Documents', value: 3 }],
        ingestion_jobs_by_status: { pending: 1 },
        chat_sessions_by_status: {},
        gold_answers_by_status: {},
        qa_review_items_by_status: {},
        embedding_jobs_by_status: {},
      }),
    )
    const client = createApiClient({
      apiKey: 'dev-api-key',
      fetchImpl,
      getAccessToken: () => 'access-token',
    })

    await client.admin.getDashboardMetrics()

    const headers = new Headers(requests[0].init?.headers)
    expect(headers.get('Authorization')).toBe('Bearer access-token')
    expect(headers.get('x-api-key')).toBe('dev-api-key')
  })

  it('sends PDF uploads as multipart form data without forcing a JSON content type', async () => {
    const { fetchImpl, requests } = createFetchStub(
      jsonResponse({
        job_id: 7,
        document_id: 4,
        status: 'pending',
        source_path: '/uploads/hash.pdf',
        content_hash: 'abc123',
        size_bytes: 12,
        document_created: true,
      }),
    )
    const client = createApiClient({ fetchImpl, getAccessToken: () => 'access-token' })
    const file = new File(['%PDF-1.4'], 'guide.pdf', { type: 'application/pdf' })

    const result = await client.admin.uploadPdf(file, 'content-v2')

    const headers = new Headers(requests[0].init?.headers)
    expect(result.job_id).toBe(7)
    expect(requests[0].init?.body).toBeInstanceOf(FormData)
    expect(headers.get('Content-Type')).toBeNull()
  })

  it('normalizes backend error details into ApiError', async () => {
    const { fetchImpl } = createFetchStub(
      jsonResponse(
        {
          detail: { code: 'AUTH_INVALID_CREDENTIALS', message: 'Invalid username or password' },
        },
        { status: 401, statusText: 'Unauthorized' },
      ),
    )
    const client = createApiClient({ fetchImpl })

    await expect(client.auth.login('admin', 'bad-password')).rejects.toMatchObject({
      name: 'ApiError',
      status: 401,
      code: 'AUTH_INVALID_CREDENTIALS',
      message: 'Invalid username or password',
    } satisfies Partial<ApiError>)
  })
})