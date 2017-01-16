# coding: utf-8
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///tmp/db.shutters', echo=True)
Base = declarative_base()

    
class ShutterDevice(Base):
    __tablename__ = 'shutter_devices'
    id = Column(Integer, primary_key=True)
    location = Column(String(50))
    mac_address = Column(String(17))
    ip = Column(String(15))
    extend_existing = True
    def __repr__(self):
        return "<ShutterDevice(location='{}, ip={}>".format(self.location, self.ip)
    

Base.metadata.create_all(engine)
