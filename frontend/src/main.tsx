import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App'

const THEME_STORAGE_KEY = 'farmer-helper.theme-mode'

if (typeof window !== 'undefined') {
  const storedTheme = window.localStorage.getItem(THEME_STORAGE_KEY)
  const theme = storedTheme === 'light' || storedTheme === 'dark' ? storedTheme : 'dark'
  document.documentElement.classList.toggle('dark', theme === 'dark')
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
