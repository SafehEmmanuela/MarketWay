import React, { useState } from 'react';
import { Send, Mic, Square } from 'lucide-react';
import { useVoiceRecording } from '../hooks/useVoiceRecording';
import { marketApi } from '../services/marketApi';

interface InputBarProps {
    onSend: (message: string) => void;
    loading: boolean;
}

export function InputBar({ onSend, loading }: InputBarProps) {
    const [input, setInput] = useState('');
    const { isRecording, error: voiceError, startRecording, stopRecording } = useVoiceRecording();
    const [processingVoice, setProcessingVoice] = useState(false);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (input.trim() && !loading) {
            onSend(input);
            setInput('');
        }
    };

    const handleVoiceClick = async () => {
        if (isRecording) {
            // Stop recording and process
            try {
                setProcessingVoice(true);
                const audioBlob = await stopRecording();

                // Send to backend for speech-to-text
                const responseBlob = await marketApi.voiceQuery(audioBlob);

                // Play the audio response
                const audioUrl = URL.createObjectURL(responseBlob);
                const audio = new Audio(audioUrl);
                audio.play();

                setProcessingVoice(false);
            } catch (err) {
                console.error('Voice processing error:', err);
                setProcessingVoice(false);
            }
        } else {
            // Start recording
            startRecording();
        }
    };

    return (
        <form onSubmit={handleSubmit} className="relative w-full">
            <div className="relative flex items-center">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder={isRecording ? "Recording..." : "Ask about products, lines, or directions..."}
                    disabled={loading || isRecording || processingVoice}
                    className="w-full pl-6 pr-24 py-4 bg-white/80 backdrop-blur-md border border-gray-200 rounded-full shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent transition-all disabled:opacity-50 text-gray-700 placeholder-gray-400"
                />
                <div className="absolute right-2 flex gap-1">
                    <button
                        type="button"
                        onClick={handleVoiceClick}
                        disabled={loading || processingVoice}
                        className={`p-2 rounded-full transition-colors ${isRecording
                                ? 'bg-red-500 text-white hover:bg-red-600 animate-pulse'
                                : 'text-gray-400 hover:text-blue-600 hover:bg-blue-50'
                            } disabled:opacity-50`}
                        title={isRecording ? "Stop recording" : "Voice input"}
                    >
                        {isRecording ? <Square size={20} /> : <Mic size={20} />}
                    </button>
                    <button
                        type="submit"
                        disabled={!input.trim() || loading || isRecording}
                        className="p-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed shadow-md"
                    >
                        <Send size={20} />
                    </button>
                </div>
            </div>
            {voiceError && (
                <p className="text-red-500 text-xs mt-1 ml-4">{voiceError}</p>
            )}
            {processingVoice && (
                <p className="text-blue-500 text-xs mt-1 ml-4">Processing voice...</p>
            )}
        </form>
    );
}
