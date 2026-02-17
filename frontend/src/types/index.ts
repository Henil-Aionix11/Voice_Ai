// API Types
export interface Document {
    document_id: string
    filename: string
    file_size: number
    total_chunks: number
    status: 'indexed' | 'processing' | 'failed'
    uploaded_at?: string
}

export interface UploadResponse {
    success: boolean
    data: {
        successful: Document[]
        failed: Array<{ filename: string; error: string }>
    }
    total_uploaded: number
    total_failed: number
}

export interface PromptResponse {
    success: boolean
    data: {
        prompt: string
    }
}

export interface LiveKitTokenData {
    token: string
    url: string
    room_name: string
    participant_name: string
}

export interface LiveKitTokenResponse {
    success: boolean
    data: LiveKitTokenData
}

export interface QueryResponse {
    success: boolean
    answer: string
    sources: Source[]
    chunks_used: number
}

export interface Source {
    document_name: string
    text: string
    similarity?: number
}

// UI Types
export interface TranscriptItem {
    id: string
    speaker: 'user' | 'agent'
    text: string
    timestamp: Date
}

export interface AppState {
    documents: Document[]
    currentPrompt: string
    isLoading: boolean
    error: string | null
}

export interface VoiceState {
    isConnected: boolean
    isMuted: boolean
    isAgentSpeaking: boolean
    transcript: TranscriptItem[]
    sources: Source[]
}
