import type { AdminDashboardMetricCard } from '../api/client'

type MetricGridProps = {
  metrics: AdminDashboardMetricCard[]
}

export function MetricGrid({ metrics }: MetricGridProps) {
  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4" aria-label="Admin metrics">
      {metrics.map((metric) => (
        <article key={metric.label} className="rounded-lg border border-neutral-200 bg-white p-4 shadow-sm dark:border-neutral-800 dark:bg-neutral-950">
          <p className="text-sm text-neutral-500 dark:text-neutral-400">{metric.label}</p>
          <p className="mt-1 text-2xl font-semibold text-neutral-900 dark:text-neutral-50">
            {Intl.NumberFormat().format(metric.value)}
          </p>
        </article>
      ))}
    </div>
  )
}
