# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="youtubeSpotifyConverter",
    version="0.1.4",
    description="Convert between Spotify, YouTube and YouTube Music URLs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["youtubeSpotifyConverter"],
    license="MIT",
    include_package_data=True,
    install_requires=["requests", "pybase64"]
)