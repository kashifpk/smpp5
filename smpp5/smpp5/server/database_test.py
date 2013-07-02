import db
from db import DBSession
from models import User
import hashlib

if '__main__' == __name__:
    db.bind_session()
    passhash = hashlib.sha1(bytes(password, encoding="utf8")).hexdigest()
    DBSession.query(User).filter_by(user_id=system_id, system_type=system_type, password=passhash).first()
    u = DBSession.query(User).first()
    print(u.user_id)
    print(u.password)

