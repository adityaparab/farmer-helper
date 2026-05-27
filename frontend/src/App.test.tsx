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

function mockAuthSuccess(role: 'admin' | 'user') {
  return vi
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
    expect(screen.getByText('Documents')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Select PDF' })).toBeInTheDocument()
    expect(fetchSpy).toHaveBeenCalledWith('/auth/login', expect.any(Object))
    expect(fetchSpy).toHaveBeenCalledWith('/auth/me', expect.any(Object))
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
    mockAuthSuccess('user')
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
      screen.getByText(
        'A: Draft answer generated from current backend contract. TanStack AI streaming integration is next in the implementation queue.',
      ),
    ).toBeInTheDocument()
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
