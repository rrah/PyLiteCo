import py2exe
from distutils.core import setup


setup(console = ['__main__.py'], zipfile = None, options = {"py2exe": {"bundle_files": 1}})