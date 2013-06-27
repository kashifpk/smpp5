import db
from db import DBSession
from models import User

if '__main__' == __name__:
    db.bind_session()
    u = DBSession.query(User).first()
    print(u.user_id)
    print(u.password)

