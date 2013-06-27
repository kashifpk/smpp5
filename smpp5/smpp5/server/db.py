from sqlalchemy import create_engine
from models import DBSession

def bind_session():
    engine = create_engine("sqlite:///../../../smpp5web/smpp5web.db")
    DBSession.configure(bind=engine)

