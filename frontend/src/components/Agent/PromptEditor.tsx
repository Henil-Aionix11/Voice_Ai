import React, { useState, useEffect } from 'react'
import { Save, RotateCcw } from 'lucide-react'
import { useAppStore } from '../../stores/useAppStore'

const PromptEditor: React.FC = () => {
    const { currentPrompt, updatePrompt, resetPrompt, isLoading } = useAppStore()
    const [editedPrompt, setEditedPrompt] = useState(currentPrompt || '')

    useEffect(() => {
        setEditedPrompt(currentPrompt || '')
    }, [currentPrompt])

    const hasChanges = editedPrompt !== (currentPrompt || '')

    return (
        <div className="glass-card p-6">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold">Agent System Prompt</h2>
                <div className="flex gap-2">
                    <button
                        onClick={() => resetPrompt()}
                        disabled={isLoading}
                        className="btn-secondary flex items-center gap-2"
                        title="Reset to default"
                    >
                        <RotateCcw size={18} />
                        Reset
                    </button>
                    <button
                        onClick={() => updatePrompt(editedPrompt)}
                        disabled={isLoading || !hasChanges}
                        className="btn-primary flex items-center gap-2"
                    >
                        <Save size={18} />
                        Save Changes
                    </button>
                </div>
            </div>

            <textarea
                value={editedPrompt}
                onChange={(e) => setEditedPrompt(e.target.value)}
                disabled={isLoading}
                className="input-field w-full min-h-[400px] font-mono text-sm resize-y"
                placeholder="Enter system prompt..."
            />

            <div className="mt-4 flex items-center justify-between text-sm">
                <p className="text-text-secondary">
                    {(editedPrompt || '').length} characters
                </p>
                {hasChanges && (
                    <p className="text-accent-blue">
                        Unsaved changes
                    </p>
                )}
            </div>

            <div className="mt-4 bg-primary-card border border-primary-border rounded-lg p-4">
                <p className="text-text-secondary text-sm">
                    <strong className="text-text-primary">Tip:</strong> The system prompt defines how the AI
                    agent behaves during voice calls. Be specific about personality, tone, and how to use the
                    uploaded documents.
                </p>
            </div>
        </div>
    )
}

export default PromptEditor
