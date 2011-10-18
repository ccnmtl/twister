from setuptools import setup, find_packages
import sys, os

version = '0.2'

setup(name='twister',
      version=version,
      description="Random Number Generation Microapp",
      long_description="""\
Generates random numbers for a number of different distributions.""",
      classifiers=[], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      keywords='REST random',
      author='Anders Pearson',
      author_email='anders@columbia.edu',
      url='http://code.google.com/p/microapps/wiki/Twister',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
