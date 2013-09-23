
from sqlalchemy import (
    Column,
    Integer,
    Float,
    Unicode,
    ForeignKey,
    DateTime)
import datetime
from . import DBSession, Base
from . auth import User

# Create your models here.


class Packages(Base):
    __tablename__ = 'packages'

    package_name = Column(Unicode(50), primary_key=True)
    rates = Column(Float)
    smses = Column(Integer)
    duration = Column(Unicode(100))

    def __init__(self, package_name=None, rates=None, smses=None, duration=None):
        package_name = self.package_name
        rates = self.rates
        smses = self.smses
        duration = self.duration


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
    package_name = Column(Unicode(50), ForeignKey(Packages.package_name))
    rates = Column(Float)

    def __init__(self, sms_type=None, sms_from=None, sms_to=None, msg=None, timestamp=None, status=None, msg_type=None,
                 user_id=None, package_name=None, rates=None):
        self.sms_type = sms_type
        self.sms_from = sms_from
        self.sms_to = sms_to
        self.msg = msg
        self.timestamp = timestamp
        self.status = status
        self.msg_type = msg_type
        self.user_id = user_id
        self.package_name = package_name
        self.rates = rates


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


class Selected_package(Base):
    __tablename__ = 'selected_package'

    id = Column(Integer, primary_key=True)
    user_id = Column(Unicode(100), ForeignKey(User.user_id))
    package_name = Column(Unicode(50), ForeignKey(Packages.package_name))
    smses = Column(Integer)
    rates = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(Unicode(100))

    def __init__(self, user_id=None, package_name=None, smses=None, rates=None, start_date=None, end_date=None,
                 status=None):
        package_name = self.package_name
        smses = self.smses
        rates = self.rates
        start_date = self.start_date
        end_date = self.end_date
        status = self.status


class Rates(Base):
    __tablename__ = 'rates'

    id = Column(Integer, primary_key=True)
    network_type = Column(Unicode(50))
    rates = Column(Float)

    def __init__(self, network_type=None, rates=None):
        network_type = self.network_type
        rates = self.rates

