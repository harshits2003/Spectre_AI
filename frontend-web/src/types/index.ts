export interface User {
  username: string;
  email: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface ChatSession {
  id: string;
  title: string;
  messages: ChatMessage[];
  createdAt: Date;
  updatedAt: Date;
}

export interface AssistantStatus {
  status: string;
  isListening: boolean;
  isThinking: boolean;
  isAnswering: boolean;
}