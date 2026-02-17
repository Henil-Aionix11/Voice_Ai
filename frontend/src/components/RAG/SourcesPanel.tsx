import React, { useState } from 'react'
import { BookOpen, ChevronDown, ChevronUp } from 'lucide-react'
import { useVoiceStore } from '../../stores/useVoiceStore'

const SourcesPanel: React.FC = () => {
    const { sources } = useVoiceStore()
    const [expandedIndex, setExpandedIndex] = useState<number | null>(null)

    if (sources.length === 0) {
        return (
            <div className="glass-card p-6">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="font-semibold">RAG Sources</h3>
                </div>
                <div className="text-center py-8">
                    <BookOpen className="mx-auto mb-4 text-text-secondary" size={48} />
                    <p className="text-text-secondary text-sm">
                        Retrieved document chunks will appear here during conversation
                    </p>
                </div>
            </div>
        )
    }

    return (
        <div className="glass-card p-6">
            <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold">RAG Sources</h3>
                <span className="text-xs bg-accent-blue/20 text-accent-blue px-2 py-1 rounded">
                    {sources.length} chunks
                </span>
            </div>

            <div className="space-y-2 max-h-[400px] overflow-y-auto pr-2">
                {sources.map((source, index) => (
                    <div
                        key={index}
                        className="bg-primary-card border border-primary-border rounded-lg overflow-hidden"
                    >
                        <button
                            onClick={() => setExpandedIndex(expandedIndex === index ? null : index)}
                            className="w-full p-3 flex items-center justify-between hover:bg-primary-card/80 transition-colors"
                        >
                            <div className="flex items-center gap-2 flex-1 min-w-0">
                                <BookOpen size={16} className="text-accent-blue flex-shrink-0" />
                                <span className="text-sm font-medium truncate">{source.document_name}</span>
                            </div>
                            <div className="flex items-center gap-2 flex-shrink-0">
                                {source.similarity !== undefined && (
                                    <span className="text-xs text-text-secondary">
                                        {(source.similarity * 100).toFixed(0)}%
                                    </span>
                                )}
                                {expandedIndex === index ? (
                                    <ChevronUp size={16} className="text-text-secondary" />
                                ) : (
                                    <ChevronDown size={16} className="text-text-secondary" />
                                )}
                            </div>
                        </button>

                        {expandedIndex === index && (
                            <div className="px-3 pb-3">
                                <div className="bg-primary-bg/50 rounded p-3 text-sm text-text-secondary">
                                    {source.text}
                                </div>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    )
}

export default SourcesPanel
