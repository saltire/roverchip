import inspect
import os


celltypes = {}

for mfile in os.listdir(os.path.dirname(__file__)):
    if mfile != '__init__.py' and mfile[-3:] == '.py' and mfile[:-3] != 'cell':
        module = __import__(mfile[:-3], globals())
        celltypes.update(dict(inspect.getmembers(module, inspect.isclass)))
