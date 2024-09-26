from sqlalchemy import Column, Integer, String, Text
from database import Base

class Museum(Base):
    __tablename__ = "museums"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    description = Column(Text)