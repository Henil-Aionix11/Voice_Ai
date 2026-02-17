import api from './api'
import type { Document, UploadResponse } from '../types'

export const documentService = {
    // Upload multiple documents
    upload: async (files: File[]): Promise<UploadResponse> => {
        const formData = new FormData()
        files.forEach((file) => {
            formData.append('files', file)
        })

        const response = await api.post<UploadResponse>('/documents/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })
        return response.data
    },

    // List all documents
    list: async (): Promise<Document[]> => {
        const response = await api.get<{ success: boolean; data: Document[] }>('/documents')
        return response.data.data  // Backend returns { success, data: [...] }
    },

    // Delete document by ID
    delete: async (documentId: string): Promise<void> => {
        await api.delete(`/documents/${documentId}`)
    },
}
