#!/usr/bin/env python

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
from os.path import join, dirname
from plotprofile.version import version as __version__


setup(
    name="PlotProfile.py",
    version=__version__,
    description="Plots profiles analyzed by immunogold labeling analysis tools",
    long_description=open(join(dirname(__file__), "README.rst")).read(),
    author="Max Larsson",
    author_email="max.larsson@liu.se",
    license="MIT",
    url="http://www.liu.se/medfak/forskning/larsson-max/software",
    packages=find_packages(),
    entry_points={
    'console_scripts':
        ['PlotProfile = PlotProfile:main'],
    'gui_scripts':
        ['PlotProfile = PlotProfile:main']        
    },
    data_files=[('PlotProfile', ['plotprofile/plotprofile.ico'])],
    install_requires=['matplotlib']
)