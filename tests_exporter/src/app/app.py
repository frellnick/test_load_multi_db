import logging
from config import DATA
from db import get_db, query_db
import os

log = logging.getLogger(__name__)


def _test_db():
    try:
        d = get_db()
    except Exception as e:
        raise e


def _load_sql(p:str) -> str:
    p = os.path.join(DATA['SQL'], p)
    with open(p, 'r') as f:
        s = f.read()
    return s


def _table_exists(tablename:str) -> bool:
    try:
        query_db(f'SELECT * FROM {tablename}')
        return True
    except Exception as e:
        return False


def _execute(query:str):
    try:
        query_db(query)
    except Exception as e:
        raise e


def _create_tables():
    tables = ['test']
    if _table_exists(tables[0]):
        print('table already exists')
    else:
        _execute(
            _load_sql('create_test.sql')
            )
        _execute(
            _load_sql('load_test.sql')
            )



def run():
    _test_db()
    _create_tables()
    print('hello from python app')

if __name__ == "__main__":
    run()
