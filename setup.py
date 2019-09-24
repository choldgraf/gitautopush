from setuptools import setup, find_packages
from os import path as op
from gitautopush import __version__

# read the contents of your README file
this_directory = op.abspath(op.dirname(__file__))
with open(op.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='gitautopush',
    version=__version__,
    author='John Lee and Chris Holdgraf',
    author_email='choldgraf@berkeley.edu',
    license='BSD',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'gitautopush = gitautopush.gitautopush:main',
        ]
    },
)
