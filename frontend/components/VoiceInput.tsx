'use client';

import React, { useState, useEffect, useCallback } from 'react';

interface VoiceInputProps {
    onTranscript: (text: string) => void;
    isListening: boolean;
    setIsListening: (listening: boolean) => void;
}

export default function VoiceInput({ onTranscript, isListening, setIsListening }: VoiceInputProps) {
    const [recognition, setRecognition] = useState<any>(null);

    useEffect(() => {
        if (typeof window !== 'undefined' && ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)) {
            // @ts-ignore
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognitionInstance = new SpeechRecognition();
            recognitionInstance.continuous = false;
            recognitionInstance.interimResults = false;
            recognitionInstance.lang = 'en-US';

            recognitionInstance.onresult = (event: any) => {
                const transcript = event.results[0][0].transcript;
                onTranscript(transcript);
                setIsListening(false);
            };

            recognitionInstance.onerror = (event: any) => {
                console.error('Speech recognition error', event.error);
                setIsListening(false);
            };

            recognitionInstance.onend = () => {
                setIsListening(false);
            };

            setRecognition(recognitionInstance);
        }
    }, [onTranscript, setIsListening]);

    const toggleListening = useCallback(() => {
        if (!recognition) {
            alert("Speech recognition is not supported in this browser.");
            return;
        }

        if (isListening) {
            recognition.stop();
        } else {
            recognition.start();
            setIsListening(true);
        }
    }, [isListening, recognition, setIsListening]);

    return (
        <button
            onClick={toggleListening}
            className={`p-3 rounded-full transition-all duration-300 ${isListening
                ? 'bg-red-500 hover:bg-red-600 animate-pulse shadow-[0_0_15px_rgba(239,68,68,0.5)]'
                : 'bg-slate-700 hover:bg-slate-600'
                }`}
            title={isListening ? 'Stop Listening' : 'Start Voice Input'}
        >
            {isListening ? (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
                </svg>
            ) : (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                </svg>
            )}
        </button>
    );
}

export const speakText = (text: string) => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        // Optional: Select a specific voice if desired
        // const voices = window.speechSynthesis.getVoices();
        // utterance.voice = voices.find(voice => voice.name.includes('Google US English')) || null;
        window.speechSynthesis.speak(utterance);
    }
};
