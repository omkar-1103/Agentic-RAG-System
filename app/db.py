import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

# We use the existing DATABASE_URL from .env.
# If it's missing, we default to a local SQLite file to ensure it works smoothly.
db_uri = os.getenv("DATABASE_URL")
if not db_uri or "free-tier.gcp-us-central1.cockroachlabs.cloud" in db_uri:
    db_uri = "sqlite:///./chat_history.db"

# Setting up SQLAlchemy Engine and Session
# Connect_args is only needed for sqlite to prevent thread issues
connect_args = {"check_same_thread": False} if db_uri.startswith("sqlite") else {}
engine = create_engine(db_uri, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Defining the Chat History Database Table
class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True) # To group chats if multiple users use it
    user_query = Column(Text, nullable=False)
    agent_workflow_data = Column(JSON, nullable=True) # Store the JSON state of all the agent steps
    final_answer = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

def init_db():
    """Creates the tables in the database if they don't exist yet."""
    Base.metadata.create_all(bind=engine)

def save_chat(session_id: str, user_query: str, workflow_data: dict, final_answer: str):
    """Saves a new chat message and the entire agent thought process to the database."""
    db = SessionLocal()
    try:
        new_chat = ChatHistory(
            session_id=session_id,
            user_query=user_query,
            agent_workflow_data=workflow_data,
            final_answer=final_answer
        )
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)
        return new_chat
    finally:
        db.close()

def get_chat_history(session_id: str = None):
    """Retrieves all chat messages, optionally filtered by a specific session."""
    db = SessionLocal()
    try:
        if session_id:
            return db.query(ChatHistory).filter(ChatHistory.session_id == session_id).order_by(ChatHistory.timestamp.asc()).all()
        return db.query(ChatHistory).order_by(ChatHistory.timestamp.asc()).all()
    finally:
        db.close()
