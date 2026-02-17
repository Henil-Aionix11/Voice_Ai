import React from 'react'
import { FileText, Trash2, File } from 'lucide-react'
import { useAppStore } from '../../stores/useAppStore'
import type { Document } from '../../types'

const DocumentList: React.FC = () => {
    const { documents, deleteDocument, isLoading } = useAppStore()

    if (!documents || documents.length === 0) {
        return (
            <div className="glass-card p-12 text-center">
                <File className="mx-auto mb-4 text-text-secondary" size={48} />
                <p className="text-text-secondary">No documents uploaded yet</p>
                <p className="text-text-secondary text-sm mt-2">
                    Upload documents to start building your knowledge base
                </p>
            </div>
        )
    }

    return (
        <div className="glass-card p-6">
            <h2 className="text-xl font-semibold mb-4">Uploaded Documents</h2>

            <div className="space-y-3">
                {documents.map((doc: Document) => (
                    <div
                        key={doc.document_id}
                        className="bg-primary-card border border-primary-border rounded-lg p-4 flex items-center justify-between hover:border-accent-blue/50 transition-colors"
                    >
                        <div className="flex items-center gap-3 flex-1">
                            <FileText className="text-accent-blue flex-shrink-0" size={24} />
                            <div className="flex-1 min-w-0">
                                <p className="font-medium truncate">{doc.filename}</p>
                                <div className="flex items-center gap-4 mt-1">
                                    <span className="text-text-secondary text-xs">
                                        {(doc.file_size / 1024).toFixed(1)} KB
                                    </span>
                                    <span className="text-text-secondary text-xs">
                                        {doc.total_chunks} chunks
                                    </span>
                                    <span
                                        className={`text-xs px-2 py-1 rounded ${doc.status === 'indexed'
                                            ? 'bg-accent-green/20 text-accent-green'
                                            : 'bg-accent-purple/20 text-accent-purple'
                                            }`}
                                    >
                                        {doc.status}
                                    </span>
                                </div>
                            </div>
                        </div>

                        <button
                            onClick={() => deleteDocument(doc.document_id)}
                            disabled={isLoading}
                            className="text-text-secondary hover:text-accent-red transition-colors p-2 rounded-lg hover:bg-accent-red/10 disabled:opacity-50"
                            title="Delete document"
                        >
                            <Trash2 size={18} />
                        </button>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default DocumentList
