from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    ForeignKey,
    DateTime)
import datetime
from . import DBSession, Base
from . auth import User

# Create your models here.


class Sms(Base):
    __tablename__ = 'sms'

    id = Column(Integer, primary_key=True)
    sms_type = Column(Unicode(40))
    sms_from = Column(Unicode(40))
    sms_to = Column(Unicode(40))
    msg = Column(Unicode(100))
    timestamp = Column(DateTime)
    status = Column(Unicode(40))
    msg_type = Column(Unicode(40))
    user_id = Column(Unicode(100), ForeignKey(User.user_id))

    def __init__(self, sms_type=None, sms_from=None, sms_to=None, msg=None, timestamp=None, status=None, msg_type=None, user_id=None):
        self.sms_type = sms_type
        self.sms_from = sms_from
        self.sms_to = sms_to
        self.msg = msg
        self.timestamp = timestamp
        self.status = status
        self.msg_type = msg_type
        self.user_id = user_id


class User_Number(Base):
    __tablename__ = 'user_number'

    user_id = Column(Unicode(100), ForeignKey(User.user_id), primary_key=True)
    cell_number = Column(Unicode(40), primary_key=True)

    def __init__(self, cell_number=None, user_id=None):
        self.user_id = user_id
        self.cell_number = cell_number

class Prefix_Match(Base):
    __tablename__ = 'prefix_match'
    
    prefix = Column(Unicode(4), primary_key=True)           
    user_id = Column(Unicode(100), ForeignKey(User.user_id))
        
    def __init__(self, prefix=None, user_id=None):
        self.prefix = prefix
        self.user_id = user_id
    
