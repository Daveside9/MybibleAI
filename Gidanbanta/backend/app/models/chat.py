"""
Chat Message Model
Handles chat messages and reactions
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base

class MessageType(str, enum.Enum):
    TEXT = "text"
    REACTION = "reaction"  # Camera reaction
    EMOJI = "emoji"
    SYSTEM = "system"

class ModerationStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    FLAGGED = "flagged"
    REMOVED = "removed"

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Message content
    type = Column(Enum(MessageType), default=MessageType.TEXT, nullable=False)
    content = Column(String, nullable=False)
    media_url = Column(String, nullable=True)  # For camera reactions
    
    # Moderation
    moderation_status = Column(Enum(ModerationStatus), default=ModerationStatus.PENDING)
    is_visible = Column(Boolean, default=True)
    flagged_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    moderated_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="chat_messages")
    
    def __repr__(self):
        return f"<ChatMessage {self.type} by user_id={self.user_id}>"
