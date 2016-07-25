from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.types import TypeDecorator
from sqlalchemy.dialects.mysql import DOUBLE, TEXT
from datetime import datetime
import pytz
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
        if value.tzinfo is not None:
            value = value.replace(tzinfo = pytz.utc).replace(tzinfo = None)
        return (value-datetime(1970, 1, 1)).total_seconds()*1000.

    def process_result_value(self, value, dialect):
        return datetime.utcfromtimestamp(float(value)/1000.).replace(tzinfo = pytz.utc)

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

class Accelerometer(Base):
    __tablename__ = "accelerometer"

    _id = Column(Integer, primary_key=True)
    timestamp = Column(DoubleTimestamp)
    device_id = Column(String(150))
    double_values_0 = Column(DOUBLE(asdecimal=False))
    double_values_1 = Column(DOUBLE(asdecimal=False))
    double_values_2 = Column(DOUBLE(asdecimal=False))
    accuracy = Column(Integer)
    label = Column(TEXT)

    def __repr__(self):
        return '<Accelerometer "%d" Device "%s">' % (self._id, self.device_id)

class Processor(Base):
    __tablename__ = "processor"

    _id = Column(Integer, primary_key=True)
    timestamp = Column(DoubleTimestamp)
    device_id = Column(String(150))
    double_last_user = Column(DOUBLE(asdecimal=False))
    double_last_system = Column(DOUBLE(asdecimal=False))
    double_last_idle = Column(DOUBLE(asdecimal=False))
    double_user_load = Column(DOUBLE(asdecimal=False))
    double_system_load = Column(DOUBLE(asdecimal=False))
    double_idle_load = Column(DOUBLE(asdecimal=False))

def __repr__(self):
    return '<Processor "%d" Device "%s">' % (self._id, self.device_id)
