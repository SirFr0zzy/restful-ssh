from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    host = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False)
    user = Column(Text, nullable=False)
    password = Column(Text)
    private_key = Column(Text)
    owner_ip = Column(Text)
    agent_session_uuid = Column(String(36))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))