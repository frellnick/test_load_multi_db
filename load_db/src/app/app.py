import logging
from config import lconfig
from db import get_db, query_db
import os
import json
import argparse


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

def _database_type_valid(dbtype:str) -> bool:
    return dbtype in lconfig['SUPPORTED_DB']

def _update_tablename(s:str, tablename) -> str:
    return s.replace('{tablename}', tablename)


def _execute(query:str):
    try:
        query_db(query)
    except Exception as e:
        raise e


def _create_load_table(tablename:str):
    if _table_exists(tablename):
        print(f'Table {tablename} already exists')
        log.info(f'Table {tablename} already exists')
    else:
        print(f'Creating table: {tablename}')
        log.info(f'Creating table: {tablename}')
        _execute(
            _load_sql(f'create_{tablename}.sql')
            )
        print(f'Loading table: {tablename}')
        _execute(
            _update_tablename(
                _load_sql(f'load.sql'), tablename
            )
            )


def _create_tables():
    qplan = _read_json(lconfig['QUERY_PLAN'])
    tables = qplan['tables']
    for t in tables:
        try:
            _create_load_table(t)
        except Exception as e:
            raise e

def run():
    print('Testing Database Connection')
    log.info('Testing Database Connection')
    _test_db()
    print("Running table creation and loading.")
    log.info("Running table creation and loading.")
    _create_tables()
    print('Load complete')
    log.info('Load complete')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load database with prepared data.`')
    parser.add_argument(
        '--dbtype', 
        metavar='db', 
        type=str,
        help="Database Type. Currently support 'mysql' or 'postgres'."
        )
    parser.add_argument(
        '--uri',
        metavar='uri',
        type=str,
        help='Database URI.  Must be fully constructed.  Example postgres://user:pass@ip.add/db_name'
    )
    parser.add_argument(
        '--datadir',
        metavar='data',
        nargs='?',
        type=str,
        help='Path to data directory'
    )

    args = parser.parse_args()
    if args.dbtype is not None:
        assert args.uri is not None, f'Must provide a URI to {args.dbtype} database.'
        assert _database_type_valid(args.dbtype), f'{args.dbtype} not supported.'
        lconfig['DBTYPE'] = args.dbtype
        lconfig['DBURI'] = args.uri

    if args.datadir is not None:
        assert os.path.exists(args.datadir), f'{args.datadir} not found'
        lconfig['DATADIR'] = args.datadir
        

    run()
