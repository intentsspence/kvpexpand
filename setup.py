import setuptools

exec(open("src/kvpexpand/_version.py").read())
setuptools.setup(name="kvpexpand", version=__version__)