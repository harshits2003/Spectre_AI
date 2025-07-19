# Enhanced Spectre AI Web GUI

This is a modern, web-based GUI for the Spectre AI assistant that replaces the PyQt5 interface with a sleek React application.

## Features

### 🔐 Authentication System
- **Sign Up/Sign In**: Users can create accounts or sign in with existing credentials
- **User Management**: Username is automatically updated in the `.env` file upon login
- **Persistent Sessions**: User sessions are maintained across browser refreshes

### 🎨 Modern UI Design
- **Glass Morphism**: Beautiful translucent design with backdrop blur effects
- **Gradient Themes**: Purple and pink gradient color scheme throughout
- **Smooth Animations**: Framer Motion animations for enhanced user experience
- **Responsive Design**: Works perfectly on desktop and mobile devices

### 💬 Enhanced Chat Interface
- **Real-time Messaging**: Instant message delivery and responses
- **Message History**: All conversations are saved and can be accessed later
- **Typing Indicators**: Visual feedback when the AI is thinking or responding
- **Voice Controls**: Microphone toggle for voice input
- **Audio Controls**: Speaker toggle for voice output

### 📚 Chat History Management
- **Sidebar History**: All chat sessions displayed in an organized sidebar
- **Session Grouping**: Chats grouped by date (Today, Yesterday, etc.)
- **Session Management**: Create new chats, delete individual sessions
- **Clear All History**: Option to clear entire chat history with confirmation
- **Search & Navigation**: Easy navigation between different chat sessions

### 🎯 Status Indicators
- **Real-time Status**: Visual indicators showing AI status (Available, Listening, Thinking, Answering)
- **Animated Indicators**: Pulsing dots to show current AI state
- **Voice Status**: Clear indication when microphone is active/inactive

## Installation & Setup

### Frontend (React)
```bash
cd frontend-web
npm install
npm run dev
```

### Backend Integration (Flask API)
```bash
cd backend-integration
pip install -r requirements.txt
python api.py
```

## File Structure

```
frontend-web/
├── src/
│   ├── components/
│   │   ├── AuthPage.tsx          # Login/Signup interface
│   │   ├── MainInterface.tsx     # Main chat application
│   │   ├── Sidebar.tsx           # Chat history sidebar
│   │   └── ChatArea.tsx          # Chat messages and input
│   ├── types/
│   │   └── index.ts              # TypeScript type definitions
│   ├── App.tsx                   # Main application component
│   └── index.css                 # Global styles and animations
├── tailwind.config.js            # Tailwind CSS configuration
└── package.json                  # Dependencies and scripts

backend-integration/
├── api.py                        # Flask API for frontend-backend communication
└── requirements.txt              # Python dependencies
```

## Key Components

### AuthPage
- Handles user authentication (sign up/sign in)
- Form validation and error handling
- Password visibility toggle
- Smooth transitions between sign up and sign in modes

### MainInterface
- Main application layout
- Manages chat sessions and user state
- Handles logout functionality
- Coordinates between sidebar and chat area

### Sidebar
- Displays chat history organized by date
- User profile section with logout option
- New chat creation
- Individual session management (delete)
- Clear all history with confirmation dialog

### ChatArea
- Real-time chat interface
- Message display with timestamps
- Voice input/output controls
- Status indicators
- Typing animations and loading states

## Integration with Existing Backend

The web GUI integrates with your existing Python backend through a Flask API that:

1. **Processes Messages**: Routes user messages through your existing AI pipeline
2. **Manages Chat History**: Reads/writes to your existing `ChatLog.json` file
3. **Status Updates**: Monitors your existing status files
4. **User Settings**: Updates the `.env` file with user information

## Customization

### Styling
- Modify `tailwind.config.js` for color schemes and themes
- Update `index.css` for custom animations and effects
- Adjust component styles in individual `.tsx` files

### Functionality
- Add new features by creating additional components
- Extend the API in `backend-integration/api.py`
- Modify types in `src/types/index.ts` for new data structures

## Benefits Over PyQt5 GUI

1. **Modern Design**: Contemporary web-based interface
2. **Cross-Platform**: Works on any device with a web browser
3. **Easier Maintenance**: Web technologies are more widely known
4. **Better UX**: Smooth animations and responsive design
5. **Extensibility**: Easy to add new features and integrations
6. **Accessibility**: Better support for accessibility features

## Running the Application

1. Start the backend API:
   ```bash
   cd backend-integration
   python api.py
   ```

2. Start the frontend development server:
   ```bash
   cd frontend-web
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:3000`

The web GUI provides a modern, intuitive interface for your Spectre AI assistant while maintaining full compatibility with your existing Python backend infrastructure.