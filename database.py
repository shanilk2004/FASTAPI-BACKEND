from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

URL = "postgresql://postgres:shanil2004@localhost:5432/student_detail"

engine = create_engine(URL)

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass