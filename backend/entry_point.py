from db.session import db_engine
from db.base import Base


def create_table():
    Base.metadata.create_all(bind=db_engine)
