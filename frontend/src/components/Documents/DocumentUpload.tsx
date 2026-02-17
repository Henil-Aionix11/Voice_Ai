import React, { useCallback, useState } from 'react'
import { Upload, X } from 'lucide-react'
import { useAppStore } from '../../stores/useAppStore'

const DocumentUpload: React.FC = () => {
    const [dragActive, setDragActive] = useState(false)
    const { uploadDocuments, isLoading } = useAppStore()

    const handleDrag = useCallback((e: React.DragEvent) => {
        e.preventDefault()
        e.stopPropagation()
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true)
        } else if (e.type === 'dragleave') {
            setDragActive(false)
        }
    }, [])

    const handleDrop = useCallback(
        (e: React.DragEvent) => {
            e.preventDefault()
            e.stopPropagation()
            setDragActive(false)

            if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
                const files = Array.from(e.dataTransfer.files)
                uploadDocuments(files)
            }
        },
        [uploadDocuments]
    )

    const handleChange = useCallback(
        (e: React.ChangeEvent<HTMLInputElement>) => {
            if (e.target.files && e.target.files.length > 0) {
                const files = Array.from(e.target.files)
                uploadDocuments(files)
            }
        },
        [uploadDocuments]
    )

    return (
        <div className="glass-card p-6">
            <h2 className="text-xl font-semibold mb-4">Upload Documents</h2>

            <div
                className={`border-2 border-dashed rounded-lg p-8 text-center transition-all ${dragActive
                        ? 'border-accent-blue bg-accent-blue/10'
                        : 'border-primary-border hover:border-accent-blue/50'
                    } ${isLoading ? 'opacity-50 pointer-events-none' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
            >
                <Upload className="mx-auto mb-4 text-text-secondary" size={48} />
                <p className="text-lg font-medium mb-2">
                    {dragActive ? 'Drop files here' : 'Drag & drop files here'}
                </p>
                <p className="text-text-secondary text-sm mb-4">or</p>
                <label className="btn-primary cursor-pointer inline-block">
                    <input
                        type="file"
                        multiple
                        accept=".pdf,.txt"
                        onChange={handleChange}
                        className="hidden"
                        disabled={isLoading}
                    />
                    Browse Files
                </label>
                <p className="text-text-secondary text-xs mt-4">Supports: PDF, TXT (Max 10MB per file)</p>
            </div>

            {isLoading && (
                <div className="mt-4 text-center">
                    <div className="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-accent-blue"></div>
                    <p className="text-text-secondary text-sm mt-2">Processing documents...</p>
                </div>
            )}
        </div>
    )
}

export default DocumentUpload
