import React, { useEffect, useRef } from 'react'
import { MessageCircle, Trash2 } from 'lucide-react'
import { useVoiceStore } from '../../stores/useVoiceStore'
import { format } from 'date-fns'

const TranscriptViewer: React.FC = () => {
    const { transcript, clearTranscript } = useVoiceStore()
    const bottomRef = useRef<HTMLDivElement>(null)

    // Auto-scroll to bottom
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [transcript])

    if (transcript.length === 0) {
        return (
            <div className="glass-card p-6">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="font-semibold">Live Transcript</h3>
                </div>
                <div className="text-center py-12">
                    <MessageCircle className="mx-auto mb-4 text-text-secondary" size={48} />
                    <p className="text-text-secondary">
                        Start a conversation to see the transcript here
                    </p>
                </div>
            </div>
        )
    }

    return (
        <div className="glass-card p-6">
            <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold">Live Transcript</h3>
                <button
                    onClick={clearTranscript}
                    className="text-text-secondary hover:text-accent-red transition-colors p-2 rounded-lg hover:bg-accent-red/10"
                    title="Clear transcript"
                >
                    <Trash2 size={18} />
                </button>
            </div>

            <div className="space-y-3 max-h-[400px] overflow-y-auto pr-2">
                {transcript.map((item) => (
                    <div
                        key={item.id}
                        className={`rounded-lg p-3 ${item.speaker === 'user'
                                ? 'bg-accent-blue/20 border border-accent-blue/30'
                                : 'bg-primary-card border border-primary-border'
                            }`}
                    >
                        <div className="flex items-center justify-between mb-1">
                            <span className="text-xs font-medium text-text-secondary">
                                {item.speaker === 'user' ? 'You' : 'Agent'}
                            </span>
                            <span className="text-xs text-text-secondary">
                                {format(item.timestamp, 'HH:mm:ss')}
                            </span>
                        </div>
                        <p className="text-sm">{item.text}</p>
                    </div>
                ))}
                <div ref={bottomRef} />
            </div>
        </div>
    )
}

export default TranscriptViewer
