
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from ..database import database

Base = declarative_base()

class Conversation(database.Base):
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True, index=True)
    wa_id = Column(String, index=True)  # WhatsApp ID of the user
    message_id = Column(String)  # Unique message ID
    phone_number_id = Column(String)  # Phone number ID
    message_content = Column(Text)  # Message body
    timestamp = Column(DateTime, default=datetime.utcnow)  # Message timestamp
    context_message_id = Column(String, nullable=True,default= None)  # ID of the message that this is replying to
    message_type = Column(String)  # Type of message (e.g., text, image)
    is_first_message = Column(Boolean, default=False)  # Indicates if it's the first message in the conversation
    direction = Column(String, nullable=False)  # Track message direction


class First_Conversation(database.Base):
    __tablename__ = 'first_conversations'

    # first_chat_time = Column(DateTime)
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String)  # Unique message ID
    message_content = Column(Text)  # Message body
    business_account_id = Column(String, nullable=False)  # ID of the business account
    sender_wa_id = Column(String, nullable=False)  # WhatsApp ID of the sender
    receiver_wa_id = Column(String, nullable=False)  # WhatsApp ID of the recipient
    first_chat_time = Column(DateTime,default=datetime.utcnow)  # Timestamp for the first chat
    active = Column(Boolean, default=True)  # Status of the conversation

    def __init__(self, business_account_id, sender_wa_id, receiver_wa_id, first_chat_time=None, message_content= None ,message_id = None, active=True):
        self.business_account_id = business_account_id
        self.message_id = message_id
        self.message_content = message_content
        self.sender_wa_id = sender_wa_id
        self.receiver_wa_id = receiver_wa_id
        self.first_chat_time = first_chat_time or datetime.now()
        self.active = active
