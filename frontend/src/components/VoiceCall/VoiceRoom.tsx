import React, { useState, useEffect } from 'react'
import { Phone, PhoneOff, Mic, MicOff, Volume2, Loader2 } from 'lucide-react'
import {
    LiveKitRoom,
    useVoiceAssistant,
    RoomAudioRenderer,
    useRoomContext
} from '@livekit/components-react'
import type { ParticipantInfo } from 'livekit-client'
import { useVoiceStore } from '../../stores/useVoiceStore'
import { livekitService } from '../../services/livekit'
import toast from 'react-hot-toast'

const LIVEKIT_URL = import.meta.env.VITE_LIVEKIT_URL || 'ws://localhost:7880'

const VoiceRoom: React.FC = () => {
    const [token, setToken] = useState<string>('')
    const [isConnecting, setIsConnecting] = useState(false)
    const { isConnected, setConnected, isMuted, setMuted, reset, roomName, setRoomName } = useVoiceStore()

    const handleConnect = async () => {
        try {
            setIsConnecting(true)
            const newRoomName = `voice-ai-room-${Date.now()}`
            setRoomName(newRoomName)
            const response = await livekitService.getToken(
                newRoomName,
                `user-${Date.now()}`
            )
            setToken(response.token)
            setConnected(true)
            toast.success('Connected to voice room')
        } catch (error: any) {
            console.error('Failed to get LiveKit token:', error)
            toast.error('Failed to connect to voice room')
        } finally {
            setIsConnecting(false)
        }
    }

    const handleDisconnect = () => {
        setToken('')
        setConnected(false)
        reset()
        toast.success('Disconnected from voice room')
    }

    return (
        <div className="glass-card p-6">
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h2 className="text-xl font-semibold">Voice Call</h2>
                    <p className="text-text-secondary text-sm mt-1">
                        {isConnected ? 'Connected - Start talking!' : 'Click to start voice conversation'}
                    </p>
                    {roomName && (
                        <p className="text-text-secondary text-xs mt-1">
                            Room: {roomName}
                        </p>
                    )}
                </div>

                <div className="flex items-center gap-2">
                    {isConnected ? (
                        <>
                            <button
                                onClick={() => setMuted(!isMuted)}
                                className={`p-3 rounded-lg transition-colors ${isMuted
                                    ? 'bg-accent-red text-white'
                                    : 'bg-primary-card hover:bg-primary-card/80 text-text-primary'
                                    }`}
                                title={isMuted ? 'Unmute' : 'Mute'}
                            >
                                {isMuted ? <MicOff size={20} /> : <Mic size={20} />}
                            </button>
                            <button
                                onClick={handleDisconnect}
                                className="bg-accent-red hover:bg-accent-red/80 text-white px-6 py-3 rounded-lg font-medium flex items-center gap-2"
                            >
                                <PhoneOff size={20} />
                                End Call
                            </button>
                        </>
                    ) : (
                        <button
                            onClick={handleConnect}
                            disabled={isConnecting}
                            className="bg-accent-blue hover:bg-accent-blue/80 text-white px-6 py-3 rounded-lg font-medium flex items-center gap-2 disabled:opacity-50"
                        >
                            {isConnecting ? (
                                <>
                                    <Loader2 size={20} className="animate-spin" />
                                    Connecting...
                                </>
                            ) : (
                                <>
                                    <Phone size={20} />
                                    Start Call
                                </>
                            )}
                        </button>
                    )}
                </div>
            </div>

            {/* LiveKit Room */}
            {isConnected && token && (
                <div className="bg-primary-card border border-primary-border rounded-lg p-8">
                    <LiveKitRoom
                        token={token}
                        serverUrl={LIVEKIT_URL}
                        connect={isConnected}
                        audio={true}
                        video={false}
                        onDisconnected={handleDisconnect}
                        className="livekit-room-dark"
                    >
                        <VoiceAssistantUI />
                        <RoomAudioRenderer />
                    </LiveKitRoom>
                </div>
            )}

            {!isConnected && (
                <div className="bg-primary-card border border-primary-border rounded-lg p-12 text-center">
                    <Volume2 className="mx-auto mb-4 text-text-secondary animate-pulse-slow" size={64} />
                    <p className="text-lg font-medium mb-2">Ready to start conversation</p>
                    <p className="text-text-secondary text-sm">
                        Click "Start Call" to begin talking with the AI agent
                    </p>
                </div>
            )}
        </div>
    )
}

// Voice Assistant UI Component (inside LiveKit Room)
const VoiceAssistantUI: React.FC = () => {
    const { state } = useVoiceAssistant()
    const { setAgentSpeaking, addTranscript, setSources } = useVoiceStore()
    const room = useRoomContext()

    useEffect(() => {
        setAgentSpeaking(state === 'speaking')
    }, [state, setAgentSpeaking])

    // Listen for data messages (RAG sources)
    useEffect(() => {
        if (!room) return

        const handleDataReceived = (payload: Uint8Array) => {
            try {
                const decoder = new TextDecoder()
                const data = JSON.parse(decoder.decode(payload))

                if (data.type === 'rag_sources' && data.sources) {
                    setSources(data.sources)
                }
            } catch (error) {
                console.error('Error parsing data:', error)
            }
        }

        room.on('dataReceived', handleDataReceived)

        return () => {
            room.off('dataReceived', handleDataReceived)
        }
    }, [room, setSources])

    // Listen for LiveKit transcription stream
    useEffect(() => {
        if (!room) return

        const handler = async (reader: any, participantInfo: ParticipantInfo) => {
            try {
                const message = await reader.readAll()
                const attrs = reader.info?.attributes || {}
                const isFinal = attrs['lk.transcription_final'] === 'true'

                if (!isFinal || !message) return

                const identity = participantInfo?.identity || ''
                const isAgent =
                    identity.startsWith('agent') ||
                    identity.startsWith('assistant') ||
                    identity.startsWith('livekit') ||
                    identity.includes('agent')

                addTranscript({
                    speaker: isAgent ? 'agent' : 'user',
                    text: message,
                })
            } catch (error) {
                console.error('Error handling transcription:', error)
            }
        }

        room.registerTextStreamHandler('lk.transcription', handler)

        return () => {
            room.unregisterTextStreamHandler?.('lk.transcription', handler)
        }
    }, [room, addTranscript])

    const getStatusText = () => {
        switch (state) {
            case 'listening':
                return 'Listening...'
            case 'thinking':
                return 'Processing...'
            case 'speaking':
                return 'Speaking...'
            default:
                return 'Connected'
        }
    }

    const getStatusColor = () => {
        switch (state) {
            case 'listening':
                return 'text-accent-blue'
            case 'thinking':
                return 'text-accent-purple'
            case 'speaking':
                return 'text-accent-green'
            default:
                return 'text-text-secondary'
        }
    }

    return (
        <div className="text-center py-8">
            <div className="inline-flex items-center gap-3">
                <div
                    className={`h-3 w-3 rounded-full ${state === 'listening' || state === 'speaking' ? 'animate-pulse' : ''
                        } ${state === 'listening'
                            ? 'bg-accent-blue'
                            : state === 'thinking'
                                ? 'bg-accent-purple'
                                : state === 'speaking'
                                    ? 'bg-accent-green'
                                    : 'bg-text-secondary'
                        }`}
                />
                <p className={`text-lg font-medium ${getStatusColor()}`}>{getStatusText()}</p>
            </div>
        </div>
    )
}

export default VoiceRoom
