"""Record positive memories."""
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

BASE = declarative_base()
SESSION = sessionmaker()


class Memory(BASE):

    """A positive memory."""

    __tablename__ = 'memories'
    mid = Column(Integer, primary_key=True)
    date = Column(Date)
    text = Column(String)


class SessionScope(object):

    """Content manager that creates sessions."""

    def __init__(self):
        """Create session."""
        self._session = SESSION()

    def __enter__(self):
        """Return session."""
        return self._session

    def __exit__(self, e_type, e_value, trace):
        """Commit or roll back, then do cleanup."""
        if e_type is not None:
            self._session.rollback()
        else:
            self._session.commit()
        self._session.close()

ENGINE = create_engine('sqlite:///positivityjar.sql', echo=False)
SESSION.configure(bind=ENGINE)
BASE.metadata.create_all(ENGINE)

TEXT = raw_input("Memory: ")
with SessionScope() as session:
    memory = Memory(date=datetime.date.today(), text=TEXT)
    print "Added memory to positivity jar."
