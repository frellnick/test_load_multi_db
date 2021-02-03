from decouple import config
import os
import logging
import json


def _mpath(*args) -> str:
    p = os.path.join(*args)
    if os.path.isdir(p):
        return p
    else:
        t = os.path.join(os.getcwd(), p)
        return t


DEFAULTS = {
    'SUPPORTED_DB': config('SUPPORTED_DB').split(','),
    'DEBUG': config('DEBUG'),
    'DATADIR': config('DATADIR'),
    'SQLDIR': config('SQLDIR'),
    'QUERY_PLAN': config('QUERY_PLAN'),
}

# Live Config
#   Create a config that read/writes to temporary file to allow multicomponent setting 
#   without environment corruption.
class Config():
    def __init__(self, defaults=DEFAULTS):
        self.store = {}
        self.savepath = '/tmp/appsettings.json'
        self.update(defaults)
        

    def update(self, keyvals):
        for key in keyvals:
            self.store[key] = keyvals[key]
        self.save()

        if 'DBTYPE' in keyvals:
            data_paths = self._gen_data_paths()
            self.update(data_paths)


    def save(self):
        with open(self.savepath, 'w+') as f:
            json.dump(self.store, f)
    

    def read(self):
        with open(self.savepath, 'r') as f:
            self.update(json.load(f))


    def __getitem__(self, idx):
        self.read()
        return self.store[idx]

    
    def __setitem__(self, key, val):
        self.update({key:val})


    def _gen_data_paths(self) -> dict:
        dbtype = self.store['DBTYPE']
        root = self.store['DATADIR']
        sqldir = self.store['SQLDIR']
        query_plan = self.store['QUERY_PLAN']
        d = {
        'DATA': _mpath(
            root
            ),
        'SQL': _mpath(
            root, 
            sqldir, 
            dbtype
            ),
        'QUERY_PLAN': _mpath(
            root,
            query_plan
            ),
        }
        return d