from sqlalchemy import create_engine, Column, Integer, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///automgtic.db', echo=True)

Session = scoped_session(sessionmaker(bind=engine))
session = Session()


class AutomgticBase(object):
    query = Session.query_property()

Base = declarative_base(cls=AutomgticBase)


class Config(Base):
    __tablename__ = 'core__config'

    id = Column(Integer, primary_key=True)
    key = Column(Unicode, index=True, unique=True)
    value = Column(Unicode, index=True)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return '<{0} {1}: {2} = {3}>'.format(
                self.__class__.__name__,
                self.id,
                self.key.decode('ascii', 'replace'),
                self.value.decode('ascii', 'replace'))
