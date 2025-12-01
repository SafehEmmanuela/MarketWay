import { useState, useRef, useCallback } from 'react';

export function useVoiceRecording() {
    const [isRecording, setIsRecording] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const chunksRef = useRef<Blob[]>([]);

    const startRecording = useCallback(async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const mediaRecorder = new MediaRecorder(stream);
            mediaRecorderRef.current = mediaRecorder;
            chunksRef.current = [];

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    chunksRef.current.push(event.data);
                }
            };

            mediaRecorder.start();
            setIsRecording(true);
            setError(null);
        } catch (err) {
            setError('Microphone access denied or not available');
            console.error('Error accessing microphone:', err);
        }
    }, []);

    const stopRecording = useCallback((): Promise<Blob> => {
        return new Promise((resolve, reject) => {
            const mediaRecorder = mediaRecorderRef.current;

            if (!mediaRecorder || mediaRecorder.state === 'inactive') {
                reject(new Error('No active recording'));
                return;
            }

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });

                // Stop all tracks
                mediaRecorder.stream.getTracks().forEach(track => track.stop());

                setIsRecording(false);
                resolve(audioBlob);
            };

            mediaRecorder.stop();
        });
    }, []);

    return {
        isRecording,
        error,
        startRecording,
        stopRecording,
    };
}
