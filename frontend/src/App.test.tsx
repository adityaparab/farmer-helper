import { afterEach, describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

function jsonResponse(payload: unknown, init: ResponseInit = {}) {
  return new Response(JSON.stringify(payload), {
    status: init.status ?? 200,
    statusText: init.statusText,
    headers: { 'Content-Type': 'application/json' },
  })
}

function metricsPayload() {
  return {
    cards: [
      { label: 'Documents', value: 9 },
      { label: 'Embedded chunks', value: 52910 },
      { label: 'Chat messages', value: 4 },
      { label: 'QA review items', value: 2 },
      { label: 'Audit events', value: 12 },
    ],
    ingestion_jobs_by_status: { pending: 1 },
    chat_sessions_by_status: {},
    gold_answers_by_status: {},
    qa_review_items_by_status: { pending: 2 },
    embedding_jobs_by_status: {},
  }
}

function mockAuthSuccess(role: 'admin' | 'user') {
  const fetchSpy = vi
    .spyOn(globalThis, 'fetch')
    .mockResolvedValueOnce(
      jsonResponse({
        access_token: `${role}-access-token`,
        refresh_token: `${role}-refresh-token`,
        token_type: 'bearer',
        expires_in_seconds: 1800,
        user: { id: role === 'admin' ? 1 : 2, username: role, role },
      }),
    )
    .mockResolvedValueOnce(
      jsonResponse({ id: role === 'admin' ? 1 : 2, username: role, role }),
    )

  if (role === 'admin') {
    fetchSpy.mockResolvedValueOnce(jsonResponse(metricsPayload()))
  }

  return fetchSpy
}

describe('App', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders a concise landing and authentication experience for guests', () => {
    render(<App />)

    expect(screen.getByText('Precision support for farm operations')).toBeInTheDocument()
    expect(screen.getByText('Grounded AI Guidance')).toBeInTheDocument()
    expect(screen.getByRole('form', { name: 'Login or register' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Continue' })).toBeInTheDocument()
  })

  it('routes backend admin users to the admin dashboard', async () => {
    const fetchSpy = mockAuthSuccess('admin')
    const user = userEvent.setup()
    render(<App />)

    await user.type(screen.getByLabelText('Username'), 'admin')
    await user.type(screen.getByLabelText('Password'), 'P@ssw0rd')
    await user.click(screen.getByRole('button', { name: 'Continue' }))

    expect(await screen.findByRole('region', { name: 'Admin dashboard' })).toBeInTheDocument()
    expect(await screen.findByText('Documents')).toBeInTheDocument()
    expect(screen.getByText('52,910')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Select PDF' })).toBeInTheDocument()
    expect(fetchSpy).toHaveBeenCalledWith('/auth/login', expect.any(Object))
    expect(fetchSpy).toHaveBeenCalledWith('/auth/me', expect.any(Object))
    expect(fetchSpy).toHaveBeenCalledWith('/admin/dashboard/metrics', expect.any(Object))
  })

  it('uploads an admin PDF through the backend upload endpoint', async () => {
    const fetchSpy = mockAuthSuccess('admin')
    fetchSpy
      .mockResolvedValueOnce(
        jsonResponse({
          job_id: 42,
          document_id: 7,
          status: 'pending',
          source_path: '/uploads/soil.pdf',
          content_hash: 'hash',
          size_bytes: 12,
          document_created: true,
        }),
      )
      .mockResolvedValueOnce(jsonResponse(metricsPayload()))
    const user = userEvent.setup()
    render(<App />)

    await user.type(screen.getByLabelText('Username'), 'admin')
    await user.type(screen.getByLabelText('Password'), 'P@ssw0rd')
    await user.click(screen.getByRole('button', { name: 'Continue' }))
    await screen.findByRole('region', { name: 'Admin dashboard' })

    const file = new File(['%PDF-1.4'], 'soil.pdf', { type: 'application/pdf' })
    await user.upload(screen.getByLabelText('PDF file'), file)
    await user.clear(screen.getByLabelText('Content version'))
    await user.type(screen.getByLabelText('Content version'), 'content-v2')
    await user.click(screen.getByRole('button', { name: 'Upload PDF' }))

    expect(await screen.findByText('Upload accepted. Ingestion job 42 is pending.')).toBeInTheDocument()
    expect(fetchSpy).toHaveBeenCalledWith('/admin/documents/upload', expect.any(Object))
  })

  it('routes backend user-role users to chat and history in the same view', async () => {
    mockAuthSuccess('user')
    const user = userEvent.setup()
    render(<App />)

    await user.type(screen.getByLabelText('Username'), 'field-user')
    await user.type(screen.getByLabelText('Password'), 'secret')
    await user.click(screen.getByRole('button', { name: 'Continue' }))

    expect(await screen.findByRole('region', { name: 'User workspace' })).toBeInTheDocument()
    expect(screen.getByRole('complementary', { name: 'Question history' })).toBeInTheDocument()
  })

  it('adds submitted user questions to the top of history', async () => {
    const fetchSpy = mockAuthSuccess('user')
    fetchSpy.mockResolvedValueOnce(
      jsonResponse({
        response_mode: 'concise',
        language: 'en',
        decision: 'answer',
        answer: 'Increase organic matter and mulch around the root zone.',
        citations: [],
        clarification_message: null,
        clarification_code: null,
        refusal_reason: null,
        refusal_code: null,
        model: 'mock-chat-v1',
        finish_reason: 'stop',
        input_tokens: 12,
        output_tokens: 9,
        reliability_status: 'normal',
        reliability_retryable: null,
        reliability_code: null,
        degraded: false,
        degradation_code: null,
      }),
    )
    const user = userEvent.setup()
    render(<App />)

    await user.type(screen.getByLabelText('Username'), 'field-user')
    await user.click(screen.getByRole('button', { name: 'Continue' }))
    await screen.findByRole('region', { name: 'User workspace' })
    await user.type(
      screen.getByPlaceholderText('Ask about crop planning, irrigation, or disease response...'),
      'How do I improve soil moisture retention?',
    )
    await user.click(screen.getByRole('button', { name: 'Ask question' }))

    expect(screen.getByText('Q: How do I improve soil moisture retention?')).toBeInTheDocument()
    expect(
      screen.getByText('A: Increase organic matter and mulch around the root zone.'),
    ).toBeInTheDocument()
    expect(fetchSpy).toHaveBeenCalledWith('/answers/generate', expect.any(Object))
  })

  it('shows a chat error when answer generation fails', async () => {
    const fetchSpy = mockAuthSuccess('user')
    fetchSpy.mockResolvedValueOnce(
      jsonResponse(
        { detail: { code: 'ANSWER_UNAVAILABLE', message: 'Answer service unavailable' } },
        { status: 503, statusText: 'Service Unavailable' },
      ),
    )
    const user = userEvent.setup()
    render(<App />)

    await user.type(screen.getByLabelText('Username'), 'field-user')
    await user.click(screen.getByRole('button', { name: 'Continue' }))
    await screen.findByRole('region', { name: 'User workspace' })
    await user.type(screen.getByPlaceholderText('Ask about crop planning, irrigation, or disease response...'), 'What next?')
    await user.click(screen.getByRole('button', { name: 'Ask question' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Answer service unavailable')
    expect(screen.queryByText('Q: What next?')).not.toBeInTheDocument()
  })

  it('shows a backend login error without entering a role view', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce(
      jsonResponse(
        { detail: { code: 'AUTH_INVALID_CREDENTIALS', message: 'Invalid username or password' } },
        { status: 401, statusText: 'Unauthorized' },
      ),
    )
    const user = userEvent.setup()
    render(<App />)

    await user.type(screen.getByLabelText('Username'), 'admin')
    await user.type(screen.getByLabelText('Password'), 'wrong-password')
    await user.click(screen.getByRole('button', { name: 'Continue' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Invalid username or password')
    expect(screen.queryByRole('region', { name: 'Admin dashboard' })).not.toBeInTheDocument()
    expect(screen.getByRole('form', { name: 'Login or register' })).toBeInTheDocument()
  })

  it('logs out through the backend and returns to the guest auth view', async () => {
    const fetchSpy = mockAuthSuccess('user')
    fetchSpy.mockResolvedValueOnce(jsonResponse({ status: 'logged_out' }))
    const user = userEvent.setup()
    render(<App />)

    await user.type(screen.getByLabelText('Username'), 'field-user')
    await user.click(screen.getByRole('button', { name: 'Continue' }))
    await screen.findByRole('region', { name: 'User workspace' })
    await user.click(screen.getByRole('button', { name: 'Sign out' }))

    expect(await screen.findByRole('form', { name: 'Login or register' })).toBeInTheDocument()
    expect(screen.queryByRole('region', { name: 'User workspace' })).not.toBeInTheDocument()
    expect(fetchSpy).toHaveBeenCalledWith('/auth/logout', expect.any(Object))
  })
})
