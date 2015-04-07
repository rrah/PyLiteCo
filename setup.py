import py2exe
from distutils.core import setup

setup(console = [{"script":"__main__.py", 
                  "dest_base" : "pyliteco"}], 
      zipfile = None, 
      options = {"py2exe": {"bundle_files": 1}})