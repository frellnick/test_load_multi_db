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


DATA = {
    'DATA': _mpath(
        config('DATADIR')),
    'SQL': _mpath(
        config('DATADIR'), 
        config('SQLDIR'), 
        config('DBTYPE')),
    'QUERY_PLAN': _mpath(
        config('DATADIR'),
        config('QUERY_PLAN'),
        'query_plan.json'
        ),
}

