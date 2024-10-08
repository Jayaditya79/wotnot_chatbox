from ..database import database
from sqlalchemy import Integer,Column,String,ARRAY,JSON
from . import User

from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, func



class Integration(database.Base):
    __tablename__="Integration"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey(User.User.id))
    api_key=Column(String)
    app=Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    type=Column(String)


class WooIntegration(database.Base):
    __tablename__="Woo_Integration"
    id=Column(Integer,primary_key=True)
    integration_id=Column(Integer,ForeignKey(Integration.id))
    user_id=Column(Integer,ForeignKey(User.User.id))
    api_key=Column(String)
    type=Column(String)
    template=Column(String)
    parameters=Column(JSON)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
