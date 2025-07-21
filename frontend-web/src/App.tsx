import React, { useState, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import AuthPage from './components/AuthPage';
import MainInterface from './components/MainInterface';
import { User } from './types';

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    const savedUser = localStorage.getItem('spectreUser');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
    setIsLoading(false);
  }, []);

  const handleLogin = (userData: User) => {
    setUser(userData);
    localStorage.setItem('spectreUser', JSON.stringify(userData));
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('spectreUser');
    localStorage.removeItem('chatHistory');
  };


  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <AnimatePresence mode="wait">
        {!user ? (
          <AuthPage key="auth" onLogin={handleLogin} />
        ) : (
          <MainInterface key="main" user={user} onLogout={handleLogout} />
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;