import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

describe('App', () => {
  it('renders a concise landing and authentication experience for guests', () => {
    render(<App />)

    expect(screen.getByText('Precision support for farm operations')).toBeInTheDocument()
    expect(screen.getByText('Grounded AI Guidance')).toBeInTheDocument()
    expect(screen.getByRole('form', { name: 'Login or register' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Continue' })).toBeInTheDocument()
  })

  it('routes admin username to the admin dashboard', async () => {
    const user = userEvent.setup()
    render(<App />)

    await user.type(screen.getByLabelText('Username'), 'admin')
    await user.type(screen.getByLabelText('Password'), 'P@ssw0rd')
    await user.click(screen.getByRole('button', { name: 'Continue' }))

    expect(screen.getByRole('region', { name: 'Admin dashboard' })).toBeInTheDocument()
    expect(screen.getByText('Documents')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Select PDF' })).toBeInTheDocument()
  })

  it('routes non-admin users to chat and history in the same view', async () => {
    const user = userEvent.setup()
    render(<App />)

    await user.type(screen.getByLabelText('Username'), 'field-user')
    await user.type(screen.getByLabelText('Password'), 'secret')
    await user.click(screen.getByRole('button', { name: 'Continue' }))

    expect(screen.getByRole('region', { name: 'User workspace' })).toBeInTheDocument()
    expect(screen.getByRole('complementary', { name: 'Question history' })).toBeInTheDocument()
  })

  it('adds submitted user questions to the top of history', async () => {
    const user = userEvent.setup()
    render(<App />)

    await user.type(screen.getByLabelText('Username'), 'field-user')
    await user.click(screen.getByRole('button', { name: 'Continue' }))
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
})
