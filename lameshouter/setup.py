from distutils.core import setup, Extension

m = Extension("lameshouter", libraries = ["mp3lame", "shout"], sources = ["lameshouter.c"])
setup(name = "lameshouter", version = "0.1", ext_modules = [m])
