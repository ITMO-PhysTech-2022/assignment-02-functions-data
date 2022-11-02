import sys
import importlib


def unload(module):
    if not isinstance(module, str):
        module = module.__name__
    if module in sys.modules:
        del sys.modules[module]