from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    ForeignKey,
    DateTime
    )
import datetime
from . import DBSession, Base
from . auth import User

# Create your models here.
class Sms(Base):
    __tablename__ = 'sms'

    sms_id = Column(Unicode(100), primary_key=True)
    sms_type = Column(Unicode(40))
    sms_from = Column(Unicode(40))
    sms_to = Column(Unicode(40))
    msg = Column(Unicode(40))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(Unicode(40))
    user_id = Column(Unicode(100), ForeignKey(User.user_id))
 
    def __init__(self, sms_id=None, sms_type=None, sms_from=None, sms_to=None, msg=None, status=None, msg_type=None, user_id=None):
        self.sms_id = sms_id
        self.sms_type = sms_type
        self.sms_from = sms_from
        self.sms_to = sms_to
        self.msg = msg
        self.status = status
        self.user_id = user_id
