import sys
sys.path.insert(0,'/opt/airflow/dags/scripts/')
from config import DB_CONNECTION_STRING_WAREHOUSE
import uuid
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Date, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base,relationship
from sqlalchemy.sql import func


class Connection(object):
    def __init__(self,engine=None):
        if engine is not None:
            self.engine = engine
        else:
            self.engine = create_engine(DB_CONNECTION_STRING_WAREHOUSE)

    def get_session(self):
        Session = sessionmaker(bind=self.engine)

        return Session()

    def get_engine(self):
        return self.engine


Base = declarative_base()


def init_db():
    engine = create_engine(DB_CONNECTION_STRING_WAREHOUSE)
    Base.metadata.create_all(bind=engine)

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'raw'} 

	# define required database columes
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    gender = Column(String)
    name = Column(String)
    first = Column(String)
    last = Column(String)
    date_of_birth = Column(Date)
    created_at = Column(DateTime, default=func.now())

    locations = relationship("Locations", back_populates="user")
    additional = relationship("Additional", back_populates="user")

    def __init__(self, id, gender,name,first, last, date_of_birth):
        self.id=id
        self.gender = gender
        self.name = name
        self.name = name
        self.last = last
        self.date_of_birth = date_of_birth
    #     # init database model
    #     # pass


class Locations(Base):
    __tablename__ = 'locations'
    __table_args__ = {'schema': 'raw'}

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    postcode = Column(String)
    country_code = Column(String)
    created_at = Column(DateTime, default=func.now())

    user_id = Column(UUID(as_uuid=True), ForeignKey('raw.users.id'))
    user = relationship("Users", back_populates="locations")

    def __init__(self, id,city, state, country, postcode, country_code,user_id):
        # init database model
        self.id=id
        self.city = city
        self.state = state
        self.country = country
        self.postcode = postcode
        self.country_code = country_code
        self.user_id=user_id

        # pass
class Additional(Base):
    __tablename__ = 'additional'
    __table_args__ = {'schema': 'raw'}

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    phone = Column(String)
    email = Column(String)
    picture_large = Column(String)
    created_at = Column(DateTime, default=func.now())

    user_id = Column(UUID(as_uuid=True), ForeignKey('raw.users.id'))
    user = relationship("Users", back_populates="additional")

    def __init__(self,id, phone,email, picture_large,user_id):
        # init database model
        self.id=id
        self.phone = phone
        self.email=email
        self.picture_large=picture_large
        self.user_id=user_id

        # pass
