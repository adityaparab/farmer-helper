import type { Metric } from '../types'
import { MetricGrid } from './MetricGrid'
import { PdfUploadPanel } from './PdfUploadPanel'

type AdminDashboardProps = {
  metrics: Metric[]
}

export function AdminDashboard({ metrics }: AdminDashboardProps) {
  return (
    <section className="space-y-6" aria-label="Admin dashboard">
      <MetricGrid metrics={metrics} />
      <PdfUploadPanel />
    </section>
  )
}
