"""C++ magic"""
__version__ = '0.1'

from .build_util import CppMagic

def load_ipython_extension(ipython):
    ipython.register_magics(CppMagic)
