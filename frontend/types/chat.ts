export interface Message {
    id: string;
    sender: 'user' | 'bot';
    text: string;
    image_url?: string;
}
export interface ChatResponse {
    query: string;
    direction: string;
    name: string;
}


