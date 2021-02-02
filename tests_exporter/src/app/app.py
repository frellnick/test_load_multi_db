import logging
from config import DATA
from db import get_db, query_db
import os
import json

log = logging.getLogger(__name__)


def _test_db():
    try:
        d = get_db()
    except Exception as e:
        raise e


def _read(p:str) -> str:
    with open(p, 'r') as f:
        s = f.read()
    return s


def _read_json(p:str) -> dict:
    with open(p, 'r') as f:
        d = json.load(f)
    return d


def _load_sql(p:str) -> str:
    p = os.path.join(DATA['SQL'], p)
    return _read(p)


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


def _create_load_table(tablename:str):
    if _table_exists(tablename):
        print('table already exists')
    else:
        _execute(
            _load_sql(f'create_{tablename}.sql')
            )
        _execute(
            _load_sql(f'load_{tablename}.sql')
            )


def _create_tables():
    qplan = _read_json(DATA['QUERY_PLAN'])
    tables = qplan['tables']
    for t in tables:
        try:
            _create_load_table(t)    
        except Exception as e:
            raise e

def run():
    _test_db()
    _create_tables()
    print('hello from python app')



if __name__ == "__main__":
    run()
