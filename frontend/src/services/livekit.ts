import api from './api'
import type { LiveKitTokenResponse, LiveKitTokenData } from '../types'

export const livekitService = {
    // Generate LiveKit token
    getToken: async (roomName: string, participantName: string): Promise<LiveKitTokenData> => {
        const response = await api.post<LiveKitTokenResponse>('/livekit/token', {
            room_name: roomName,
            participant_name: participantName,
        })
        return response.data.data
    },
}
