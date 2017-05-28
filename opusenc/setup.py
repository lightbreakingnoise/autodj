from distutils.core import setup, Extension

m = Extension("opusenc", libraries = ["opus"], sources = ["opusenc.c"])
setup(name = "opusenc", version = "0.1", ext_modules = [m])
