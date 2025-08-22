from sqlalchemy import Integer , String , Column , Boolean , DateTime , func , ForeignKey , ARRAY
from .database import Base
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer , primary_key=True, index=True , nullable=False)
    title = Column(String , index=True, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean,server_default="True", nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    voters_id = Column(ARRAY(Integer),server_default="{}",nullable=False)
    voters = Column(Integer,server_default="0",nullable=False)
    
    owner = relationship("User")
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer , primary_key=True, index=True , nullable=False)
    email = Column(String, nullable=False,unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)