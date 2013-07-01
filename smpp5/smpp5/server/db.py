from sqlalchemy import create_engine
from models import DBSession

def bind_session():
    #engine = create_engine("sqlite:///../../../smpp5web/smpp5web.db")

    engine = create_engine("mysql+pymysql://smpp5:smpp5@localhost/smpp5")
    DBSession.configure(bind=engine)

