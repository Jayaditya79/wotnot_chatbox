from ..database import database
from sqlalchemy import Integer,Column,String,ARRAY,TIMESTAMP,func,ForeignKey
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import JSON
from . import User
from sqlalchemy.dialects.postgresql import JSONB

class Contact(database.Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer,ForeignKey(User.User.id))
    name = Column(String, index=True)
    email = Column(String,  index=True)
    phone = Column(String,  index=True)
    tags = Column(MutableList.as_mutable(JSONB), default=[])
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())