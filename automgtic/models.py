from sqlalchemy import create_engine, Column, Integer, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///automgtic.db')

Session = scoped_session(sessionmaker(bind=engine))
session = Session()


class AutomgticBase(object):
    query = Session.query_property()

Base = declarative_base(cls=AutomgticBase)


class Media(Base):
    __tablename__ = 'core__media'

    id = Column(Integer, primary_key=True)
    digest = Column(Unicode(255), index=True, unique=True)
    name = Column(Unicode(1024))
    mediagoblin_data = Column(Unicode(8096))

    def __init__(self, digest, name, mediagoblin_data):
        self.digest = unicode(digest)
        self.name = unicode(name)
        self.mediagoblin_data = unicode(mediagoblin_data)

    def __repr__(self):
        return '<{0} #{1} {2} ({3})>'.format(
                self.__class__.__name__,
                self.id,
                self.digest,
                self.name)
