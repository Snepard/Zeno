export type JobStatus = 'pending' | 'partial' | 'complete' | 'failed'

export type JobType = 'lecture' | 'podcast' | 'flashcards'

export interface JobResponse {
  job_id: string
  status: JobStatus
  type?: JobType
  output?: Record<string, unknown>
  error?: string | null
}
