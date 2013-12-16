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
    duration = Column(Integer)

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
    schedule_delivery_time = Column(DateTime)
    validity_period = Column(DateTime)
    msg = Column(Unicode(500))
    timestamp = Column(DateTime)
    status = Column(Unicode(40))
    user_id = Column(Unicode(100), ForeignKey(User.user_id))
    package_name = Column(Unicode(50), ForeignKey(Packages.package_name))
    rates = Column(Float)
    target_network = Column(Unicode(100))
    client_type = Column(Unicode(30))

    def __init__(self, sms_type=None, sms_from=None, sms_to=None, schedule_delivery_time=None, validity_period=None,
                 msg=None, timestamp=None, status=None, user_id=None, package_name=None, rates=None, target_network=None):
        self.sms_type = sms_type
        self.sms_from = sms_from
        self.sms_to = sms_to
        self.schedule_delivery_time = schedule_delivery_time
        self.validity_period = validity_period
        self.msg = msg
        self.timestamp = timestamp
        self.status = status
        self.user_id = user_id
        self.package_name = package_name
        self.rates = rates
        self.target_network = target_network


class User_Number(Base):
    __tablename__ = 'user_number'

    user_id = Column(Unicode(100), ForeignKey(User.user_id), primary_key=True)
    cell_number = Column(Unicode(40), primary_key=True)

    def __init__(self, cell_number=None, user_id=None):
        self.user_id = user_id
        self.cell_number = cell_number


class Prefix_Match(Base):
    __tablename__ = 'prefix_match'

    prefix = Column(Unicode(10), primary_key=True)
    network = Column(Unicode(100))

    def __init__(self, prefix=None, network=None):
        self.prefix = prefix
        self.network = network


class Network(Base):
    __tablename__ = 'network'

    network = Column(Unicode(100))
    username = Column(Unicode(100))
    password = Column(Unicode(100))
    system_type = Column(Unicode(100))
    ip = Column(Unicode(100))
    port = Column(Integer)
    id = Column(Integer, primary_key=True)

    def __init__(self, network=None, username=None, password=None, system_type=None, ip=None, port=None):
        self.network = network
        self.username = username
        self.password = password
        self.system_type = system_type
        self.ip = ip
        self.port = port


class Mnp(Base):
    __tablename__ = 'mnp'

    cell_number = Column(Unicode(40), primary_key=True)
    target_network = Column(Unicode(100))

    def __init__(self, cell_number=None, target_network=None):
        self.cell_number = cell_number
        self.target_network = target_network


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


