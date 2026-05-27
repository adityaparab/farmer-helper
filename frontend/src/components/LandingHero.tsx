import { Bot, ChartNoAxesCombined, FileUp, Sparkles } from 'lucide-react'

const highlights = [
  {
    icon: Bot,
    text: 'TanStack AI chat flow for real-time support.',
  },
  {
    icon: ChartNoAxesCombined,
    text: 'Admin analytics for ingestion and quality signals.',
  },
  {
    icon: FileUp,
    text: 'PDF upload to continuously improve answers.',
  },
]

export function LandingHero() {
  return (
    <article className="rounded-3xl border border-neutral-200 bg-gradient-to-br from-amber-50 via-orange-50 to-lime-50 p-6 shadow-sm md:p-8">
      <div className="inline-flex items-center gap-2 rounded-full border border-amber-200 bg-white/70 px-3 py-1 text-xs font-semibold text-amber-700">
        <Sparkles className="h-4 w-4" />
        Grounded AI Guidance
      </div>
      <p className="mt-4 max-w-xl text-lg leading-8 text-neutral-700">
        Query trusted documents, trace citations, and operationalize agronomy knowledge with a
        role-secured workflow for admins and field users.
      </p>
      <div className="mt-8 grid gap-3 text-sm text-neutral-700 md:grid-cols-3">
        {highlights.map((item) => (
          <div key={item.text} className="rounded-2xl border border-white/80 bg-white/80 p-4">
            <item.icon className="mb-2 h-5 w-5 text-orange-600" />
            {item.text}
          </div>
        ))}
      </div>
    </article>
  )
}
