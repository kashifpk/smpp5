from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    DateTime,
    )

from . import DBSession, Base
from auth import User

# Create your models here.
class Sms(Base):
    __tablename__ = 'sms'

    sms_id = Column(Unicode(100), primary_key=True)
    sms_type = Column(Unicode(40))
    sms_from = Column(Unicode(40))
    sms_to = Column(Unicode(40))
    msg = Column(Unicode(40))
    timestamp = Column(u'timestamp', TIMESTAMP(timezone=True), primary_key=False, nullable=False, default=time_now),
    user_id = Column(Unicode(100), ForeignKey(User.user_id))
 
    #def __init__(self, user_id=None, password=None, system_type=None):
    #    self.user_id = user_id
    #    self.password = password
    #    self.system_type = system_type
