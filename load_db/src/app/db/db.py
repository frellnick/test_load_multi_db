"""
Database
    Initialize and create connection control flow for database 
"""

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
import logging
from config import lconfig


###############################
### SQL Database Connection ###
###############################
def get_db(raw=False) -> sqlalchemy.engine:
    """
    Returns current database connection.  If connection not present,
    initiates connection to configured database.  Default is non-authenticated SQL.
    """
    db_uri = lconfig['DBURI']
    db_logger = logging.getLogger(__name__ + '.getdb')
    db_logger.info('Attempting connection to {}.'.format(db_uri))
    try:
        engine = create_engine(db_uri)
        if raw:
            return engine.raw_connection()
        db = engine.connect()
    except:
        db_logger.error('Could not establish connection.  Aborting.')
        raise ConnectionError

    return db


@contextmanager
def get_session(raw=False):
    # Setup session with thread engine.
    #   Allows for usage: with get_session() as session: session...
    engine = get_db(raw)
    session = scoped_session(sessionmaker(bind=engine))
    try:
        yield session
    finally:
        session.commit()
        session.close()


def close_db(e=None):
    db = get_session()
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    Base.metadata.create_all(db)


## SQL DB Utils ##

def query_db(query, raw=False):
    with get_session() as session:
        res = session.execute(query)
    return res