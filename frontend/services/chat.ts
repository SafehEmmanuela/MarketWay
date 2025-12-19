import { ChatResponse } from '../types/chat';

const API_URL = 'http://127.0.0.1:8000';

export const ChatService = {
    async sendMessage(message: string): Promise<ChatResponse> {
        try {
            const response = await fetch(`${API_URL}/chat?q=${encodeURIComponent(message)}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.statusText}`);
            }

            const data = await response.json();
            return data as ChatResponse;
        } catch (error) {
            console.error('ChatService Error:', error);
            throw error;
        }
    }
};