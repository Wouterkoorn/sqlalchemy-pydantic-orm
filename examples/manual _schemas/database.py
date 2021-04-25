from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

engine = create_engine("sqlite://", echo=False)  # SQLLite memory database

DatabaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class ConnectionDatabase:
    def __init__(self):
        self.db: Session = DatabaseSession()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
