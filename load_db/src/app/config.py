from decouple import config
import os
import logging
import json
import warnings

def _mpath(*args) -> str:
    def _check_fullpath(p:str) -> (bool, str):
        fp = os.path.join(os.getcwd(), p)
        return os.path.isfile(fp) or os.path.isdir(fp), fp

    p = os.path.join(*args)
    if os.path.isdir(p) or os.path.isfile(p):
        return p
    else:
        exists, fp = exists, fp = _check_fullpath(p)
        if exists:
            return fp
        warnings.warn(f"{p} or {fp} not found or is not a directory")
        return p


DEFAULTS = {
    'SUPPORTED_DB': config('SUPPORTED_DB').split(','),
    'DEBUG': config('DEBUG'),
    'DATADIR': config('DATADIR', default=''),
    'SQLDIR': config('SQLDIR'),
    'QUERY_PLAN': config('QUERY_PLAN'),
    'DBTYPE': config('DBTYPE', default='postgres'),
}

# Live Config
#   Create a config that read/writes to temporary file to allow multicomponent setting 
#   without environment corruption.
class Config():
    def __init__(self, defaults=DEFAULTS):
        self.store = defaults
        self.savepath = '/tmp/appsettings.json'
        self.save
        self.update(defaults) ## sanity check
        

    def update(self, keyvals):

        if 'DATADIR' in keyvals:
            print('Updating root data directory.')
            data_paths = self._gen_data_paths(root=keyvals['DATADIR'])
            print(data_paths)
            keyvals.update(data_paths)
            print(keyvals)

        for key in keyvals:
            self.store[key] = keyvals[key]
        self.save()


    def save(self):
        with open(self.savepath, 'w+') as f:
            json.dump(self.store, f)
    

    def read(self):
        with open(self.savepath, 'r') as f:
            self.store = json.load(f)


    def __getitem__(self, idx):
        self.read()
        return self.store[idx]

    
    def __setitem__(self, key, val):
        self.update({key:val})


    def _gen_data_paths(self, root) -> dict:
        dbtype = self.store['DBTYPE']
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


lconfig = Config()