import api from './api'
import type { PromptResponse } from '../types'

export const agentService = {
    // Get current prompt
    getPrompt: async (): Promise<string> => {
        const response = await api.get<PromptResponse>('/agent/prompt')
        return response.data.data.prompt
    },

    // Update prompt
    updatePrompt: async (prompt: string): Promise<string> => {
        const response = await api.put<PromptResponse>('/agent/prompt', { prompt })
        return response.data.data.prompt
    },

    // Reset prompt to default
    resetPrompt: async (): Promise<string> => {
        const response = await api.post<PromptResponse>('/agent/prompt/reset')
        return response.data.data.prompt
    },
}
