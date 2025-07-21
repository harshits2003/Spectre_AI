# 🌌 Spectre AI Enhanced - Multi-User AI Assistant with Persistent Memory

This enhanced version of Spectre AI includes user authentication, multi-user support, and persistent memory capabilities.

## 🚀 New Features

### 1. User Authentication System
- **Sign Up/Sign In UI**: Beautiful Tkinter-based authentication interface
- **Secure Password Hashing**: Using bcrypt for password security
- **JWT Token Authentication**: Secure session management
- **User Profile Management**: Each user has their own profile and settings

### 2. Multi-User Support with FastAPI
- **RESTful API**: FastAPI backend for handling multiple users
- **User Isolation**: Each user's data is completely isolated
- **Concurrent Sessions**: Multiple users can use the system simultaneously
- **Session Management**: Persistent chat sessions per user

### 3. Persistent Memory System
- **Long-term Memory**: AI remembers user preferences, facts, and context
- **Memory Types**: 
  - **Preferences**: User likes, dislikes, favorites
  - **Facts**: Important personal information
  - **Context**: Recent conversation context
- **Intelligent Memory Extraction**: Automatically extracts and stores relevant information
- **Memory-Enhanced Responses**: AI uses stored memories to provide personalized responses

### 4. Dual Interface Options
- **Voice Interface**: Original GUI with speech recognition and voice commands
- **Chat Interface**: Modern text-based chat with persistent sessions
- **Interface Selection**: Beautiful main menu to choose preferred interface
- **Session Management**: Chat history, new chat creation, and session switching
## 🏗️ Architecture

### Database Schema
- **Users**: User accounts with authentication
- **ChatSessions**: Organized chat conversations
- **ChatMessages**: Individual messages in conversations
- **Memories**: Persistent memory storage with importance scoring

### API Endpoints
- `POST /register` - User registration
- `POST /token` - User authentication
- `GET /users/me` - Get current user info
- `POST /chat` - Send message with memory context
- `GET /chat/sessions` - Get user's chat sessions
- `POST /memories` - Create/update memories
- `GET /memories` - Retrieve user memories

## 🛠️ Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Update your `.env` file with the new variables:
```env
SECRET_KEY=your-very-long-secret-key-for-jwt-tokens
DATABASE_URL=sqlite:///./spectre_ai.db
```

### 3. Run the Enhanced Version
```bash
python main_enhanced.py
```

## 🎯 How It Works

### 1. Authentication Flow
1. User runs `main_enhanced.py`
2. API server starts automatically
3. Authentication UI appears
4. User signs up or signs in
5. JWT token is generated and stored
6. Main AI interface launches with user context

### 2. Memory System
1. **Automatic Extraction**: During conversations, the system automatically identifies and stores:
   - User preferences (likes, dislikes)
   - Personal facts (job, location, interests)
   - Recent conversation context

2. **Memory Integration**: When responding, the AI:
   - Retrieves relevant memories
   - Includes memory context in responses
   - Provides personalized, contextual answers

3. **Memory Types**:
   - **Preferences** (importance 2-3): "I love pizza", "I prefer tea over coffee"
   - **Facts** (importance 3-4): "I work as a developer", "I live in New York"
   - **Context** (importance 1): Recent conversation snippets

### 3. Multi-User Support
- Each user has isolated data
- Concurrent sessions supported
- User-specific memory and chat history
- Secure authentication and authorization

## 🔧 Configuration

### Database
- Default: SQLite (for development)
- Production: Can be configured to use PostgreSQL/MySQL
- Automatic table creation on first run

### Memory Settings
- **Memory Limit**: 50 memories per query (configurable)
- **Importance Scoring**: 1-10 scale for memory relevance
- **Auto-cleanup**: Old, low-importance memories can be cleaned up

### API Configuration
- **Host**: 0.0.0.0 (configurable)
- **Port**: 8000 (configurable)
- **CORS**: Enabled for development (configure for production)

## 🚀 Usage Examples

### 1. First Time User
```
User: Hi, I'm John and I love playing guitar
AI: Nice to meet you, John! I'll remember that you love playing guitar. How can I help you today?

[Later conversation]
User: What should I do this weekend?
AI: Since you love playing guitar, John, maybe you could practice some new songs or even jam with friends?
```

### 2. Returning User
```
User: Hello again
AI: Welcome back, John! How's your guitar playing going? Last time we talked about your interest in jazz music.
```

### 3. Memory Management
```
User: I actually prefer rock music over jazz now
AI: Got it, John! I've updated my memory - you prefer rock music. Any particular rock bands you're into?
```

## 🔒 Security Features

- **Password Hashing**: Bcrypt with salt
- **JWT Tokens**: Secure session management
- **User Isolation**: Complete data separation
- **Input Validation**: Pydantic schemas for API validation
- **SQL Injection Protection**: SQLAlchemy ORM

## 🎨 UI Improvements

### Authentication UI
- Modern dark theme
- Smooth transitions
- Form validation
- Error handling
- User-friendly messages

### Enhanced Main UI
- Personalized greetings
- User-specific chat history
- Memory indicators
- Session management

## 🔄 Migration from Original

The enhanced version is backward compatible:
1. Existing `.env` settings are preserved
2. Original chat logs can be imported
3. All original features remain functional
4. New features are additive, not replacing

## 🚀 Future Enhancements

1. **Advanced Memory**: 
   - Semantic search in memories
   - Memory importance auto-adjustment
   - Memory clustering and categorization

2. **Enhanced UI**:
   - Web-based interface
   - Mobile app support
   - Voice-only mode

3. **Advanced Features**:
   - Memory sharing between users (with permission)
   - Export/import memory profiles
   - Advanced analytics and insights

## 🤝 Contributing

The enhanced version maintains the same contribution guidelines as the original project. New contributions should consider:
- Multi-user compatibility
- Memory system integration
- API consistency
- Security best practices

---

**Note**: This enhanced version provides a solid foundation for a production-ready AI assistant with enterprise-level features while maintaining the simplicity and effectiveness of the original Spectre AI.