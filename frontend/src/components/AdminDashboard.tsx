import { useCallback, useEffect, useState } from 'react'
import { ApiError } from '../api/client'
import type { AdminDashboardMetricsResponse, AdminPdfUploadResponse, ApiClient } from '../api/client'
import { MetricGrid } from './MetricGrid'
import { PdfUploadPanel } from './PdfUploadPanel'

type AdminDashboardProps = {
  apiClient: ApiClient
}

type MetricsState =
  | { status: 'loading' }
  | { status: 'ready'; metrics: AdminDashboardMetricsResponse }
  | { status: 'error'; message: string }

function errorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    return error.message
  }

  return 'Unable to load admin data.'
}

export function AdminDashboard({ apiClient }: AdminDashboardProps) {
  const [metricsState, setMetricsState] = useState<MetricsState>({ status: 'loading' })

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

  return (
    <section className="space-y-6" aria-label="Admin dashboard">
      <AdminMetricsView state={metricsState} />
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
