from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, synonym
from sqlalchemy.dialects.mysql import DOUBLE, TEXT
from datetime import datetime
import os

Base = declarative_base()
engine = create_engine(os.environ.get('DATABASE_URL'))
Session = sessionmaker(bind=engine)

def get_session():
    return Session()

class Device(Base):
    __tablename__ = "aware_device"

    _id = Column(Integer, primary_key=True)
    _timestamp = Column("timestamp", DOUBLE)
    device_id = Column(String(150))
    board = Column(TEXT)
    brand = Column(TEXT)
    device = Column(TEXT)
    build_id = Column(TEXT)
    hardware = Column(TEXT)
    manufacturer = Column(TEXT)
    model = Column(TEXT)
    product = Column(TEXT)
    serial = Column(TEXT)
    release = Column(TEXT)
    release_type = Column(TEXT)
    sdk = Column(Integer)
    label = Column(TEXT)

    @hybrid_property
    def timestamp(self):
        return datetime.utcfromtimestamp(float(self._timestamp)/1000.)

    @timestamp.setter
    def timestamp(self, dt):
        self._timestamp = DOUBLE(float(dt.strftime("%s"))*1000.)

    def __repr__(self):
        return '<Device "%s">' % self.device_id

    # timestamp = synonym('_timestamp', descriptor=timestamp)

class Screen(Base):
    __tablename__ = "screen"

    _id = Column(Integer, primary_key=True)
