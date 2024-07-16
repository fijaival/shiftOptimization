import os


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import declarative_base


database_uri = 'mysql+pymysql://{user}:{password}@{host}:{PORT}/{db_name}?charset=utf8'.format(**{
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host':     os.getenv('DB_HOST'),
    'PORT':    os.getenv('DB_PORT'),
    'db_name': os.getenv('DB_NAME'),
})
engine = create_engine(database_uri, pool_pre_ping=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import api.v1.models
    Base.metadata.create_all(bind=engine)
