from sqlalchemy import Column, Integer, String
from models import Base

class User(Base):
    """The user model.
    This is the model that represents a user in the database.
    """

    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement="auto")
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)