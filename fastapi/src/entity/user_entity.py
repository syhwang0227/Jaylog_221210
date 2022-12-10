
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from database.database import DBase


class UserEntity(DBase):
    __tablename__ = "User"
    
    idx = Column(Integer, primary_key=True, index=True)
    id = Column(String, unique=True, index=True)
    password = Column(String)
    simple_desc = Column(String)
    profile_image = Column(String)
    role = Column(String)
    create_date = Column(DateTime, default=datetime.now)
    update_date = Column(DateTime, onupdate=datetime.now)
    delete_date = Column(DateTime)
    
    # back_populates: 반대편 관계를 가져오도록 설정
    postEntitys = relationship("PostEntity", back_populates="userEntity")