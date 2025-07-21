from sqlalchemy.orm import Session
from database.models import Memory, User
from api.schemas import MemoryCreate
from typing import List, Dict, Any
import json

class MemoryService:
    def __init__(self, db: Session, user: User):
        self.db = db
        self.user = user
    
    def store_memory(self, memory_type: str, key: str, value: str, importance: int = 1):
        """Store a memory for the user"""
        # Check if memory already exists
        existing_memory = self.db.query(Memory).filter(
            Memory.user_id == self.user.id,
            Memory.key == key,
            Memory.memory_type == memory_type
        ).first()
        
        if existing_memory:
            # Update existing memory
            existing_memory.value = value
            existing_memory.importance = importance
            self.db.commit()
            return existing_memory
        else:
            # Create new memory
            memory = Memory(
                user_id=self.user.id,
                memory_type=memory_type,
                key=key,
                value=value,
                importance=importance
            )
            self.db.add(memory)
            self.db.commit()
            self.db.refresh(memory)
            return memory
    
    def get_memories(self, memory_type: str = None, limit: int = 50) -> List[Memory]:
        """Retrieve memories for the user"""
        query = self.db.query(Memory).filter(Memory.user_id == self.user.id)
        
        if memory_type:
            query = query.filter(Memory.memory_type == memory_type)
        
        return query.order_by(Memory.importance.desc(), Memory.updated_at.desc()).limit(limit).all()
    
    def get_memory(self, key: str, memory_type: str = None) -> Memory:
        """Get a specific memory"""
        query = self.db.query(Memory).filter(
            Memory.user_id == self.user.id,
            Memory.key == key
        )
        
        if memory_type:
            query = query.filter(Memory.memory_type == memory_type)
        
        return query.first()
    
    def delete_memory(self, key: str, memory_type: str = None):
        """Delete a memory"""
        query = self.db.query(Memory).filter(
            Memory.user_id == self.user.id,
            Memory.key == key
        )
        
        if memory_type:
            query = query.filter(Memory.memory_type == memory_type)
        
        memory = query.first()
        if memory:
            self.db.delete(memory)
            self.db.commit()
            return True
        return False
    
    def get_context_for_chat(self) -> str:
        """Get relevant context for chat based on stored memories"""
        memories = self.get_memories(limit=20)
        
        context_parts = []
        context_parts.append(f"User's name: {self.user.username}")
        
        # Group memories by type
        preferences = [m for m in memories if m.memory_type == 'preference']
        facts = [m for m in memories if m.memory_type == 'fact']
        contexts = [m for m in memories if m.memory_type == 'context']
        
        if preferences:
            context_parts.append("User preferences:")
            for pref in preferences[:5]:  # Top 5 preferences
                context_parts.append(f"- {pref.key}: {pref.value}")
        
        if facts:
            context_parts.append("Important facts about user:")
            for fact in facts[:5]:  # Top 5 facts
                context_parts.append(f"- {fact.key}: {fact.value}")
        
        if contexts:
            context_parts.append("Recent context:")
            for ctx in contexts[:3]:  # Top 3 contexts
                context_parts.append(f"- {ctx.value}")
        
        return "\n".join(context_parts)
    
    def extract_and_store_from_conversation(self, user_message: str, assistant_response: str):
        """Extract and store memories from conversation"""
        # Simple keyword-based extraction (can be enhanced with NLP)
        user_lower = user_message.lower()
        
        # Extract preferences
        if any(word in user_lower for word in ['like', 'prefer', 'favorite', 'love', 'enjoy']):
            if 'music' in user_lower:
                self.store_memory('preference', 'music_preference', user_message, 3)
            elif 'food' in user_lower:
                self.store_memory('preference', 'food_preference', user_message, 3)
            elif 'color' in user_lower:
                self.store_memory('preference', 'color_preference', user_message, 2)
        
        # Extract personal facts
        if any(word in user_lower for word in ['my name is', 'i am', 'i work', 'i live']):
            if 'work' in user_lower or 'job' in user_lower:
                self.store_memory('fact', 'occupation', user_message, 4)
            elif 'live' in user_lower or 'from' in user_lower:
                self.store_memory('fact', 'location', user_message, 3)
        
        # Store recent context
        self.store_memory('context', f'conversation_{len(self.get_memories("context"))}', 
                         f"User: {user_message[:100]}... Assistant: {assistant_response[:100]}...", 1)