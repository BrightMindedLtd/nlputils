from setuptools import setup

# load dependencies from requirements.txt
# based on https://stackoverflow.com/questions/26900328/install-dependencies-from-setup-py
import os

reqpath = f'{os.path.dirname( os.path.realpath( __file__ ) )}/requirements.txt'
reqlist = []

if os.path.isfile( reqpath ):
    with open( reqpath ) as f:
        reqlist = f.read().splitlines()

setup(
    name='nlputils',
    packages=['nlp'],
    description='A library of utilities for text preprocessing for machine learning tasks',
    version='1.0.1',
    url='https://github.com/BrightMindedLtd/kapow-datautils',
    author='moneyball@brightminded.com',
    author_email='moneyball@brightminded.com',
    install_requires=reqlist,
    keywords=['text','machine learning', 'AI']
)
