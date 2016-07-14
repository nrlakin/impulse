from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.types import TypeDecorator
from sqlalchemy.dialects.mysql import DOUBLE, TEXT
from datetime import datetime
import os

Base = declarative_base()
engine = create_engine(os.environ.get('DATABASE_URL'))
Session = sessionmaker(bind=engine)

def get_session():
    return Session()

class DoubleTimestamp(TypeDecorator):
    impl = DOUBLE

    def __init__(self):
        TypeDecorator.__init__(self, asdecimal=False)

    def process_bind_param(self, value, dialect):
        return (value-datetime(1970, 1, 1)).total_seconds()*1000.

    def process_result_value(self, value, dialect):
        return datetime.utcfromtimestamp(float(value)/1000.)

class Device(Base):
    __tablename__ = "aware_device"

    _id = Column(Integer, primary_key=True)
    timestamp = Column(DoubleTimestamp)
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
    # calls = relationship("Call", backref="device", lazy="dynamic")

    def __repr__(self):
        return '<Device "%d" Device "%s">' % (self._id, self.device_id)

class Call(Base):
    __tablename__ = "calls"

    _id = Column(Integer, primary_key=True)
    timestamp = Column(DoubleTimestamp)
    device_id = Column(String(150))
    call_type = Column(Integer)
    call_duration = Column(Integer)
    trace = Column(TEXT)

    def __repr__(self):
        return '<Call "%s">' % self._id

class Screen(Base):
    __tablename__ = "screen"

    _id = Column(Integer, primary_key=True)
    timestamp = Column(DoubleTimestamp)
    device_id = Column(String(150))
    screen_status = Column(Integer)

    def __repr__(self):
        return '<Screen "%d" Device "%s">' % (self._id, self.device_id)
