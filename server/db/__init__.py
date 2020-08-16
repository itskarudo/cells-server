from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa


Base = declarative_base()
engine = sa.create_engine('sqlite:///data.db', echo=True)
Base.metadata.bind = engine
session = orm.scoped_session(orm.sessionmaker())(bind=engine)
