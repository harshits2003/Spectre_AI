import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Send, 
  Mic, 
  MicOff, 
  Sparkles,
  Volume2,
  VolumeX,
  Loader2
} from 'lucide-react';
import { ChatSession, ChatMessage, AssistantStatus } from '../types';

interface ChatAreaProps {
  currentSession: ChatSession | null;
  assistantStatus: AssistantStatus;
  onSendMessage: (message: Omit<ChatMessage, 'id' | 'timestamp'>) => void;
  onStatusChange: (status: AssistantStatus) => void;
}

const ChatArea: React.FC<ChatAreaProps> = ({
  currentSession,
  assistantStatus,
  onSendMessage,
  onStatusChange
}) => {
  const [inputValue, setInputValue] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [currentSession?.messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      role: 'user' as const,
      content: inputValue.trim()
    };

    onSendMessage(userMessage);
    setInputValue('');

    // Update status to thinking
    onStatusChange({
      ...assistantStatus,
      status: 'Thinking...',
      isThinking: true
    });

    try {
      const response = await fetch('/api/chat/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage.content
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const assistantMessage = {
          role: 'assistant' as const,
          content: data.response
        };

        onSendMessage(assistantMessage);
        onStatusChange({
          ...assistantStatus,
          status: 'Available...',
          isThinking: false
        });
      } else {
        throw new Error('Failed to send message');
      }
    } catch (error) {
      const errorMessage = {
        role: 'assistant' as const,
        content: 'Sorry, I encountered an error. Please try again.'
      };
      onSendMessage(errorMessage);
      onStatusChange({
        ...assistantStatus,
        status: 'Available...',
        isThinking: false
      });
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleListening = () => {
    setIsListening(!isListening);
    onStatusChange({
      ...assistantStatus,
      isListening: !isListening,
      status: !isListening ? 'Listening...' : 'Available...'
    });
  };

  const toggleSpeaking = () => {
    setIsSpeaking(!isSpeaking);
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  if (!currentSession) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <Sparkles className="w-16 h-16 text-purple-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-white mb-2">Welcome to Spectre AI</h2>
          <p className="text-gray-400">Start a new conversation to begin</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-white/10 bg-slate-800/30">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-white font-medium">Spectre AI</h2>
              <div className="flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full ${
                  assistantStatus.isListening ? 'bg-green-500 animate-pulse' :
                  assistantStatus.isThinking ? 'bg-yellow-500 animate-pulse' :
                  assistantStatus.isAnswering ? 'bg-blue-500 animate-pulse' :
                  'bg-gray-500'
                }`} />
                <span className="text-sm text-gray-400">{assistantStatus.status}</span>
              </div>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={toggleSpeaking}
              className={`p-2 rounded-lg transition-colors ${
                isSpeaking ? 'bg-blue-500 text-white' : 'text-gray-400 hover:text-white hover:bg-white/10'
              }`}
            >
              {isSpeaking ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
            </button>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <AnimatePresence>
          {currentSession.messages.map((message, index) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-[70%] ${message.role === 'user' ? 'order-2' : 'order-1'}`}>
                <div className={`p-4 rounded-2xl ${
                  message.role === 'user'
                    ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                    : 'bg-slate-700/50 text-white border border-white/10'
                }`}>
                  <p className="whitespace-pre-wrap">{message.content}</p>
                </div>
                <p className={`text-xs text-gray-400 mt-1 ${
                  message.role === 'user' ? 'text-right' : 'text-left'
                }`}>
                  {formatTime(message.timestamp)}
                </p>
              </div>
              
              {message.role === 'assistant' && (
                <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mr-3 flex-shrink-0">
                  <Sparkles className="w-4 h-4 text-white" />
                </div>
              )}
            </motion.div>
          ))}
        </AnimatePresence>

        {assistantStatus.isThinking && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex justify-start"
          >
            <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mr-3 flex-shrink-0">
              <Sparkles className="w-4 h-4 text-white" />
            </div>
            <div className="bg-slate-700/50 border border-white/10 rounded-2xl p-4">
              <div className="flex items-center space-x-2">
                <Loader2 className="w-4 h-4 text-purple-400 animate-spin" />
                <span className="text-gray-300">Thinking...</span>
              </div>
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-white/10 bg-slate-800/30">
        <div className="flex items-end space-x-3">
          <div className="flex-1 relative">
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              className="w-full p-4 pr-12 bg-slate-700/50 border border-white/20 rounded-2xl text-white placeholder-gray-400 focus:outline-none focus:border-purple-500 transition-colors resize-none"
              disabled={assistantStatus.isThinking}
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || assistantStatus.isThinking}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 p-2 text-purple-400 hover:text-purple-300 disabled:text-gray-500 disabled:cursor-not-allowed transition-colors"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
          
          <motion.button
            onClick={toggleListening}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className={`p-4 rounded-2xl transition-all ${
              isListening
                ? 'bg-red-500 text-white shadow-lg shadow-red-500/25'
                : 'bg-slate-700/50 text-gray-400 hover:text-white hover:bg-slate-600/50 border border-white/20'
            }`}
          >
            {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
          </motion.button>
        </div>
      </div>
    </div>
  );
};

export default ChatArea;