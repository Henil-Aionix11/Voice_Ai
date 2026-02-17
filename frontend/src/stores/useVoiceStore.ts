import { create } from 'zustand'
import type { TranscriptItem, Source } from '../types'

interface VoiceStore {
    // State
    isConnected: boolean
    isMuted: boolean
    isAgentSpeaking: boolean
    livekitToken: string | null
    roomName: string
    transcript: TranscriptItem[]
    sources: Source[]

    // Actions
    setConnected: (connected: boolean) => void
    setMuted: (muted: boolean) => void
    setAgentSpeaking: (speaking: boolean) => void
    setLivekitToken: (token: string | null) => void
    setRoomName: (name: string) => void
    addTranscript: (item: Omit<TranscriptItem, 'id' | 'timestamp'>) => void
    clearTranscript: () => void
    setSources: (sources: Source[]) => void
    clearSources: () => void
    reset: () => void
}

export const useVoiceStore = create<VoiceStore>((set) => ({
    // Initial state
    isConnected: false,
    isMuted: false,
    isAgentSpeaking: false,
    livekitToken: null,
    roomName: 'voice-ai-room',
    transcript: [],
    sources: [],

    // Actions
    setConnected: (connected) => set({ isConnected: connected }),

    setMuted: (muted) => set({ isMuted: muted }),

    setAgentSpeaking: (speaking) => set({ isAgentSpeaking: speaking }),

    setLivekitToken: (token) => set({ livekitToken: token }),

    setRoomName: (name) => set({ roomName: name }),

    addTranscript: (item) =>
        set((state) => ({
            transcript: [
                ...state.transcript,
                {
                    ...item,
                    id: `${Date.now()}-${Math.random()}`,
                    timestamp: new Date(),
                },
            ],
        })),

    clearTranscript: () => set({ transcript: [] }),

    setSources: (sources) => set({ sources }),

    clearSources: () => set({ sources: [] }),

    reset: () =>
        set({
            isConnected: false,
            isMuted: false,
            isAgentSpeaking: false,
            livekitToken: null,
            transcript: [],
            sources: [],
        }),
}))
