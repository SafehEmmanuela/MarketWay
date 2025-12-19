import { useState, useCallback } from 'react';
import { Message } from '../types/chat';
import { ChatService } from '../services/chat';

export const useChat = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const sendMessage = useCallback(async (text: string) => {
        if (!text.trim()) return;

        setIsLoading(true);
        setError(null);

        const userMessage: Message = {
            id: Date.now().toString(),
            sender: 'user',
            text: text,
        };

        setMessages((prev) => [...prev, userMessage]);

        try {
            const response = await ChatService.sendMessage(text);

            const botMessage: Message = {
                id: (Date.now() + 1).toString(),
                sender: 'bot',
                text: response.direction,
                image_url: response.name ? `http://127.0.0.1:8000/images/${response.name}.jpg` : undefined
            };

            setMessages((prev) => [...prev, botMessage]);
        } catch (err) {
            setError('Failed to send message. Please try again.');
            const errorMessage: Message = {
                id: (Date.now() + 1).toString(),
                sender: 'bot',
                text: "I'm having trouble connecting to the server. Please try again later.",
            };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    }, []);

    const clearMessages = useCallback(() => {
        setMessages([]);
    }, []);

    return {
        messages,
        isLoading,
        error,
        sendMessage,
        clearMessages
    };
};
