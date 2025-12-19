'use client';

import React, { useState, useRef, useEffect } from 'react';
import VoiceInput, { speakText } from '@/components/VoiceInput';
import { useChat } from '@/hooks/useChat';

export default function ChatPage() {
    const { messages, sendMessage, isLoading, clearMessages } = useChat();
    const [inputText, setInputText] = useState('');
    const [isListening, setIsListening] = useState(false);
    const [selectedImage, setSelectedImage] = useState<string | null>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        const lastMessage = messages[messages.length - 1];
        if (lastMessage && lastMessage.sender === 'bot') {
            // speakText(lastMessage.text); // Auto-play disabled as per request for manual control
        }
    }, [messages]);

    const handleSendMessage = async (text: string) => {
        if (!text.trim()) return;
        setInputText('');
        await sendMessage(text);
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage(inputText);
        }
    };

    return (
        <div className="flex h-screen bg-slate-950 text-white font-sans overflow-hidden">
            {/* Sidebar - Desktop */}
            <aside className="hidden md:flex flex-col w-64 border-r border-slate-800 bg-slate-900/50 p-4">
                <div className="flex items-center gap-2 mb-8">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-teal-400 to-purple-500"></div>
                    <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-teal-200 to-purple-400">Sabi Chat</h1>
                </div>

                <button
                    onClick={clearMessages}
                    className="flex items-center gap-2 px-4 py-3 bg-teal-600/20 text-teal-300 rounded-lg hover:bg-teal-600/30 transition-colors mb-6"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                    </svg>
                    New Chat
                </button>

                <div className="flex-1 overflow-y-auto">
                    <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">Recent</h3>
                    <div className="space-y-1">
                        <button className="w-full text-left px-3 py-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-md transition-colors text-sm truncate">
                            Where are shoes?
                        </button>
                        <button className="w-full text-left px-3 py-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-md transition-colors text-sm truncate">
                            Finding pharmacy
                        </button>
                    </div>
                </div>

                <div className="mt-auto border-t border-slate-800 pt-4">
                    <div className="flex items-center gap-3 px-2">
                        <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center text-xs">U</div>
                        <div className="text-sm">
                            <p className="font-medium">User</p>
                            <p className="text-xs text-slate-500">Free Plan</p>
                        </div>
                    </div>
                </div>
            </aside>

            {/* Main Chat Area */}
            <main className="flex-1 flex flex-col relative">

                {/* Image Modal */}
                {selectedImage && (
                    <div className="absolute inset-0 z-[60] flex items-center justify-center" onClick={() => setSelectedImage(null)}>
                        <button
                            onClick={() => setSelectedImage(null)}
                            className="absolute top-6 right-6 z-10 p-3 bg-white/90 hover:bg-white rounded-full transition-all shadow-lg"
                            aria-label="Close image"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-slate-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                        <img
                            src={selectedImage}
                            alt="Full view"
                            className="w-screen h-screen object-cover"
                            onClick={(e) => e.stopPropagation()}
                        />
                    </div>
                )}


                {/* Chat Content */}
                {messages.length === 0 ? (
                    <div className="flex-1 flex flex-col items-center justify-center text-center p-8 animate-fade-in-up">
                        <div className="w-24 h-24 mb-6 rounded-full bg-gradient-to-t from-teal-500/20 to-purple-500/20 flex items-center justify-center relative">
                            <div className="absolute w-16 h-16 bg-gradient-to-r from-teal-400 to-purple-500 rounded-full blur-xl opacity-50 animate-pulse"></div>
                            <div className="w-16 h-16 bg-gradient-to-r from-teal-400 to-purple-500 rounded-full shadow-lg relative z-10"></div>
                        </div>
                        <h2 className="text-3xl font-bold mb-2">Ready to find something?</h2>
                        <p className="text-slate-400 max-w-md">
                            Ask me about any product, store, or location in the market. I can guide you there directly.
                        </p>
                        <div className="mt-8 grid grid-cols-2 gap-4">
                            <button onClick={() => handleSendMessage("Where can I find shoes?")} className="px-4 py-3 bg-slate-900 hover:bg-slate-800 rounded-xl border border-slate-800 text-sm transition-all text-left">
                                👟 Where can I find shoes?
                            </button>
                            <button onClick={() => handleSendMessage("Show me pharmacies")} className="px-4 py-3 bg-slate-900 hover:bg-slate-800 rounded-xl border border-slate-800 text-sm transition-all text-left">
                                💊 Show me pharmacies
                            </button>
                        </div>
                    </div>
                ) : (
                    <div className="flex-1 overflow-y-auto p-4 space-y-6">
                        <div className="max-w-4xl mx-auto w-full space-y-6">
                            {messages.map((msg) => (
                                <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                                    <div className={`max-w-[80%] md:max-w-xl rounded-2xl overflow-hidden ${msg.sender === 'user'
                                        ? 'bg-teal-600 text-white rounded-tr-sm p-4'
                                        : 'bg-slate-800 text-slate-100 rounded-tl-sm border border-slate-700'
                                        }`}>

                                        {/* Display Image if any (Moved to top for bot messages) */}
                                        {msg.image_url && (
                                            <div className={`${msg.sender === 'user' ? 'mb-4' : ''}`}>
                                                <div
                                                    className={`relative h-48 w-full cursor-pointer hover:opacity-90 transition-opacity ${msg.sender === 'bot' ? 'rounded-t-2xl' : 'rounded-lg border border-white/20'}`}
                                                    onClick={() => setSelectedImage(msg.image_url || null)}
                                                >
                                                    <img
                                                        src={msg.image_url}
                                                        alt="Market item"
                                                        className="object-cover w-full h-full pointer-events-none"
                                                    />
                                                    {msg.sender === 'bot' && (
                                                        <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-transparent to-transparent opacity-60"></div>
                                                    )}
                                                </div>
                                            </div>
                                        )}

                                        <div className={`${msg.sender === 'bot' ? 'p-4' : ''}`}>
                                            <p className="whitespace-pre-wrap">{msg.text}</p>

                                            {/* Audio Play Button for Bot Messages */}
                                            {msg.sender === 'bot' && (
                                                <button
                                                    onClick={() => speakText(msg.text)}
                                                    className="mt-3 flex items-center gap-2 text-xs text-slate-400 hover:text-teal-400 transition-colors"
                                                    title="Read aloud"
                                                >
                                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
                                                    </svg>
                                                    Play Audio
                                                </button>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            ))}
                            {isLoading && (
                                <div className="flex justify-start">
                                    <div className="bg-slate-800 text-slate-100 rounded-tl-sm border border-slate-700 p-4 rounded-2xl">
                                        <div className="flex space-x-2">
                                            <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
                                            <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-100"></div>
                                            <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-200"></div>
                                        </div>
                                    </div>
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </div>
                    </div>
                )}

                {/* Input Area */}
                <div className="p-4 border-t border-slate-800 bg-slate-900/50 backdrop-blur-md">
                    <div className="max-w-4xl mx-auto relative flex items-center gap-3">
                        <div className="flex-1 relative">
                            <textarea
                                value={inputText}
                                onChange={(e) => setInputText(e.target.value)}
                                onKeyDown={handleKeyPress}
                                placeholder="Ask knowing..."
                                className="w-full bg-slate-800 border border-slate-700 text-white placeholder-slate-500 rounded-2xl pl-4 pr-12 py-3 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent resize-none h-[52px]"
                                rows={1}
                                disabled={isLoading}
                            />
                            <button
                                onClick={() => handleSendMessage(inputText)}
                                disabled={!inputText.trim() || isLoading}
                                className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-teal-500 hover:text-teal-400 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd" />
                                </svg>
                            </button>
                        </div>

                        <VoiceInput onTranscript={(text) => handleSendMessage(text)} isListening={isListening} setIsListening={setIsListening} />
                    </div>
                    {/* <p className="text-center text-xs text-slate-600 mt-2">
                        Ai can make mistakes, so double check it.
                    </p> */}
                </div>
            </main>
        </div>
    );
}
