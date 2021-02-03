from decouple import config
import os
import logging


def _mpath(*args) -> str:
    p = os.path.join(*args)
    if os.path.isdir(p):
        return p
    else:
        t = os.path.join(os.getcwd(), p)
        return t


def _get_dburi()->str:
    t = config('DBTYPE').upper()
    return config(f'{t}_DBURI')

VALIDATION = {
    'SUPPORTED_DB': config('SUPPORTED_DB').split(',')
}


DATABASE = {
    'DBURI': _get_dburi(),
    'DBTYPE': config('DBTYPE', default='postgres')
}


def gen_data_paths(root:str, dbtype=None) -> dict:
    if dbtype is None:
        dbtype = config('DBTYPE')
    d = {
    'DATA': _mpath(
        root),
    'SQL': _mpath(
        root, 
        config('SQLDIR'), 
        dbtype),
    'QUERY_PLAN': _mpath(
        root,
        config('QUERY_PLAN'),
        'query_plan.json'
        )
    }
    return d

DATA = gen_data_paths(config('DATADIR'))