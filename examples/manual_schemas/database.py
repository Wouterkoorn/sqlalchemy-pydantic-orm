from typing import Any, Optional

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta, Session, sessionmaker

engine = create_engine("sqlite://", echo=False)  # SQLite memory database

DatabaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base()


class ConnectionDatabase:
    def __init__(self) -> None:
        self.db: Session = DatabaseSession()

    def __enter__(self) -> Session:
        return self.db

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        self.db.close()
