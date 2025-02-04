from sqlalchemy import Column,Integer,String,Float
from database import Base

class Students(Base):

    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True )
    name = Column(String,nullable=False)
    department = Column(String,nullable=False)
    cgpa= Column(Float,nullable=False)
