import { create } from 'zustand'
import type { Document } from '../types'
import { documentService } from '../services/documents'
import { agentService } from '../services/agent'
import toast from 'react-hot-toast'

interface AppStore {
    // State
    documents: Document[]
    currentPrompt: string
    isLoading: boolean
    error: string | null

    // Document actions
    fetchDocuments: () => Promise<void>
    uploadDocuments: (files: File[]) => Promise<void>
    deleteDocument: (id: string) => Promise<void>

    // Prompt actions
    fetchPrompt: () => Promise<void>
    updatePrompt: (prompt: string) => Promise<void>
    resetPrompt: () => Promise<void>

    // Utility
    setLoading: (loading: boolean) => void
    setError: (error: string | null) => void
}

export const useAppStore = create<AppStore>((set, get) => ({
    // Initial state
    documents: [],
    currentPrompt: '',
    isLoading: false,
    error: null,

    // Document actions
    fetchDocuments: async () => {
        try {
            set({ isLoading: true, error: null })
            const documents = await documentService.list()
            set({ documents, isLoading: false })
        } catch (error: any) {
            const message = error.response?.data?.detail || 'Failed to fetch documents'
            set({ error: message, isLoading: false })
            toast.error(message)
        }
    },

    uploadDocuments: async (files: File[]) => {
        try {
            set({ isLoading: true, error: null })
            const result = await documentService.upload(files)

            if (result.total_uploaded > 0) {
                toast.success(`Successfully uploaded ${result.total_uploaded} document(s)`)
            }

            if (result.total_failed > 0) {
                toast.error(`Failed to upload ${result.total_failed} document(s)`)
            }

            // Refresh document list
            await get().fetchDocuments()
        } catch (error: any) {
            const message = error.response?.data?.detail || 'Failed to upload documents'
            set({ error: message, isLoading: false })
            toast.error(message)
        }
    },

    deleteDocument: async (id: string) => {
        try {
            set({ isLoading: true, error: null })
            await documentService.delete(id)
            toast.success('Document deleted')

            // Refresh document list
            await get().fetchDocuments()
        } catch (error: any) {
            const message = error.response?.data?.detail || 'Failed to delete document'
            set({ error: message, isLoading: false })
            toast.error(message)
        }
    },

    // Prompt actions
    fetchPrompt: async () => {
        try {
            set({ isLoading: true, error: null })
            const prompt = await agentService.getPrompt()
            set({ currentPrompt: prompt, isLoading: false })
        } catch (error: any) {
            const message = error.response?.data?.detail || 'Failed to fetch prompt'
            set({ error: message, isLoading: false })
            toast.error(message)
        }
    },

    updatePrompt: async (prompt: string) => {
        try {
            set({ isLoading: true, error: null })
            const updatedPrompt = await agentService.updatePrompt(prompt)
            set({ currentPrompt: updatedPrompt, isLoading: false })
            toast.success('Prompt updated')
        } catch (error: any) {
            const message = error.response?.data?.detail || 'Failed to update prompt'
            set({ error: message, isLoading: false })
            toast.error(message)
        }
    },

    resetPrompt: async () => {
        try {
            set({ isLoading: true, error: null })
            const prompt = await agentService.resetPrompt()
            set({ currentPrompt: prompt, isLoading: false })
            toast.success('Prompt reset to default')
        } catch (error: any) {
            const message = error.response?.data?.detail || 'Failed to reset prompt'
            set({ error: message, isLoading: false })
            toast.error(message)
        }
    },

    // Utility
    setLoading: (loading: boolean) => set({ isLoading: loading }),
    setError: (error: string | null) => set({ error }),
}))
