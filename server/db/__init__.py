from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa


Base = declarative_base()
engine = sa.create_engine('sqlite:///data.db')

session_factory = orm.sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.bind = engine

Session = orm.scoped_session(session_factory)
