import { useRef, useState } from 'react'
import { FileUp } from 'lucide-react'
import { ApiError } from '../api/client'
import type { AdminPdfUploadResponse } from '../api/client'

type PdfUploadPanelProps = {
  onUpload: (file: File, contentVersion: string) => Promise<AdminPdfUploadResponse>
}

type UploadState =
  | { status: 'idle' }
  | { status: 'uploading' }
  | { status: 'success'; response: AdminPdfUploadResponse }
  | { status: 'error'; message: string }

function uploadErrorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    return error.message
  }

  return 'Unable to upload PDF.'
}

export function PdfUploadPanel({ onUpload }: PdfUploadPanelProps) {
  const inputRef = useRef<HTMLInputElement | null>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [contentVersion, setContentVersion] = useState('v1')
  const [uploadState, setUploadState] = useState<UploadState>({ status: 'idle' })

  const chooseFile = () => inputRef.current?.click()

  const uploadSelectedFile = async () => {
    if (!selectedFile) {
      setUploadState({ status: 'error', message: 'Select a PDF before uploading.' })
      return
    }

    setUploadState({ status: 'uploading' })
    try {
      const response = await onUpload(selectedFile, contentVersion)
      setUploadState({ status: 'success', response })
    } catch (error) {
      setUploadState({ status: 'error', message: uploadErrorMessage(error) })
    }
  }

  return (
    <article className="rounded-3xl border border-neutral-200 bg-white p-6 shadow-sm">
      <h2 className="font-heading text-2xl font-semibold text-neutral-900">Upload PDF</h2>
      <p className="mt-1 text-sm text-neutral-600">
        Add curated source documents for ingestion, embedding, and grounded answer generation.
      </p>
      <input
        ref={inputRef}
        type="file"
        accept="application/pdf,.pdf"
        aria-label="PDF file"
        className="sr-only"
        onChange={(event) => setSelectedFile(event.target.files?.[0] ?? null)}
      />
      <label className="mt-4 block max-w-xs text-sm font-medium text-neutral-700">
        Content version
        <input
          className="mt-1 w-full rounded-xl border border-neutral-300 px-3 py-2 outline-none transition focus:border-amber-500"
          value={contentVersion}
          onChange={(event) => setContentVersion(event.target.value)}
        />
      </label>
      {selectedFile ? <SelectedFileName name={selectedFile.name} /> : null}
      <UploadStateMessage state={uploadState} />
      <button
        type="button"
        onClick={chooseFile}
        className="mt-4 inline-flex items-center gap-2 rounded-xl border border-neutral-300 px-4 py-2 text-sm font-medium text-neutral-700 transition hover:bg-neutral-50"
      >
        <FileUp className="h-4 w-4" />
        Select PDF
      </button>
      <button
        type="button"
        onClick={uploadSelectedFile}
        disabled={uploadState.status === 'uploading'}
        className="ml-3 mt-4 inline-flex items-center gap-2 rounded-xl bg-neutral-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-neutral-800 disabled:cursor-not-allowed disabled:bg-neutral-500"
      >
        Upload PDF
      </button>
    </article>
  )
}

type SelectedFileNameProps = {
  name: string
}

function SelectedFileName({ name }: SelectedFileNameProps) {
  return <p className="mt-3 text-sm text-neutral-700">Selected: {name}</p>
}

type UploadStateMessageProps = {
  state: UploadState
}

function UploadStateMessage({ state }: UploadStateMessageProps) {
  if (state.status === 'idle') {
    return null
  }

  if (state.status === 'uploading') {
    return <p className="mt-3 text-sm text-neutral-600" role="status">Uploading PDF...</p>
  }

  if (state.status === 'error') {
    return <p className="mt-3 text-sm text-red-700" role="alert">{state.message}</p>
  }

  return (
    <p className="mt-3 text-sm text-emerald-700" role="status">
      Upload accepted. Ingestion job {state.response.job_id} is {state.response.status}.
    </p>
  )
}
