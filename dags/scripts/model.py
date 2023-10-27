import config
import uuid

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import create_engine, Column, String


class Connection(object):
    def __init__(self,engine=None):
        if engine is not None:
            self.engine = engine
        else:
            self.engine = create_engine(config.DB_CONNECTION_STRING_WAREHOUSE)

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
    gender = Column(String)
    name = Column(String)
    first = Column(String)
    last = Column(String)
    date_of_birth = Column(String)

    def __init__(self, gender,name,first, last, date_of_birth):
        self.gender = gender
        self.name = name
        self.name = name
        self.last = last
        self.date_of_birth = date_of_birth
        # init database model
        # pass


class Locations(Base):
    __tablename__ = 'locations'

	# define required database columes
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    postcode = Column(String)
    country_code = Column(String) 

    def __init__(self, city, state, country, postcode, country_code):
        # init database model
        self.city = city
        self.state = state
        self.country = country
        self.postcode = postcode
        self.country_code = country_code

        # pass

class Additional(Base):
    __tablename__ = 'additional'

	# define required database columes
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String)
    email = Column(String)
    picture_large = Column(String) 

    def __init__(self, phone,email, picture_large):
        # init database model
        self.phone = phone
        self.email=email
        self.picture_large=picture_large
        # pass
