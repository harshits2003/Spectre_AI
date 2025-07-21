from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
import asyncio

from database.database import get_db, create_tables
from database.models import User, ChatSession, ChatMessage
from api.schemas import *
from api.auth import *
from api.memory_service import MemoryService

# Import your existing backend modules
from Backend.model import FirstLayerDMM
from Backend.Chatbot import ChatBot
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation

app = FastAPI(title="Spectre AI API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

@app.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = get_user(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.post("/chat", response_model=ChatMessageResponse)
async def chat(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Initialize memory service
    memory_service = MemoryService(db, current_user)
    
    # Get or create chat session
    if chat_request.session_id:
        session = db.query(ChatSession).filter(
            ChatSession.id == chat_request.session_id,
            ChatSession.user_id == current_user.id
        ).first()
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
    else:
        # Create new session
        session = ChatSession(
            user_id=current_user.id,
            title=chat_request.message[:50] + "..." if len(chat_request.message) > 50 else chat_request.message
        )
        db.add(session)
        db.commit()
        db.refresh(session)
    
    # Store user message
    user_message = ChatMessage(
        session_id=session.id,
        role="user",
        content=chat_request.message
    )
    db.add(user_message)
    db.commit()
    
    # Get memory context
    memory_context = memory_service.get_context_for_chat()
    
    # Process message through your existing AI pipeline
    try:
        # Add memory context to the message
        enhanced_message = f"Context about {current_user.username}:\n{memory_context}\n\nUser message: {chat_request.message}"
        
        decision = FirstLayerDMM(enhanced_message)
        
        # Determine response type
        if any(d.startswith('general') for d in decision):
            response = ChatBot(enhanced_message)
        elif any(d.startswith('realtime') for d in decision):
            response = RealtimeSearchEngine(chat_request.message)
        else:
            # Handle automation tasks
            await Automation(decision)
            response = "Task executed successfully."
        
        # Store assistant response
        assistant_message = ChatMessage(
            session_id=session.id,
            role="assistant",
            content=response
        )
        db.add(assistant_message)
        db.commit()
        db.refresh(assistant_message)
        
        # Extract and store memories from conversation
        memory_service.extract_and_store_from_conversation(chat_request.message, response)
        
        return assistant_message
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.get("/chat/sessions", response_model=List[ChatSessionResponse])
async def get_chat_sessions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id
    ).order_by(ChatSession.updated_at.desc()).all()
    return sessions

@app.get("/chat/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(
    session_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return session

@app.delete("/chat/sessions/{session_id}")
async def delete_chat_session(
    session_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    db.delete(session)
    db.commit()
    return {"message": "Chat session deleted successfully"}

@app.post("/memories", response_model=MemoryResponse)
async def create_memory(
    memory: MemoryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    memory_service = MemoryService(db, current_user)
    stored_memory = memory_service.store_memory(
        memory.memory_type,
        memory.key,
        memory.value,
        memory.importance
    )
    return stored_memory

@app.get("/memories", response_model=List[MemoryResponse])
async def get_memories(
    memory_type: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    memory_service = MemoryService(db, current_user)
    memories = memory_service.get_memories(memory_type)
    return memories

@app.delete("/memories/{memory_id}")
async def delete_memory(
    memory_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    memory = db.query(Memory).filter(
        Memory.id == memory_id,
        Memory.user_id == current_user.id
    ).first()
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    
    db.delete(memory)
    db.commit()
    return {"message": "Memory deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)