import type { Metric } from '../types'

type MetricGridProps = {
  metrics: Metric[]
}

export function MetricGrid({ metrics }: MetricGridProps) {
  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4" aria-label="Admin metrics">
      {metrics.map((metric) => (
        <article key={metric.label} className="rounded-2xl border border-neutral-200 bg-white p-4 shadow-sm">
          <p className="text-sm text-neutral-500">{metric.label}</p>
          <p className="mt-1 text-2xl font-semibold text-neutral-900">{metric.value}</p>
        </article>
      ))}
    </div>
  )
}
