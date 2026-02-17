import { useEffect, useState } from 'react'
import { Toaster } from 'react-hot-toast'
import { FileText, Mic, Settings } from 'lucide-react'
import DocumentUpload from './components/Documents/DocumentUpload'
import DocumentList from './components/Documents/DocumentList.tsx'
import PromptEditor from './components/Agent/PromptEditor'
import VoiceRoom from './components/VoiceCall/VoiceRoom'
import TranscriptViewer from './components/VoiceCall/TranscriptViewer.tsx'
import SourcesPanel from './components/RAG/SourcesPanel'
import { useAppStore } from './stores/useAppStore'

type Tab = 'voice' | 'documents' | 'prompt'

function App() {
    const [activeTab, setActiveTab] = useState<Tab>('voice')
    const { fetchDocuments, fetchPrompt } = useAppStore()

    // Load initial data
    useEffect(() => {
        fetchDocuments()
        fetchPrompt()
    }, [fetchDocuments, fetchPrompt])

    return (
        <div className="min-h-screen bg-primary-bg">
            <Toaster
                position="top-right"
                toastOptions={{
                    className: 'glass-card',
                    style: {
                        background: '#1a1f2e',
                        color: '#f3f4f6',
                        border: '1px solid #2d3748',
                    },
                }}
            />

            {/* Header */}
            <header className="glass-card mx-4 mt-4">
                <div className="px-6 py-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-2xl font-bold text-white">Voice AI Agent</h1>
                            <p className="text-text-secondary text-sm">Real-time voice conversation with RAG</p>
                        </div>

                        {/* Tab Navigation */}
                        <div className="flex gap-2">
                            <button
                                onClick={() => setActiveTab('voice')}
                                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${activeTab === 'voice'
                                    ? 'bg-accent-blue text-white'
                                    : 'bg-primary-card text-text-secondary hover:text-white'
                                    }`}
                            >
                                <Mic size={18} />
                                Voice Call
                            </button>
                            <button
                                onClick={() => setActiveTab('documents')}
                                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${activeTab === 'documents'
                                    ? 'bg-accent-blue text-white'
                                    : 'bg-primary-card text-text-secondary hover:text-white'
                                    }`}
                            >
                                <FileText size={18} />
                                Documents
                            </button>
                            <button
                                onClick={() => setActiveTab('prompt')}
                                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${activeTab === 'prompt'
                                    ? 'bg-accent-blue text-white'
                                    : 'bg-primary-card text-text-secondary hover:text-white'
                                    }`}
                            >
                                <Settings size={18} />
                                Prompt
                            </button>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="mx-4 my-6">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Main Panel */}
                    <div className="lg:col-span-2">
                        {activeTab === 'voice' && <VoiceRoom />}
                        {activeTab === 'documents' && (
                            <div className="space-y-6">
                                <DocumentUpload />
                                <DocumentList />
                            </div>
                        )}
                        {activeTab === 'prompt' && <PromptEditor />}
                    </div>

                    {/* Sidebar */}
                    <div className="space-y-6">
                        {activeTab === 'voice' && (
                            <>
                                <TranscriptViewer />
                                <SourcesPanel />
                            </>
                        )}

                        {activeTab === 'documents' && (
                            <div className="glass-card p-6">
                                <h3 className="font-semibold mb-2">About Documents</h3>
                                <p className="text-text-secondary text-sm">
                                    Upload PDF or TXT files to create your knowledge base. The agent will use these
                                    documents to answer questions during voice calls.
                                </p>
                            </div>
                        )}

                        {activeTab === 'prompt' && (
                            <div className="glass-card p-6">
                                <h3 className="font-semibold mb-2">System Prompt</h3>
                                <p className="text-text-secondary text-sm">
                                    Customize how the AI agent behaves by editing the system prompt. Changes take
                                    effect on the next voice call.
                                </p>
                            </div>
                        )}
                    </div>
                </div>
            </main>
        </div>
    )
}

export default App
