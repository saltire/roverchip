import inspect
import os


spritetypes = {}

for mfile in os.listdir(os.path.dirname(__file__)):
    if mfile != '__init__.py' and mfile[-3:] == '.py' and mfile[:-3] != 'sprite':
        module = __import__(mfile[:-3], globals())
        spritetypes.update(dict(inspect.getmembers(module, inspect.isclass)))
