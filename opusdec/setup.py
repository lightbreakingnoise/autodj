from distutils.core import setup, Extension

m = Extension("opusdec", libraries = ["opus"], sources = ["opusdec.c"])
setup(name = "opusdec", version = "0.1", ext_modules = [m])
