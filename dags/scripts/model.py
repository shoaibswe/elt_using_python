import config
import uuid

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import create_engine, Column


class Connection(object):
    def __init__(self):
        engine = create_engine(config.DB_CONNECTION_STRING_WAREHOUSE)
        self.engine = engine

    def get_session(self):
        Session = sessionmaker(bind=self.engine)

        return Session()

    def get_engine(self):
        return self.engine


Base = declarative_base()


def init_db():
    engine = create_engine(config.DB_CONNECTION_STRING_WAREHOUSE)
    Base.metadata.create_all(bind=engine)

class Users(Base):
    __tablename__ = 'users'

	# define required database columes
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    def __init__(self, name, gender):
        # init database model
        pass


class Locations(Base):
    __tablename__ = 'locations'

	# define required database columes

    def __init__(self, state):
        # init database model
        pass

class Additional(Base):
    __tablename__ = 'additional'

	# define required database columes

    def __init__(self, phone):
        # init database model
        pass
