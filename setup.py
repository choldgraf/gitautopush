from setuptools import setup, find_packages
from gitautopush import __version__

setup(
    name='gitautopush',
    version=__version__,
    author='John Lee and Chris Holdgraf',
    author_email='choldgraf@gmail.com',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'gitautopush = gitautopush.gitautopush:main',
        ]
    },
)
