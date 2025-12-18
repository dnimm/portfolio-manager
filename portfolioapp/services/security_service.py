from portfolioapp.db import db
from portfolioapp.domain.security import Security

def get_all_securities():
    return Security.query.all()

def create_security(data):
    sec = Security(**data)
    db.session.add(sec)
    db.session.commit()
    return sec
