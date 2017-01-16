# coding: utf-8
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
shutter = ShutterDevice(location='okno1', ip='172.30.1.231')
session.add(shutter)
session.commit()
