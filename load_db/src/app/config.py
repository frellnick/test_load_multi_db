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
    'PLANNINGFILE': config('PLANNINGFILE'),
    'QUERY_PLAN': config('QUERY_PLAN', default='query_plan.json'),
    'DBTYPE': config('DBTYPE', default='postgres'),
    'DBURI': config('DBURI', default=None),
    'POSTGRES_DBURI': config(
        'POSTGRES_DBURI', 
        default='postgres://docker:dockerpass@127.0.0.1:5432/testdata',
    ),
    'MYSQL_DBURI': config(
        'MYSQL_DBURI', 
        default='mysql+pymysql://docker:dockerpass@127.0.0.1:3306/testdata?local_infile=1',
    )
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
        def _contains_root_update_field(keyvals):
            root_list = ['DBTYPE', 'SQLDIR', 'QUERY_PLAN', 'DATADIR']
            for key in keyvals:
                if key in root_list:
                    return True
            return False
        
        def _get_root_datadir(keyvals):
            if 'DATADIR' in keyvals:
                return keyvals['DATADIR']
            return self['DATADIR']

        if _contains_root_update_field(keyvals):
            print('Updating root data directory.')
            root = _get_root_datadir(keyvals)
            data_paths = self._gen_data_paths(root=root, **keyvals)
            keyvals.update(data_paths)

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


    def _gen_data_paths(self, root, **kwargs) -> dict:
        def _default_or_new(key, kwargs=kwargs):
            if key in kwargs:
                return kwargs[key]
            return self.store[key]

        dbtype = _default_or_new('DBTYPE')
        sqldir = _default_or_new('SQLDIR')
        query_plan = _default_or_new('PLANNINGFILE')

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
            sqldir,
            query_plan
            ),
        }
        print(d)
        return d


lconfig = Config()