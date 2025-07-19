import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Sidebar from './Sidebar';
import ChatArea from './ChatArea';
import { User, ChatSession, ChatMessage, AssistantStatus } from '../types';

interface MainInterfaceProps {
  user: User;
  onLogout: () => void;
}

const MainInterface: React.FC<MainInterfaceProps> = ({ user, onLogout }) => {
  const [chatSessions, setChatSessions] = useState<ChatSession[]>([]);
  const [currentSession, setCurrentSession] = useState<ChatSession | null>(null);
  const [assistantStatus, setAssistantStatus] = useState<AssistantStatus>({
    status: 'Available...',
    isListening: false,
    isThinking: false,
    isAnswering: false
  });

  useEffect(() => {
    // Load chat history from localStorage
    const savedHistory = localStorage.getItem('chatHistory');
    if (savedHistory) {
      const sessions = JSON.parse(savedHistory);
      setChatSessions(sessions);
      if (sessions.length > 0) {
        setCurrentSession(sessions[0]);
      }
    } else {
      // Create initial session
      createNewSession();
    }
  }, []);

  const createNewSession = () => {
    const newSession: ChatSession = {
      id: Date.now().toString(),
      title: 'New Chat',
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date()
    };
    
    setChatSessions(prev => [newSession, ...prev]);
    setCurrentSession(newSession);
    
    // Save to localStorage
    const updatedSessions = [newSession, ...chatSessions];
    localStorage.setItem('chatHistory', JSON.stringify(updatedSessions));
  };

  const updateSession = (sessionId: string, updates: Partial<ChatSession>) => {
    setChatSessions(prev => {
      const updated = prev.map(session => 
        session.id === sessionId 
          ? { ...session, ...updates, updatedAt: new Date() }
          : session
      );
      localStorage.setItem('chatHistory', JSON.stringify(updated));
      return updated;
    });

    if (currentSession?.id === sessionId) {
      setCurrentSession(prev => prev ? { ...prev, ...updates, updatedAt: new Date() } : null);
    }
  };

  const addMessage = (message: Omit<ChatMessage, 'id' | 'timestamp'>) => {
    if (!currentSession) return;

    const newMessage: ChatMessage = {
      ...message,
      id: Date.now().toString(),
      timestamp: new Date()
    };

    const updatedMessages = [...currentSession.messages, newMessage];
    
    // Update session title if it's the first user message
    let title = currentSession.title;
    if (message.role === 'user' && currentSession.messages.length === 0) {
      title = message.content.slice(0, 30) + (message.content.length > 30 ? '...' : '');
    }

    updateSession(currentSession.id, {
      messages: updatedMessages,
      title
    });
  };

  const clearHistory = () => {
    setChatSessions([]);
    setCurrentSession(null);
    localStorage.removeItem('chatHistory');
    createNewSession();
  };

  const deleteSession = (sessionId: string) => {
    setChatSessions(prev => {
      const updated = prev.filter(session => session.id !== sessionId);
      localStorage.setItem('chatHistory', JSON.stringify(updated));
      return updated;
    });

    if (currentSession?.id === sessionId) {
      const remainingSessions = chatSessions.filter(s => s.id !== sessionId);
      setCurrentSession(remainingSessions.length > 0 ? remainingSessions[0] : null);
      
      if (remainingSessions.length === 0) {
        createNewSession();
      }
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.5 }}
      className="flex h-screen"
    >
      <Sidebar
        user={user}
        chatSessions={chatSessions}
        currentSession={currentSession}
        onSessionSelect={setCurrentSession}
        onNewChat={createNewSession}
        onClearHistory={clearHistory}
        onDeleteSession={deleteSession}
        onLogout={onLogout}
      />
      
      <ChatArea
        currentSession={currentSession}
        assistantStatus={assistantStatus}
        onSendMessage={addMessage}
        onStatusChange={setAssistantStatus}
      />
    </motion.div>
  );
};

export default MainInterface;