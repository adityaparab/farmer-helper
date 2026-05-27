import { FileUp } from 'lucide-react'

export function PdfUploadPanel() {
  return (
    <article className="rounded-3xl border border-neutral-200 bg-white p-6 shadow-sm">
      <h2 className="font-heading text-2xl font-semibold text-neutral-900">Upload PDF</h2>
      <p className="mt-1 text-sm text-neutral-600">
        Add curated source documents for ingestion, embedding, and grounded answer generation.
      </p>
      <button
        type="button"
        className="mt-4 inline-flex items-center gap-2 rounded-xl border border-neutral-300 px-4 py-2 text-sm font-medium text-neutral-700 transition hover:bg-neutral-50"
      >
        <FileUp className="h-4 w-4" />
        Select PDF
      </button>
    </article>
  )
}
