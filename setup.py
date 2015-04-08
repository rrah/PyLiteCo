import py2exe
from distutils.core import setup


class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        self.version = "0.9b2"
        self.copyright = "(c) 2015, Robert Walker"
        self.name = "pyliteco"
      
myservice = Target(
                   description = "Indicator light for echo box",
                   modules = ["win_service"],
                   cmdline_style = "pywin32",
                   create_exe = True,
                   create_dll = False
                   )
      
setup(service = [myservice],
      zipfile = None, 
      options = {
                 "py2exe": {
                            "bundle_files": 1
                            }
                 },
      )
      