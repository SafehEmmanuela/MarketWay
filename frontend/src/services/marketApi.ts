import apiClient from '../api/client';

export interface AskResponse {
    answer: string;
    source: 'local' | 'online' | 'combined';
    images: string[];
}

export interface ProductSearchResponse {
    query: string;
    results: any[];
}

export const marketApi = {
    async askMarket(question: string): Promise<AskResponse> {
        const { data } = await apiClient.post('/ask', { question });
        return data;
    },

    async searchProducts(query: string): Promise<ProductSearchResponse> {
        const { data } = await apiClient.get(`/product/search?q=${encodeURIComponent(query)}`);
        return data;
    },

    async voiceQuery(audioBlob: Blob): Promise<Blob> {
        const formData = new FormData();
        formData.append('file', audioBlob, 'audio.webm');

        const { data } = await apiClient.post('/voice/query', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
            responseType: 'blob',
        });
        return data;
    },
};
