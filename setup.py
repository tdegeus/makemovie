
from setuptools import setup
from setuptools import find_packages

import re

filepath = 'makemovie/__init__.py'
__version__ = re.findall(r'__version__ = \'(.*)\'', open(filepath).read())[0]

setup(
    name = 'makemovie',
    version = __version__,
    license = 'MIT',
    author = 'Tom de Geus',
    author_email = 'tom@geus.me',
    description = 'Create a movie from a bunch of images.',
    long_description = 'Create a movie from a bunch of images.',
    keywords = 'ffmpeg',
    url = 'https://github.com/tdegeus/makemovie',
    packages = find_packages(),
    install_requires = ['docopt>=0.6.2', 'click>=4.0'],
    entry_points = {
        'console_scripts': [
            'makemovie = makemovie.cli.makemovie:main',
            'trim_images = makemovie.cli.trim_images:main']})
